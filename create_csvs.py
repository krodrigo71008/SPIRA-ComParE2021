import glob
import random
import pandas as pd
from pathlib import Path
import os

if __name__ == "__main__":
    audio_csv = pd.read_csv("../data/public_dataset/metadata_compiled.csv")
    filter_1 = audio_csv["diagnosis_1"].notna()
    filter_2 = audio_csv["diagnosis_2"].notna()
    filter_3 = audio_csv["diagnosis_3"].notna()
    filter_4 = audio_csv["cough_detected"] > 0.8
    audio_csv = audio_csv[(filter_1 | filter_2 | filter_3) & filter_4]
    audio_csv["covid"] = ((audio_csv["diagnosis_1"] == "COVID-19") | 
                          (audio_csv["diagnosis_2"] == "COVID-19") | 
                          (audio_csv["diagnosis_3"] == "COVID-19")).astype(int)
    root_path = "../data/public_dataset"
    error = 0
    lines = []
    for i, v in audio_csv[["uuid"]].iterrows():
        if (not os.path.exists(os.path.join(root_path, f"{v.iloc[0]}.webm"))):
            error += 1
        else:
            lines.append(i)
    print(f"{error} files not found!")
    audio_csv = audio_csv.loc[lines, :]
    seed = 727
    SAMPLE_PERCENTAGE = 1.0
    TRAIN_PERCENTAGE = 0.7
    VAL_PERCENTAGE = 0.2
    TEST_PERCENTAGE = 1 - TRAIN_PERCENTAGE - VAL_PERCENTAGE
    random.seed(seed)
    final_csv = audio_csv.sample(int(len(audio_csv)*SAMPLE_PERCENTAGE), random_state=seed)
    train_len = int(len(final_csv)*TRAIN_PERCENTAGE)
    val_len = int(len(final_csv)*VAL_PERCENTAGE)
    train_csv = final_csv.iloc[:train_len, :]
    val_csv = final_csv.iloc[train_len:train_len+val_len, :]
    test_csv = final_csv.iloc[train_len+val_len:, :]
    train_csv.to_csv(f"train_{SAMPLE_PERCENTAGE}_{seed}.csv", index=False)
    val_csv.to_csv(f"val_{SAMPLE_PERCENTAGE}_{seed}.csv", index=False)
    test_csv.to_csv(f"test_{SAMPLE_PERCENTAGE}_{seed}.csv", index=False)
    print(f"done, {len(train_csv)} train, {len(val_csv)} val, {len(test_csv)} test")
    # 1248 train, 356 val, 180 test
