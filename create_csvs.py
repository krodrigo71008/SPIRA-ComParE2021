import glob
import random
import pandas as pd
from pathlib import Path
import os

if __name__ == "__main__":
    audio_csv = pd.read_csv("audio_metadata.csv")
    participant_csv = pd.read_csv("participant_metadata.csv")
    full_csv = audio_csv.merge(
        participant_csv[["participant_identifier", "covid_test_result"]], 
        on="participant_identifier")
    full_csv = full_csv[full_csv["covid_test_result"].notna()]
    full_csv = full_csv[full_csv["exhalation_file_name"].notna()]
    full_csv = full_csv[full_csv["cough_file_name"].notna()]
    full_csv = full_csv[full_csv["three_cough_file_name"].notna()]
    root_path = "../data/audio"
    error = 0
    lines = []
    for i, v in full_csv[["exhalation_file_name", "cough_file_name", "three_cough_file_name"]].iterrows():
        if (not os.path.exists(os.path.join(root_path, v.iloc[0])) or 
            not os.path.exists(os.path.join(root_path, v.iloc[1])) or 
            not os.path.exists(os.path.join(root_path, v.iloc[2]))):
            error += 1
        else:
            lines.append(i)
    print(f"{error} files not found!")
    full_csv = full_csv.loc[lines, :]
    seed = 727
    SAMPLE_PERCENTAGE = 0.1
    TRAIN_PERCENTAGE = 0.7
    VAL_PERCENTAGE = 0.2
    TEST_PERCENTAGE = 1 - TRAIN_PERCENTAGE - VAL_PERCENTAGE
    random.seed(seed)
    final_csv = full_csv.sample(int(len(full_csv)*SAMPLE_PERCENTAGE), random_state=seed)
    train_len = int(len(final_csv)*TRAIN_PERCENTAGE)
    val_len = int(len(final_csv)*VAL_PERCENTAGE)
    train_csv = final_csv.iloc[:train_len, :]
    val_csv = final_csv.iloc[train_len:train_len+val_len, :]
    test_csv = final_csv.iloc[train_len+val_len:, :]
    train_csv.to_csv(f"train_{SAMPLE_PERCENTAGE}_{seed}.csv")
    val_csv.to_csv(f"val_{SAMPLE_PERCENTAGE}_{seed}.csv")
    test_csv.to_csv(f"test_{SAMPLE_PERCENTAGE}_{seed}.csv")
    print(f"done")
