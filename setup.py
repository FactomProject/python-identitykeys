from setuptools import setup
import os

setup(name='python-identitykeys',
      version='0.21',
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
      long_description="""\
=============================
Python Identity Keys
=============================

This package allows you to generate public-private key pairs and use them to sign and validate signatures.


============
Requirements
============

Python 3.4+

====================
Installation
====================

***********
pip install
***********

You can install the package hosted on PyPi by using pip:

.. code-block:: shell

  pip install python-identitykeys

Then import the package:
::

  import identitykeys


====================
Usage Guide
====================

**************
Generate Keys
**************
::

  private_key, public_key = identitykeys.generate_key_pair()
  print(private_key.to_string(), " - ", public_key.to_string())

**************
Sign Message
**************
::

  message = b'hello'
  signature = private_key.sign(message)
  print(signature.to_string())

*****************
Validate Message
*****************
::

  result = public_key.verify(signature, message)
  print(result.to_string())


=============================
Harmony Connect Documentation
=============================
This package is built to help you use the `Factom Signing Standard <https://docs.harmony.factom.com/docs/factom-signing-standard>`_ on the Factom blockchain. To learn how to easily write to the Factom Blockchain, please visit the Harmony Connect `documentation <https://docs.harmony.factom.com>`_.

You can create a free account at `Factom.com <https://account.factom.com>`_.
    """
)
