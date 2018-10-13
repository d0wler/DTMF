import numpy as np
import wave
import struct
import matplotlib.pyplot as plt
import random
 
'''
Sine wave formula: y(t) = A * sin(2 * pi * f * t)
A = amplitude<br>
f = frequency<br>
t = sample<br><br>
'''

# Initialize parameters for analog sine waves
sampling_rate = int(8000) # The sampling rate of the analog to digital convert
num_samples = 4000 # 4K correlates to 1/2 a second since the sample rate is 48K
amplitude = 16000

# Initialize list of numeric values that represent the DTMF sine waves
samples = []

# Initialize wave file
file = "test.wav"

# Create noise
noise = random.randint(0,8001)

'''
The max value of signed 16-bit number is 32767 (2^15 – 1).
Setting amplitude to 16000 to limit scale to half of full-scale audio (32767).<br><br>
'''

# Get phone number
while True:
    try:
        phoneNumber = int(input("Please enter the only the digits of a phone number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")

# Convert phoneNumber to string
phoneNumber = str(phoneNumber)

dtmfDict = {'1': [int(697),int(1209)],'2': [int(697),int(1336)],'3': [int(697),int(1477)],
            '4': [int(770),int(1209)],'5': [int(770),int(1336)],'6': [int(770),int(1477)],
            '7': [int(852),int(1209)],'8': [int(852),int(1336)],'9': [int(852),int(1477)],
                                      '0': [int(941),int(1336)]}

# Run each sample through the sine wave formula and put the results into a list.
for num in phoneNumber :
    # Obtain digital samples of the analog DTMF frequencies and append those samples
    samples.extend([((np.sin(2 * np.pi * dtmfDict.get(num)[0] * (x+1)/sampling_rate))*amplitude + 
    	              (np.sin(2 * np.pi * dtmfDict.get(num)[1] * (x+1)/sampling_rate))*amplitude) + noise
                    for x in range(num_samples)])
    # Input silence between dial tones
    samples.extend([(noise) for x in range(num_samples)])

# Set paramerters for Python's wave library
nframes=num_samples
comptype="NONE" #compression
compname="not compressed" #compression type
nchannels=1
sampwidth=2 #2 bytes per sample (Wave files are written as 16-bit short integers)

wav_file=wave.open(file, 'w')

wav_file.setparams((nchannels, sampwidth, int(sampling_rate), nframes, comptype, compname))

'''
For each sample, multiply it by the amplitude and write it to the wave file

for sample in samples:
    wav_file.writeframes(struct.pack('h', int(sample*amplitude)))
    
    Struct is a Python library that takes our data and packs it as binary data. 
    The h in the code means 16 bit number.
'''

plt.subplot(211)
plt.title('Time Domain')
plt.xlabel('Time')
plt.ylabel('Power')
plt.plot(range(len(samples)),samples)
plt.subplot(212)
plt.title('Spectrogram')
plt.xlabel('Frequency')
plt.ylabel('Samples')
plt.specgram(samples, NFFT=256, Fs=sampling_rate, noverlap=0, mode='magnitude', scale='linear')
plt.tight_layout()
plt.show()