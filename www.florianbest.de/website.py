# -*- coding: utf-8 -*-

from __future__ import absolute_import

import base64
import datetime
import smtplib
import psutil
from email.mime.text import MIMEText

from httoop import FOUND, URI, UNAUTHORIZED
from httoop.status import UNPROCESSABLE_ENTITY
from circuits.http.server.resource import method
from circuits.http.server.content import ContentType, Security
from circuits.http.events import response
from circuits import handler

from .base import Resource, _Resource
from .ip2country import Ip2CountryResolver


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


def image(string, image):
	class String(unicode):
		pass

	string = String(string)
	string.image = image
	return string


class Header(Resource):
	"""This resource shows us the HTTP request headers and the querystring parameters."""
	path = '/header'

	ISP = {
		'alicedsl.de': 'Alice',
		'aol.com': 'AOL',
		'einsundeins.de': '1&1',
		'pools.arcor-ip.net': 'Arcor',
		't-dialin.net': 'Telekom',
		't-ipconnect.de': 'Telekom',
		'vodafone.de': 'Vodafone',
		'd1-online.com': 'T-Mobile',
		'superkabel.de': 'Kabel Deutschland',
		'kabel-deutschland.de': 'Kabel Deutschland',
		'ewe-ip-backbone.de': 'EWE TEL',
		'pppool.de': 'Freenet',
		'hosteurope.de': 'Host Europe',
		'kabelbw.de': 'Kabel BW',
		'ish.de': 'Unitymedia',
		'unitymediagroup.de': 'Unitymedia',
		'mediaways.net': 'Telefonica',
		'mnet-online.de': 'M-net',
		'netcologne.de': 'NetCologne',
		'osnanet.de': 'osnatel',
		'qsc.de': 'QSC',
		'sat-kabel-online.de': 'Sat-Kabel',
		'versanet.de': 'Versatel',
		'viaginterkom.de': 'ViagInterkom',
	}
	OS = {
		'windows': 'Windows',
		'NT 4.0': 'Windows NT',
		'NT 5.0': 'Windows 2000',
		'NT 5.1': 'Windows XP',
		'NT 6.0': 'Windows Vista',
		'NT 6.1': 'Windows 7',
		'NT 6.2': 'Windows 8',
		'NT 10': 'Windows 10',
		'Windows NT': 'Windows',
		'linux': 'Linux',
		'ubuntu': 'Ubuntu',
		'suse': 'Suse Linux',
		'debian': 'Debian',
		'gentoo': 'Gentoo',
		'mint': 'Linux-Mint',
		'archlinux': 'Archlinux',
		'fedora': 'Fedora',
		'backtrack': 'Backtrack',
		'unix': 'Unix',
		'jvm': 'JVM',
		'freebsd': 'FreeBSD',
		'bsd': 'BSD',
		'mac os': 'Mac OS',
		'solaris': 'Solaris',
		'sunos': 'SunOS',
		'irix': 'IRIX',
		'amiga os': 'Amiga OS',
		'openvms': 'OpenVMS',
		'beos': 'BeOS',
		'symbian os': 'Symbian OS',
		'palm os': 'Palm OS',
		'playstation': 'PlayStation Portable',
		'os/2': 'OS/2',
	}

	BROWSER = {
		'opera': 'Opera',
		'chromium': 'Chromium',
		'chrome': 'Google-Chrome',
		'Firefox/': 'Mozilla Firefox',
		'Trident/7.0': 'Internet Explorer 11',
		'MSIE 10': 'Internet Explorer 10',
		'MSIE 9': 'Internet Explorer 9',
		'MSIE 8': 'Internet Explorer 8',
		'MSIE 7': 'Internet Explorer 7',
		'MSIE 6': 'Internet Explorer 6',
		'MSIE 5': 'Internet Explorer 5',
		'MSIE': 'Internet Explorer',
		'Trident': 'Internet Explorer',
		'safari': 'Safari',
		'lynx': 'Lynx',
		'konqueror': 'Konqueror',
		'mozilla': 'Mozilla',
		'w3m': 'w3m',
		'curl': 'cURL',
	}

	def init(self, *args, **kwargs):
		self.ip2country = Ip2CountryResolver()

	@method
	def GET(self, client):
		headers = dict(client.request.headers.items())
		for authorization in ('Cookie', 'Authorization', 'Proxy-Authorization'):
			if authorization in headers:
				headers[authorization] = '***'
		for key in headers.keys():
			if key.startswith('X-Forwarded-') or key == 'Forwarded':
				headers.pop(key)

		country = self.ip2country.get_country(client.remote.ip)
		infos = [
			('Internet Service Provider', self.get_isp(client)),
			('Operating System', self.get_operating_system(client)),
			('Browser', self.get_browser(client)),
			('Country', image(country.country, 'country/%s' % (country.country_code,))),
			('Language', [image(lang.value, 'country/%s' % lang.value.split('-')[-1]) for lang in client.request.headers.elements('Accept-Language') if '-' in lang.value]),
			('Username', client.user.username),
			('IP-Address', client.remote.ip),
			('Hostname', client.remote.name),
			('Secure connection', client.server.secure),
			('Transport protocol', client.request.uri.scheme),
		]
		infos = [info for info in infos if info[1]]
		# TODO: add number of SQL queries
		# TODO: add site statistics: online atm, visitor total, visitor today, visitor yesterday, online today, online total

		memory = psutil.virtual_memory()
		server = [
			('WSGI', None),  # TODO
			('CPU Usage', '%s%%' % (psutil.cpu_percent(),)),
			('RAM Usage', '%s%%' % (memory.percent,)),
			('RAM Total', '%s MiB' % (memory.total / 1024 / 1024,)),
			('RAM Used', '%s MiB' % (memory.used / 1024 / 1024,)),
			('RAM Free', '%s MiB' % (memory.free / 1024 / 1024,)),
		]
		server = [info for info in server if info[1]]

		return dict(
			infos=infos,
			server=server,
			headers=sorted(headers.items()),
			params=dict(client.request.uri.query).items()
		)
	GET.codec('application/json', 0.9)

	def get_operating_system(self, client):
		ops = [
			'NT 4.0', 'NT 5.0', 'NT 5.1', 'NT 6.0', 'NT 6.1', 'NT 6.2', 'NT 10', 'Windows NT',  # Windows
			'ubuntu', 'suse', 'debian', 'gentoo', 'mint', 'archlinux', 'fedora', 'backtrack', 'linux',  # Linux
			'unix', 'jvm', 'freebsd', 'bsd', 'mac os', 'solaris', 'sunos', 'irix', 'amiga os', 'openvms', 'beos', 'symbian OS',
			'palm os', 'playstation', 'os/2', 'RISK OS', 'Nintendo', 'HP-UX', 'AIX', 'Plan 9', 'RIM OS', 'QNX', 'MorphOS', 'NetWare',
			'SCO', 'SkyOS', 'iPhone OS', 'Haiku OS', 'DangerOS', 'Syllable',
		]
		user_agent = client.request.headers.get('User-Agent', '').lower()
		for op in ops:
			if op.lower() in user_agent:
				return image(self.OS.get(op, op), 'client/%s' % op)

	def get_isp(self, client):
		isps = [
			'alicedsl.de', 'aol.com', 'einsundeins.de', 'pools.arcor-ip.net', 't-dialin.net', 't-ipconnect.de', 'vodafone.de', 'kabel-deutschland.de',
			'd1-online.com', 'superkabel.de', 'ewe-ip-backbone.de', 'pppool.de', 'hosteurope.de', 'kabelbw.de', 'ish.de', 'unitymediagroup.de',
			'mediaways.net', 'mnet-online.de', 'netcologne.de', 'osnanet.de', 'qsc.de', 'sat-kabel-online.de', 'versanet.de', 'viaginterkom.de',
		]
		hostname = client.remote.name
		for isp in isps:
			if isp in hostname:
				return image(self.ISP.get(isp, isp), 'client/%s' % isp)

	def get_browser(self, client):
		browsers = [
			'Firefox/',
			'MSIE 10', 'MSIE 9', 'MSIE 8', 'MSIE 7', 'MSIE 6', 'MSIE 5', 'MSIE', 'Trident/7.0', 'Trident',
			'chrome',
			'opera',
			'chromium',
			'safari',
			'lynx',
			'links',
			'konqueror',
			'mozilla',
			'w3m',
			'seamonkey',
			'curl',
		]
		user_agent = client.request.headers.get('User-Agent', '').lower()
		for browser in browsers:
			if browser.lower() in user_agent:
				return image(self.BROWSER.get(browser, browser), 'client/%s' % browser.replace('/', ''))

	def get_rendering_engine(self, client):
		engines = [
			'Gecko',  # Mozilla, Firefox
			'WebKit',  # Safari, Chromium, Google-Chrome
			'Presto',  # Opera
			'Trident',  # MS, IE
			'KHTML',
			'Tasman',
			'Robin',
			'Links',
			'Lynx',
		]
		user_agent = client.request.headers.get('User-Agent', '')
		for engine in engines:
			if engine in user_agent:
				return engine


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
