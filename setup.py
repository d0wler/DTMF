from setuptools import setup

setup(name='dtmf',
      version='0.1',
      description='Creates wave file with DTMF from input phone number',
      url='https://github.com/d0wler/DTMF'
      author='Ryan Dowler',
      author_email='ryandowler05@gmail.com',
      license='MIT',
      packages=['dtmf'],
      install_requires=[
          'numpy==1.15.2',
      ],
      zip_safe=False)