# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from ConfigParser import ConfigParser

from circuits import handler
from circuits.http.server.resource import Domain as _Domain
from circuits.http.events import request
from .website import Index, Header, Login, Logout, Favicon, HTTPError
from .robots import Robots
from .cms import Page, Navigation
from .color import Color
from .static import JavaScript, CascadeStyleSheet, Images
from .db import create_engine, sessionmaker


class Domain(_Domain):

	def __init__(self, *args, **kwargs):
		self.www_path = os.path.realpath(os.path.dirname(__file__))
		self.template_path = os.path.join(self.www_path, 'templates')
		self.static_path = os.path.join(self.www_path, 'files')

		self.config = ConfigParser()
		self.config.read(os.path.join(self.www_path, 'config.cfg'))

		super(Domain, self).__init__(*args, **kwargs)
		self.aliases.add(self.fqdn.replace('www.', ''))

		root = Index(channel='website-index')
		self += root
		root = self
		root += Header(channel='website-header')
		root += Login(channel='website-login')
		root += Logout(channel='website-logout')
		root += Favicon(channel='website-favicon')
		root += Robots(channel='website-robots')
		root += Color(channel='website-layoutcolors')
		root += Page(channel='website-cms-page')
		root += JavaScript(channel='website-javascript')
		root += CascadeStyleSheet(channel='website-css')
		root += Images(channel='website-images')
		root += Navigation(channel='website-navigation')
		root += HTTPError(channel='%s.error' % (self.channel,))

	def init(self, *args, **kwargs):
		engine = create_engine(self.config.get('base', 'sql_uri'))
		engine.connect()
		self.session = sessionmaker(bind=engine)()

	@handler('httperror')
	def _on_httperror(self, event, client, httperror):
		event.stop()
		client.response.status = httperror.status
		client.response.headers.update(httperror.headers)
		client.response.body = httperror.body
		self.fire(request(client), '%s.error' % (self.channel,))


def main(server, fqdn):
	server.domains += Domain(fqdn)
