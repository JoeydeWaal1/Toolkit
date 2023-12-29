import ssl, socket
import os

from log import log_init, log_json

fields = ["hostname","subject","issuer","serialNumber","notAfter","notBefore","version","cert"]


def scan_cert(host: str):
    log_init("scanning " + host)

    result = get_cert_details(host)
    log_json(result)


def get_cert_details(myhostname: str, port=443):
    myctx = ssl.create_default_context()
    myctx.check_hostname = False
    myctx.verify_mode = ssl.CERT_NONE

    s = myctx.wrap_socket(socket.socket(), server_hostname=myhostname)
    s.connect((myhostname, port))
    bcert = s.getpeercert(binary_form=True)
    cert = ssl.DER_cert_to_PEM_cert(bcert)

    cert_dict = decode_cert_PEM(cert)

    result = {
        "subject":      dict(x[0] for x in cert_dict["subject"]),
        "issuer":       dict(x[0] for x in cert_dict["issuer"]),
        "serialNumber": cert_dict["serialNumber"],
        "notAfter":     cert_dict["notAfter"],
        "notBefore":    cert_dict["notBefore"],
        "version":      cert_dict["version"],
        "cert":         ssl.get_server_certificate((myhostname, port)).replace("\n", ""),
        "hostname":     myhostname
    }
    return result

def decode_cert_PEM(cert):
    f = open('mycert.pem','w')
    f.write(cert)
    f.close()
    cert_dict = ssl._ssl._test_decode_cert('mycert.pem')
    os.remove('mycert.pem')
    return cert_dict
