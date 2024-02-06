import hashlib

from cryptography import x509
from cryptography.hazmat.primitives import hashes


def parse_x509_der(file):
    cert = x509.load_der_x509_certificate(file)
    sha1 = bytearray(cert.fingerprint(hashes.SHA1())).hex()
    return {
        "created_at": cert.not_valid_before_utc,
        "expired_at": cert.not_valid_after_utc,
        "fingerpint_sha1": sha1
    }
