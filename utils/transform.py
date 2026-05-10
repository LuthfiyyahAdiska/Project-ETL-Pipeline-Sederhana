import pandas as pd
from datetime import datetime


def transform_data(df):
    """
    Membersihkan dan mentransformasi data mentah hasil scraping.
    
    Langkah transformasi:
    1. Hapus baris dengan Title 'Unknown Product' (data tidak valid)
    2. Hapus duplikat dan baris yang memiliki nilai kosong (NaN)
    3. Konversi Price dari USD ke IDR (kurs 16000)
    4. Ekstrak nilai numerik dari Rating
    5. Ekstrak angka dari Colors (misal: '3 Colors' -> 3)
    6. Bersihkan prefix 'Size: ' dan 'Gender: '
    7. Tambahkan kolom timestamp
    
    Args:
        df: DataFrame hasil scraping atau None
        
    Returns:
        pd.DataFrame atau None jika input kosong
    """
    if df is None or df.empty:
        return None
    
    # Hapus produk yang tidak valid (title = Unknown Product)
    df = df[df['Title'] != "Unknown Product"].copy()
    
    # Hapus data duplikat dan baris dengan nilai kosong
    df = df.drop_duplicates().dropna()
    
    # Konversi harga dari USD ke IDR (kurs 16000)
    df['Price'] = df['Price'].str.replace('$', '').str.replace(',', '').astype(float) * 16000
    
    # Ekstrak nilai rating numerik (misal: "Rating: ⭐ 4.5 / 5" -> 4.5)
    df['Rating'] = df['Rating'].str.extract(r'(\d+\.?\d*)').astype(float)
    
    # Ekstrak angka dari Colors (misal: "3 Colors" -> 3)
    df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(int)
    
    # Hapus prefix 'Size: ' dan 'Gender: '
    df['Size'] = df['Size'].str.replace('Size: ', '')
    df['Gender'] = df['Gender'].str.replace('Gender: ', '')
    
    # Tambahkan timestamp kapan data diproses
    df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return df