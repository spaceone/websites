# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os.path

from circuits.http.server.resource import StaticResource


class JavaScript(StaticResource):
	path = r'/js/{path:.*\.js}'

	def directory(self, client):
		return os.path.join(client.domain.static_path, 'js/')


class CascadeStyleSheet(StaticResource):
	path = r'/css/{path:.*\.css}'

	def directory(self, client):
		return os.path.join(client.domain.static_path, 'css/')


class Images(StaticResource):
	path = '/images/{path:.*}'

	def directory(self, client):
		return os.path.join(client.domain.static_path, 'images/')
