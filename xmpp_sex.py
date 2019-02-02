#!/usr/bin/env python
import os
from nacl.public import PrivateKey, PublicKey, Box
import nacl


PUBKEY_FILE = '{jid}.pubkey'
SECKEY_FILE = '{jid}.seckey'

class XMMPPSex():
	def __init__(self, jid):
		self.jid = jid
		self.pk = {}
		if os.path.isfile(SECKEY_FILE.format(jid=jid)):
			print("Reading secret key for {} from file.".format(jid))
			with open(SECKEY_FILE.format(jid=jid), 'rb') as f:
				self.sk = PrivateKey(nacl.encoding.URLSafeBase64Encoder.decode(f.read()))
		else:
			print("Generating new secret key for {} and writing it to file.".format(jid))
			self.sk = PrivateKey.generate()
			with open(SECKEY_FILE.format(jid=jid), 'wb') as f:
				f.write(self.sk.encode(encoder=nacl.encoding.URLSafeBase64Encoder))

		if not os.path.isfile(PUBKEY_FILE.format(jid=jid)):
			print("Writing public key for {} to file.".format(jid))
			with open(PUBKEY_FILE.format(jid=jid), 'wb') as f:
				f.write(self.sk.public_key.encode(encoder=nacl.encoding.URLSafeBase64Encoder))

	def addPubkey(self, jid):
		print("Adding public key for {} from file.".format(jid))
		with open(PUBKEY_FILE.format(jid=jid), 'rb') as f:
			self.pk[jid] = PublicKey(nacl.encoding.URLSafeBase64Encoder.decode(f.read()))

	def encryptTo(self, jid, message):
		if not jid in self.pk:
			self.addPubkey(jid)
		box = Box(self.sk, self.pk[jid])
		nonce = nacl.utils.random(Box.NONCE_SIZE)
		return (nacl.encoding.URLSafeBase64Encoder.encode(nonce).decode('utf-8'),
			box.encrypt(message.encode('utf-8'), nonce, nacl.encoding.URLSafeBase64Encoder).ciphertext.decode('utf-8'))

	def decryptFrom(self, jid, message, nonce):
		if not jid in self.pk:
			self.addPubkey(jid)
		box = Box(self.sk, self.pk[jid])
		return box.decrypt(message,
			nacl.encoding.URLSafeBase64Encoder.decode(nonce),
			nacl.encoding.URLSafeBase64Encoder).decode('utf-8')
