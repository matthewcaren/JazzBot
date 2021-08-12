from __future__ import print_function
import tensorflow as tf
import numpy as np
import random
import sys
import codecs
import os
import json

nepochs = 20
batchsize = 128

f = open('./miditext/original/original-song.txt', 'r')
music_as_chunks = []
chunk_chords = [] # currently this is populated with harmony that corresponds to music_as_chunks, but is not used

for elem in f:
    music_as_chunks.append(elem.rstrip("\n"))
f.close()

for i in range(len(music_as_chunks)):
    elem_parts = music_as_chunks[i].split("-")
    music_as_chunks[i] = elem_parts[0]
    chunk_chords = elem_parts[1]


music_as_chunks = music_as_chunks[1:]

unique_chunks = sorted(list(set(music_as_chunks)))
chunk_indices = dict((c, i) for i, c in enumerate(unique_chunks))
indices_chunk = dict((i, c) for i, c in enumerate(unique_chunks))

maxlen = 15
step = 1
part_of_songs = []
next_chunks = []
start_ix = 0

for i in range(start_ix, len(music_as_chunks) - maxlen, step):
    part_of_songs.append(music_as_chunks[i: i + maxlen])
    next_chunks.append(music_as_chunks[i + maxlen])

X = np.zeros((len(part_of_songs), maxlen, len(unique_chunks)), dtype=np.bool)
y = np.zeros((len(part_of_songs), len(unique_chunks)), dtype=np.bool)

for i, part_of_song in enumerate(part_of_songs):
    for t, chunk in enumerate(part_of_song):
        X[i, t, chunk_indices[chunk]] = 1
        y[i, chunk_indices[next_chunks[i]]] = 1

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.LSTM(256, input_shape=(maxlen, len(unique_chunks))))
model.add(tf.keras.layers.Dense(len(unique_chunks)))
model.add(tf.keras.layers.Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.01))

model.fit(X, y, batch_size=batchsize, epochs=nepochs)

if not os.path.exists("./model/"):
    os.mkdir("./model/")
model.save('./model/model.h5');
model.save_weights("./model/weights.h5")
