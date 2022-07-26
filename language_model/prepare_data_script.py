# Based on code from:
# https://towardsdatascience.com/training-neural-networks-to-create-text-like-a-human-23bfdc23c28
# https://www.thepythoncode.com/article/text-generation-keras-python

import tensorflow.keras.utils as ku
import tensorflow as tf
import numpy as np
import re

import random
import regex
import os

from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras import regularizers

import pandas as pd

FILE_PATH = "cleaned_dataset.txt"
BASENAME = os.path.basename(FILE_PATH)

data = []
with open(FILE_PATH,
          encoding='utf-8') as f:
    for l in f:
        data.append(l)
        print("This is line", l)


def preprocess(text):
    # text_input = re.sub('[^a-zA-Z1-9]+', ' ', str(text))

    # custom function because we need spanish accented chars
    text_input = regex.sub('[^\p{Latin}]+', ' ', str(text))

    output = re.sub(r'\d+', '', text_input)
    return output.lower().strip()


corpus_cleaned = []
for line in data:
    clean_line = preprocess(line)
    corpus_cleaned.append(clean_line)

print(corpus_cleaned)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(corpus_cleaned)

input_sequences = []

for line in corpus_cleaned:
    token_list = tokenizer.texts_to_sequences([line])[0]
    print()
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i + 1]
        input_sequences.append(n_gram_sequence)

# pad sequences
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(
    pad_sequences(
        input_sequences,
        maxlen=max_sequence_len,
        padding='pre'
    ))

# create predictors and label
total_words = len(tokenizer.word_index) + 1
predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
label = ku.to_categorical(label, num_classes=total_words)

model = Sequential()
model.add(Embedding(total_words, 240, input_length=max_sequence_len - 1))
model.add(Bidirectional(LSTM(150, return_sequences=True)))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dense(total_words / 2, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
model.add(Dense(total_words, activation='softmax'))

model_weights_path = f"results/{BASENAME}-{max_sequence_len}.h5"

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)


class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('accuracy') > 0.93:
            print("\nReached 93% accuracy so cancelling training!")
            self.model.stop_training = True


callbacks = myCallback()

if not os.path.isdir("results"):
    os.mkdir("results")

model.fit(predictors, label, epochs=300, verbose=1, callbacks=[callbacks])

# saving model after training
model.save(model_weights_path)

next_words = 10

# TODO: create a custom function to pick two words as starting text seed for the text generation.
# random_item = random.choice(data)
# print(random_item)
#
# seed_text = ""


# TODO: use this to create a function that takes the random seed texts and then produces
#  the generated text using the language model
# for _ in range(next_words):
#     token_list = tokenizer.texts_to_sequences([seed_text])[0]
#     token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
#     predicted = model.predict_classes(token_list, verbose=0)
#     output_word = ""
#     for word, index in tokenizer.word_index.items():
#         if index == predicted:
#             output_word = word
#             break
#     seed_text += " " + output_word

# seed_text = (seed_text + ".").capitalize()
# print(seed_text)
