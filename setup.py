from setuptools import setup

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(name='apitweet',
      version='0.1',
      description='tweeter automation',
      url='http://github.com/Arcturus122/apitweet',
      author='Louis-Alexis Dubief',
      author_email='louisalexis.dubief@gmail.com',
      license='MIT',
      packages=['apitweet'],
      install_requires=requirements,
      scripts=['bin/launch-apitweet'],
      zip_safe=False)
