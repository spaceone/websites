# -*- coding: utf-8 -*-

from __future__ import absolute_import

import base64
import datetime
import smtplib
from email.mime.text import MIMEText

from httoop import FOUND, URI, UNAUTHORIZED
from httoop.status import UNPROCESSABLE_ENTITY
from circuits.http.server.resource import method
from circuits.http.server.content import ContentType, Security
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
	GET.codec('application/json', 0.9)


class HTTPError(Resource):

	default_features = [ContentType, Security]

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
#		client.request.headers.append('Accept', '*/*; q=0.1')

	def content_type(self, client):
		return super(HTTPError, self).content_type(client) or client.method.available_mimetypes[0]

	@handler('request_success', priority=2)
	def _on_request_done(self, event, evt, value):
		# TODO: understand this again
		if event.stopped:
			return
		event.stop()
		client = evt.args[0]
		self.fire(response(client), client.server.channel)


class Header(Resource):
	"""This resource shows us the HTTP request headers and the querystring parameters."""
	path = '/header'

	@method
	def GET(self, client):
		headers = dict(client.request.headers.items())
		for authorization in ('Cookie', 'Authorization', 'Proxy-Authorization'):
			if authorization in headers:
				headers[authorization] = '***'

		infos = [
			('Username', client.user.username),
			('IP-Address', client.remote.ip),
			('Hostname', client.remote.name),
			('Secure connection', client.server.secure),
		]
		# TODO: add used / free / total space, RAM, CPU usage
		# TODO: add number of SQL queries
		# TODO: add WSGI info
		# TODO: add screen resolution: document.write(screen.width + 'x' + screen.height);
		# TODO: add Country, OS, Browser, Provider (as images)
		# TODO: add site statistics: online atm, visitor total, visitor today, visitor yesterday, online today, online total

		return dict(
			infos=infos,
			headers=sorted(headers.items()),
			params=dict(client.request.uri.query).items()
		)
	GET.codec('application/json', 0.9)


class Contact(Resource):

	path = '/contact/'

	@method
	def GET(self, client):
		return {}

	@method
	def POST(self, client):
		def escape(s):
			return repr(s).lstrip('u')[1:-1]

		default_sender = unicode(client.domain.config.get('contact', 'sender_address'))
		receiver = unicode(client.domain.config.get('contact', 'receive_address'))
		data = {}
		for key, val in dict(client.request.body.data).items():
			if isinstance(val, unicode):
				val = val.encode('latin-1', 'replace').decode('utf-8', 'replace')
			data[key] = val
		data.setdefault('copy', False)
		copy = data['copy'] == 'on'
		subject = escape(data.get('subject', u''))
		sender = escape(data.get('from', default_sender))
		if u'@' not in sender:
			copy = False
			sender = default_sender
		if data.get('name') and '<' not in data['name'] and '>' not in data['name']:
			sender = u'%s <%s>' % (escape(data['name']), sender)
			sender = sender.replace(u',', '')

		text = u'''Contact form:
%s %s <%s> wrote a message via the contact form.
Website: %s
Copy: %s
Subject: %s
HTTP-Request: %s
IP-Address: %s
Hostname: %s
Date: %s
Message: %s
		'''
		try:
			text = text % (
				data['title'], data['name'], data['from'], data['website'], data['copy'],
				data['subject'], '\n'.join('%s: %s' % (escape(key), escape(val)) for key, val in client.request.headers.items()), client.remote.ip,
				client.remote.name, datetime.datetime.now().isoformat(), data['message']
			)
		except KeyError as exc:
			raise UNPROCESSABLE_ENTITY('Missing field: %r' % (str(exc),))

		message = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
		message['From'] = sender
		message['To'] = receiver
		message['Subject'] = subject
		if copy:
			message['CC'] = sender

		connection = smtplib.SMTP('localhost')
		connection.sendmail(sender, [receiver], message.as_string())
		connection.quit()
	POST.accept('application/x-www-form-urlencoded')


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


class CSPViolation(_Resource):

	path = '/csp-violation'

	@method
	def GET(self, client):
		client.response.status = 204

	@method
	def POST(self, client):
		print client.request.body
