from music21 import *
import matplotlib.pyplot as plt 

def pitch_toMidi(pitchName):
    p=pitch.Pitch(pitchName)
    return p.midi
def sortPitches(pitches):
    return sorted(pitches, key=lambda x:pitch_toMidi(x))

try:
    score= converter.parse('/Users/macbook/Desktop/furelise_new.xml')
except Exception as e:
    print("Could not Load")
    raise e

composer=score.metadata.composer
title=score.metadata.title
print(f"Title: {title}")
print(f"Composer: {composer}")

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
plt.figure(figsize=(10,6))
plt.plot(offset,pitches,marker='o',linestyle='-',color='yellow')
plt.xlabel('Note Index')
plt.ylabel('MIDI PITCH')
plt.title('Melodic Contour')
y_ticks=pitches
y_labels=[note.Note(midi).nameWithOctave for midi in y_ticks]
plt.yticks(y_ticks,y_labels)
plt.show()

import numpy as np
#INTER-ONSET INTERVALS (IOIs)
iois=np.diff(offset)
plt.figure(figsize=(10,6))
plt.hist(iois, bins=20, color='blue')
plt.xlabel('Inter-Onset Interval')
plt.ylabel('Frequency')
plt.title('Rhytmic Pattern-Inter Onset Intervals')
plt.show()

#--Chord Analysis
chordified=score.chordify()
chord_prog=[]
for c in chordified.recurse().getElementsByClass('Chord'):
    if(c.commonName is not "note"):
        chord_prog.append(c)

with open("chord.txt","w") as f:
    f.write("CHORD PROGRESSION\n")
    f.write("--------------\n")
    for c in chord_prog:
        chord_name=c.commonName if c.commonName is not None else ""
        chord_pitches=[p.nameWithOctave for p in c.pitches]
        f.write(f"OFFSET: {c.offset}\n \tChord: {chord_name}\n \tPitches: {chord_pitches}")
        f.write("\n")
