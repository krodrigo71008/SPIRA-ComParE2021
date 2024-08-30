# Speech
echo "==================== Experiments with 5 Folds Eval - Train ===================="

# CUDA_VISIBLE_DEVICES=1 python test_eval_K-Fold_CV_models.py --experiment_dir logs/Experiments_Final_kfolds/Experiment-1/ > logs/Experiments_Final_kfolds/Experiment-1/cv_dev_Train_results.txt

# CUDA_VISIBLE_DEVICES=1 python test_eval_K-Fold_CV_models.py --experiment_dir logs/Experiments_Final_kfolds/Experiment-2/ > logs/Experiments_Final_kfolds/Experiment-2/cv_dev_Train_results.txt

# CUDA_VISIBLE_DEVICES=1 python test_eval_K-Fold_CV_models.py --experiment_dir logs/Experiments_Final_kfolds/Experiment-3/ > logs/Experiments_Final_kfolds/Experiment-3/cv_dev_Train_results.txt

# CUDA_VISIBLE_DEVICES=0 python test_eval_K-Fold_CV_models.py --experiment_dir logs/Experiments_Final_kfolds/Experiment-4/ > logs/Experiments_Final_kfolds/Experiment-4/cv_dev_Train_results.txt

# Cough

CUDA_VISIBLE_DEVICES=1 python test_eval_K-Fold_CV_models.py --experiment_dir logs/Tosse/Experiments_Final_kfolds/Experiment-1/ > logs/Tosse/Experiments_Final_kfolds/Experiment-1/cv_dev_Train_results.txt
CUDA_VISIBLE_DEVICES=1 python test_eval_K-Fold_CV_models.py --experiment_dir logs/Tosse/Experiments_Final_kfolds/Experiment-2/ > logs/Tosse/Experiments_Final_kfolds/Experiment-2/cv_dev_Train_results.txt
CUDA_VISIBLE_DEVICES=1 python test_eval_K-Fold_CV_models.py --experiment_dir logs/Tosse/Experiments_Final_kfolds/Experiment-3/ > logs/Tosse/Experiments_Final_kfolds/Experiment-3/cv_dev_Train_results.txt
CUDA_VISIBLE_DEVICES=1 python test_eval_K-Fold_CV_models.py --experiment_dir logs/Tosse/Experiments_Final_kfolds/Experiment-4/ > logs/Tosse/Experiments_Final_kfolds/Experiment-4/cv_dev_Train_results.txt
