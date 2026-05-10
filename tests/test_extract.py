import requests
import pandas as pd
from utils import extract


# =========================
# TEST 1: SUCCESS PATH
# =========================
def test_scrape_success(monkeypatch):
    class FakeResponse:
        status_code = 200
        text = """
        <div class="collection-card">
            <h3 class="product-title">Test Product</h3>
            <div class="price-container"><span class="price">$10.00</span></div>
            <p>Rating: ⭐ 4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        """

    def fake_get(url, timeout=10):
        return FakeResponse()

    monkeypatch.setattr(extract.requests, "get", fake_get)

    result = extract.scrape_fashion_studio()

    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result.iloc[0]["Title"] == "Test Product"


# =========================
# TEST 2: FORCE 404 ERROR
# =========================
def test_scrape_404(monkeypatch):
    class FakeResponse:
        status_code = 404

    def fake_get(url, timeout=10):
        return FakeResponse()

    monkeypatch.setattr(extract.requests, "get", fake_get)

    result = extract.scrape_fashion_studio()

    assert isinstance(result, pd.DataFrame)
    assert result.empty


# =========================
# TEST 3: FORCE REQUEST EXCEPTION
# =========================
def test_scrape_request_error(monkeypatch):
    def fake_get(url, timeout=10):
        raise Exception("forced error")

    monkeypatch.setattr(extract.requests, "get", fake_get)

    result = extract.scrape_fashion_studio()

    assert isinstance(result, pd.DataFrame)
    assert result.empty


# =========================
# TEST 4: NO PRODUCT CARDS FOUND
# =========================
def test_scrape_no_products(monkeypatch):
    class FakeResponse:
        status_code = 200
        text = "<html><body><p>No products here</p></body></html>"

    def fake_get(url, timeout=10):
        return FakeResponse()

    monkeypatch.setattr(extract.requests, "get", fake_get)

    result = extract.scrape_fashion_studio()

    assert isinstance(result, pd.DataFrame)
    assert result.empty


# =========================
# TEST 5: MISSING FIELDS IN PRODUCT
# =========================
def test_scrape_missing_fields(monkeypatch):
    class FakeResponse:
        status_code = 200
        text = """
        <div class="collection-card">
            <h3 class="product-title">Incomplete Product</h3>
        </div>
        """

    def fake_get(url, timeout=10):
        return FakeResponse()

    monkeypatch.setattr(extract.requests, "get", fake_get)

    result = extract.scrape_fashion_studio()

    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result.iloc[0]["Title"] == "Incomplete Product"
    assert result.iloc[0]["Price"] is None