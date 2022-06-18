import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


def get_freq(audio_file, dir, file_index):
    f1 = open(dir + "/" + dir + "_max_freq.txt", "a")
    Fs,data = wavfile.read(audio_file)
    n = len(data)
    k = np.arange(n)
    T = n/Fs
    frq = k / T
    frq = frq[:len(frq) // 2]
    Y = np.fft.fft(data)
    Y = Y[:n//2]
    delta = 2
    segments_amp_averages = []
    is_man = True
    for i in range(0, len(frq), delta):
        avr_amp = np.average(abs(Y[i: i + delta]))
        segments_amp_averages.append(avr_amp)
    print(frq[int(np.argmax(segments_amp_averages)*delta+delta/2)])
    if (frq[int(np.argmax(segments_amp_averages)*delta+delta/2)] > 280):
        print("Record " + str(file_index) + " is a woman!\n")
        is_man = False
    else:
        print("Record " + str(file_index) + " is a man!\n")
    max_freq = frq[np.argmax(abs(Y))]
    fig = plt.figure(figsize = (12, 8))
    plt.plot(frq, abs(Y))
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')
    plt.savefig(dir + "/" + str(file_index) + '.png')
    plt.close()
    f1.write(str(file_index) + ", " + str(max_freq) + "\n")
    f1.close()
    return is_man

print("Men:")
men_count = 0.0
women_count = 0.0
for i in range(15):
    is_man = get_freq("Men/" + str(i) + ".wav", "Men", i)
    if is_man:
        men_count = men_count + 1.0
accuracy = men_count / 15.0
print("men detection accuracy = " + str(accuracy))
print("-------------------")
print("Women:")
for i in range(15):
    is_man = get_freq("Women/" + str(i) + ".wav", "Women", i)
    if not is_man:
        women_count = women_count + 1.0
accuracy = women_count / 15.0
print("women detection accuracy = " + str(accuracy))
