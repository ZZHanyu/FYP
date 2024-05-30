# from utils import model
from main_class import main
from utils import preprocess
from utils import network

import os
import torch
from tqdm import tqdm
import pandas as pd

'''
    A tool-kit used for testing existed trained model
'''


def test_all_model():
    main.initialize()
    preprocess.data_handler.initialize()

    model = network.LstmNet(
        hidden_size = 128,
        hidden_size_linear = 64,
        num_layers = 2,
        dropout = 0,
        dropout_linear = 0,
        activation_linear = 'LeakyReLU'
    ).to(preprocess.data_handler._device)

    model_path = '/Users/taotao/Documents/GitHub/FYP/trained_model/'
    data_generator = preprocess.data_handler.get_generator()


    if os.path.exists(model_path):
        file_list = os.listdir(model_path)
        accuary_list = {}

        for single_model_name in tqdm(file_list, desc=f"Total Testing Progress...", leave=True):
            print(f"\n ------------MODEL{single_model_name}------------\n")
            preprocess.data_handler.reset()

            full_path = model_path + single_model_name
            checkpoint = torch.load(full_path)
            try:
                model.load_state_dict(checkpoint)
            except RuntimeError as e:
                accuary_list[single_model_name] = None
                continue

            accuary = 0
            total_size = 0

            model.eval()   
            for _ in tqdm(range(50), desc="in single model...", leave=False): # 50 * 20 = 1000 test data to calculate the accuary
                single_chunk = next(data_generator)
                total_size += len(single_chunk)
                for data_idx in tqdm(range(len(single_chunk)), desc="Handling single row in a chunk", leave=False):
                    feature = torch.tensor(single_chunk[data_idx][0], dtype=torch.float32, device=main._device, requires_grad=True)
                    target = torch.tensor([single_chunk[data_idx][1]], dtype=torch.float32, device=main._device, requires_grad=True)
                    y_pred = model.forward(feature)
                    

                    if y_pred >= 0.5 and target[0] == 1:
                        accuary += 1
                    elif y_pred <= 0.5 and target[0] == 0:
                        accuary += 1
                    else:
                        continue
            accuary /= total_size
                
            
            accuary_list[single_model_name] = accuary
    
    print(accuary_list)


def test_specific_model():
    main.initialize()
    preprocess.data_handler.initialize()

    model = network.LstmNet(
        hidden_size = 128,
        hidden_size_linear = 64,
        num_layers = 2,
        dropout = 0,
        dropout_linear = 0,
        activation_linear = 'LeakyReLU'
    ).to(preprocess.data_handler._device)
    data_generator = preprocess.data_handler.get_generator()


    full_path = "/Users/taotao/Documents/GitHub/FYP/trained_model/model2024_04_22.pth"
    checkpoint = torch.load(full_path)
    try:
        model.load_state_dict(checkpoint)
    except RuntimeError as e:
        print(f"\n\tError ! \n {e}\n")
    accuary = 0
    total_size = 0
    model.eval()   
    for _ in tqdm(range(50), desc="in single model...", leave=False): # 50 * 20 = 1000 test data to calculate the accuary
        single_chunk_tuple = next(data_generator)
        single_chunk_idx = single_chunk_tuple[0]
        single_chunk = single_chunk_tuple[1]
        total_size += len(single_chunk)
        
        for data_idx in tqdm(range(len(single_chunk)), desc="Handling single row in a chunk", leave=False):
            feature = torch.tensor(single_chunk[data_idx][0], dtype=torch.float32, device=main._device, requires_grad=True)
            target = torch.tensor([single_chunk[data_idx][1]], dtype=torch.float32, device=main._device, requires_grad=True)
            y_pred = model.forward(feature)
            

            if y_pred >= 0.5 and target[0] == 1:
                accuary += 1
            elif y_pred <= 0.5 and target[0] == 0:
                accuary += 1
            else:
                continue
            accuary /= total_size
                
    print(f"\n **** For model = {full_path}, \n accuary = {accuary} !\n")



if __name__ == '__main__':
    
    #test_all_model()
    test_specific_model()

