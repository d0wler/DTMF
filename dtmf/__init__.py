import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
 
'''
Sine wave formula: y(t) = A * sin(2 * pi * f * t)
A = amplitude<br>
f = frequency<br>
t = sample<br><br>
'''

'''
The max value of signed 16-bit number is 32767 (2^15 – 1).
Setting amplitude to 16000 to limit scale to half of full-scale audio (32767).<br><br>
'''
dtmfDict = {'1': [int(697),int(1209)],'2': [int(697),int(1336)],'3': [int(697),int(1477)],
            '4': [int(770),int(1209)],'5': [int(770),int(1336)],'6': [int(770),int(1477)],
            '7': [int(852),int(1209)],'8': [int(852),int(1336)],'9': [int(852),int(1477)],
                                      '0': [int(941),int(1336)]}



def main():
	
	signal = Signal()
	phone_number = get_phone_number()
	for num in phone_number:
		signal.insert_dtmf_tones(num)
		signal.insert_silence(.5)

	create_wav_file(signal)
	plot_spectrogram(signal)

class Signal:

	# Initialize parameters for analog sine waves
	def __init__(self):
		self.sr = int(8000)
		self.interval = np.arange(0, .5, 1/self.sr) # )interval * sr
		self.amplitude = int(16000)
		self.file = "test.wav"
		self.samples = np.zeros((len(self.interval)), dtype=float)

	def insert_dtmf_tones(self, num):
		freq1 = dtmfDict.get(num)[0]
		freq2 = dtmfDict.get(num)[1]
		dtmf_tones = self.create_tone(freq1) + self.create_tone(freq2)
		self.samples = np.hstack([self.samples, dtmf_tones])

	def create_tone(self, F):
		tone = np.zeros((len(self.interval)), dtype=float)
		t = self.interval
		for sample,val in enumerate(t):  # val is a throwaway variable here
			tone[sample] = np.cos(2*np.pi*F*t[sample]) *self.amplitude
		return tone
    
	def insert_silence(self, duration):
		silence = np.zeros((int(duration*self.sr)), dtype=float)
		self.samples = np.hstack([self.samples, silence])

	def create_tones(self, phoneNumber):
		# Run each sample through the sine wave formula and put the results into a list.
		for num in phoneNumber :
			# Obtain digital samples of the analog DTMF frequencies and append those samples
			self.samples.extend([((np.sin(2 * np.pi * dtmfDict.get(num)[0] * (x+1)/self.sr))*self.amplitude + 
    	              (np.sin(2 * np.pi * dtmfDict.get(num)[1] * (x+1)/self.sr))*self.amplitude) for x in range(self.num_samples)])
			# Input silence between dial tones
			self.samples.extend([(0) for x in range(self.num_samples)])
			self.samples = np.array(self.samples)


def get_phone_number():
    # Get phone number
    while True:
        try:
            phoneNumber = int(input("Please enter the only the digits of a phone number: "))
            break
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    return str(phoneNumber)
'''
For each sample, multiply it by the amplitude and write it to the wave file

    
    Struct is a Python library that takes our data and packs it as binary data. 
    The h in the code means 16 bit number.
'''
def create_wav_file(signal):

    write(signal.file, signal.sr, signal.samples)

def plot_spectrogram(signal):

    plt.subplot(211)
    plt.title('Time Domain')
    plt.xlabel('Time')
    plt.ylabel('Power')
    plt.plot(range(len(signal.samples)),signal.samples)
    plt.subplot(212)
    plt.title('Spectrogram')
    plt.xlabel('Frequency')
    plt.ylabel('Samples')
    plt.specgram(signal.samples, NFFT=256, Fs=signal.sr, noverlap=0, mode='magnitude', scale='linear')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()





