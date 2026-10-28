import os
import glob
import requests
from bs4 import BeautifulSoup

# Config Pinterest
PINTEREST_ACCESS_TOKEN = os.environ.get("PINTEREST_ACCESS_TOKEN")
BOARD_ID = os.environ.get("PINTEREST_BOARD_ID")
BASE_URL = "https://www.vetnaturel.fr/"

def extract_article_info(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Extraire les métadonnées SEO
    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag['content'] if desc_tag else ""
    
    # Construire l'URL canonique ou relative
    page_name = os.path.basename(html_file)
    link = f"{BASE_URL}{page_name}"
    
    # Image de couverture par défaut ou extraite du HTML
    img_tag = soup.find('meta', property='og:image')
    image_url = img_tag['content'] if img_tag else "https://www.vetnaturel.fr/images/banner-default.jpg"

    return {
        "title": title,
        "description": description,
        "link": link,
        "image_url": image_url
    }

def create_pinterest_pin(title, description, link, image_url):
    url = "https://api.pinterest.com/v5/pins"
    headers = {
        "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "board_id": BOARD_ID,
        "title": title[:100],
        "description": description[:500],
        "link": link,
        "media_source": {
            "source_type": "image_url",
            "url": image_url
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    html_files = [f for f in glob.glob("*.html") if f not in ["index.html", "mentions-legales.html", "politique-confidentialite.html"]]
    
    for file in html_files:
        info = extract_article_info(file)
        if info["title"]:
            print(f"Publication de l'épingle pour : {info['title']}")
            # res = create_pinterest_pin(info["title"], info["description"], info["link"], info["image_url"])
            # print(res)
