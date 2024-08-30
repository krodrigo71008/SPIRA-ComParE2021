echo "==================== Experiments with 5 seeds ===================="

echo "==================== Experiment 1 ===================="
echo "____________________EVALUATION____________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/devel.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-1/
echo "--------------------------------------------------"
echo "______________________TRAIN_______________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/train.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-1/
echo "--------------------------------------------------"
echo "========================================================="

echo "==================== Experiment 2 ===================="
echo "____________________EVALUATION____________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/devel.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-2/
echo "--------------------------------------------------"
echo "______________________TRAIN_______________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/train.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-2/
echo "--------------------------------------------------"
echo "========================================================="

echo "==================== Experiment 3 ===================="
echo "____________________EVALUATION____________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/devel.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-3/
echo "--------------------------------------------------"
echo "______________________TRAIN_______________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/train.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-3/
echo "--------------------------------------------------"
echo "========================================================="

echo "==================== Experiment 4 ===================="
echo "____________________EVALUATION____________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/devel.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-4/
echo "--------------------------------------------------"
echo "______________________TRAIN_______________________"
python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/train.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-4/
echo "--------------------------------------------------"
echo "========================================================="



# exemplo para o test
# CUDA_VISIBLE_DEVICES=1 python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/test.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-4/ --debug 0
# CUDA_VISIBLE_DEVICES=1 python test_all_seeds_or_folds.py  --test_csv ../data/compare/ComParE2021_CSS/lab/test.csv -r ../data/compare/ComParE2021_CSS/wav --experiment_dir logs/Experiments_Final/Experiment-4/ --debug 0