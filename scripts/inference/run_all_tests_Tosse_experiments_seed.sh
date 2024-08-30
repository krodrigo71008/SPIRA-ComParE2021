echo "==================== Experiments with 5 seeds ===================="

echo "==================== Experiment 1 ===================="
echo "____________________EVALUATION____________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CCS/lab/devel.csv -r ../data/compare/ComParE2021_CCS/wav --experiment_dir logs/Tosse/Experiments_Final/Experiment-1/
echo "--------------------------------------------------"
echo "______________________TRAIN_______________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CCS/lab/train.csv -r ../data/compare/ComParE2021_CCS/wav --experiment_dir logs/Tosse/Experiments_Final/Experiment-1/
echo "--------------------------------------------------"
echo "========================================================="

echo "==================== Experiment 2 ===================="
echo "____________________EVALUATION____________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CCS/lab/devel.csv -r ../data/compare/ComParE2021_CCS/wav --experiment_dir logs/Tosse/Experiments_Final/Experiment-2/
echo "--------------------------------------------------"
echo "______________________TRAIN_______________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CCS/lab/train.csv -r ../data/compare/ComParE2021_CCS/wav --experiment_dir logs/Tosse/Experiments_Final/Experiment-2/
echo "--------------------------------------------------"
echo "========================================================="

echo "==================== Experiment 3 ===================="
echo "____________________EVALUATION____________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CCS/lab/devel.csv -r ../data/compare/ComParE2021_CCS/wav --experiment_dir logs/Tosse/Experiments_Final/Experiment-3/
echo "--------------------------------------------------"
echo "______________________TRAIN_______________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CCS/lab/train.csv -r ../data/compare/ComParE2021_CCS/wav --experiment_dir logs/Tosse/Experiments_Final/Experiment-3/
echo "--------------------------------------------------"
echo "========================================================="

echo "==================== Experiment 4 ===================="
echo "____________________EVALUATION____________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CCS/lab/devel.csv -r ../data/compare/ComParE2021_CCS/wav --experiment_dir logs/Tosse/Experiments_Final/Experiment-4/
echo "--------------------------------------------------"
echo "______________________TRAIN_______________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CCS/lab/train.csv -r ../data/compare/ComParE2021_CCS/wav --experiment_dir logs/Tosse/Experiments_Final/Experiment-4/
echo "--------------------------------------------------"
echo "========================================================="