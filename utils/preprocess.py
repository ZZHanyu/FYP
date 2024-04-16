from transformers import PreTrainedTokenizerFast
import pandas
from tqdm import tqdm
import time 
# import re # wanan to remove other special charactors, ex: [] % ^ @ / ...
# import json
import numpy as np
from datetime import datetime
import os
import logging

# utils
from utils import network


class charactors_hander():
    def __init__(self, chunks: pandas.io.parsers.readers.TextFileReader, main_args) -> None:
        # super().__init__(main_args)
        self._meta_data = chunks
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained('bert-base-uncased')
        # self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        self._json_result = {}
        self.args = main_args
        self._LSTM_NetWork = network.trainer(main_args=main_args)


    def _split_single_word(self) -> list:
        return self._raw_str.split()
    
    def display_elements(self):
        return self._raw_str
    
    def _remove_empty_line(self, single_chunk):
        for index, row in single_chunk.iterrows():
            if pandas.isnull(row['title']) or pandas.isnull(row['text']) or pandas.isnull(row['label']):
                single_chunk.drop(index, inplace=True)
            elif type(row['title']) != str or type(row['text']) != str or type(row['label']) != int:
                single_chunk.drop(index, inplace=True)
            elif len(row['title']) < 5 or len(row['text']) < 5:
                single_chunk.drop(index, inplace=True)
        return single_chunk

    def _normalize(self, text):
        norm2 = np.linalg.norm(text)
        for j in len(text):
            text[j] = text[j] / norm2
        return text
    
    def _dataset_divder(self):
        pass

    # def _save_to_file(self, count_num):
    #     with open(self.args.result_path + "tokenized{}.npy".format(str(count_num)), 'a+') as json_file:
    #         json.dump(self._json_result, json_file, sort_keys=True, indent=4)

    def _file_exist_checker(self, chunk_idx) -> bool:
        if not os.path.exists(self.args.result_path + "tokenized{}.npy".format(chunk_idx)):
            return False
        else:
            return True


    def run(self):
        for index, chunk in enumerate(tqdm(self._meta_data, desc="Layer1: Data Preprocess", leave=True)):
            # Check wether specifc file number exist:
            # if self._file_exist_checker(index):
            #     print(f"File tokenized{index} already existed!\n")
            #     continue

            # STEP 1: Remove empty line
            chunk = self._remove_empty_line(single_chunk=chunk)
            chunk_tokenized = [] # initiaize and re-initiaze
            for single_index, row in tqdm(chunk.iterrows(), leave=True, desc="Processing in a single chunk..."):
                # Concating the news title and main body            
                text_merge = row['title'] + row['text']
                
                # STEP 2: Lower all charactors in string
                text_merge = text_merge.lower()
                
                # STEP 3: Split string into charactor list
                text_merge = text_merge.split()
                # print(f"\nHOW many words inside a sequence = {len(text_merge)}\n")

                encoder_text = self.tokenizer(text=text_merge, max_length=8, padding='max_length', truncation=True, return_tensors='pt')
                # print(f"\n The encodered text is = {encoder_text['input_ids']}\n length = {encoder_text['input_ids'].size()} \n")
                # temp = np.pad(encoder_text['input_ids'], ((0,0), (0, 512 - encoder_text['input_ids'].shape[1])), mode='constant')
                # chunk_tokenized.append((np.pad(encoder_text['input_ids'], ((0,0), (0, 512 - encoder_text['input_ids'].shape[1])), mode='constant'), [row['label']]))
                chunk_tokenized.append( (encoder_text['input_ids'], row['label']) )
                # print(f"size after = {temp.shape}")
            
            self._LSTM_NetWork.start(chunk_tokenized, index)
                

