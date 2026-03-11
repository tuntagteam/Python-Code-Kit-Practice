import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

# Use service role key if available, otherwise anon key
api_key = SUPABASE_SERVICE_ROLE_KEY if SUPABASE_SERVICE_ROLE_KEY else SUPABASE_ANON_KEY
supabase: Client = create_client(SUPABASE_URL, api_key)


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

def update_product_image_url(product_id, image_url):
    """Update the image_url field in the products table"""
    try:
        response = supabase.table('products').update({
            'image_url': image_url
        }).eq('id', product_id).execute()
        
        if response.data:
            return f"✅ Updated product {product_id} with image URL"
        else:
            return f"❌ Failed to update product {product_id}"
    except Exception as e:
        return f"❌ Database update error for product {product_id}: {e}"

def resize_if_large(path, max_width=1600, max_height=1600):
    """
    Resize image if larger than the allowed size while keeping aspect ratio.
    """
    try:
        with Image.open(path) as img:
            width, height = img.size
            if width <= max_width and height <= max_height:
                return

            img.thumbnail((max_width, max_height))
            img.save(path)
    except Exception:
        pass

def compress_webp(path, quality=75):
    with Image.open(path) as img:
        img.save(path, 'WEBP', quality=quality, optimize=True)


def upload_to_supabase_bucket(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_name = Path(file_path).name

            ext = Path(file_path).suffix.lower()
            content_type = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.webp': 'image/webp'
            }.get(ext, 'application/octet-stream')

            supabase.storage.from_(SUPABASE_BUCKET).upload(
                file_name,
                f,
                {"content-type": content_type, "upsert": "true"}
            )

        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)

        return {
            "success": True,
            "file_name": file_name,
            "url": public_url
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def process_image(path, upload=False, update_db=False):
    path = Path(path)
    before = path.stat().st_size

    try:
        resize_if_large(path)

        if path.suffix.lower() in [".jpg", ".jpeg"]:
            compress_jpg(path)

        elif path.suffix.lower() == ".png":
            compress_png(path)

        elif path.suffix.lower() == ".webp":
            compress_webp(path)

        upload_result = ""
        db_result = ""

        if upload:
            upload_response = upload_to_supabase_bucket(path)

            if upload_response["success"]:
                upload_result = f"✅ Uploaded {upload_response['file_name']}"

                if update_db:
                    try:
                        product_id = int(path.stem)
                        db_result = update_product_image_url(
                            product_id,
                            upload_response["url"]
                        )
                    except:
                        db_result = "⚠️ Could not detect product_id from filename"
            else:
                upload_result = f"❌ Upload failed: {upload_response['error']}"

    except Exception as e:
        return f"❌ {path.name} failed: {e}"

    after = path.stat().st_size
    saved = 100 - (after / before * 100)

    result = (
        f"{path.name}\n"
        f"  Before: {format_size(before)}\n"
        f"  After : {format_size(after)}\n"
        f"  Saved : {saved:.1f}%\n"
    )
    if upload_result:
        result += f"  {upload_result}\n"
    if db_result:
        result += f"  {db_result}\n"
    return result


def compress_folder(folder, upload_to_supabase=False, update_database=False):
    files = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        files.extend(Path(folder).glob(ext))

    total_before = sum(f.stat().st_size for f in files)
    total_after = 0

    print(f"\n🔥 Strong compressing {len(files)} images...\n")

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as ex:
        futures = [ex.submit(process_image, f, upload_to_supabase, update_database) for f in files]
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
upload_to_supabase = True
update_database = True  # Set to True to update products table
compress_folder(r"./downloads", upload_to_supabase=upload_to_supabase, update_database=update_database)