import unittest

import identitykeys


class TestIdentityKeys(unittest.TestCase):

    def test_generate_key_pair(self):
        private_key, public_key = identitykeys.generate_key_pair()
        assert isinstance(private_key, identitykeys.PrivateIdentityKey)
        assert isinstance(public_key, identitykeys.PublicIdentityKey)

    def test_key_string_validity_checkers(self):
        # Valid pair. All zeros private key
        private = 'idsec19zBQP2RjHg8Cb8xH2XHzhsB1a6ZkB23cbS21NSyH9pDbzhnN6'
        public = 'idpub2Cy86teq57qaxHyqLA8jHwe5JqqCvL1HGH4cKRcwSTbymTTh5n'
        assert identitykeys.is_valid_idsec(private)
        assert identitykeys.is_valid_idpub(public)

        # Bad prefix
        private = 'Xdsec19zBQP2RjHg8Cb8xH2XHzhsB1a6ZkB23cbS21NSyH9pDbzhnN6'
        public = 'Xdpub2Cy86teq57qaxHyqLA8jHwe5JqqCvL1HGH4cKRcwSTbymTTh5n'
        assert not identitykeys.is_valid_idsec(private)
        assert not identitykeys.is_valid_idpub(public)

        # Bad body
        private = 'idsec19zBQP2RjHg8CbXXXXXHzhsB1a6ZkB23cbS21NSyH9pDbzhnN6'
        public =  'idpub2Cy86teq57qaxHXXXXXjHwe5JqqCvL1HGH4cKRcwSTbymTTh5n'
        assert not identitykeys.is_valid_idsec(private)
        assert not identitykeys.is_valid_idpub(public)

        # Bad checksums
        private = 'idsec19zBQP2RjHg8Cb8xH2XHzhsB1a6ZkB23cbS21NSyH9pDbzhnNX'
        public = 'idpub2Cy86teq57qaxHyqLA8jHwe5JqqCvL1HGH4cKRcwSTbymTTh5X'
        assert not identitykeys.is_valid_idsec(private)
        assert not identitykeys.is_valid_idpub(public)

    def test_key_imports_and_exports(self):
        private_bytes = b'\0' * 32
        private_string = 'idsec19zBQP2RjHg8Cb8xH2XHzhsB1a6ZkB23cbS21NSyH9pDbzhnN6'
        public_string = 'idpub2Cy86teq57qaxHyqLA8jHwe5JqqCvL1HGH4cKRcwSTbymTTh5n'

        private_from_bytes = identitykeys.PrivateIdentityKey(seed_bytes=private_bytes)
        private_from_string = identitykeys.PrivateIdentityKey(key_string=private_string)
        assert private_from_bytes.to_bytes() == private_bytes
        assert private_from_string.to_bytes() == private_bytes
        assert private_from_bytes.to_string() == private_string
        assert private_from_string.to_string() == private_string

        public_from_private = private_from_string.get_public_key()
        public_from_string = identitykeys.PublicIdentityKey(key_string=public_string)
        assert public_from_private.to_bytes() == public_from_string.to_bytes()
        assert public_from_private.to_string() == public_string
        assert public_from_string.to_string() == public_string


if __name__ == '__main__':
    unittest.main()
