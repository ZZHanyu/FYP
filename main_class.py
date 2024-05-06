import argparse
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

# utils
# from utils import preprocess
# # from utils import custom_dataloader
# from utils import network
# from utils import topicModel


# other modules
import opendatasets as od
import os
from datetime import datetime, timedelta
import logging

'''
    Super main class
    Abstract super class : To avoid repeat defination
'''
class main(object):
    def __init__(self) -> None:
        self.args = self.__parser()
        logging.basicConfig(filename=self.args.logging_path + f'{self.args.date_time}', level=logging.INFO)
        self.device = self.__select_device()


    def __parser(self):
        parser = argparse.ArgumentParser(description="Parameters for Classifier")
        parser.add_argument("--dataset_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/data/", help="the path of your dataset")
        parser.add_argument("--dataset_name", type=str, default='fake-news-classification', help="the dataset name from kaggle")
        parser.add_argument("--chunk_size", type=int, default=20, help="control how many lines read once / single batch size")
        parser.add_argument("--max_epochs", type=int, default=50, help="epochs of training")
        parser.add_argument("--test_batch", type=int, default=5, help="how many batch dataset used for testing")
        parser.add_argument("--train_persentage", type=float, default=0.8, help="dataset persentage used for training")
        parser.add_argument("--result_path", type=str, default="result/", help="result output destnation file")
        parser.add_argument("--date_time", type=str, default=datetime.now().strftime("%Y_%m_%d_%H:%M"), help="date_form_Y_M_D_h_m")
        parser.add_argument("--logging_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/log/", help="log file recorded path")
        parser.add_argument("--pretrianed_emb_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/pretrain_embedding/", help="path store pretrianed embeddings model")
        parser.add_argument("--pretrained_embedding_model_name", type=str, default="fasttext-wiki-news-subwords-300", help="pretrained embedding model name from gensim")
        parser.add_argument("--model_save_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/trained_model/", help="trained model saving path")
        parser.add_argument("--batch_model", type=bool, default=True, help="whether using batch during train step")
        parser.add_argument("--LDA_only", type=bool, default=False, help="whether start from train")
        parser.add_argument("--LDA_model_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/LDA_Model/", help="LDA model path")
        parser.add_argument("--num_epoches", type=int, default=10, help="epoch means train thourgh a whole dataset")
        args = parser.parse_args()
        return args
    
    def __select_device(self):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            if torch.backends.mps.is_built():
                device = torch.device("mps")
        else:
            device = torch.device("cpu")
        logging.info(f"\n *** Devices selected = {device} ! \n")
        return device


        


# class main(super_main):
#     def __init__(self) -> None:
#         super().__init__()
#         self._chunks = None
#         self._total_length = 0
#         self._chunk_number = 0
#         self._topic_model = None
#         self.device = None
#         self.data_handler = None
#         #           preprocess.charactors_hander(chunks=self._chunks,
#         #                                         main_args=self.args,
#         #                                         total_len=self._total_length,
#         #                                         device=self.device)
        

#     def datarow_count(self):
#         with open(self.args.dataset_path + self.args.dataset_name + '/WELFake_Dataset.csv') as fileobject:
#             self._total_length = sum(1 for row in fileobject)
#         logging.info(f"\n ** DataFile have {self._total_length} rows of data! \n")
#         # calculate the total chunk number
#         self._chunk_number = self._total_length // self.args.chunk_size # this is estimate, because later iterator will delete some row in every chunk


#     def _select_device(self):
#         # check avaliable devices
#         if torch.cuda.is_available():
#             self.device = torch.device("cuda")
#         elif torch.backends.mps.is_available():
#             if torch.backends.mps.is_built():
#                 self.device = torch.device("mps")
#         else:
#             self.device = torch.device("cpu")
#         logging.info(f"\n *** Devices selected = {self.device} ! \n")
        

