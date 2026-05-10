import os

def save_to_csv(df):
    try:
        path = os.path.join(os.getcwd(), "products.csv")
        df.to_csv(path, index=False)
        print("Saved:", path)
        return path
    except Exception as e:
        print("Error saving CSV:", e)
        return None