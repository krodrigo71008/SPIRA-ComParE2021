import math
import glob

import scipy
import librosa
import numpy as np

if __name__ == "__main__":
    folder_path = "../SPIRA-ACL2021/data/ACL-Dataset/controle"
    # folder_path = "../SPIRA-ACL2021/data/ACL-Dataset/pacientes"

    audios = glob.glob(f"{folder_path}/**/*.wav", recursive=True)
    for audio_file in audios:
        audio, sr = librosa.load(audio_file, sr=None)
        zcr = librosa.zero_crossings(audio)
        energy = np.sum(audio**2)
        peak=scipy.signal.find_peaks(audio,rel_height=0.5)
        #JITTER, SHIMMER, JITTERRAP 
        sums = 0
        for i in range(1,len(peak[0])-1):
            sums=sums+abs(20*math.log10(peak[0][i+1]/peak[0][i]))

        #SHIMMER
        shimmer=sums/(len(peak[0])-1)
        peakf=abs(np.fft.fft(peak[0]))
        sumps=0
        for i in range(1,len(peakf)-1):
            sumps=sumps+(peakf[i+1]**-1)-(peakf[i]**-1)

        #JITTER
        jitter=sumps/(len(peakf)-1)
        sortedp=np.sort(peak[0])
        sortedf=abs(np.fft.fft(sortedp))
        dif=abs(sortedp[11]-sortedp[15])
        suh=0
        avgabsdiff=(dif)/4
        avgneigh1=(abs(sortedp[6]-sortedp[10]))
        avgneigh2=abs(sortedp[17]-sortedp[22])
        avg=(dif+avgneigh1+avgneigh2)/3

        for i in range(11,16):
            suh=suh+abs(sortedf[i]**-1)
        period=suh/5

        #JITTERRAP
        jitterrap=(avgabsdiff+avg)/period

        f0 = librosa.pyin(audio, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        print("a")
