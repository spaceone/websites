# -*- coding: utf-8 -*-

import sys
import os
import importlib
from pprint import pprint
from ConfigParser import ConfigParser, NoSectionError

from httoop import ServerHeader
from circuits import handler
from circuits.http.server.__main__ import HTTPServer


class Server(HTTPServer):

	logformat = '%(h)s %(l)s %(u)s %(t)s %(s)s "%(r)s" "%(H)s" %(b)s "%(f)s" "%(a)s"'

	def add_arguments(self):
		add = self.parser.add_argument

		add('-c', '--config', metavar='configuration file',
			help='Specifies an alternative per-user configuration file.')

		super(Server, self).add_arguments()

	def add_components(self):
		self.add_config()
		super(Server, self).add_components()
		self.add_domains()

	def add_config(self):
		self.config = ConfigParser()
		if self.arguments.config:
			self.config.read(self.arguments.config)

	def add_domains(self):
		try:
			domains = self.config.get('general', 'domains', '').split(',')
		except NoSectionError:
			return
		for domain in domains:
			path = self.config.get(domain, 'module')
			module = importlib.import_module(path)
			module.main(self, domain)

	@handler('response.complete', priority=-0.2)
	def _log_failed_responses(self, client):
		request = client.request
		response = client.response

		if response.status > 399:
			print((int(response.status), unicode(request.method), tuple(request.protocol), unicode(request.uri)))
			pprint(dict(request.headers))


if __name__ == '__main__':
	ServerHeader.value = 'circuits.http/1.0 %s' % (ServerHeader,)
	Server.main()
