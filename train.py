import os
import math
import torch
import torch.nn as nn
import traceback

import time
import numpy as np

import argparse

from utils.generic_utils import load_config, save_config_file
from utils.generic_utils import set_init_dict

from utils.generic_utils import NoamLR, binary_acc

from utils.generic_utils import save_best_checkpoint

from utils.tensorboard import TensorboardWriter

from utils.dataset import train_dataloader, eval_dataloader

from models.spiraconv import SpiraConvV1, SpiraConvV2
from utils.audio_processor import AudioProcessor 

def validation(criterion, ap, model, c, testloader, tensorboard, step,  cuda):
    padding_with_max_lenght = c.dataset['padding_with_max_lenght'] or c.dataset['split_wav_using_overlapping']
    model.zero_grad()
    model.eval()
    loss = 0
    loss_control = 0
    loss_patient = 0 
    acc = 0
    preds = []
    targets = []
    with torch.no_grad():
        for feature, target, slices, targets_org in testloader:       
            
            #try:
            if cuda:
                feature = feature.cuda()
                target = target.cuda()
            output = model(feature).float()

            # output = torch.round(output * 10**4) / (10**4)

            
            if c.dataset['split_wav_using_overlapping']:
                # unpack overlapping for calculation loss and accuracy 
                if slices is not None and targets_org is not None:
                    idx = 0
                    new_output = []
                    new_target = []
                    for i in range(slices.size(0)):
                        num_samples = int(slices[i].cpu().numpy())

                        samples_output = output[idx:idx+num_samples]
                        output_mean = samples_output.mean()
                        samples_target = target[idx:idx+num_samples]
                        target_mean = samples_target.mean()

                        new_target.append(target_mean)
                        new_output.append(output_mean)
                        idx += num_samples

                    target = torch.stack(new_target, dim=0)
                    output = torch.stack(new_output, dim=0)
                    #print(target, targets_org)
                    if cuda:
                        output = output.cuda()
                        target = target.cuda()
                        targets_org = targets_org.cuda()
                    if not torch.equal(targets_org, target):
                        raise RuntimeError("Integrity problem during the unpack of the overlay for the calculation of accuracy and loss. Check the dataloader !!")

            loss += criterion(output, target).item()
            idxs = (target == c.dataset['control_class'])
            loss_control += criterion(output[idxs], target[idxs]).item()
            idxs = (target == c.dataset['patient_class'])
            loss_patient += criterion(output[idxs], target[idxs]).item()

            # calculate binnary accuracy
            y_pred_tag = torch.round(output)
            acc += (y_pred_tag == target).float().sum().item()
            targets += target.reshape(-1).int().cpu().numpy().tolist()
            preds += y_pred_tag.reshape(-1).int().cpu().numpy().tolist()
            
    targets = np.array(targets)
    preds = np.array(preds)

    idxs = np.nonzero(targets == c.dataset['control_class'])
    control_target = targets[idxs]
    control_preds = preds[idxs]
    idxs = np.nonzero(targets == c.dataset['patient_class'])
    
    patient_target = targets[idxs]
    patient_preds = preds[idxs]
    
    acc_control = (control_preds == control_target).mean()
    acc_patient = (patient_preds == patient_target).mean()

    acc_balanced = (acc_control + acc_patient) / 2

    loss_control = loss_control / len(control_target)
    loss_patient = loss_patient / len(patient_target)

    loss_balanced = (loss_control + loss_patient) / 2 

    mean_acc = acc / len(testloader.dataset)
    mean_loss = loss / len(testloader.dataset)
    print("Validation:")
    print("Acurracy: ", mean_acc, "Acurracy Control: ", acc_control, "Acurracy Patient: ", acc_patient, "Acurracy Balanced", acc_balanced)
    print("Loss:", mean_loss, "Loss Control:", loss_control, "Loss Patient:", loss_patient, "Loss balanced: ", loss_balanced)
    tensorboard.log_evaluation(mean_loss, mean_acc, step, loss_balanced, acc_balanced)
    model.train()
    return loss_balanced

