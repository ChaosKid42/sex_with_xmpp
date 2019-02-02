#!/usr/bin/env python
import logging
import getpass
import ssl

from optparse import OptionParser

from sleekxmpp import ClientXMPP

from sleekxmpp.xmlstream import JID

from xmpp_sex import XMMPPSex

from box import Box

class SexRcv(ClientXMPP):
	def __init__(self, jid, password):
		ClientXMPP.__init__(self, jid, password)
		
		self.add_event_handler("session_start", self.session_start)
		self.add_event_handler("message", self.message)
		
		self.ssl_version = ssl.PROTOCOL_TLS

		self.xmppSex = XMMPPSex(jid)

	def session_start(self, event):
		self.send_presence()

	def message(self, msg):
		if msg['type'] in ('chat', 'normal'):
			print(msg)
			print("Body: {}".format(msg['body']))
			jid = JID(msg['from']).bare
			nonce = msg['box'].get_nonce()
			box = msg['box'].get_box()
			print("Nonce: {}".format(nonce))
			print("Box: {}".format(box))
			cleartext = self.xmppSex.decryptFrom(jid, box, nonce)
			print("Cleartext: {}\n".format(cleartext))

if __name__ == '__main__':
	optp = OptionParser()

	# Output verbosity options.
	optp.add_option('-q', '--quiet', help='set logging to ERROR',
					action='store_const', dest='loglevel',
					const=logging.ERROR, default=logging.INFO)
	optp.add_option('-d', '--debug', help='set logging to DEBUG',
					action='store_const', dest='loglevel',
					const=logging.DEBUG, default=logging.INFO)
	optp.add_option('-v', '--verbose', help='set logging to COMM',
					action='store_const', dest='loglevel',
					const=5, default=logging.INFO)

	# JID and password options.
	optp.add_option("-j", "--jid", dest="jid",
					help="JID to use")
	optp.add_option("-p", "--password", dest="password",
					help="password to use")

	opts, args = optp.parse_args()

	# Setup logging.
	logging.basicConfig(level=opts.loglevel,
						format='%(levelname)-8s %(message)s')

	if opts.jid is None:
		opts.jid = input("Username: ")
	if opts.password is None:
		opts.password = getpass.getpass("Password: ")



	xmpp = SexRcv(opts.jid, opts.password)
	xmpp.connect()
	xmpp.process(block=True)