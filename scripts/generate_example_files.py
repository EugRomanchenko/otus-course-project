from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_self_signed_cert(
        not_valid_before: datetime,
        not_valid_after: datetime,
        cert_filename: str,
        key_filename: str,
):
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend(),
    )

    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "example.com")
    ])
    alt_names = [x509.DNSName("example.net")]
    san = x509.SubjectAlternativeName(alt_names)
    basic_constraints = x509.BasicConstraints(ca=True, path_length=0)

    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(1000)
        .not_valid_before(not_valid_before)
        .not_valid_after(not_valid_after)
        .add_extension(basic_constraints, False)
        .add_extension(san, False)
        .sign(key, hashes.SHA512(), default_backend())
    )
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.DER)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(f"{cert_filename}.cer", "wb") as f:
        f.write(cert_pem)
    with open(f"{key_filename}.key", "wb") as f:
        f.write(key_pem)


generate_self_signed_cert(
    not_valid_before=datetime.utcnow() - timedelta(days=5),
    not_valid_after=datetime.utcnow() - timedelta(days=2),
    cert_filename="cert_expired",
    key_filename="key_expired",
)

generate_self_signed_cert(
    not_valid_before=datetime.utcnow(),
    not_valid_after=datetime.utcnow() + timedelta(days=20),
    cert_filename="cert_expired_20days",
    key_filename="key_expired_20days",
)

generate_self_signed_cert(
    not_valid_before=datetime.utcnow(),
    not_valid_after=datetime.utcnow() + timedelta(days=120),
    cert_filename="cert_not_expired",
    key_filename="key_not_expired",
)
