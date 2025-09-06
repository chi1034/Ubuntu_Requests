import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """
    Extract filename from URL, or generate one if missing.
    Uses hash to avoid duplicates.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    if not filename or '.' not in filename:  
        # No proper filename in URL, generate one
        filename = "image_" + hashlib.md5(url.encode()).hexdigest()[:8] + ".jpg"

    return filename

def download_image(url):
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)

        # Add headers to mimic a real browser
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0 Safari/537.36"
            )
        }

        # Fetch the image with timeout and headers
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Check content type
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped: {url} (not an image, Content-Type={content_type})")
            return

        # Extract or generate filename
        filename = get_filename_from_url(url)
        filepath = os.path.join("Fetched_Images", filename)

        # Prevent duplicates
        if os.path.exists(filepath):
            print(f"✓ Skipped duplicate: {filename}")
            return

        # Handle SVG as text, others as binary
        if content_type == "image/svg+xml" or filename.lower().endswith(".svg"):
            mode = "w"
            content = response.text
        else:
            mode = "wb"
            content = response.content

        with open(filepath, mode) as f:
            f.write(content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Accept multiple URLs (comma separated)
    urls = input("Please enter one or more image URLs (comma separated): ").split(",")

    for url in [u.strip() for u in urls if u.strip()]:
        download_image(url)

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
