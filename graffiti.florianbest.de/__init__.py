# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from circuits.http.server.resource import Domain as _Domain

from .website import Graffiti, Kunstwerke, Images, Workshopangebot, Zeitungsartikel, Kontakt, Robots


class Domain(_Domain):

	def __init__(self, *args, **kwargs):
		super(Domain, self).__init__(*args, **kwargs)

		self.www_path = os.path.realpath(os.path.dirname(__file__))
		self.template_path = os.path.join(self.www_path, 'templates')
		self.static_path = os.path.join(self.www_path, 'files')
		#self.localedir = self.config.get('i18n', 'localedir')
		#self.textdomain = self.config.get('i18n', 'textdomain')

		root = Graffiti(channel='graffiti')
		self += root
		root = self
		root += Kunstwerke(channel='graffiti-artwork')
		root += Images(channel='graffiti-images')
		root += Workshopangebot(channel='graffiti-workshop')
		root += Zeitungsartikel(channel='graffiti-zeitungsartikel')
		root += Kontakt(channel='graffiti-kontakt')
		root += Robots(channel='graffiti-robots')


def main(server, fqdn):
	server.domains += Domain(fqdn)
