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