#!/opt/local/bin/python2.5
# @file paTest1.py
#	@ingroup test_src
#	@brief Ring modulate the audio input with a sine wave for 20 seconds.
#       @author Dale Cieslak <dsizzle@github>
#	@author (C program by Ross Bencina <rossb@audiomulch.com>)
#
# $Id: paTest1.py 1 2010-04-28 12:51:15Z dale $
# 
# This program uses the PortAudio Portable Audio Library.
# For more information see: http://www.portaudio.com
# Copyright (c) 1999-2000 Ross Bencina and Phil Burk
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 

# 
# The text above constitutes the entire PortAudio license; however, 
# the PortAudio community also makes the following non-binding requests:
# 
# Any person wishing to distribute modifications to the Software is
# requested to send the modifications to the original developer so that
# they can be incorporated into the canonical version. It is also 
# requested that these non-binding requests be included along with the 
# license above.
# 

import math
import sys

import pappy

gSampleRate = 44100
gFramesPerBuffer = 512

# This routine will be called by the PortAudio engine when audio is needed.
# It may called at interrupt level on some machines so don't do anything
# that could mess up the system.

def paCallbackWrapper(userData):
	funcdict = {}
	
	def patestCallback(inputBuffer, 
						framesPerBuffer,			\
						timeInfo,					\
						statusFlags):
		out = []
		data = userData
		framesToCalc = framesPerBuffer

		if (data['sampsToGo'] < framesPerBuffer):
			framesToCalc = data['sampsToGo']
			finished = pappy.pyPaComplete
		else:
			finished = pappy.pyPaContinue

		sineData = data['sine']

		for i in range(0, framesToCalc-1):
			out.append(inputBuffer[i] * sineData[data['phase']])
			out.append(inputBuffer[i+1] * sineData[data['phase']])
			data['phase'] += 1 
			if (data['phase'] >= 100):
				data['phase'] = 0
			
		data['sampsToGo'] -= framesToCalc
			
		for i in range(framesToCalc+1, framesPerBuffer):
			out.append(0)
			out.append(0)

		return finished, out
	
	funcdict['streamcallback'] = patestCallback
	return funcdict

# *******************************************************************
def main():
	print "paTest1.py\n"
	print "Ring modulate input for 20 seconds.\n"

	# initialize sinusoidal wavetable
	data = {}
	data['sine'] = []

	for i in range(0, 100):
		data['sine'].append(math.sin((float(i)/float(100.)) * math.pi * 2. ))
   
	data['phase'] = 0
	data['sampsToGo'] = gSampleRate * 20;	# 20 seconds
	# Initialize portaudio subsystem.

	err = pappy.pyPaNoError
	
	try:
		err = pappy.paInitialize()
		if (not err == pappy.pyPaNoError):
			raise SystemError
		
		inputParameters = {}
		inputParameters['device'] = pappy.paGetDefaultInputDevice()
		if (inputParameters['device'] == pappy.pyPaNoDevice):
			sys.stderr.write("ERROR: no default input device")
			raise SystemError

		inputParameters['channelCount'] = 2
		inputParameters['sampleFormat'] = pappy.pyPaFloat32
		inputParameters['suggestedLatency'] = pappy.paGetDeviceInfo( inputParameters['device'] )['defaultLowInputLatency']
		inputParameters['hostApiSpecificStreamInfo'] = None;

		outputParameters = {}
		outputParameters['device'] = pappy.paGetDefaultOutputDevice()
		if (outputParameters['device'] == pappy.pyPaNoDevice):
			sys.stderr.write("ERROR: no default output device")
			raise SystemError

		outputParameters['channelCount'] = 2
		outputParameters['sampleFormat'] = pappy.pyPaFloat32
		outputParameters['suggestedLatency'] = pappy.paGetDeviceInfo( outputParameters['device'] )['defaultLowOutputLatency']
		outputParameters['hostApiSpecificStreamInfo'] = None;
	
		stream = None
		pyPaTestCallback = paCallbackWrapper(data)
		(err, stream) = pappy.paOpenStream(inputParameters,		\
											outputParameters,	\
											gSampleRate,		\
											gFramesPerBuffer,	\
											pappy.pyPaClipOff,	\
											pyPaTestCallback)

		if (not err == pappy.pyPaNoError):
			raise SystemError																
		
		err = pappy.paStartStream(stream)
		if (not err == pappy.pyPaNoError):
			raise SystemError
		
		print "Press any key to end.\n"

		char = sys.stdin.read(1)

		err = pappy.paAbortStream(stream)
		if (not err == pappy.pyPaNoError):
			raise SystemError
		
		print "Waiting for stream to complete...\n"

		# sleep until playback has finished
		err = pappy.paIsStreamActive(stream)
		while (err == 1):
			pappy.paSleep( 1000 )
			err = pappy.paIsStreamActive(stream) 

		if (not err == pappy.pyPaNoError):
			raise SystemError

		err = pappy.paCloseStream(stream)
		if (not err == pappy.pyPaNoError):
			raise SystemError
		
		pappy.paTerminate()
		print "Test finished.\n"
	
		return err
	
	except SystemError:
		pappy.paTerminate()
		sys.stderr.write("An error occured while using the portaudio stream")
		sys.stderr.write("Error number: %d" % err)
		sys.stderr.write("Error message: %s" % pappy.paGetErrorText(err))
		return err

sys.exit(main())
