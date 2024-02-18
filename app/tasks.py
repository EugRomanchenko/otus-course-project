from datetime import timedelta
import http.client
import logging
import json
import os

from db.engine import session_factory
from crud import find_expired_certificates, delete_expired_certificates, delete_certificate_by_fingerprint
from schemas import Certificate as CertificateSchema

logger = logging.getLogger(__name__)


async def print_expired_certificates():
    if os.path.isfile("expired_certificates_list.json"):
        os.remove('expired_certificates_list.json')
        print("file successfully deleted")
    session = session_factory
    async with session() as db:
        certificates = await find_expired_certificates(session=db, time_delta=timedelta(days=120))
        print(certificates)
        for cert in certificates:
            cert_model = CertificateSchema.model_validate(cert)
            body_message = cert_model.model_dump_json()
            with open('expired_certificates_list.json', 'a') as f:
                json.dump(body_message, f)

        if len(certificates) != 0:
            print("found expired certificates")
            with open('expired_certificates_list.json', 'r') as f:
                conn = http.client.HTTPConnection("eoie9djun83ed29.m.pipedream.net")
                conn.request("POST", "/", f.read(), {'Content-Type': 'application/json'})
                response = conn.getresponse()
                print(response.status, response.reason)
        else:
            print("No expired certificates found")


async def remove_expired_certificates():
    session = session_factory
    async with session() as db:
        await delete_expired_certificates(session=db, time_delta=timedelta(days=120))
