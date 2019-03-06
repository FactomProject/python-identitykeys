from setuptools import setup
import os

setup(name='python-identitykeys',
      version='0.2',
      description='Tools for using Factom identity keys',
      url='https://github.com/FactomProject/python-identitykeys',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Topic :: Software Development :: Libraries",
          "Topic :: Utilities",
      ],
      keywords=['factom', 'identity'],
      license='MIT',
      py_modules=['identitykeys'],
      install_requires=[
          'ed25519',
          'python-bitcoinlib'
      ],
      zip_safe=False)