def train(args, log_dir, checkpoint_path, trainloader, testloader, tensorboard, c, model_name, ap, cuda=True):
    padding_with_max_lenght = c.dataset['padding_with_max_lenght'] or c.dataset['split_wav_using_overlapping']
    if(model_name == 'spiraconv_v1'):
        model = SpiraConvV1(c)
    elif (model_name == 'spiraconv_v2'):
        model = SpiraConvV2(c)
    #elif(model_name == 'voicesplit'):
    else:
        raise Exception(" The model '"+model_name+"' is not suported")

    if c.train_config['optimizer'] == 'adam':
        optimizer = torch.optim.Adam(model.parameters(),
                                     lr=c.train_config['learning_rate'], weight_decay=c.train_config['weight_decay'])
    else:
        raise Exception("The %s  not is a optimizer supported" % c.train['optimizer'])

    step = 0
    if checkpoint_path is not None:
        print("Continue training from checkpoint: %s" % checkpoint_path)
        try:
            if c.train_config['reinit_layers']:
                raise RuntimeError
            checkpoint = torch.load(checkpoint_path, map_location='cpu')
            model.load_state_dict(checkpoint['model'])
            if cuda:
                model = model.cuda()
        except:
            print(" > Partial model initialization.")
            model_dict = model.state_dict()
            model_dict = set_init_dict(model_dict, checkpoint, c)
            model.load_state_dict(model_dict)
            del model_dict
        try:
            optimizer.load_state_dict(checkpoint['optimizer'])
        except:
            print(" > Optimizer state is not loaded from checkpoint path, you see this mybe you change the optimizer")
        
        step = checkpoint['step']
    else:
        print("Starting new training run")
        step = 0


    if c.train_config['lr_decay']:
        scheduler = NoamLR(optimizer,
                           warmup_steps=c.train_config['warmup_steps'],
                           last_epoch=step - 1)
    else:
        scheduler = None
    # convert model from cuda
    if cuda:
        model = model.cuda()

    # define loss function
    criterion = nn.BCELoss()
    eval_criterion = nn.BCELoss(reduction='sum')

    best_loss = float('inf')

    # early stop definitions
    early_epochs = 0

    model.train()
    for epoch in range(c.train_config['epochs']):
        for feature, target in trainloader:
                if cuda:
                    feature = feature.cuda()
                    target = target.cuda()

                output = model(feature)

                # Calculate loss
                # adjust target dim
                if not padding_with_max_lenght:
                    target = target[:, :output.shape[1],:]
                loss = criterion(output, target)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                # update lr decay scheme
                if scheduler:
                    scheduler.step()
                step += 1

                loss = loss.item()
                if loss > 1e8 or math.isnan(loss):
                    print("Loss exploded to %.02f at step %d!" % (loss, step))
                    break

                # write loss to tensorboard
                if step % c.train_config['summary_interval'] == 0:
                    tensorboard.log_training(loss, step)
                    print("Write summary at step %d" % step, ' Loss: ', loss)

                # save checkpoint file  and evaluate and save sample to tensorboard
                if step % c.train_config['checkpoint_interval'] == 0:
                    save_path = os.path.join(log_dir, 'checkpoint_%d.pt' % step)
                    torch.save({
                        'model': model.state_dict(),
                        'optimizer': optimizer.state_dict(),
                        'step': step,
                        'config_str': str(c),
                    }, save_path)
                    print("Saved checkpoint to: %s" % save_path)
                    # run validation and save best checkpoint
                    val_loss = validation(eval_criterion, ap, model, c, testloader, tensorboard, step,  cuda=cuda)
                    best_loss, _ = save_best_checkpoint(log_dir, model, optimizer, c, step, val_loss, best_loss, early_epochs if c.train_config['early_stop_epochs'] != 0 else None)
        
        print('=================================================')
        print("Epoch %d End !"%epoch)
        print('=================================================')
        # run validation and save best checkpoint at end epoch
        val_loss = validation(eval_criterion, ap, model, c, testloader, tensorboard, step,  cuda=cuda)
        best_loss, early_epochs = save_best_checkpoint(log_dir, model, optimizer, c, step, val_loss, best_loss,  early_epochs if c.train_config['early_stop_epochs'] != 0 else None)
        if c.train_config['early_stop_epochs'] != 0:
            if early_epochs is not None:
                if early_epochs >= c.train_config['early_stop_epochs']:
                    break # stop train
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_path', type=str, required=True,
                        help="json file with configurations")
    parser.add_argument('--checkpoint_path', type=str, default=None,
                        help="path of checkpoint pt file, for continue training")
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help="Seed for training")
    args = parser.parse_args()

    c = load_config(args.config_path)
    ap = AudioProcessor(**c.audio)
    if args.seed is None:
        log_path = os.path.join(c.train_config['logs_path'], c.model_name)
    else:
        log_path = os.path.join(os.path.join(c.train_config['logs_path'], str(args.seed)), c.model_name)
        c.train_config['seed'] = args.seed

    os.makedirs(log_path, exist_ok=True)

    tensorboard = TensorboardWriter(os.path.join(log_path,'tensorboard'))

    trainloader = train_dataloader(c, ap, class_balancer_batch=c.dataset['class_balancer_batch'])
    max_seq_len = trainloader.dataset.get_max_seq_lenght()
    c.dataset['max_seq_len'] = max_seq_len

    # save config in train dir, its necessary for test before train and reproducity
    save_config_file(c, os.path.join(log_path,'config.json'))

    evaloader = eval_dataloader(c, ap, max_seq_len=max_seq_len)

    train(args, log_path, args.checkpoint_path, trainloader, evaloader, tensorboard, c, c.model_name, ap, cuda=True)