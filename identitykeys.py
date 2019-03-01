import ed25519
from bitcoin import base58
from hashlib import sha256

IDPUB_PREFIX = b'\x03E\xef\x9d\xe0'  # 0x03, 0x45, 0xef, 0x9d, 0xe0
IDSEC_PREFIX = b'\x03E\xf3\xd0\xd6'  # 0x03, 0x45, 0xf3, 0xd0, 0xd6
IDKEY_PREFIX_LENGTH = 5
IDKEY_CHECKSUM_LENGTH = 4
IDKEY_BODY_LENGTH = 37
IDKEY_TOTAL_LENGTH = 41


def generate_key_pair():
    '''Returns a tuple containing (PrivateIdentityKey, PublicIdentityKey)'''
    signer, verifier = ed25519.create_keypair()
    return PrivateIdentityKey(signer.to_seed()), PublicIdentityKey(verifier.to_bytes())


def to_string(key_bytes):
    '''Convert prefix + key bytes into idpub/idsec strings with a checksum'''
    prefix = key_bytes[:IDKEY_PREFIX_LENGTH]
    assert prefix == IDPUB_PREFIX or prefix == IDSEC_PREFIX, 'Invalid key prefix.'
    temp_hash = sha256(key_bytes[:IDKEY_BODY_LENGTH]).digest()
    checksum = sha256(temp_hash).digest()[:IDKEY_CHECKSUM_LENGTH]
    return base58.encode(key_bytes + checksum)


def is_valid_idpub(key):
    '''Returns true if key is a valid public identity key string in idpub format'''
    if not isinstance(key, str):
        return False
    try:
        decoded = base58.decode(key)
    except base58.InvalidBase58Error as e:
        return False

    if len(decoded) != IDKEY_TOTAL_LENGTH or decoded[:5] != IDPUB_PREFIX:
        return False

    checksum_claimed = decoded[IDKEY_BODY_LENGTH:]
    temp_hash = sha256(decoded[:IDKEY_BODY_LENGTH]).digest()
    checksum_actual = sha256(temp_hash).digest()[:IDKEY_CHECKSUM_LENGTH]

    return checksum_actual == checksum_claimed


def is_valid_idsec(key):
    '''Returns true if key is a valid secret identity key string in idsec format'''
    if not isinstance(key, str):
        return False
    try:
        decoded = base58.decode(key)
    except base58.InvalidBase58Error as e:
        return False

    if len(decoded) != IDKEY_TOTAL_LENGTH or decoded[:5] != IDSEC_PREFIX:
        return False

    checksum_claimed = decoded[IDKEY_BODY_LENGTH:]
    temp_hash = sha256(decoded[:IDKEY_BODY_LENGTH]).digest()
    checksum_actual = sha256(temp_hash).digest()[:IDKEY_CHECKSUM_LENGTH]

    return checksum_actual == checksum_claimed


class BadKeyStringError(Exception):
    pass


class PrivateIdentityKey(object):
    def __init__(self, seed_bytes=None, key_string=None):
        assert (seed_bytes and not key_string) or (not seed_bytes and key_string), \
            "Only provide one of seed_bytes or key_string, not both"

        if key_string:
            if not is_valid_idsec(key_string):
                raise BadKeyStringError()
            decoded = base58.decode(key_string)
            seed_bytes = decoded[IDKEY_PREFIX_LENGTH:IDKEY_BODY_LENGTH]

        assert isinstance(seed_bytes, bytes)
        assert len(seed_bytes) == 32
        self.__signer = ed25519.SigningKey(seed_bytes)

    def to_bytes(self):
        '''Returns the 32 byte raw private key'''
        return self.__signer.to_seed()

    def to_string(self):
        '''Returns the key as a human-readable string in idsec format'''
        secret_body = IDSEC_PREFIX + self.__signer.to_seed()
        return to_string(secret_body)

    def get_public_key(self):
        '''Derive and return the corresponding PublicIdentityKey'''
        public_bytes = self.__signer.get_verifying_key().to_bytes()
        return PublicIdentityKey(public_bytes)

    def sign(self, message):
        '''Signs the given message and returns the signature bytes'''
        return self.__signer.sign(message)


class PublicIdentityKey(object):
    def __init__(self, public_bytes=None, key_string=None):
        assert (public_bytes and not key_string) or (not public_bytes and key_string), \
            "Only provide one of public_bytes or key_string, not both"

        if key_string:
            if not is_valid_idpub(key_string):
                raise BadKeyStringError()
            decoded = base58.decode(key_string)
            public_bytes = decoded[IDKEY_PREFIX_LENGTH:IDKEY_BODY_LENGTH]

        assert isinstance(public_bytes, bytes)
        assert len(public_bytes) == 32
        self.__verifier = ed25519.VerifyingKey(public_bytes)

    def to_bytes(self):
        '''Returns the 32 byte raw public key'''
        return self.__verifier.to_bytes()

    def to_string(self):
        '''Returns the key as a human-readable string in idpub format'''
        public_body = IDPUB_PREFIX + self.to_bytes()
        return to_string(public_body)

    def verify(self, signature, message):
        '''Returns True if this key successfully verifies the signature for the given message'''
        try:
            self.__verifier.verify(signature, message)
            return True
        except ed25519.BadSignatureError:
            return False
