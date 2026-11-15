# FILE: src/models/train.py

import os
import json
import inspect

import numpy as np
import pandas as pd
import torch

from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    EarlyStoppingCallback,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    set_seed,
)

from configs.config import (
    SEED,
    MODEL_NAME,
    MAX_LENGTH,
    DATA_PATH,
    OUTPUT_DIR,
    TRAIN_BATCH_SIZE,
    EVAL_BATCH_SIZE,
    GRADIENT_ACCUMULATION_STEPS,
    NUM_TRAIN_EPOCHS,
    LEARNING_RATE,
    WEIGHT_DECAY,
    EARLY_STOPPING_PATIENCE,
)

from src.data.preprocess import (
    load_and_clean_data,
    encode_and_split,
)


def prepare_dataset(frame, tokenizer):
    ds = Dataset.from_pandas(
        frame[["text", "label"]].reset_index(drop=True),
        preserve_index=False,
    )

    ds = ds.map(
        lambda batch: tokenizer(
            batch["text"],
            truncation=True,
            max_length=MAX_LENGTH,
        ),
        batched=True,
    )

    ds = ds.remove_columns(["text"])
    ds = ds.rename_column("label", "labels")

    return ds


def compute_metrics(eval_pred):
    logits = eval_pred.predictions

    if isinstance(logits, tuple):
        logits = logits[0]

    labels = eval_pred.label_ids
    predictions = np.argmax(logits, axis=-1)

    return {
        "accuracy": accuracy_score(labels, predictions),
        "macro_f1": f1_score(
            labels,
            predictions,
            average="macro",
            zero_division=0,
        ),
        "weighted_f1": f1_score(
            labels,
            predictions,
            average="weighted",
            zero_division=0,
        ),
    }


def make_training_args(output_dir):
    params = inspect.signature(
        TrainingArguments.__init__
    ).parameters

    args = {
        "output_dir": output_dir,
        "learning_rate": LEARNING_RATE,
        "per_device_train_batch_size": TRAIN_BATCH_SIZE,
        "per_device_eval_batch_size": EVAL_BATCH_SIZE,
        "gradient_accumulation_steps": GRADIENT_ACCUMULATION_STEPS,
        "num_train_epochs": NUM_TRAIN_EPOCHS,
        "weight_decay": WEIGHT_DECAY,
        "load_best_model_at_end": True,
        "metric_for_best_model": "eval_accuracy",
        "greater_is_better": True,
        "fp16": torch.cuda.is_available(),
        "report_to": "none",
        "save_total_limit": 1,
        "seed": SEED,
    }

    if "eval_strategy" in params:
        args["eval_strategy"] = "epoch"
    elif "evaluation_strategy" in params:
        args["evaluation_strategy"] = "epoch"
    else:
        raise RuntimeError(
            "No supported evaluation strategy found."
        )

    optional_args = {
        "save_strategy": "epoch",
        "logging_strategy": "epoch",
        "warmup_ratio": 0.1,
        "dataloader_num_workers": 0,
        "use_cpu": not torch.cuda.is_available(),
    }

    for key, value in optional_args.items():
        if key in params:
            args[key] = value

    return TrainingArguments(
        **{
            key: value
            for key, value in args.items()
            if key in params
        }
    )


def train_model():
    set_seed(SEED)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = load_and_clean_data(DATA_PATH)

    train_df, val_df, test_df, encoder = encode_and_split(data)

    id2label = {
        idx: str(label)
        for idx, label in enumerate(encoder.classes_)
    }

    label2id = {
        label: idx
        for idx, label in id2label.items()
    }

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_ds = prepare_dataset(train_df, tokenizer)
    val_ds = prepare_dataset(val_df, tokenizer)
    test_ds = prepare_dataset(test_df, tokenizer)

    collator = DataCollatorWithPadding(
        tokenizer=tokenizer
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(encoder.classes_),
        id2label=id2label,
        label2id=label2id,
    )

    trainer = Trainer(
        model=model,
        args=make_training_args(OUTPUT_DIR),
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=collator,
        compute_metrics=compute_metrics,
        callbacks=[
            EarlyStoppingCallback(
                early_stopping_patience=EARLY_STOPPING_PATIENCE
            )
        ],
    )

    print("Model:", MODEL_NAME)
    print("Class weighting: False")

    trainer.train()

    print("Best checkpoint:", trainer.state.best_model_checkpoint)
    print("Best validation accuracy:", trainer.state.best_metric)

    test_results = trainer.evaluate(
        eval_dataset=test_ds,
        metric_key_prefix="test",
    )

    predictions_output = trainer.predict(test_ds)

    logits = predictions_output.predictions

    if isinstance(logits, tuple):
        logits = logits[0]

    predictions = np.argmax(logits, axis=-1)

    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    with open(
        os.path.join(OUTPUT_DIR, "label_classes.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            encoder.classes_.tolist(),
            f,
            indent=2,
            ensure_ascii=False,
        )

    pd.DataFrame(
        trainer.state.log_history
    ).to_csv(
        os.path.join(OUTPUT_DIR, "training_history.csv"),
        index=False,
    )

    with open(
        os.path.join(OUTPUT_DIR, "test_metrics.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            {
                key: float(value)
                for key, value in test_results.items()
            },
            f,
            indent=2,
        )

    print("Test metrics:", test_results)
    print("Model saved to:", OUTPUT_DIR)

    return trainer, test_ds, predictions_output, encoder


if __name__ == "__main__":
    train_model()