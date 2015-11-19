# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from ConfigParser import ConfigParser

from circuits.http.server.resource import Domain as _Domain
from .website import Index, Header, Login, Logout, Favicon
from .robots import Robots
#from .cms import Page, Navigation
from .color import Color
from .static import JavaScript, CascadeStyleSheet, Images


class Domain(_Domain):

	def __init__(self, *args, **kwargs):
		super(Domain, self).__init__(*args, **kwargs)
		self.aliases.add(self.fqdn.replace('www.', ''))

		self.www_path = os.path.realpath(os.path.dirname(__file__))
		self.template_path = os.path.join(self.www_path, 'templates')
		self.static_path = os.path.join(self.www_path, 'files')

		self.config = ConfigParser()
		self.config.read(os.path.join(self.www_path, 'config.cfg'))

		root = Index(channel='website-index')
		self += root
		root = self
		root += Header(channel='website-header')
		root += Login(channel='website-login')
		root += Logout(channel='website-logout')
		root += Favicon(channel='website-favicon')
		root += Robots(channel='website-robots')
		root += Color(channel='website-layoutcolors')
#		root += Page(channel='website-cms-page')
		root += JavaScript(channel='website-javascript')
		root += CascadeStyleSheet(channel='website-css')
		root += Images(channel='website-images')
#		root += Navigation(channel='website-navigation')
#		root += (channel='website-')


def main(server, fqdn):
	server.domains += Domain(fqdn)
