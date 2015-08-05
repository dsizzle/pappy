#!/opt/local/bin/python2.5
# @file paExSaw.py
#	@ingroup examples_src
#	@brief Play a simple (aliasing) sawtooth wave.
#       @author Dale Cieslak <dsizzle@github>
#	@author (C program by Phil Burk <philburk@softsynth.com>)
#
# $Id: paExSaw.py 1 2010-04-28 12:51:15Z dale $
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

gNumSeconds = 4
gSampleRate = 44100
gFramesPerBuffer = 256

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
		
		for i in range(0, framesPerBuffer):
			out.append(userData['left_phase'])
			out.append(userData['right_phase'])
			# Generate simple sawtooth phaser that ranges between -1.0 and 1.0.
			userData['left_phase'] += 0.01
			# When signal reaches top, drop back down.
			if (userData['left_phase'] >= 1.0):
				userData['left_phase'] -= 2.0
			
			# higher pitch so we can distinguish left and right
			userData['right_phase'] += 0.03 
			if (userData['right_phase'] >= 1.0):
				userData['right_phase'] -= 2.0
				 	
		return pappy.pyPaContinue, out
	
	funcdict['streamcallback'] = patestCallback
	return funcdict

# *******************************************************************
def main():
	print "PortAudio Test: output sawtooth wave.\n"
	
	# Initialize our data for use by callback.
	data = {}
	data['left_phase'] = 0
	data['right_phase'] = 0
	# Initialize library before making any other calls.

	err = pappy.pyPaNoError
	
	try:
		err = pappy.paInitialize()
		if (not err == pappy.pyPaNoError):
			raise SystemError
		
		stream = None
		pyPaTestCallback = paCallbackWrapper(data)
		(err, stream) = pappy.paOpenDefaultStream(0,			\
											2,					\
											pappy.pyPaFloat32,	\
											gSampleRate,		\
											gFramesPerBuffer,	\
											pyPaTestCallback)
		if (not err == pappy.pyPaNoError):
			raise SystemError									
		
		err = pappy.paStartStream(stream)
		if (not err == pappy.pyPaNoError):
			raise SystemError
		
		# sleep for several seconds
		pappy.paSleep(gNumSeconds * 1000)
		
		err = pappy.paStopStream(stream)
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
