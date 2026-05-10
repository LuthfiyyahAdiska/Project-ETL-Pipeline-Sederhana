import os


def save_to_csv(df):
    """
    Menyimpan DataFrame ke file CSV di direktori kerja saat ini.
    
    Args:
        df: DataFrame yang akan disimpan
        
    Returns:
        str: path file CSV jika berhasil, None jika gagal
    """
    try:
        path = os.path.join(os.getcwd(), "products.csv")
        df.to_csv(path, index=False)
        print("Saved:", path)
        return path
    except Exception as e:
        print("Error saving CSV:", e)
        return None