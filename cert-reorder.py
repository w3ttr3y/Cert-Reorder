#!/usr/bin/env python

#!/opt/splunk/bin/python

import argparse
import logging
import sys
import OpenSSL

def buildParser():
    parser = argparse.ArgumentParser(description='Manipulate the order of certificates in a pem style file')
    parser.add_argument('file', type=argparse.FileType('r'), default='-', nargs="?")
    action = parser.add_mutually_exclusive_group()
    action.add_argument('-r', '--reverse', dest='action', action='store_const',
                   const=reverse, default=interactive, help='Reverse the order of certificates.')
    action.add_argument('-p', '--print', dest='action', action='store_const', const=print_cert_name, help="")
    action.add_argument('-a', '--auto', dest='action', action='store_const', const=auto, help='')
    return parser


class CertParser:
	def __init__(self):
		self._begin = "-----BEGIN CERTIFICATE-----"
		self._end   = "-----END CERTIFICATE-----"

	def _get_lines(self, file):
		return [line.strip() for line in file.readlines()]
	
	def _get_certificates(self, lines):
		start=None
		end=None
		certs = []
		for i in range(len(lines)):
			if start == None:
				if lines[i] == self._begin:
					start = i
					continue
			elif end == None:
				if lines[i] != self._end:
					continue
				end = i
				certs.append(lines[start:end+1])
				start, end = None, None
		return certs

	def parse(self, file):
		content = self._get_lines(file)
		certs = ["\n".join(x) for x in self._get_certificates(content)]
		return certs

	def get_common_name(self, cert):
		return OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert).get_subject().commonName
		

def reverse(certs):
	certs.reverse()
	print asChain(certs)

def print_cert_name(certs):
	p = CertParser()
	for cert in certs:
		print p.get_common_name(cert)

def asChain(certs):
	return "\n".join(certs)

def find_root(certs):
	for (i, cert) in enumerate(certs):
		if cert['cert'].get_issuer().commonName == cert['cert'].get_subject().commonName:
			del certs[i]
			return cert

def parse(certs):
	x = []
	for cert in certs:
		x.append({
			'text': cert,
			'cert': OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)})
	return x

def add_next(pcerts, certs):
	parent = pcerts['cert'].get_subject().commonName
	for(i, cert) in enumerate(certs):
		if cert['cert'].get_issuer().commonName == parent:
			del certs[i]
			return cert
	return None

def auto(certs):
	certs = parse(certs)
	chain = []
	chain.insert(0, find_root(certs))
	while True:
		next = add_next(chain[0], certs)
		if next == None:
			break
		chain.insert(0, next)
	chain = [c['text'] for c in chain ]
	print asChain(chain)

def interactive(certs):
	print "Not yet implemented"

if __name__ == '__main__':
	args = buildParser().parse_args()
	args.action(CertParser().parse(args.file))
