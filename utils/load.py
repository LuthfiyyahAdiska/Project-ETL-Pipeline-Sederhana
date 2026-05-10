import os
import gspread

def save_to_csv(df):
    """
    Menyimpan DataFrame ke file CSV di direktori kerja saat ini
    dan meng-uploadnya ke Google Sheets.
    
    Args:
        df: DataFrame yang akan disimpan
        
    Returns:
        str: path file CSV jika berhasil, None jika gagal
    """
    try:
        # 1. Simpan ke CSV lokal
        try:
            path = os.path.join(os.getcwd(), "products.csv")
            df.to_csv(path, index=False)
            print("Saved locally:", path)
        except Exception as e:
            print(f"Warning: Gagal menyimpan CSV lokal (Mungkin file sedang dibuka di Excel?): {e}")
            path = None
        
        # 2. Upload ke Google Sheets
        try:
            print("Mengupload ke Google Sheets...")
            
            gc = gspread.service_account(filename="etl-submission-pemda-b82b806d5816.json")
            
            sh = gc.open_by_key("1DpF-uYjNgLxrR3czssjIsp2-Yu0GVHMC0zqzjnyQVXE")
            
            worksheet = sh.sheet1
            
            worksheet.clear()
            
            data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
            
            worksheet.update(values=data_to_upload, range_name="A1")
            print("Berhasil diupload ke Google Sheets!")
        except Exception as sheet_error:
            print("Gagal upload ke Google Sheets:", sheet_error)
            
        return path
    except Exception as e:
        print("Error in save_to_csv:", e)
        return None