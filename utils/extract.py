import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time


def scrape_fashion_studio():
    """
    Melakukan scraping data produk dari website Fashion Studio.
    Mengambil data dari 50 halaman (halaman 1 sampai 50).
    Setiap halaman berisi 20 produk, total 1000 produk.
    
    Returns:
        pd.DataFrame: DataFrame berisi data mentah produk.
    """
    base_url = "https://fashion-studio.dicoding.dev"
    all_products = []
    
    logging.info("Memulai scraping 50 halaman...")
    
    # Looping halaman 1 sampai 50
    for page in range(1, 51):
        # Halaman 1 = root URL, halaman 2+ = /page{n}
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
            
            # Setiap produk ada di dalam div.collection-card
            products = soup.find_all('div', class_='collection-card')
            
            if not products:
                logging.warning(f"Halaman {page} berhasil dibuka tapi tidak ada produk.")
                continue

            for p in products:
                # Ambil judul produk dari h3.product-title
                title_tag = p.find('h3', class_='product-title')
                title = title_tag.text.strip() if title_tag else "Unknown Product"
                
                # Ambil harga dari span.price
                price_tag = p.find('span', class_='price')
                price = price_tag.text.strip() if price_tag else None
                
                # Rating, Colors, Size, Gender ada di tag <p> biasa
                # Identifikasi berdasarkan teks konten
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
            
            logging.info(f"Halaman {page}: {len(products)} produk berhasil diambil.")
            
            # Delay antar request untuk menghindari rate limit
            time.sleep(0.5)
            
        except Exception as e:
            logging.error(f"Error di halaman {page}: {e}")
            
    df_result = pd.DataFrame(all_products)
    return df_result