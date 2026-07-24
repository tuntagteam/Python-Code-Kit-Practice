import os
import requests
import pandas as pd
from pathlib import Path
from PIL import Image
from supabase import create_client
from tqdm import tqdm
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

# ---------------- CONFIG ----------------
load_dotenv()
CSV_FILE = "products_rows.csv"
UPLOAD_FOLDER = "./downloads"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
BUCKET = os.getenv("SUPABASE_BUCKET")
SEARCH_LIMIT = 10
MAX_SIZE_MB = 1
MAX_RESOLUTION = 2000
WORKERS = 8
MIN_IMAGE_SIZE = 200  # skip tiny icons/logos
PRODUCT_TABLE = "products"
# ----------------------------------------
missing = []
if not SUPABASE_URL:
    missing.append("SUPABASE_URL")
if not SUPABASE_KEY:
    missing.append("SUPABASE_SERVICE_ROLE_KEY")
if not BUCKET:
    missing.append("SUPABASE_BUCKET")
if missing:
    raise RuntimeError(
        "Missing environment variables: "
        + ", ".join(missing)
        + "\nCreate a .env file next to this script, for example:\n"
        + "SUPABASE_URL=https://your-project.supabase.co\n"
        + "SUPABASE_SERVICE_ROLE_KEY=your_service_role_key\n"
        + "SUPABASE_BUCKET=product-images\n"
    )
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- COMPRESSION ----------------
def compress_png(path):
    subprocess.run(
        ["pngquant", "--force", "--quality=60-80", "--ext", ".png", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["optipng", "-o7", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def compress_jpg(path):
    subprocess.run(
        ["jpegoptim", "--strip-all", "--max=75", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def resize_if_large(path):
    with Image.open(path) as img:
        w, h = img.size
        if max(w, h) > MAX_RESOLUTION:
            scale = MAX_RESOLUTION / max(w, h)
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.LANCZOS)
            img.save(path)

def ensure_under_1mb(path):
    size = Path(path).stat().st_size / (1024 * 1024)
    if size > MAX_SIZE_MB:
        with Image.open(path) as img:
            img.save(path, quality=70, optimize=True)

# Convert image to WebP format
def convert_to_webp(path):
    path = Path(path)
    webp_path = path.with_suffix(".webp")
    quality_steps = [80, 70, 60, 50, 40]
    with Image.open(path) as img:
        if image_has_transparency(img):
            working = img.convert("RGBA")
        else:
            working = img.convert("RGB")
        for quality in quality_steps:
            working.save(webp_path, "WEBP", quality=quality, method=6)
            size_mb = webp_path.stat().st_size / (1024 * 1024)
            if size_mb <= MAX_SIZE_MB:
                break
    try:
        os.remove(path)
    except:
        pass
    return webp_path

def image_has_transparency(img):
    try:
        if img.mode in ("RGBA", "LA"):
            alpha = img.getchannel("A")
            lo, hi = alpha.getextrema()
            return lo < 255
        if img.mode == "P" and "transparency" in img.info:
            return True
    except:
        pass
    return False

def estimate_background_whiteness(img):
    try:
        rgb = img.convert("RGB")
        w, h = rgb.size
        points = [
            (0, 0),
            (w - 1, 0),
            (0, h - 1),
            (w - 1, h - 1),
            (w // 2, 0),
            (w // 2, h - 1),
            (0, h // 2),
            (w - 1, h // 2),
        ]
        score = 0
        for x, y in points:
            r, g, b = rgb.getpixel((x, y))
            if r >= 235 and g >= 235 and b >= 235:
                score += 1
        return score / len(points)
    except:
        return 0.0

def score_image_file(path):
    try:
        with Image.open(path) as img:
            w, h = img.size
            if min(w, h) < MIN_IMAGE_SIZE:
                return -1
            ratio = w / h if h else 999
            if ratio < 0.4 or ratio > 2.5:
                return -1
            score = 0
            if image_has_transparency(img):
                score += 5
            white_score = estimate_background_whiteness(img)
            score += int(white_score * 4)
            area = w * h
            if area >= 500 * 500:
                score += 2
            if area >= 900 * 900:
                score += 2
            if 0.75 <= ratio <= 1.35:
                score += 2
            elif 0.6 <= ratio <= 1.8:
                score += 1
            return score
    except:
        return -1

# ---------------- SCRAPE IMAGES FROM DIFFERENT SOURCES ----------------
def scrape_google(query):
    image_links = []
    search_url = f"https://www.google.com/search?tbm=isch&q={requests.utils.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        res = requests.get(search_url, headers=headers, timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and src.startswith('http'):
                    image_links.append(src)
    except Exception as e:
        print(f"Error scraping Google: {e}")
    return image_links[:SEARCH_LIMIT]

def scrape_bing(query):
    image_links = []
    search_url = f"https://www.bing.com/images/search?q={requests.utils.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        res = requests.get(search_url, headers=headers, timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.find_all('div', class_='item'):
                a_tag = item.find('a', class_='iusc')
                if a_tag and 'm' in a_tag.attrs:
                    import json
                    meta = json.loads(a_tag['m'])
                    if 'murl' in meta:
                        image_links.append(meta['murl'])
    except Exception as e:
        print(f"Error scraping Bing: {e}")
    return image_links[:SEARCH_LIMIT]

def scrape_yahoo(query):
    image_links = []
    search_url = f"https://images.search.yahoo.com/search/images?p={requests.utils.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        res = requests.get(search_url, headers=headers, timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for a in soup.find_all('a', class_='thmb'):
                href = a.get('href')
                if href:
                    parsed = urlparse(href)
                    qs = parse_qs(parsed.query)
                    if 'imgurl' in qs:
                        image_links.append(qs['imgurl'][0])
    except Exception as e:
        print(f"Error scraping Yahoo: {e}")
    return image_links[:SEARCH_LIMIT]

# ---------------- DOWNLOAD IMAGE ----------------
def download_image(query, filename):
    candidates = []
    search_query = f"{query} product packshot png Thai food"  # Added "Thai food" to improve relevance
    sources = [scrape_google, scrape_bing, scrape_yahoo]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    for scrape_func in sources:
        image_links = scrape_func(search_query)
        for i, url in enumerate(image_links):
            try:
                res = requests.get(url, headers=headers, timeout=15)
                if res.status_code != 200 or not res.content:
                    continue
                ext = url.split('.')[-1].lower()
                if ext not in ['jpg', 'jpeg', 'png']:
                    continue
                tmp_name = Path(filename).with_name(
                    Path(filename).stem + f"_tmp_{len(candidates)}_{i}.{ext}"
                )
                with open(tmp_name, "wb") as f:
                    f.write(res.content)
                score = score_image_file(tmp_name)
                if score >= 0:
                    candidates.append((score, str(tmp_name)))
                else:
                    try:
                        os.remove(tmp_name)
                    except:
                        pass
            except Exception as e:
                print(f"Error downloading {url}: {e}")
                continue
        if candidates:
            break  # Stop if we found candidates from this source

    if not candidates:
        return False
    candidates.sort(key=lambda x: x[0], reverse=True)
    best_path = candidates[0][1]
    os.replace(best_path, filename)
    for _, extra_path in candidates[1:]:
        try:
            os.remove(extra_path)
        except:
            pass
    return True

# ---------------- PROCESS IMAGE ----------------
def process_image(path):
    resize_if_large(path)
    ext = Path(path).suffix.lower()
    if ext == ".png":
        compress_png(path)
    if ext in [".jpg", ".jpeg"]:
        compress_jpg(path)
    ensure_under_1mb(path)
    # convert to webp after compression
    webp_path = convert_to_webp(path)
    return webp_path

# ---------------- UPLOAD SUPABASE ----------------
def upload_to_supabase(path, product_id):
    file_name = f"{product_id}.webp"
    with open(path, "rb") as f:
        supabase.storage.from_(BUCKET).upload(
            file_name,
            f,
            {"content-type": "image/webp", "x-upsert": "true"}
        )
    public_url = supabase.storage.from_(BUCKET).get_public_url(file_name)
    # update product table with image url
    try:
        supabase.table(PRODUCT_TABLE).update(
            {"image_url": public_url}
        ).eq("id", product_id).execute()
    except Exception as e:
        print("DB update failed:", e)
    return public_url

def process_product(row):
    product_id = row["id"]
    name = row["name_en"]
    filename = f"{UPLOAD_FOLDER}/{product_id}.png"
    webp_filename = f"{UPLOAD_FOLDER}/{product_id}.webp"
    if Path(filename).exists() or Path(webp_filename).exists():
        return f"Skip existing: {product_id}"
    try:
        ok = download_image(name, filename)
        if not ok:
            return f"❌ Image not found: {name}"
        webp_path = process_image(filename)
        url = upload_to_supabase(webp_path, product_id)
        return f"Uploaded: {url}"
    except Exception as e:
        return f"Error processing {name}: {e}"

# ---------------- MAIN PIPELINE ----------------
df = pd.read_csv(CSV_FILE)
print(f"🚀 Starting parallel crawler with {WORKERS} workers")
rows = [row for _, row in df.iterrows()]
with ThreadPoolExecutor(max_workers=WORKERS) as executor:
    futures = [executor.submit(process_product, row) for row in rows]
    for future in tqdm(as_completed(futures), total=len(futures)):
        print(future.result())