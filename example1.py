from music21 import *

try:
    score= converter.parse('/Users/macbook/Desktop/furelise_new.xml')
except Exception as e:
    print("Could not Load")
    raise e

furKey=score.analyze('key')

# first_part=score.parts[0]
# time_sign=first_part.getElementsByClass(meter.TimeSignature)[0]
time_sign=score.recurse().getElementsByClass(meter.TimeSignature)[0]
print(time_sign)
all_notes=score.recurse().getElementsByClass(note.Note)
noteCnt=len(all_notes)

score_summ={
    "Key": furKey,
    "Time Signature": time_sign.ratioString,
    "Note Count": noteCnt
}



print("==SUMMARY OF FUR ELISE==")
for item, value in score_summ.items():
    print(f"{item}: {value}")

chordy=score.chordify()
# chordes=score.chordify()
# for c in chordes:
#     if c.commonName != "note":
#         chordy=c

for c in chordy.recurse().getElementsByClass(chord.Chord):
    if(c.commonName != "note"):
        print(f"Chord (Pitch Classes): {c.normalOrder} | Name: {c.commonName}")

# with open('chord_output.txt', 'w') as f:
#     for c in chordy.recurse().getElementsByClass(chord.Chord):
#         f.write(f"Chord (Pitch Classes): {c.normalOrder} | Name: {c.commonName}\n")
# print("Chord details saved to chord_output.txt")



if score.metadata is not None:
    print("Title: ",score.metadata.title)
    print("Composer: ",score.metadata.composer)

import matplotlib.pyplot as plt 
from collections import Counter

chord_list = [c.commonName if c.commonName is not None else str(c.normalOrder) 
              for c in chordy.recurse().getElementsByClass(chord.Chord)]

chordCnt=Counter(chord_list)

plt.figure(figsize=(10,6))
plt.bar(chordCnt.keys(),chordCnt.values())
plt.xticks(rotation=45, ha='right')
#plt.show()

chordCnt=Counter()

for c in chordy.flat.notes:
    if isinstance(c, chord.Chord):
        chord_symbol=c.commonName or 'Not Detected'
        chordCnt[chord_symbol] = chordCnt[chord_symbol] +1

chord_freq=dict(chordCnt)

chords=list(chord_freq.keys())
freq=list(chord_freq.values())

plt.figure(figsize=(10,8))
plt.bar(chords,freq,color="red")
plt.xlabel("Chords")
plt.ylabel("Frequency")
plt.title("Chord Frequency Distribution")
plt.tight_layout()
#plt.show()


durs=[]

for c in chordy.recurse().getElementsByClass(chord.Chord):
    durs.append(c.duration.quarterLength)
3

flat_score = score.flatten().notes

# Extract Pitch objects from the notes
pitches = [n.pitch for n in flat_score if isinstance(n, note.Note)]

# Compute intervals between consecutive pitches
intervals = [interval.Interval(pitches[i], pitches[i + 1]).cents for i in range(len(pitches) - 1)]

# Plot the melodic contour
plt.figure(figsize=(12, 6))
plt.plot([p.midi for p in pitches], marker='o', linestyle='-', color='b')
plt.xlabel('Note Index')
plt.ylabel('MIDI Pitch')
plt.title('Melodic Contour')
plt.grid(True)
#plt.show()

notes=[]
for n in flat_score:
    if isinstance(n, note.Note):
        offset=n.offset
        dur=n.duration.quarterLength
        notes.append((offset,dur))

chord_d=[]
for e in score.recurse().getElementsByClass('Chord'):
    r=e.root().name
    qu=e.quality
    chord_name=f"{r} {qu}"
    chord_d.append({
        'offset':e.offset,
        'chord_name':chord_name
    })

import pandas as pd
df=pd.DataFrame(chord_d)
df['chord_id']=pd.factorize(df['chord_name'])[0]
print(df['chord_id'])
print(df)

import plotly.express as px
fig=px.scatter(df, x='offset',y='chord_name')
fig.show()

import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display

chords = []
for element in score.recurse().getElementsByClass('Chord'):
    chords.append({
        'offset': element.offset,
        'pitches': [p.nameWithOctave for p in element.pitches]
    })

fig = go.Figure()

for chord_info in chords:
    fig.add_trace(go.Scatter(
        x=[chord_info['offset']],
        y=[1],  # Arbitrary y-value for visualization
        mode='markers+text',
        marker=dict(size=10),
        text=', '.join(chord_info['pitches']),
        textposition='top center',
        hoverinfo='text'
    ))

fig.update_layout(
    title='Interactive Timeline of Chord Changes',
    xaxis_title='Offset (beats)',
    yaxis_title='',
    yaxis=dict(showticklabels=False),  # Hide y-axis labels
    showlegend=False
)

fig.show()


# Slider to select a range of offsets
offset_slider = widgets.FloatRangeSlider(
    value=[0, max(chord['offset'] for chord in chords)],
    min=0,
    max=max(chord['offset'] for chord in chords),
    step=0.1,
    description='Offset Range:',
    continuous_update=False
)

# Output widget to display the plot
output = widgets.Output()

def update_plot(change):
    with output:
        output.clear_output()
        selected_range = offset_slider.value
        filtered_chords = [chord for chord in chords if selected_range[0] <= chord['offset'] <= selected_range[1]]
        
        fig = go.Figure()

        for chord_info in filtered_chords:
            fig.add_trace(go.Scatter(
                x=[chord_info['offset']],
                y=[1],
                mode='markers+text',
                marker=dict(size=10),
                text=', '.join(chord_info['pitches']),
                textposition='top center',
                hoverinfo='text'
            ))

        fig.update_layout(
            title=f'Chord Changes from Offset {selected_range[0]} to {selected_range[1]}',
            xaxis_title='Offset (beats)',
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            showlegend=False
        )

        fig.show()

# Attach the update function to the slider
offset_slider.observe(update_plot, names='value')

# Display the widgets
display(offset_slider, output)

# Initialize the plot
update_plot(None)

