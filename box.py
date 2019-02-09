#!/usr/bin/env python

from sleekxmpp.xmlstream import ElementBase
from sleekxmpp.xmlstream import register_stanza_plugin
from sleekxmpp.stanza import Message

class Box(ElementBase):
	namespace = 'urn:xmpp:sex:0'
	name = 'box'
	plugin_attrib = 'box'
	interfaces = set('nonce')

	def set_nonce(self, value):
		self._set_attr('nonce', str(value))

	def get_nonce(self):
		return self._get_attr('nonce')

	def get_box(self):
		return self.xml.text

	def set_box(self, value):
		self.xml.text = value

	def del_box(self):
		self.xml.text = ''


register_stanza_plugin(Message, Box)