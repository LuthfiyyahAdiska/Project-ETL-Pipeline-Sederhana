import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time

def scrape_fashion_studio():
    base_url = "https://fashion-studio.dicoding.dev"
    all_products = []
    
    logging.info("Memulai scraping 50 halaman...")
    
    for page in range(1, 51): 
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}/page{page}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                logging.warning(f"Halaman {page} tidak ditemukan (Status: {response.status_code})")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            products = soup.find_all('div', class_='collection-card')
            
            if not products:
                logging.warning(f"Halaman {page} berhasil dibuka tapi tidak ada 'collection-card'.")
                continue

            for p in products:
                title_tag = p.find('h3', class_='product-title')
                title = title_tag.text.strip() if title_tag else "Unknown Product"
                
                price_tag = p.find('span', class_='price')
                price = price_tag.text.strip() if price_tag else None
                
                all_p_tags = p.find_all('p')
                rating = None
                colors = None
                size = None
                gender = None
                
                for tag in all_p_tags:
                    text = tag.text.strip()
                    if text.startswith('Rating:') or '⭐' in text:
                        rating = text
                    elif 'Colors' in text:
                        colors = text
                    elif text.startswith('Size:'):
                        size = text
                    elif text.startswith('Gender:'):
                        gender = text
                
                all_products.append({
                    'Title': title,
                    'Price': price,
                    'Rating': rating,
                    'Colors': colors,
                    'Size': size,
                    'Gender': gender
                })
            
            logging.info(f"✅ Halaman {page}: Berhasil mengambil {len(products)} produk.")
            
        except Exception as e:
            logging.error(f"❌ Error di halaman {page}: {e}")
            
    df_result = pd.DataFrame(all_products)
    return df_result