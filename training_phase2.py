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


class LossEvaluator(evaluation.BinaryClassificationEvaluator):

    def __init__(self, loader, loss_model: nn.Module = None, name: str = '', log_dir: str = None,
                 show_progress_bar: bool = False, write_csv: bool = True):

        """
        Evaluate a model based on the loss function.
        The returned score is loss value.
        The results are written in a CSV and Tensorboard logs.
        :param loader: Data loader object
        :param loss_model: loss module object
        :param name: Name for the output
        :param log_dir: path for tensorboard logs 
        :param show_progress_bar: If true, prints a progress bar
        :param write_csv: Write results to a CSV file
        """

        self.loader = loader
        self.write_csv = write_csv
        self.logs_writer = SummaryWriter(log_dir=log_dir)
        self.name = name
        self.loss_model = loss_model

        # move model to gpu:  lidija-jovanovska
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        loss_model.to(self.device)

        if show_progress_bar is None:
            show_progress_bar = (
                    logger.getEffectiveLevel() == logging.INFO or logger.getEffectiveLevel() == logging.DEBUG)
        self.show_progress_bar = show_progress_bar

        self.csv_file = "loss_evaluation" + ("_" + name if name else '') + "_results.csv"
        self.csv_headers = ["epoch", "steps", "loss"]

    def __call__(self, model, output_path: str = None, epoch: int = -1, steps: int = -1) -> float:

        self.loss_model.eval()

        loss_value = 0
        self.loader.collate_fn = model.smart_batching_collate
        num_batches = len(self.loader)
        data_iterator = iter(self.loader)

        with torch.no_grad():
            for _ in trange(num_batches, desc="Iteration", smoothing=0.05, disable=not self.show_progress_bar):
                sentence_features, labels = next(data_iterator)
                #move data to GPU: lidija-jovanovska
                sentence_features = list(map(lambda batch: batch_to_device(batch, self.device), sentence_features))
                labels = labels.to(self.device)
                loss_value += self.loss_model(sentence_features, labels).item()

        final_loss = loss_value / num_batches
        if output_path is not None and self.write_csv:

            csv_path = os.path.join(output_path, self.csv_file)
            output_file_exists = os.path.isfile(csv_path)

            with open(csv_path, newline='', mode="a" if output_file_exists else 'w', encoding="utf-8") as f:
                writer = csv.writer(f)
                if not output_file_exists:
                    writer.writerow(self.csv_headers)

                writer.writerow([epoch, steps, final_loss])

            # ...log the running loss
            self.logs_writer.add_scalar('val_loss',
                                        final_loss,
                                        steps)

        self.loss_model.zero_grad()
        self.loss_model.train()

        return final_loss

logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO,
                        handlers=[LoggingHandler()])

# word_embedding_model = models.Transformer("vinai/phobert-large", max_seq_length=256)
# pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
model = SentenceTransformer("output2/")
print(model)


import pandas as pd
df_train = pd.read_csv("train_data_phase2.csv", index_col=0)

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
            epochs=3,
            warmup_steps=1000,
            optimizer_params={'lr': 1e-5},
            save_best_model=True,
            evaluator=evaluator,
            evaluation_steps=500,
            output_path='output2_phase2/',
            use_amp=True,
            show_progress_bar=True)