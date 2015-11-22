# -*- coding: utf-8 -*-

from __future__ import absolute_import

import base64

from httoop import FOUND, URI, UNAUTHORIZED
from circuits.http.server.resource import method
from circuits.http.events import response
from circuits import handler

from .base import Resource, _Resource


class Index(Resource):
	"""This resource is an example index page for the webserver."""
	path = '/'

	@method
	def GET(self, client, _):
		return dict(
			content=_('Hello World!'),
			username=client.user.username,
			ip=client.remote.ip,
			hostname=client.remote.name,
			secure_connection=client.server.secure
		)


class HTTPError(Resource):

#	default_features = []

	def template_name(self, client):
		return 'error.tpl'

	def identify(self, client):
		return

	@method
	def GET(self, client):
		return client.response.body.data
	GET.codec('application/json', 0.9)

	@handler('httperror', priority=2)
	def _on_httperror(self, event, client, httperror):
		event.stop()

	@handler('request', priority=2)
	def _on_request(self, client):
		client.resource = self
		self.methods[client.request.method] = client.method = self.GET
		client.request.headers.append('Accept', '*/*; q=0.1')

	def content_type(self, client):
		return super(HTTPError, self).content_type(client) or client.method.available_mimetypes[0]

	@handler('request_success')
	def _on_request_done(self, evt, value):
		client = evt.args[0]
		self.fire(response(client), client.server.channel)


class Header(Resource):
	"""This resource shows us the HTTP request headers and the querystring parameters."""
	path = '/header'

	@method
	def GET(self, client):
		headers = dict(client.request.headers.items())
		for authorization in ('Authorization', 'Proxy-Authorization'):
			if authorization in headers:
				headers[authorization] = '***'

		return dict(headers=headers.items(), params=dict(client.request.uri.query).items())


# TODO: JSLoginForm
class Login(Resource):
	"""This resource always sends a HTTP UNAUTHORIZED if the client did not provide
		an WWW-Authenticate header.
	"""
	path = '/login'

	def _require_authentication(client):
		if client.user.is_guest:
			raise UNAUTHORIZED('basic realm="%s"' % (client.domain.fqdn,))  # TODO: implement some component for this
		return True

	@method
	def GET(self, client, _):
		return _('Welcome %s, you are logged in.') % client.user.username
	GET.conditions(_require_authentication)


class Logout(Resource):
	"""This resource is a workaround for web browsers which does not support to drop
		the credentials which they stored.
		We are redirecting the user to logout@domain.
	"""
	path = '/logout'

	@method
	def GET(self, client, _):
		if client.user.is_guest:
			return dict(content=_('You are already logged out ;)'))
		location = URI(client.request.uri)
		location.username = 'logout'
		location.path = '/'  # FIXME: chromium bug client.request.uri.path
		raise FOUND(str(location), _('Logging out... Please follow the redirection: %s.') % location)


class Favicon(_Resource):

	path = '/favicon.ico'

	@method
	def GET(self, client, color='white'):
		data = b'AAABAAEAAQEAAAEAIAAwAAAAFgAAACgAAAABAAAAAgAAAAEAIAAAAAAA'\
				'BAAAAAAAAAAAAAAAAAAA\nAAAAAAD/////AAAAAA=='
		data = base64.decodestring(data)
		data = list(data)
		if color == 'green':
			data[62:65] = '\x00\x80\x00'
		elif color == 'blue':
			data[63:65] = '\x00\x00'
		elif color == 'yellow':
			data[62] = '\x00'
		elif color == 'red':
			data[62:64] = '\x00\x00'
		elif color == 'black':
			data[62:65] = '\x00\x00\x00'
		return b''.join(data)

	@GET.codec('image/x-icon')
	def _image_icon(self, client):
		return client.data
