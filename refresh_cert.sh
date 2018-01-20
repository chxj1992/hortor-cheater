#!/bin/bash

# see mitmproxy docs to learn more. http://docs.mitmproxy.org/en/latest/certinstall.html?highlight=cert

rm cert.*

openssl genrsa -out cert.key 2048

openssl req -new -x509 -key cert.key -out cert.crt

cat cert.key cert.crt > cert.pem
