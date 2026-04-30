from utils.extract import scrape_all
from utils.transform import transform_data
import urllib3
urllib3.disable_warnings()  

print("START")

# EXTRACT
data = scrape_all()
print("EXTRACT:", len(data))

# TRANSFORM
df = transform_data(data)
print("TRANSFORM:", len(df))

print("DONE")

# ❗ INI BARU BENAR
print(df.isnull().sum())