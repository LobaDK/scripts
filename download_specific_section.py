from subprocess import Popen, PIPE
from time import time
import logging

# Set up the logger
logging.basicConfig(
    filename="timeit.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logging.info(f"{'-' * 20} Start {'-' * 20}")


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
        "--limit-rate",
        "5M",
        "--get-url",
        url,
    ]
    with Popen(cmd, text=True, stdout=PIPE) as proc:
        stream_url = proc.stdout.read().strip()
    return stream_url.split("\n")


@timeit
def download_with_ytdlp(url: str):
    @timeit
    def without_trim(url: str):
        cmd = [
            "yt-dlp",
            "--limit-rate",
            "5M",
            "--force-overwrites",
            "-o",
            "download_with_ytdlp_without_trim.%(ext)s",
            url,
        ]
        with Popen(cmd) as proc:
            proc.wait()

    @timeit
    def without_postprocessor_encode(url: str):
        cmd = [
            "yt-dlp",
            "--limit-rate",
            "5M",
            "--force-overwrites",
            "-o",
            "download_with_ytdlp_without_postprocessor_encode.%(ext)s",
            "--postprocessor-args",
            "-ss 00:01:00 -t 00:01:00",
            url,
        ]
        with Popen(cmd) as proc:
            proc.wait()

    @timeit
    def with_postprocessor_encode(url: str):
        cmd = [
            "yt-dlp",
            "--limit-rate",
            "5M",
            "--force-overwrites",
            "-o",
            "download_with_ytdlp_with_postprocessor_encode.%(ext)s",
            "--postprocessor-args",
            "-ss 00:01:00 -t 00:01:00 -c:a copy -c:v libvpx-vp9",
            url,
        ]
        with Popen(cmd) as proc:
            proc.wait()

    @timeit
    def with_ffmpeg_reencode(url: str):
        cmd = [
            "yt-dlp",
            "--limit-rate",
            "5M",
            "--force-overwrites",
            "-o",
            "download_with_ytdlp_with_ffmpeg_reencode_temp.%(ext)s",
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
            "download_with_ytdlp_with_ffmpeg_reencode_temp.webm",
            "-c:a",
            "copy",
            "-c:v",
            "libvpx-vp9",
            "download_with_ytdlp_with_ffmpeg_reencode.webm",
        ]
        with Popen(cmd) as proc:
            proc.wait()

    without_trim(url)
    without_postprocessor_encode(url)
    with_postprocessor_encode(url)
    with_ffmpeg_reencode(url)


@timeit
def download_with_ffmpeg(url: str):
    stream_url = get_stream_urls(url)

    @timeit
    def without_trim(stream_url: list):
        @timeit
        def ffmpeg_download_video_stream(stream_url: str):
            # Download video
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                stream_url,
                "-c:v",
                "copy",
                "download_with_ffmpeg_without_trim_video.webm",
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
                "-f",
                "opus",
                "-c:a",
                "copy",
                "download_with_ffmpeg_without_trim_audio.webm",
            ]
            with Popen(cmd) as proc:
                proc.wait()

        @timeit
        def ffmpeg_combine_audio_video():
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                "download_with_ffmpeg_without_trim_audio.webm",
                "-i",
                "download_with_ffmpeg_without_trim_video.webm",
                "-c",
                "copy",
                "download_with_ffmpeg_without_trim.webm",
            ]
            with Popen(cmd) as proc:
                proc.wait()

        ffmpeg_download_video_stream(stream_url[0])
        ffmpeg_download_audio_stream(stream_url[1])
        ffmpeg_combine_audio_video()

    @timeit
    def with_trim_after_input(stream_url: list):
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
                "download_with_ffmpeg_with_trim_after_input_video.webm",
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
                "opus",
                "-c:a",
                "copy",
                "download_with_ffmpeg_with_trim_after_input_audio.webm",
            ]
            with Popen(cmd) as proc:
                proc.wait()

        @timeit
        def ffmpeg_combine_audio_video():
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                "download_with_ffmpeg_with_trim_after_input_audio.webm",
                "-i",
                "download_with_ffmpeg_with_trim_after_input_video.webm",
                "-c",
                "copy",
                "download_with_ffmpeg_with_trim_after_input.webm",
            ]
            with Popen(cmd) as proc:
                proc.wait()

        ffmpeg_download_video_stream(stream_url[0])
        ffmpeg_download_audio_stream(stream_url[1])
        ffmpeg_combine_audio_video()

    @timeit
    def with_trim_before_input(stream_url: list):
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
                "copy",
                "download_with_ffmpeg_with_trim_before_input_video.webm",
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
                "-c:a",
                "copy",
                "download_with_ffmpeg_with_trim_before_input_audio.webm",
            ]
            with Popen(cmd) as proc:
                proc.wait()

        @timeit
        def ffmpeg_combine_audio_video():
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                "download_with_ffmpeg_with_trim_before_input_audio.webm",
                "-i",
                "download_with_ffmpeg_with_trim_before_input_video.webm",
                "-c",
                "copy",
                "download_with_ffmpeg_with_trim_before_input.webm",
            ]
            with Popen(cmd) as proc:
                proc.wait()

        ffmpeg_download_video_stream(stream_url[0])
        ffmpeg_download_audio_stream(stream_url[1])
        ffmpeg_combine_audio_video()

    @timeit
    def with_trim_before_input_reencode(stream_url: list):
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
                "download_with_ffmpeg_with_trim_before_input_reencode_video.webm",
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
                "-c:a",
                "libopus",
                "download_with_ffmpeg_with_trim_before_input_reencode_audio.webm",
            ]
            with Popen(cmd) as proc:
                proc.wait()

        @timeit
        def ffmpeg_combine_audio_video():
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                "download_with_ffmpeg_with_trim_before_input_reencode_audio.webm",
                "-i",
                "download_with_ffmpeg_with_trim_before_input_reencode_video.webm",
                "-c",
                "copy",
                "download_with_ffmpeg_with_trim_before_input_reencode.webm",
            ]
            with Popen(cmd) as proc:
                proc.wait()

        ffmpeg_download_video_stream(stream_url[0])
        ffmpeg_download_audio_stream(stream_url[1])
        ffmpeg_combine_audio_video()

    without_trim(stream_url)
    logging.info("-" * 50)
    with_trim_after_input(stream_url)
    logging.info("-" * 50)
    with_trim_before_input(stream_url)
    logging.info("-" * 50)
    with_trim_before_input_reencode(stream_url)


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=saxIyKW1lK0"
    download_with_ytdlp(url)
    logging.info("-" * 50)
    download_with_ffmpeg(url)
