import hashlib

from cryptography import x509
from cryptography.hazmat.primitives import hashes


def parse_x509_der(file):
    cert = x509.load_der_x509_certificate(file)
    sha1 = bytearray(cert.fingerprint(hashes.SHA1())).hex()
    return {
        "generate_date": cert.not_valid_before_utc,
        "expiration_date": cert.not_valid_after_utc,
        "fingerpint": sha1
    }