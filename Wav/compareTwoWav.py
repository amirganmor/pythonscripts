import scipy.io.wavfile 
import matplotlib.pyplot as plt
import numpy as np
import scipy

# Graphing helper function
def setup_graph(title='', x_label='', y_label='', fig_size=None):
    fig = plt.figure()
    if fig_size != None:
        fig.set_size_inches(fig_size[0], fig_size[1])
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


(sample_rate1, input_signal1) = scipy.io.wavfile.read("out1.wav")
time_array1 = np.arange(0, len(input_signal1)/sample_rate1, 1/sample_rate1)
(sample_rate, input_signal) = scipy.io.wavfile.read("filtered-talk.wav")
time_array = np.arange(0, len(input_signal)/sample_rate, 1/sample_rate)
setup_graph(title='Ah vowel sound', x_label='time (in seconds)', y_label='amplitude', fig_size=(14,7))
plt.plot(time_array1[0:58000], input_signal1[0:58000] , "b-*") 
plt.plot(time_array[0:58000], input_signal[0:58000] , "r-+") 


plt.show()


