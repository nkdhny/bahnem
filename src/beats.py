#! /usr/bin/env python

import sys
import time
from pygame import mixer
from aubio import tempo, source, pitch
from numpy import zeros, hstack, diff

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size
downsample = 2**4
amplitudes = zeros(0,)

filename = "mfdoom.mp3"
samplerate = 0

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = tempo("default", win_s, hop_s, samplerate)
amplitudes = zeros(0,)
# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 4. * hop_s

# list of beats, in samples
beats = []

tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

pitches = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    is_beat = o(samples)
    pitch = pitch_o(samples)[0]
    if is_beat:
        this_beat = o.get_last_s()
        beats.append(this_beat)
    total_frames += read
    pitches.append([total_frames / float(samplerate), pitch])
    new_maxes = (abs(samples.reshape(hop_s//downsample, downsample))).max(axis=0)
    amplitudes = hstack([amplitudes, new_maxes])
    if read < hop_s: break


bpms = 60./ diff(beats)
amplitudes = (amplitudes > 0) * amplitudes
amplitudes_times = [ ( float (t) / downsample ) * hop_s for t in range(len(amplitudes)) ]


mixer.init()
mixer.music.load(filename)
mixer.music.play()

beat_delays = [y - x for x,y in zip(beats,beats[1:])]

print len(beats)
print len(beat_delays)
print len(pitches)
print len(amplitudes)
print len(amplitudes_times)
# for b in delays:
# 	time.sleep(b)
# 	print b
