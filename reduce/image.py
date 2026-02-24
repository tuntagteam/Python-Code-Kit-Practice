import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image


def format_size(b):
    return f"{b / (1024 * 1024):.2f} MB"


def compress_jpg(path, quality=75):
    subprocess.run(
        [
            "jpegoptim",
            "--strip-all",
            "--all-progressive",
            f"--max={quality}",
            str(path)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def compress_png(path):
    # pngquant (lossy but still PNG)
    subprocess.run(
        [
            "pngquant",
            "--force",
            "--quality=60-80",
            "--skip-if-larger",
            "--ext", ".png",
            str(path)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # optipng (lossless optimization)
    subprocess.run(
        [
            "optipng",
            "-o7",
            str(path)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def resize_if_large(path, max_size=2500):
    with Image.open(path) as img:
        w, h = img.size
        if max(w, h) > max_size:
            scale = max_size / max(w, h)
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.LANCZOS)
            img.save(path)


def process_image(path):
    path = Path(path)
    before = path.stat().st_size

    try:
        resize_if_large(path)

        if path.suffix.lower() in [".jpg", ".jpeg"]:
            compress_jpg(path)

        elif path.suffix.lower() == ".png":
            compress_png(path)

    except Exception as e:
        return f"❌ {path.name} failed: {e}"

    after = path.stat().st_size
    saved = 100 - (after / before * 100)

    return (
        f"{path.name}\n"
        f"  Before: {format_size(before)}\n"
        f"  After : {format_size(after)}\n"
        f"  Saved : {saved:.1f}%\n"
    )


def compress_folder(folder):
    files = []
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        files.extend(Path(folder).glob(ext))

    total_before = sum(f.stat().st_size for f in files)
    total_after = 0

    print(f"\n🔥 Strong compressing {len(files)} images...\n")

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as ex:
        futures = [ex.submit(process_image, f) for f in files]
        for f in as_completed(futures):
            print(f.result())

    total_after = sum(f.stat().st_size for f in files)

    print("=" * 50)
    print("SUMMARY")
    print("Before:", format_size(total_before))
    print("After :", format_size(total_after))
    print("Saved :", f"{100 - (total_after / total_before * 100):.1f}%")
    print("=" * 50)


# 👇 CHANGE PATH HERE
compress_folder(r"C:\Your\Image\Folder")