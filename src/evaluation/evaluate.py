# FILE: src/evaluation/evaluate.py

import os
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from configs.config import OUTPUT_DIR


def evaluate_predictions(y_true, y_pred, class_names, output_dir=OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "weighted_f1": f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0,
        ),
    }

    print("Evaluation metrics:")
    print(metrics)

    report = classification_report(
        y_true,
        y_pred,
        labels=np.arange(len(class_names)),
        target_names=class_names,
        zero_division=0,
        output_dict=True,
    )

    print("\nClassification report:")
    print(
        classification_report(
            y_true,
            y_pred,
            labels=np.arange(len(class_names)),
            target_names=class_names,
            zero_division=0,
        )
    )

    pd.DataFrame(report).transpose().to_csv(
        os.path.join(output_dir, "classification_report.csv")
    )

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=np.arange(len(class_names)),
    )

    pd.DataFrame(
        matrix,
        index=class_names,
        columns=class_names,
    ).to_csv(
        os.path.join(output_dir, "confusion_matrix.csv")
    )

    with open(
        os.path.join(output_dir, "evaluation_metrics.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(metrics, f, indent=2)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.imshow(matrix, interpolation="nearest")
    ax.set_title("Support Queue Confusion Matrix")
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    ax.set_xticks(np.arange(len(class_names)))
    ax.set_yticks(np.arange(len(class_names)))
    ax.set_xticklabels(class_names, rotation=90)
    ax.set_yticklabels(class_names)
    plt.tight_layout()

    fig.savefig(
        os.path.join(output_dir, "confusion_matrix.png"),
        dpi=150,
    )
    plt.show()

    return metrics