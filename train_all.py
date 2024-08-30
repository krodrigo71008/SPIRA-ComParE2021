import os

if __name__ == "__main__":
    commands = [
        "python train.py -c Configs/Experiments_Final_kfold/configs/Speech/exp1.json -s 42",
        "python train.py -c Configs/Experiments_Final_kfold/configs/Speech/exp2.json -s 42",
        "python train.py -c Configs/Experiments_Final_kfold/configs/Speech/exp3.json -s 42",
        "python train.py -c Configs/Experiments_Final_kfold/configs/Speech/exp4.json -s 42",
        "python train.py -c Configs/Experiments_Final_kfold/configs/Tosse/exp1.json -s 42",
        "python train.py -c Configs/Experiments_Final_kfold/configs/Tosse/exp2.json -s 42",
        "python train.py -c Configs/Experiments_Final_kfold/configs/Tosse/exp3.json -s 42",
        "python train.py -c Configs/Experiments_Final_kfold/configs/Tosse/exp4.json -s 42",
        "python train.py -c Configs/Experiments_Final_holdout/configs/Speech/exp1.json -s 42",
        "python train.py -c Configs/Experiments_Final_holdout/configs/Speech/exp2.json -s 42",
        "python train.py -c Configs/Experiments_Final_holdout/configs/Speech/exp3.json -s 42",
        "python train.py -c Configs/Experiments_Final_holdout/configs/Speech/exp4.json -s 42",
        "python train.py -c Configs/Experiments_Final_holdout/configs/Tosse/exp1.json -s 42",
        "python train.py -c Configs/Experiments_Final_holdout/configs/Tosse/exp2.json -s 42",
        "python train.py -c Configs/Experiments_Final_holdout/configs/Tosse/exp3.json -s 42",
        "python train.py -c Configs/Experiments_Final_holdout/configs/Tosse/exp4.json -s 42",
        "python train.py -c Configs/Experiments_Final_windowed_Holdout/configs/Speech/exp1.json -s 42",
        "python train.py -c Configs/Experiments_Final_windowed_Holdout/configs/Speech/exp2.json -s 42",
        "python train.py -c Configs/Experiments_Final_windowed_Holdout/configs/Speech/exp3.json -s 42",
        "python train.py -c Configs/Experiments_Final_windowed_Holdout/configs/Speech/exp4.json -s 42",
        "python train.py -c Configs/Experiments_Final_windowed_Holdout/configs/Tosse/exp1.json -s 42",
        "python train.py -c Configs/Experiments_Final_windowed_Holdout/configs/Tosse/exp2.json -s 42",
        "python train.py -c Configs/Experiments_Final_windowed_Holdout/configs/Tosse/exp3.json -s 42",
        "python train.py -c Configs/Experiments_Final_windowed_Holdout/configs/Tosse/exp4.json -s 42",
    ]

    for command in commands:
        os.system(command)