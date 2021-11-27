from creds import creds
from zenpy import Zenpy

zenpy_client = Zenpy(**creds)

for ticket in zenpy_client.search(type='ticket'):
    print(ticket)