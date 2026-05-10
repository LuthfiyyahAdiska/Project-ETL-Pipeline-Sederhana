from utils.extract import scrape_fashion_studio
from utils.transform import transform_data
from utils.load import save_to_csv

def main():
    print("START")

    # EXTRACT
    raw_data = scrape_fashion_studio()
    print("EXTRACT:", len(raw_data))

    if raw_data.empty:
        print("❌ Waduh, data tidak ditemukan! Cek URL website-nya ya.")
        return 

    # TRANSFORM
    df = transform_data(raw_data) 
    if df is not None:
        print("TRANSFORM:", len(df))
    else:
        print("❌ Data setelah dibersihkan jadi kosong.")

    # LOAD (INI KUNCI)
    save_to_csv(df)

    print(df.head())
    print(df.columns)
    print("DONE")

if __name__ == "__main__":
    main()