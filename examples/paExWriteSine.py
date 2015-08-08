#!/opt/local/bin/python2.5
# @file paExWriteSine.py
#	@ingroup examples_src
#	@brief Play a sine wave for several seconds using the blocking API (Pa_WriteStream())
#       @author Dale Cieslak <dsizzle@github>
#	@author (C program by Ross Bencina <rossb@audiomulch.com>)
#	@author (C program by Phil Burk <philburk@softsynth.com>)
#
# $Id: paExWriteSine.py 1 2010-04-28 12:51:15Z dale $
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

gNumSeconds = 5
gSampleRate = 44100
gFramesPerBuffer = 1024

gTableSize = 200

# *******************************************************************
def main():
	left_phase = 0
	right_phase = 0
	left_inc = 1
	right_inc = 3
	buffer = []

	print "PortAudio Test: output sine wave. SR = %d, BufSize = %d\n" % (gSampleRate, gFramesPerBuffer)

	# initialize sinusoidal wavetable
	sine = []

	for i in range(0, gTableSize):
		sine.append(math.sin((float(i)/float(gTableSize)) * math.pi * 2. ))
   
	
	err = pappy.pyPaNoError
	
	try:
		err = pappy.paInitialize()
		if (not err == pappy.pyPaNoError):
			raise SystemError
		
		outputParameters = {}
		outputParameters['device'] = pappy.paGetDefaultOutputDevice()
		if (outputParameters['device'] == pappy.pyPaNoDevice):
			sys.stderr.write("ERROR: no default output device")
			raise SystemError

		outputParameters['channelCount'] = 2
		outputParameters['sampleFormat'] = pappy.pyPaFloat32
		outputParameters['suggestedLatency'] = 0.050 #pappy.paGetDeviceInfo( outputParameters['device'] )['defaultLowOutputLatency']
		outputParameters['hostApiSpecificStreamInfo'] = None;
	
		stream = None
		(err, stream) = pappy.paOpenStream(None,		\
											outputParameters,	\
											gSampleRate,		\
											gFramesPerBuffer,	\
											pappy.pyPaClipOff,	\
											None)

		if (not err == pappy.pyPaNoError):
			raise SystemError	

		print "Play 3 times, higher each time.\n"																
		
		for k in range(0, 3):
			err = pappy.paStartStream(stream)
			if (not err == pappy.pyPaNoError):
				raise SystemError
		
			print "Play for %d seconds.\n" % gNumSeconds

			bufferCount = ((gNumSeconds *  gSampleRate) / gFramesPerBuffer)

			buffer = []

			for i in range(0, bufferCount):
				for j in range(0, gFramesPerBuffer):
					buffer.append([sine[left_phase], sine[right_phase]])
					left_phase += left_inc
					if (left_phase >= gTableSize):
						left_phase -= gTableSize
					right_phase += right_inc
					if (right_phase >= gTableSize):
						right_phase -= gTableSize

				err = pappy.paWriteStream(stream, buffer, gFramesPerBuffer)
				if (not err == pappy.pyPaNoError):
					raise SystemError

			err = pappy.paStopStream(stream)
			if (not err == pappy.pyPaNoError):
				raise SystemError
			
			++left_inc
			++right_inc

			pappy.paSleep(1000)

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
