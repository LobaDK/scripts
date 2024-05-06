from subprocess import Popen, PIPE
from time import time
import logging

# Set up the logger
logging.basicConfig(
    filename="timeit.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} took {time() - start} seconds")
        return result

    return wrapper


@timeit
def get_stream_urls(url: str):
    cmd = [
        "yt-dlp",
        "--get-url",
        url,
    ]
    with Popen(cmd, text=True, stdout=PIPE) as proc:
        stream_url = proc.stdout.read().strip()
    return stream_url.split("\n")


@timeit
def with_ytdlp(url: str):
    @timeit
    def without_encode(url: str):
        cmd = [
            "yt-dlp",
            "--force-overwrites",
            "-o",
            "section_with_yt-dlp_postprocessor.%(ext)s",
            "--postprocessor-args",
            "-ss 00:01:00 -t 00:01:00",
            url,
        ]
        with Popen(cmd) as proc:
            proc.wait()

    @timeit
    def with_encode(url: str):
        cmd = [
            "yt-dlp",
            "--force-overwrites",
            "-o",
            "section_with_yt-dlp_postprocessor_with_reencode.%(ext)s",
            "--postprocessor-args",
            "-ss 00:01:00 -t 00:01:00 -c:a copy -c:v libvpx-vp9",
            url,
        ]
        with Popen(cmd) as proc:
            proc.wait()

    without_encode(url)
    with_encode(url)


@timeit
def with_ytdlp_with_ffmpeg_reencode(url: str):
    cmd = [
        "yt-dlp",
        "--force-overwrites",
        "-o",
        "section_with_yt-dlp_postprocessor_temp.%(ext)s",
        "--postprocessor-args",
        "-ss 00:01:00 -t 00:01:00",
        url,
    ]
    with Popen(cmd) as proc:
        proc.wait()

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        "section_with_yt-dlp_postprocessor_temp.webm",
        "-c:a",
        "copy",
        "-c:v",
        "libvpx-vp9",
        "section_with_yt-dlp_postprocessor_with_reencode.webm",
    ]
    with Popen(cmd) as proc:
        proc.wait()


@timeit
def with_ffmpeg_after_input(url: str):
    stream_url = get_stream_urls(url)

    @timeit
    def ffmpeg_download_video_stream(stream_url: str):
        # Download video
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            stream_url,
            "-ss",
            "00:01:00",
            "-t",
            "00:01:00",
            "-c:v",
            "copy",
            "section_with_ffmpeg_video.webm",
        ]
        with Popen(cmd) as proc:
            proc.wait()

    @timeit
    def ffmpeg_download_audio_stream(stream_url: str):
        # Download audio
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            stream_url,
            "-ss",
            "00:01:00",
            "-t",
            "00:01:00",
            "-f",
            "libopus",
            "-c:a",
            "copy",
            "section_with_ffmpeg_audio.webm",
        ]
        with Popen(cmd) as proc:
            proc.wait()

    @timeit
    def ffmpeg_combine_video_audio():
        # Combine video and audio
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            "section_with_ffmpeg_video.webm",
            "-i",
            "section_with_ffmpeg_audio.webm",
            "-c",
            "copy",
            "section_with_ffmpeg_after_input.webm",
        ]
        with Popen(cmd) as proc:
            proc.wait()

    ffmpeg_download_video_stream(stream_url[0])
    ffmpeg_download_audio_stream(stream_url[1])
    ffmpeg_combine_video_audio()


@timeit
def with_ffmpeg_before_input(url: str):
    stream_url = get_stream_urls(url)

    @timeit
    def ffmpeg_download_video_stream(stream_url: str):
        # Download video
        cmd = [
            "ffmpeg",
            "-y",
            "-ss",
            "00:01:00",
            "-i",
            stream_url,
            "-t",
            "00:01:00",
            "-c:v",
            "libvpx-vp9",
            "section_with_ffmpeg_video.webm",
        ]
        with Popen(cmd) as proc:
            proc.wait()

    @timeit
    def ffmpeg_download_audio_stream(stream_url: str):
        # Download audio
        cmd = [
            "ffmpeg",
            "-y",
            "-ss",
            "00:01:00",
            "-i",
            stream_url,
            "-t",
            "00:01:00",
            "-f",
            "opus",
            "section_with_ffmpeg_audio.webm",
        ]
        with Popen(cmd) as proc:
            proc.wait()

    @timeit
    def ffmpeg_combine_video_audio():
        # Combine video and audio
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            "section_with_ffmpeg_video.webm",
            "-i",
            "section_with_ffmpeg_audio.webm",
            "-c",
            "copy",
            "section_with_ffmpeg_before_input.webm",
        ]
        with Popen(cmd) as proc:
            proc.wait()

    ffmpeg_download_video_stream(stream_url[0])
    ffmpeg_download_audio_stream(stream_url[1])
    ffmpeg_combine_video_audio()


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=saxIyKW1lK0"
    with_ytdlp(url)
    logging.info("-" * 50)
    with_ytdlp_with_ffmpeg_reencode(url)
    logging.info("-" * 50)
    with_ffmpeg_after_input(url)
    logging.info("-" * 50)
    with_ffmpeg_before_input(url)
