from bs4 import BeautifulSoup
import requests
import os

def download_google_images(search_term, max_images=10):
  url = f"https://www.google.com/search?q={search_term}&tbm=isch"
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
  }
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = BeautifulSoup(response.content, "html.parser")
    image_tags = soup.find_all("img")
    image_urls = [img.get("src") for img in image_tags if img.get("src") and "http" in img.get("src")]
    if not os.path.exists(f"/opt/airflow/images/images_{search_term}"):
      os.makedirs(f"/opt/airflow/images/images_{search_term}")
    for i, image_url in enumerate(image_urls[:max_images]):
      try:
        image_data = requests.get(image_url).content
        with open(f"/opt/airflow/images/images_{search_term}/{search_term}_{i + 1}.jpg", "wb") as f:
          f.write(image_data)
        print(f"Downloaded image {i + 1}/{max_images}")
      except Exception as e:
        print(f"Error downloading image {i + 1}: {e}")
  except requests.exceptions.RequestException as e:
    print(f"Error fetching images: {e}")


