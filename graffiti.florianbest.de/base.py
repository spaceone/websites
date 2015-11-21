# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import inspect
import os

from httoop import INTERNAL_SERVER_ERROR
from circuits.http.server.resource import Resource
from circuits.http.utils import httphandler

from genshi.template import TemplateLoader, TemplateNotFound, TemplateSyntaxError
#from genshi.filters import Translator


class websiteproperty(property):

	def __init__(self, fget, *a, **kw):
		self.name = kw.pop('name', fget.__name__.replace('website_', ''))
		property.__init__(self, fget, *a, **kw)


class Resource(Resource):

	meta_description = ''
	robots = 'index, follow'

	@websiteproperty
	def website_title(self):
		return self.__class__.__name__

	@websiteproperty
	def website_navigation(self):
		navi = '''<ul class="navi">
			<li><b>graffiti.FlorianBest.de</b></li>
			%s
		</ul>'''

		link = '<li><a href="%(path)s" title="%(__name__)s">%(__name__)s</a></li>'
		from .website import Graffiti, Kunstwerke, Workshopangebot, Zeitungsartikel, Kontakt
		pages = (Graffiti, Kunstwerke, Workshopangebot, Zeitungsartikel, Kontakt)

		return navi % '\n\t'.join(link % dict(path=page.path, __name__=page.__name__) for page in pages)

	@websiteproperty
	def website_meta_description(self):
		return self.meta_description

	@websiteproperty
	def website_meta_robots(self):
		return self.robots

	@websiteproperty
	def website_doctype(self):
		return '<!DOCTYPE html>'

	@websiteproperty
	def website_base(self):
		return 'http://%s/' % self.parent.fqdn

	@websiteproperty
	def website_meta(self):
		return []

	@websiteproperty
	def website_links(self):
		return []

	@websiteproperty
	def website_language(self):
		return 'de'

	@property
	def tpl_dir(self):
		return 'website'

	@property
	def template_path(self):
		if self.parent is self:
			return
		return os.path.join(self.parent.template_path, '%s/' % self.tpl_dir)

	@property
	def template_name(self):
		return 'website.tpl'

	loaders = dict()

	@classmethod
	def load(cls, path):
		if not path in cls.loaders:
			cls.loaders[path] = TemplateLoader(path, auto_reload=True)
		return cls.loaders[path]

	@httphandler('request', priority=0.45)
	def _wrap_html_content(self, client):
		if not client.response.headers.get('Content-Type', '').startswith('text/html'):
			return
		if client.response.status in (204, 205):
			return
		if client.request.headers.get('X-Requested-With', '').lower() == 'XMLHttpRequest'.lower():
			return

		tplvars = dict(content=unicode(client.response.body))
		for iname, prop in inspect.getmembers(self.__class__, lambda prop: isinstance(prop, websiteproperty)):
			tplvars[prop.name] = getattr(self, iname)

		try:
			tpl = self.load(self.template_path).load(self.template_name)
		#	translator = Translator(translate=client.kwargs['_'])
		#	translator.setup(tpl)
			client.response.body = tpl.generate(**tplvars).render(doctype='html5')
		except TemplateNotFound:
			raise INTERNAL_SERVER_ERROR('The template %r was not found in %r' % (self.template_name, self.template_path))
		except TemplateSyntaxError:
			raise
