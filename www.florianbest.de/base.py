# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys
import inspect

from genshi.template import TemplateLoader, TemplateNotFound, TemplateSyntaxError
from genshi.filters import Translator

from httoop import INTERNAL_SERVER_ERROR
from circuits.http.utils import httphandler
from circuits.http.server.resource import Resource as BaseResource
from circuits.http.server.i18n.gettext import GettextResource
from circuits.http.server.i18n.content_language import ContentLanguage

from .config import config

try:
	unicode
except NameError:
	unicode = str


class websiteproperty(property):

	def __init__(self, fget, *a, **kw):
		self.name = kw.pop('name', fget.__name__.replace('website_', ''))
		property.__init__(self, fget, *a, **kw)


class _Resource(GettextResource, BaseResource):

	default_features = BaseResource.default_features + [ContentLanguage]

	def frame_options(self, client):
		return 'DENY'

	def xss_protection(self, client):
		return '1; mode=block'

	def content_type_options(self, client):
		return 'nosniff'

	def strict_transport_security(self, client):
		return 'max-age=16070400; includeSubDomains'

	def content_security_policy(self, client):
		return "default-src 'self'; script-src 'self' 'unsafe-inline'; object-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self'; media-src 'self'; frame-src 'self'; font-src 'none'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; report-uri /csp-violation;"

	def permitted_cross_domain_policies(self, client):
		return 'master-only'

	def cache_control(self, client):
		return 'no-cache, no-store, must-revalidate'

	def pragma(self, client):
		return 'no-cache'

	def expires(self, client):
		return '-1'

	def content_encoding(self, client):
		for encoding in client.request.headers.elements('Accept-Encoding'):
			if encoding.value in ('gzip', 'deflate'):
				return encoding.value

	def textdomain(self, client):
		return client.domain.textdomain

	def keyword_arguments(self, client):
		kwargs = super(_Resource, self).keyword_arguments(client)
		argspec = inspect.getargspec(client.method.method)
		if '_' in argspec.args:
			try:
				kwargs['_'] = client.translation.ugettext
			except AttributeError:  # Python 3
				kwargs['_'] = client.translation.gettext
		if argspec.keywords:
			kw = dict(client.request.uri.query)
			kw.update(kwargs)
			kwargs = kw

		for name, value in client.path_segments.items():
			if name in argspec.args:
				kwargs[name] = value

		return kwargs


class Resource(_Resource):

	loaders = dict()
	config = dict()

	def __init__(self, *args, **kwargs):
		super(Resource, self).__init__(*args, **kwargs)
		if not Resource.config:
			Resource.config = config()
		self.config = Resource.config.copy()

	def load(self, path):
		if path not in self.loaders:
			self.loaders[path] = TemplateLoader(path, auto_reload=True, callback=self.init_template)
		return self.loaders[path]

	def register_methods(self):
		super(Resource, self).register_methods()
		for method in self.methods:
			self.methods[method].codec('text/html', charset='UTF-8')(self.__class__._genshi_codec)

	def _genshi_codec(self, client):
		content = self.template_vars(client)
		return self.render_template(self.template_path(client), self.template_name(client), content)

	def template_vars(self, client):
		content = client.data
		if not isinstance(content, dict):
			content = dict(content=content)
		content.update(dict(
			user=client.user,
			client=client,
		))
		return content

	def template_path(self, client):
		return os.path.join(client.domain.template_path, '%s/' % (client.resource.__module__.split('.')[-1],))

	def template_name(self, client):
		method = {u'HEAD': u'GET'}.get(client.request.method, client.request.method)
		return ('%s_%s.tpl' % (client.resource.__class__.__name__, method)).lower()

	def init_template(self, template):
		return
		translator = Translator(translate=self.gettext)
		translator.setup(template)

	def render_template(self, template_path, template_name, tplvars):
		try:
			tpl = self.load(template_path).load(template_name)
			return tpl.generate(**tplvars).render(doctype='html5')
		except TemplateNotFound:
			raise INTERNAL_SERVER_ERROR('The template %r was not found in %r' % (template_name, template_path))
		except TemplateSyntaxError:
			raise

	def website_template_path(self, client):
		template_path = self.parent.template_path
		if callable(template_path):
			template_path = template_path(client)
		return os.path.join(template_path, 'website/')

	@property
	def website_template_name(self):
		return 'website.tpl'

	@websiteproperty
	def website_meta(self):
		return self.config.get('meta', [])

	@websiteproperty
	def website_scripts(self):
		return self.config.get('scripts', [])

	@websiteproperty
	def website_links(self):
		return self.config.get('links', [])

	def website_tplvars(self, client):
		module = type(self).__module__.split('.', 1)[0]
		source = sys.modules[type(self).__module__].__file__.split(module, 1)[-1]
		source = '%s%s' % (module.replace('_', '.'), source)
		if source.endswith('.pyc') or source.endswith('.pyo'):
			source = source[:-1]
		tplvars = dict(
			content=unicode(client.response.body),
			user=client.user,
			_=lambda x: x,
			source=source,
		)
		tplvars.update(self.config)
		for iname, prop in inspect.getmembers(self.__class__, lambda prop: isinstance(prop, websiteproperty)):
			tplvars[prop.name] = getattr(self, iname)
		return tplvars

	@httphandler('request', priority=0.45)
	def _wrap_html_content(self, client):
		if not client.response.headers.get('Content-Type', '').startswith('text/html'):
			return
		if client.response.status in (204, 205):
			return
		if client.request.headers.get('X-Requested-With', '').lower() == 'XMLHttpRequest'.lower():
			return

		client.response.body = self.render_template(self.website_template_path(client), self.website_template_name, self.website_tplvars(client))
