import pandas as pd
from utils.transform import transform_data


# =========================
# TEST 1: VALID TRANSFORM
# =========================
def test_transform_valid():
    df = pd.DataFrame([{
        "Title": "T-shirt",
        "Price": "$10.00",
        "Rating": "Rating: ⭐ 4.5 / 5",
        "Colors": "3 Colors",
        "Size": "Size: M",
        "Gender": "Gender: Men"
    }])

    result = transform_data(df)

    assert not result.empty
    assert result.iloc[0]["Price"] == 160000.0
    assert result.iloc[0]["Rating"] == 4.5
    assert result.iloc[0]["Size"] == "M"
    assert result.iloc[0]["Gender"] == "Men"


# =========================
# TEST 2: REMOVE UNKNOWN PRODUCT
# =========================
def test_transform_removes_unknown():
    df = pd.DataFrame([{
        "Title": "Unknown Product",
        "Price": "$10.00",
        "Rating": "Rating: ⭐ 4.5 / 5",
        "Colors": "3 Colors",
        "Size": "Size: M",
        "Gender": "Gender: Men"
    }])

    result = transform_data(df)

    assert result.empty


# =========================
# TEST 3: DROPS NULL ROWS
# =========================
def test_transform_drops_nulls():
    df = pd.DataFrame([{
        "Title": "T-shirt",
        "Price": None,
        "Rating": "Rating: ⭐ 4.5 / 5",
        "Colors": "3 Colors",
        "Size": "Size: M",
        "Gender": "Gender: Men"
    }])

    result = transform_data(df)

    assert result.empty


# =========================
# TEST 4: NONE INPUT
# =========================
def test_transform_none_input():
    result = transform_data(None)

    assert result is None


# =========================
# TEST 5: EMPTY DATAFRAME
# =========================
def test_transform_empty_df():
    result = transform_data(pd.DataFrame())

    assert result is None