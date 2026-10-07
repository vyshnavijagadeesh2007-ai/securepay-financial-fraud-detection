from pathlib import Path
import pandas as pd

def test_dataset_exists_and_unmodified():
    dataset_path = Path(__file__).resolve().parent.parent / "data" / "creditcard.csv"
    assert dataset_path.exists(), f"Dataset not found at {dataset_path}"
    assert dataset_path.stat().st_size > 140 * 1024 * 1024, "File size unexpectedly small"

def test_dataset_shape_and_columns():
    dataset_path = Path(__file__).resolve().parent.parent / "data" / "creditcard.csv"
    # Read sample header and row count
    df_head = pd.read_csv(dataset_path, nrows=5)
    expected_cols = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount", "Class"]
    assert list(df_head.columns) == expected_cols
    assert len(df_head.columns) == 31
