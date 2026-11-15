# FILE: configs/config.py

import os

SEED = 42

MODEL_NAME = "distilbert/distilbert-base-multilingual-cased"
MAX_LENGTH = 195

DATA_PATH = "data/raw/tickets.csv"
OUTPUT_BASE = "artifacts"
OUTPUT_DIR = os.path.join(OUTPUT_BASE, "standard_distilbert")

LEARNING_RATE = 2e-5
TRAIN_BATCH_SIZE = 16
EVAL_BATCH_SIZE = 32
GRADIENT_ACCUMULATION_STEPS = 1
NUM_TRAIN_EPOCHS = 4
WEIGHT_DECAY = 0.01

EARLY_STOPPING_PATIENCE = 2