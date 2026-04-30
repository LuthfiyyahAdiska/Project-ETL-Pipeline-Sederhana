import os

def save_to_csv(df):
    try:
        path = os.path.join(os.getcwd(), "products.csv")
        df.to_csv(path, index=False)
        return path
    except Exception:
        return None