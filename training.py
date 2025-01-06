from sentence_transformers import SentenceTransformer, models, InputExample, losses, LoggingHandler
from torch.utils.data import DataLoader
import pickle
from sentence_transformers import evaluation
import logging
from tqdm import tqdm
import logging
import os
import csv
import numpy as np
from typing import List, Union
import math
from tqdm.autonotebook import trange

import torch
from torch import nn
from torch.utils.tensorboard import SummaryWriter

logger = logging.getLogger(__name__)


logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO,
                        handlers=[LoggingHandler()])

word_embedding_model = models.Transformer("vinai/phobert-large", max_seq_length=256)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
print(model)


import pandas as pd
df_train = pd.read_csv("train.csv", index_col=0)

import numpy as np
df_train['label'] = df_train['label'].astype(np.int16)

def check_err(text):
  if len(str(text).split(' ')) < 5:
    return True
  return False
df_train['error'] = df_train['question'].apply(check_err)
df_train = df_train[df_train['error']==False]
df_train['error'] = df_train['answer'].apply(check_err)
df_train = df_train[df_train['error']==False]

from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(
    df_train[['question', 'answer']], df_train['label'],
    test_size=0.2, random_state=42
)

# recheck data
X_train['label'] = y_train
X_val['label'] = y_val
X_train.head()

train_examples = []
sent1 = []
sent2 = []
scores = []

for row in tqdm(X_train.itertuples()):
  # print(row.question)
  # print("------------")
  relevant = float(row.label)
  question = row.question
  answer = row.answer
  example = InputExample(texts=[question, answer], label=relevant)
  train_examples.append(example)

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
# val_dataloader = DataLoader(val_examples, batch_size=16)
train_loss = losses.ContrastiveLoss(model)

evaluator = evaluation.BinaryClassificationEvaluator(X_val['question'].values.tolist(),
                                                     X_val['answer'].values.tolist(),
                                                     X_val['label'].values.tolist())

model.fit(train_objectives=[(train_dataloader, train_loss)],
            epochs=11,
            warmup_steps=1000,
            optimizer_params={'lr': 1e-5},
            save_best_model=True,
            evaluator=evaluator,
            evaluation_steps=500,
            output_path='output3/',
            use_amp=True,
            show_progress_bar=True)