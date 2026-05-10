import pandas as pd
from datetime import datetime

def transform_data(df):
    if df is None or df.empty:
        return None
        
    df = df[df['Title'] != "Unknown Product"].copy()
    
    df = df.drop_duplicates().dropna()
    
    df['Price'] = df['Price'].str.replace('$', '').str.replace(',', '').astype(float) * 16000
    
    df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    
    df['Size'] = df['Size'].str.replace('Size: ', '')
    df['Gender'] = df['Gender'].str.replace('Gender: ', '')
    
    df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return df