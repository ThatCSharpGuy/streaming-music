import click
import jinja2
from pathlib import Path
import cairosvg
import tempfile
import moviepy.editor as mpe
from streaming_music.audio import from_youtube

TEMPLATE_FILES = Path(Path(__file__).parent, "templates")
LOADER = jinja2.FileSystemLoader(searchpath=str(TEMPLATE_FILES))
template_env = jinja2.Environment(loader=LOADER)

@click.command()
@click.argument("video_id")
@click.argument("video_name")
def cli(video_id, video_name):
    cache = Path(".cache")
    cache.mkdir(exist_ok=True)

    mp3_file = from_youtube(video_id, cache)

    template_filename = template_env.get_template(f"song-template.svg")
    variables = {
        "yt_url": f"youtu.be/{video_id}",
        "song_name": video_name,
    }
    output_text = template_filename.render(**variables)
    

    png = cairosvg.svg2png(
        bytestring=output_text.encode("utf-8"),
        output_width=1920,
        output_height=1080,
        dpi=120,
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        image = str(Path(tmp_dir, "img.png"))
        with open(image, "wb") as writable:
            writable.write(png)


        audio_clip = mpe.AudioFileClip(str(mp3_file))
        image_clip = mpe.ImageClip(image).set_duration(audio_clip.duration)
        image_clip.audio = audio_clip
        image_clip.write_videofile("my_video.mp4", fps=1)


if __name__ == "__main__":
    cli()

