from music21 import *
import matplotlib.pyplot as plt 
from collections import Counter
import pandas as pd 
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

def getTension(chord):
    cName=chord.commonName.lower() if chord.commonName is not "note" or None else ""
    if "major triad" in cName or "minor triad" in cName:
        return 1
    elif "dominant seventh" in cName:
        return 2
    elif "diminished" in cName or "augmented" in cName:
        return 3
    else:
        0

def dtwAnalysis(intervals):

    window_length = 20  # adjust as needed
    dtw_distances = []

# Slide a window over the intervals and compute DTW between the two halves
    for start in range(0, len(intervals) - window_length + 1, window_length):
        window = intervals[start:start + window_length]
        half = window_length // 2
        motif1 = window[:half]
        motif2 = window[half:]
    
    # Compute DTW using a simple absolute difference for scalars
        distance, path = fastdtw(motif1, motif2, dist=lambda x, y: abs(x - y))
        dtw_distances.append(distance)

    print("Computed DTW distances for motif pairs:", dtw_distances)

def durProgression(offset,durations):
    plt.figure(figsize=(10,6))
    plt.plot(offset,durations,marker='o')
    plt.show()

def durFreq(durations):
    ##cnt=Counter(durations)
    plt.figure(figsize=(10,6))
    plt.hist(durations)
    plt.show()

def chordFreq(chord_names):
    cntChord=Counter(chord_names)
    plt.figure(figsize=(10,6))
    #print(chord_names)
    plt.plot(cntChord.keys(),cntChord.values(),marker='o')
    plt.show()

def ioisGraph(iois):
    plt.figure(figsize=(10,6))
    plt.hist(iois, bins=20, color='blue')
    plt.xlabel('Inter-Onset Interval')
    plt.ylabel('Frequency')
    plt.title('Rhytmic Pattern-Inter Onset Intervals')
    plt.show()

def melodicProgression(offset,pitches):
    plt.figure(figsize=(10,6))
    plt.plot(offset,pitches,marker='o',linestyle='-',color='yellow')
    plt.xlabel('Note Index')
    plt.ylabel('MIDI PITCH')
    plt.title('Melodic Contour')
    y_ticks=pitches
    y_labels=[note.Note(midi).nameWithOctave for midi in y_ticks]
    plt.yticks(y_ticks,y_labels)
    plt.show()  

def chordProgression(offset, chords):
    plt.figure(figsize=(10,6))
    plt.plot(offset,chords)
    plt.show()
    
def pitch_toMidi(pitchName):
    p=pitch.Pitch(pitchName)
    return p.midi
def sortPitches(pitches):
    return sorted(pitches, key=lambda x:pitch_toMidi(x))


##################
#       MAIN     #
#       FUNC     #
##################
try:
    score= converter.parse('/Users/macbook/Desktop/furelise_new.xml')
except Exception as e:
    print("Could not Load")
    raise e

composer=score.metadata.composer
title=score.metadata.title
keyPiece=score.analyze('key')
print(f"Title: {title}")
print(f"Composer: {composer}")
print(f"Overall Key: {keyPiece}")

#to access notes
flat_score=score.flatten()
offset=[]
pitches=[]
for n in flat_score.notes:
    if isinstance(n, note.Note):
        pitches.append(n.pitch.nameWithOctave)
        offset.append(n.offset)

#



with open("my.txt","w") as f:
    f.write("Offset   Pitch\n")
    f.write("---------------\n")
    for oset,p in zip(offset,pitches):
        
        f.write(f"Offset:{oset} = Pitch:{p}\n")
        f.write("\n")
    f.write("------------------")

pitches_midi=[]
#melodicProgression(offset,pitches)

import numpy as np
#INTER-ONSET INTERVALS (IOIs)
iois=np.diff(offset)
#ioisGraph(iois)

#--Chord Analysis
chordified=score.chordify()
chord_prog=[]
for c in chordified.recurse().getElementsByClass('Chord'):
    if(c.commonName != "note"):
        chord_prog.append(c)

offsetChord = []
chord_names = []

# Open a file to write chord info (optional)
# Write chord information to file and accumulate data for plotting
with open("chord.txt", "w") as f:
    f.write("CHORD PROGRESSION\n")
    f.write("--------------\n")
    for c in chord_prog:
        chord_name = c.commonName if c.commonName is not None else "Unknown"
        chord_names.append(chord_name)
        # Use c.offset directly as you mentioned it works
        chord_offset = c.offset
        offsetChord.append(chord_offset)
        chord_pitches = [p.nameWithOctave for p in c.pitches]
        f.write(f"OFFSET: {chord_offset}\n\tChord: {chord_name}\n\tPitches: {chord_pitches}\n\n")



#chordFreq(chord_names)
#chordProgression(offsetChord,chord_names)

durInfo=[]
offInfo=[]
for sc in flat_score.notes:
    durInfo.append(sc.duration.type)
    offInfo.append(sc.offset)


#durFreq(durInfo)
#durProgression(offInfo,durInfo)


melody=list(flat_score.getElementsByClass('Note'))

intervals=[]
for i in range(1,len(melody)):
    intvl=interval.Interval(melody[i-1],melody[i])
    intervals.append(intvl.semitones)

dtwAnalysis(intervals)
offChord=[]
tension_sc=[]
chordname=[]

for c in chord_prog:
    offChord.append(c.offset)
    chordname.append(c.commonName if c.commonName is not None else "")
    tension_sc.append(getTension(c))

plt.figure(figsize=(10,6))
plt.plot(offChord,tension_sc,marker='o')
plt.xlabel('Offset')
plt.ylabel('Tension Score')
plt.yticks([1, 2, 3], ["Stable", "Moderate", "High Tension"])
plt.grid(True)
plt.show()

