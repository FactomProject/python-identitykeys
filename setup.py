from setuptools import setup
import os

def long_description_file():
    with open('pypi_description.rst') as f:
        return f.read()

setup(name='python-identitykeys',
      version='0.2.1',
      description='Tools for using Factom identity keys',
      author="Factom Inc.",
      author_email="harmony-support@factom.com",
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
      zip_safe=False,
      long_description=long_description_file()
)
