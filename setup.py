from distutils.core import setup
from Pyrex.Distutils.extension import Extension
from Pyrex.Distutils import build_ext

setup(name='pappy',
	version='0.91',
	ext_modules=[									\
		Extension(									\
			'pappy',								\
			['pappy.pyx'],							\
			libraries=['portaudio'],				\
		)],
	cmdclass = {'build_ext': build_ext},			\
	description='PortAudio wrapped in Python',	\
	author='Dale Cieslak',							\
	author_email='dsizzle@github.com',	\
	url='https://github.com/dsizzle/pappy',			\
)


