import pytest
from utils.load import save_to_csv

def test_save_to_csv_success():
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2]})
    result = save_to_csv(df)

    assert result is not None
    assert result.endswith("products.csv")


def test_save_to_csv_error():
    class FakeDF:
        def to_csv(self, *args, **kwargs):
            raise Exception("forced error")

    result = save_to_csv(FakeDF())
    assert result is None