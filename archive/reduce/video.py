import argparse
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}


def format_size(bytes_size):
    return f"{bytes_size / (1024 * 1024):.2f} MB"


def require_ffmpeg():
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "FFmpeg is required. Install it first, then make sure `ffmpeg` works in your terminal."
        )
    if shutil.which("ffprobe") is None:
        raise RuntimeError(
            "FFprobe is required. Install FFmpeg and make sure both `ffmpeg` and `ffprobe` work in your terminal."
        )


def get_video_frame_rate(input_path):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=r_frame_rate",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(input_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "FFprobe failed")

    output = result.stdout.strip()
    if not output:
        raise RuntimeError("Unable to determine video frame rate with ffprobe.")

    if "/" in output:
        num, den = output.split("/", 1)
        return float(num) / float(den)

    return float(output)


def build_output_path(input_path, output_dir=None, suffix="-web"):
    input_path = Path(input_path)

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / f"{input_path.stem}{suffix}.mp4"

    return input_path.with_name(f"{input_path.stem}{suffix}.mp4")


def compress_video(
    input_path,
    output_dir=None,
    crf=28,
    preset="medium",
    max_width=1280,
    max_fps=30,
):
    input_path = Path(input_path)
    output_path = build_output_path(input_path, output_dir)

    original_size = input_path.stat().st_size

    filters = [f"scale=min({max_width}\\,iw):-2"]
    if max_fps is not None:
        input_fps = None
        try:
            input_fps = get_video_frame_rate(input_path)
        except RuntimeError:
            input_fps = None

        if input_fps is None or input_fps > max_fps:
            filters.append(f"fps=fps={max_fps}")

    filter_arg = ",".join(filters)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vf",
        filter_arg,
        "-c:v",
        "libx264",
        "-preset",
        preset,
        "-crf",
        str(crf),
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "FFmpeg failed")

    compressed_size = output_path.stat().st_size
    reduction = 100 - (compressed_size / original_size * 100)

    return {
        "file": input_path.name,
        "output": str(output_path),
        "before": original_size,
        "after": compressed_size,
        "reduction": reduction,
    }


def find_videos(path):
    path = Path(path)

    if path.is_file():
        return [path] if path.suffix.lower() in VIDEO_EXTENSIONS else []

    return [
        file
        for file in path.rglob("*")
        if file.is_file() and file.suffix.lower() in VIDEO_EXTENSIONS
    ]


def compress_path(
    path,
    output_dir=None,
    crf=28,
    preset="medium",
    max_width=1280,
    max_fps=30,
    workers=None,
):
    require_ffmpeg()

    videos = find_videos(path)
    if not videos:
        print("No video files found.")
        return

    workers = workers or max(1, min(os.cpu_count() or 1, 4))

    total_before = 0
    total_after = 0

    print(f"\nCompressing {len(videos)} video file(s)...\n")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                compress_video,
                video,
                output_dir,
                crf,
                preset,
                max_width,
                max_fps,
            )
            for video in videos
        ]

        for future in as_completed(futures):
            result = future.result()
            total_before += result["before"]
            total_after += result["after"]

            print(
                f"{result['file']}\n"
                f"  Output: {result['output']}\n"
                f"  Before: {format_size(result['before'])}\n"
                f"  After : {format_size(result['after'])}\n"
                f"  Saved : {result['reduction']:.1f}%\n"
            )

    print("=" * 40)
    print("SUMMARY")
    print("Before:", format_size(total_before))
    print("After :", format_size(total_after))
    print("Saved :", f"{100 - (total_after / total_before * 100):.1f}%")
    print("=" * 40)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compress videos into website-friendly MP4 files."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="./videos",
        help="Video file or folder to compress. Default: ./videos",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="./videos_optimized",
        help="Folder for compressed videos. Default: ./videos_optimized",
    )
    parser.add_argument(
        "--crf",
        type=int,
        default=28,
        help="Quality level. Lower is better quality/larger file. Try 23-30. Default: 28",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=1280,
        help="Maximum video width. Default: 1280",
    )
    parser.add_argument(
        "--max-fps",
        type=int,
        default=30,
        help="Maximum frame rate. Default: 30",
    )
    parser.add_argument(
        "--preset",
        default="medium",
        choices=[
            "ultrafast",
            "superfast",
            "veryfast",
            "faster",
            "fast",
            "medium",
            "slow",
            "slower",
            "veryslow",
        ],
        help="Compression speed. Slower usually makes smaller files. Default: medium",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="How many files to compress at once. Default: up to 4",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    compress_path(
        path=args.path,
        output_dir=args.output_dir,
        crf=args.crf,
        preset=args.preset,
        max_width=args.max_width,
        max_fps=args.max_fps,
        workers=args.workers,
    )
