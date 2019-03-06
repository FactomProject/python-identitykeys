# python-identitykeys

A small module of tools to generate and use key pairs for Factom Identities.

## Usage
To install this module from pypi, run the following:
```$ pip3 install python-identitykeys```

Generating a new random key pair:
```
>>> import identitykeys
>>> private_key, public_key = identitykeys.generate_key_pair()
>>> print(private_key.to_string(), public_key.to_string())
idsec2ioPQqJvJzzwqskEW67yrWd2GwQMs1oCuLHsLHxejmBbEFpEY8 idpub23LV4aM3K3A3G1yyRebacQsMUGeBygi83jZiKwmbWM3DMP1cmr
```

Signing a message and then verifying the signature:
```
message = b'hello'
>>> signature = private_key.sign(message)
>>> if public_key.verify(signature, message):
...     print("Signature verified successfully")
... 
Signature verified successfully
```

## Format of an Identity Key Pair
*Note: the following text is taken from the [Application Identity Specification](https://github.com/FactomProject/FactomDocs/blob/FD-849_PublishNewIdentitySpec/ApplicationIdentity.md)*

For Factom Application Identities, ed25519 keys are used to sign and verify messages. Rather than simply using raw 32 byte arrays for keys, the following encoding scheme is used: 

Pseudo-code for constructing a private key string:
```
prefix_bytes = [0x03, 0x45, 0xf3, 0xd0, 0xd6]              // gives an "idsec" prefix once in base58 
key_bytes = [32 bytes of raw private key]                  // the actual ed25519 private key seed
checksum = sha256( sha256(prefix_bytes + key_bytes) )[:4]  // 4 byte integrity check on the previous 37 bytes

idsec_key_string = base58( prefix_bytes + key_bytes + checksum )
```

Pseudo-code for constructing a public key string:
```
prefix_bytes = [0x03, 0x45, 0xef, 0x9d, 0xe0]              // gives an "idpub" prefix once in base58 
key_bytes = [32 bytes of raw public key]                   // the actual ed25519 public key
checksum = sha256( sha256(prefix_bytes + key_bytes) )[:4]  // 4 byte integrity check on the previous 37 bytes

idpub_key_string = base58( prefix_bytes + key_bytes + checksum )
```

For the sake of human-readability, all characters must be in Bitcoin's base58 character set, the private key will always begin with "idsec", and the public key will always begin with "idpub". Additionally, the checksum at the end serves to signal that a user has incorrectly typed/copied their key.

Example key pair for the private key of all zeros:
- `idsec19zBQP2RjHg8Cb8xH2XHzhsB1a6ZkB23cbS21NSyH9pDbzhnN6 idpub2Cy86teq57qaxHyqLA8jHwe5JqqCvL1HGH4cKRcwSTbymTTh5n`

Example key pair for the private key of all ones:
- `idsec1ARpkDoUCT9vdZuU3y2QafjAJtCsQYbE2d3JDER8Nm56CWk9ix idpub2op91ghJbRLrukBArtxeLJotFgXhc6E21syu3Ef8V7rCcRY5cc`
