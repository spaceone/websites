# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from ConfigParser import ConfigParser

from circuits import handler
from circuits.http.server.resource import Domain as _Domain
from circuits.http.events import request
from .website import Index, Header, Login, Logout, Contact, Favicon, HTTPError, CSPViolation
from .robots import Robots
from .cms import Page, Navigation
from .color import Color
from .static import JavaScript, CascadeStyleSheet, Images
from .db import create_engine, sessionmaker
from .saml import SAML


class Domain(_Domain):

	def __init__(self, *args, **kwargs):
		self.www_path = os.path.realpath(os.path.dirname(__file__))
		self.template_path = os.path.join(self.www_path, 'templates')
		self.static_path = os.path.join(self.www_path, 'files')

		self.config = ConfigParser()
		self.config.read(os.path.join(self.www_path, 'config.cfg'))

		super(Domain, self).__init__(*args, **kwargs)
		self.aliases.add(self.fqdn.replace('www.', ''))
		self.localedir = self.config.get('i18n', 'localedir')
		self.textdomain = self.config.get('i18n', 'textdomain')

		root = Index(channel='website-index')
		self += root
		root = self
		root += SAML(channel='website-saml')
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
		root += Contact(channel='website-contact')
		root += Navigation(channel='website-navigation')
		root += CSPViolation(channel='csp-violation')
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

	@handler('routing', priority=1.45)
	def _set_user(self, client):
		client.user = type('User', (object,), {'username': 'Guest', 'is_logged_in': False, 'is_guest': True})


def main(server, fqdn):
	server.domains += Domain(fqdn)
