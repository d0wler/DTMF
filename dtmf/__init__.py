



import numpy as np
import wave
import struct
 
# Initialize parameters for analog sine waves
sampling_rate = int(8000) # The sampling rate of the analog to digital convert
num_samples = 4000 # 4K correlates to 1/2 a second since the sample rate is 48K
amplitude = 16000
'''
The max value of signed 16-bit number is 32767 (2^15 – 1).
Setting amplitude to 16000 to limit scale to half of full-scale audio (32767).<br><br>
'''

# Initialize list of numeric values that represent the DTMF sine waves
combined_wave = []

# Initialize wave file
file = "test.wav"

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

'''
  Sine wave formula: y(t) = A * sin(2 * pi * f * t)
  A = amplitude<br>
  f = frequency<br>
  t = sample<br><br>
'''

# Run each sample through the sine wave formula and put the results into a list.
for num in phoneNumber :
    # Obtain digital samples of the analog DTMF frequencies and append those samples
    combined_wave.extend([((np.sin(2 * np.pi * dtmfDict.get(num)[0] * x/sampling_rate)) + 
    	                 (np.sin(2 * np.pi * dtmfDict.get(num)[1] * x/sampling_rate))) for x in range(num_samples)])
    # Input silence between dial tones
    combined_wave.extend([(np.sin(2 * np.pi * 0 * x/sampling_rate)) for x in range(num_samples)])

# Set paramerters for Python's wave library
nframes=num_samples
comptype="NONE" #compression
compname="not compressed" #compression type
nchannels=1
sampwidth=2 #2 bytes per sample (Wave files are written as 16-bit short integers)

wav_file=wave.open(file, 'w')

wav_file.setparams((nchannels, sampwidth, int(sampling_rate), nframes, comptype, compname))

# For each sample, multiply it by the amplitude and write it to the wave file
for s in combined_wave:
    wav_file.writeframes(struct.pack('h', int(s*amplitude)))
    '''
    Struct is a Python library that takes our data and packs it as binary data. 
    The h in the code means 16 bit number.
    '''

# The test.wave file should now be created. Open it with an audio player to hear the phone number as DTMF.
