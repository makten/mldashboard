import configparser
import os
from ucsmsdk.ucshandle import UcsHandle


host = "ucs"

def ucs_login():
    config = configparser.RawConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '..', 'ucs_manager', 'connection.cfg'))

    hostname = config.get(host, "hostname")
    username = config.get(host, "username")
    password = config.get(host, "password")
    # port = config.get(host, "port")

    handle = UcsHandle(hostname, username, password)

    print(handle)
    handle.login()
    return handle


def ucs_logout(handle):
    handle.logout()