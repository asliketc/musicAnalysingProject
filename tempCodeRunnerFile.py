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
print(offset)