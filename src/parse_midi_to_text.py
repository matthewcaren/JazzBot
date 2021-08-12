import os
import midi
import numpy as np

pattern = midi.read_midifile("./midi/original/original_song.mid")
chunk_str_list = {}


elapsed_time = 0

for i, chunk in enumerate(pattern[1]):
    elapsed_time += chunk.tick
    chunk_str = ""

    if (chunk.name == "Note On" and chunk.velocity != 0):
        chunk_str = chunk_str + str(chunk.tick) + "_" + "no" + "_" + str(chunk.pitch) + "_" + str(chunk.velocity)
        chunk_str_list[elapsed_time] = chunk_str

    if (chunk.name == "Note On" and chunk.velocity == 0 or chunk.name == "Note Off"):
        chunk_str = chunk_str + str(chunk.tick) + "_" + "nf" + "_" + str(chunk.pitch) + "_" + str(chunk.velocity)
        chunk_str_list[elapsed_time] = chunk_str

    elif (chunk.name == "Set Tempo"):
        chunk_str = chunk_str + str(chunk.tick) + "_" + "st" + "_" + str(int(chunk.bpm)) + "_" + str(int(chunk.mpqn))
        chunk_str_list[elapsed_time] = chunk_str

    elif (chunk.name == "Control Change"):
        chunk_str = chunk_str + str(chunk.tick) + "_" + "cc" + "_" + str(chunk.channel)  + "_" + str(chunk.data[0]) + "_" + str(chunk.data[1])
        chunk_str_list[elapsed_time] = chunk_str



elapsed_time = 0
current_notes = np.zeros(12, dtype=int)

for i, chunk in enumerate(pattern[2]):
    elapsed_time += chunk.tick
    chunk_str = ""

    if (chunk.name == "Note On" and chunk.velocity != 0):
        current_notes[chunk.pitch % 12] = 1
        chunk_str +=  "*-" + str(current_notes)
        chunk_str_list[elapsed_time] = chunk_str

    if (chunk.name == "Note On" and chunk.velocity == 0 or chunk.name == "Note Off"):
        current_notes[chunk.pitch % 12] = 0

sorted_chunks = dict(sorted(chunk_str_list.items()))


current_chord = ""
for chunk in sorted_chunks:
    if "*" in sorted_chunks[chunk]:
        current_chord = sorted_chunks[chunk]
    else:
        sorted_chunks[chunk] += str(current_chord).split("*")[1]

final_output = {key:val for key, val in sorted_chunks.items() if "*" not in val}

if not os.path.exists("./miditext/"):
    os.mkdir("./miditext/")
    os.mkdir("./miditext/original/")
elif not os.path.exists("./miditext/original/"):
    os.mkdir("./miditext/original/")

f = open('./miditext/original/original-song.txt', 'w')
f.write("rs_" + str(pattern.resolution) + "\n")
for elm in final_output:
    f.write(str(final_output[elm]) + "\n")
f.close()
