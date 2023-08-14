# -*- coding: utf-8 -*-
"""
Created on Sat May 13 20:07:49 2023

@author: Dell
"""

import numpy as np
import matplotlib.pyplot as plt


## transformamos datos de valores en valores de temperatura, 
##escalados a valores de frecuencias audibles, 
## se utiliza la ecuacion de la recta como funcion

def frecuencia(t, m, f0, t0):
    y = (m)*(t-t0)+f0
    return float(y)    

arr_t = np.load('Documents/Python Scripts/dato-sonido/arr_t.npy')

f_min = 131.0 #C3
f_max = 987.8 #B5
 
amplitud_t= arr_t.ptp()
amplitud_f = abs(f_max-f_min)
m = amplitud_f/amplitud_t

#f = frecuencia(15.0, m, f_min, arr_t.min())
arr_f = np.vectorize(frecuencia)(arr_t, m, f_min, arr_t.min())


plt.plot(arr_f[:200],'.')
plt.show()

######

### creamos el archibo de audio utilizando pydub
from pydub import AudioSegment
import numpy as np

fs = 44100  # Frecuencia de muestreo
duration = 1  # Duración del audio en segundos

frequencies = arr_f[:200]
# Crear el objeto AudioSegment a partir del array de frecuencias
audio_data = np.array([])
for freq in frequencies:
    sine_wave = np.sin(2*np.pi*freq*np.arange(fs*duration)/fs)
    audio_data = np.concatenate([audio_data, sine_wave])
    
audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=fs, sample_width=2, channels=1)

# Exportar el archivo de audio a formato WAV
audio_segment.export("audio_generado.wav", format="wav")


###
