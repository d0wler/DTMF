from setuptools import setup

setup(
   name='dtmf',
   version='1.0',
   description='Create dial tones',
   author='d0wler',
   author_email='',
   packages=['dtmf'],   # same as name
   install_requires=['numpy', 'scipy', 'matplotlib'],  # external packages as dependencies
)
