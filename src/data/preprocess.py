# FILE: src/data/preprocess.py

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from configs.config import SEED


def load_and_clean_data(data_path):
    df = pd.read_csv(data_path)

    required_columns = {"text", "queue"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    data = df[["text", "queue"]].copy()

    data["text"] = (
        data["text"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    data["queue"] = (
        data["queue"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    data = data[
        (data["text"] != "") &
        (data["queue"] != "")
    ].reset_index(drop=True)

    before_dedup = len(data)

    data = data.drop_duplicates(
        subset=["text", "queue"]
    ).reset_index(drop=True)

    print("Duplicate rows removed:", before_dedup - len(data))
    print("Dataset size:", len(data))

    return data


def encode_and_split(data):
    encoder = LabelEncoder()

    data = data.copy()
    data["label"] = encoder.fit_transform(data["queue"])

    num_labels = len(encoder.classes_)

    print("Number of classes:", num_labels)
    print("Queue distribution:")
    print(data["queue"].value_counts())

    class_counts = data["label"].value_counts()

    if class_counts.min() < 3:
        raise ValueError(
            "Each queue needs at least 3 examples "
            "for the stratified split."
        )

    train_df, temp_df = train_test_split(
        data,
        test_size=0.20,
        random_state=SEED,
        stratify=data["label"],
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=SEED,
        stratify=temp_df["label"],
    )

    print("Training examples:", len(train_df))
    print("Validation examples:", len(val_df))
    print("Test examples:", len(test_df))

    return train_df, val_df, test_df, encoder