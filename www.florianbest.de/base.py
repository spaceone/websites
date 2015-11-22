# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys
import inspect

from genshi.template import TemplateLoader, TemplateNotFound, TemplateSyntaxError
#from genshi.filters import Translator

from httoop import INTERNAL_SERVER_ERROR
from circuits.http.utils import httphandler
from circuits.http.server.resource import Resource

from .config import config


class _Resource(Resource):

	def keyword_arguments(self, client):
		kwargs = super(_Resource, self).keyword_arguments(client)
		argspec = inspect.getargspec(client.method.method)
		if '_' in argspec.args:
			kwargs['_'] = lambda x: x
		if argspec.keywords:
			kw = dict(client.request.uri.query)
			kw.update(kwargs)
			kwargs = kw

		for name, value in client.path_segments.iteritems():
			if name in argspec.args:
				kwargs[name] = value

		return kwargs


class Resource(_Resource):

	loaders = dict()

	@classmethod
	def load(cls, path):
		if not path in cls.loaders:
			cls.loaders[path] = TemplateLoader(path, auto_reload=True)
		return cls.loaders[path]

	def register_methods(self):
		super(Resource, self).register_methods()
		self.methods['GET'].codec('text/html')(self.__class__._genshi_codec)

	def _genshi_codec(self, client):
		content = self.template_vars(client)
		return self.render_template(self.template_path(client), self.template_name(client), content)

	def template_vars(self, client):
		content = client.data
		if not isinstance(content, dict):
			content = dict(content=content)
		content.update(dict(
			user=client.user,
		))
		return content

	def template_path(self, client):
		return os.path.join(client.domain.template_path, '%s/' % (client.resource.__module__.split('.')[-1],))

	def template_name(self, client):
		return ('%s_%s.tpl' % (client.resource.__class__.__name__, client.request.method)).lower()

	def render_template(self, template_path, template_name, tplvars):
		try:
			tpl = self.load(template_path).load(template_name)
		#	translator = Translator(translate=client.kwargs['_'])
		#	translator.setup(tpl)
			return tpl.generate(**tplvars).render(doctype='html5')
		except TemplateNotFound:
			raise INTERNAL_SERVER_ERROR('The template %r was not found in %r' % (template_name, template_path))
		except TemplateSyntaxError:
			raise

	@property
	def website_template_path(self):
		return os.path.join(self.parent.template_path, 'website/')

	@property
	def website_template_name(self):
		return 'website.tpl'

	def website_tplvars(self, client):
		module = type(self).__module__.split('.', 1)[0]
		source = sys.modules[type(self).__module__].__file__.split(module, 1)[-1]
		source = '%s%s' % (module.replace('_', '.'), source)
		tplvars = dict(
			content=unicode(client.response.body),
			user=client.user,
			_=lambda x: x,
			source=source,
		)
		tplvars.update(config())
#		for iname, prop in inspect.getmembers(self.__class__, lambda prop: isinstance(prop, websiteproperty)):
#			tplvars[prop.name] = getattr(self, iname)
		return tplvars

	@httphandler('request', priority=0.45)
	def _wrap_html_content(self, client):
		if not client.response.headers.get('Content-Type', '').startswith('text/html'):
			return
		if client.response.status in (204, 205):
			return
		if client.request.headers.get('X-Requested-With', '').lower() == 'XMLHttpRequest'.lower():
			return

		client.response.body = self.render_template(self.website_template_path, self.website_template_name, self.website_tplvars(client))
