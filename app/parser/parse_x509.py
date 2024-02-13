import hashlib

from cryptography import x509
from cryptography.hazmat.primitives import hashes


def parse_x509_der(file):
    cert = x509.load_der_x509_certificate(file)
    serial_number = cert.serial_number
    issuer = cert.issuer.rfc4514_string()
    subject = cert.subject.rfc4514_string()
    sha1 = bytearray(cert.fingerprint(hashes.SHA1())).hex()
    return {
        "created_at": cert.not_valid_before_utc,
        "expired_at": cert.not_valid_after_utc,
        "fingerprint_sha1": sha1,
        "serial_number": serial_number,
        "issuer": issuer,
        "subject": subject,
    }