#     def _dataloader(self):
#         '''
#             ---------- Part 1: Dataset Loader ----------
#             Objective:
#                 - using batchs(chunks) to load csv line by line
#             Params:
#                 - args: chunk size defined
#             Return:
#                 - wda
#         '''
#         if not os.path.exists(self.args.dataset_path + self.args.dataset_name + '/WELFake_Dataset.csv'):
#             print(f"The file path {self.args.dataset_path + 'WELFake_Dataset.csv'} is missing! Now downloading...\n")
#             # kaggle datasets download -d saurabhshahane/fake-news-classification
#             od.download('https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification', data_dir=self.args.dataset_path)
            
#         try:
#             self._chunks = pd.read_csv(self.args.dataset_path + self.args.dataset_name + '/' +'WELFake_Dataset.csv', chunksize=self.args.chunk_size)
#         except Exception as e:
#             print(f"Data Loading Failed! {e}")
    

#     def _data_preprocess(self):
#         '''
#             ---------- Part 2: Text Preprocess ----------
#             Objective:
#                 - clean the symbols(,.%) and space 
#                 - lowercase the letters
#             Params:

#         '''
#         self._data_preprocess_model()
#         try:
#             self.datarow_count()
#         except Exception as e:
#             logging.info(f"\n ERROR! CSV count Failed! {e} \n")

#         self.data_handler.run()


#     def forward(self):
#         self._select_device()
#         if self.args.LDA_only == False:
#             try:
#                 self._dataloader()
#                 self._data_preprocess()
#             except Exception as e:
#                 logging.info(f"\n \t An ERROR Happend! \n Now saving model...\n")

#             # lstmNet = network.trainer(main_args=args)
#             # lstmNet.start()
#         elif self.args.LDA_only == True:
#             # try:
#             print("ok")
#             topic_model = topicModel.LDA_topic_model(self.args,
#                                                      self.device,
#                                                      self.data_handler.get_classifier_model())
#             result = topic_model.forward()
#             # except Exception as e:
#                 # logging.info(f"ERROR in topic modeling! errInfo: {e} \n")
        
#         logging.info("\n Programing Finished!\n")
        

    
            
#     # def print_arguments(self):
        






# # Start from here
# parser = argparse.ArgumentParser(description="Parameters for Classifier")
# parser.add_argument("--dataset_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/data/", help="the path of your dataset")
# parser.add_argument("--dataset_name", type=str, default='fake-news-classification', help="the dataset name from kaggle")
# parser.add_argument("--chunk_size", type=int, default=20, help="control how many lines read once / single batch size")
# parser.add_argument("--max_epochs", type=int, default=50, help="epochs of training")
# parser.add_argument("--test_batch", type=int, default=5, help="how many batch dataset used for testing")
# parser.add_argument("--train_persentage", type=float, default=0.8, help="dataset persentage used for training")
# parser.add_argument("--result_path", type=str, default="result/", help="result output destnation file")
# parser.add_argument("--date_time", type=str, default=datetime.now().strftime("%Y_%m_%d_%H:%M"), help="date_form_Y_M_D_h_m")
# parser.add_argument("--logging_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/log/", help="log file recorded path")
# parser.add_argument("--pretrianed_emb_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/pretrain_embedding/", help="path store pretrianed embeddings model")
# parser.add_argument("--pretrained_embedding_model_name", type=str, default="fasttext-wiki-news-subwords-300", help="pretrained embedding model name from gensim")
# parser.add_argument("--model_save_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/trained_model/", help="trained model saving path")
# parser.add_argument("--batch_model", type=bool, default=True, help="whether using batch during train step")
# parser.add_argument("--LDA_only", type=bool, default=False, help="whether start from train")
# parser.add_argument("--LDA_model_path", type=str, default="/Users/taotao/Documents/GitHub/FYP/LDA_Model/", help="LDA model path")
# parser.add_argument("--num_epoches", type=int, default=10, help="epoch means train thourgh a whole dataset")
# args = parser.parse_args()

# main_progress = main(args)
# logging.basicConfig(filename=args.logging_path + f'{args.date_time}', level=logging.INFO)
# logging.info(f"\n ======== Start Log Recording :{args.date_time} ========\n")
# main_progress.forward()
# logging.info(f"\n======== End of log Recording ========\n")