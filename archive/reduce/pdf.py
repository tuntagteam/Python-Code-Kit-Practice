import os
import subprocess
import tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def format_size(bytes_size):
    return f"{bytes_size / (1024 * 1024):.2f} MB"


def compress_pdf(input_path, quality="ebook"):
    input_path = Path(input_path)
    original_size = input_path.stat().st_size

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        temp_output = tmp.name

    command = [
        "gs",   # ถ้า Windows ใช้ "gswin64c"
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={temp_output}",
        str(input_path)
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    compressed_size = Path(temp_output).stat().st_size
    os.replace(temp_output, input_path)

    reduction = 100 - (compressed_size / original_size * 100)

    return {
        "file": input_path.name,
        "before": original_size,
        "after": compressed_size,
        "reduction": reduction
    }


def compress_folder(folder_path, quality="ebook", workers=os.cpu_count()):
    folder = Path(folder_path)
    pdf_files = list(folder.glob("*.pdf"))

    total_before = 0
    total_after = 0

    print(f"\nCompressing {len(pdf_files)} files...\n")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(compress_pdf, f, quality) for f in pdf_files]

        for future in as_completed(futures):
            result = future.result()
            total_before += result["before"]
            total_after += result["after"]

            print(
                f"{result['file']}\n"
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


# 👇 แก้ path ตรงนี้
compress_folder(
    folder_path="./pdf",  # เปลี่ยนเป็นโฟลเดอร์คุณ
    quality="ebook"  # screen / ebook / printer
)