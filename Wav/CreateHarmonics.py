##############################################################################
#
# Copyright (c) 2019 Mind Chasers Inc.
# All Rights Reserved.
#
#    file: harmonics.py
#
#    create and visualize harmonic waveforms
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import matplotlib.pylab as plt
import numpy as np
import argparse
import wave, struct
from scipy.io import wavfile
import soundfile as sf

def HarmonicsFunc(path , f , harmonics=0 ):    
    f = 50
    odd = 1
    mult = 2
    f1 = sf.SoundFile('in1.wav')
    samp = len(f1)
    rat = f1.samplerate
    secs = samp / rat
    start = 0.0

    t = np.linspace(start , secs , num=samp)
    y = np.zeros(samp)
    
    # compute fundamental and each harmonic
    for i in range(int(harmonics)+1):
        h = i * mult + odd
        yh = 1/h * np.sin(h * 2 * np.pi * f * t)
        y = y + yh

    my_new_list = []
    for i in y :
        my_new_list.append(int(i * 32767))
    outFor = np.asarray(my_new_list, dtype=np.int16)
    wavfile.write("out.wav", 8000 , outFor)
    
    plt.plot(t, y)
    plt.xlabel('time')
    plt.ylabel('harmonics {0}'.format(harmonics))
    plt.axis('tight')
    plt.show()


path = 'in1.wav'
HarmonicsFunc(path,50)