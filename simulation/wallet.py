"""Wallet = public/private key pair (Ed25519 digital signatures)."""
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization as ser


class Wallet:
    def __init__(self):
        self._key = Ed25519PrivateKey.generate()
        self.pub = self._key.public_key().public_bytes(
            ser.Encoding.Raw, ser.PublicFormat.Raw).hex()   # voter address / identity

    def sign(self, message: str) -> str:
        return self._key.sign(message.encode()).hex()


def verify(pub_hex: str, message: str, sig_hex: str) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex)).verify(
            bytes.fromhex(sig_hex), message.encode())
        return True
    except Exception:
        return False
