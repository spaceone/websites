# -*- coding: utf-8 -*-

# TODO: have a look at python-webcolors
import os.path

from genshi.template.text import NewTextTemplate
from genshi.template import TemplateLoader

from circuits.http.server.resource import method, Resource

__name__ = 'color'


class Color(Resource):

	path = '/color/{design}/{layout}/{color}.css'

	def identify(self, client, path_segments):
		if path_segments['color'] in self.layoutcolors:
			return self

	@method
	def GET(self, client, design='SF', layout='space', color='green'):
		color = dict(self.layoutcolors[color])
		color.update(dict(
			layout=layout,
			design=design
		))
		return color

	@GET.codec('text/css')
	def _text_css(self, client):
		template_path = os.path.join(client.domain.template_path, '%s/' % __name__)
		try:
			tpl = self.load(template_path).load('color_get.tpl', cls=NewTextTemplate)
		except Exception:
			raise ValueError(template_path)
		return tpl.generate(**client.data).render()  # doctype='html5'

	loaders = dict()

	@classmethod
	def load(cls, path):
		if path not in cls.loaders:
			cls.loaders[path] = TemplateLoader(path, auto_reload=True)
		return cls.loaders[path]

	layoutcolors = {
		'blue': {
			'base_color': 'blue',
			'design_dark': '#076df3',
			'design_light': '#00a3f9',
			'border_dark': '#076df3',
			'border_light': '#00a3f9',
		},
		'green': {
			'base_color': 'green',
			'design_dark': '#006400',
			'design_light': '#00FF00',
			'border_dark': '#006400',
			'border_light': '#00FF00',
		},
		'orange': {
			'base_color': 'orange',
			'design_dark': '#FF8C00',
			'design_light': '#FFA500',
			'border_dark': '#FF8C00',
			'border_light': '#FFA500',
		},
		'red': {
			'base_color': 'red',
			'border_light': '#a33a3a',
			'border_dark': '#8e0a0a',
			'design_light': '#FF0000',
			'design_dark': '#8B0000',
		},
		'yellow': {
			'base_color': 'yellow',
			'border_light': '#',
			'border_dark': '#',
			'design_light': '#',
			'design_dark': '#',
		},
		'purple': {
			'base_color': 'purple',
			'border_light': '#140620',
			'border_dark': '#6521a4',
			'design_light': '#6521a4',
			'design_dark': '#6521a4',
		},
		'white': {
			'base_color': 'white',
			'border_light': '#',
			'border_dark': '#',
			'design_light': '#',
			'design_dark': '#',
		},
		'black': {
			'base_color': 'black',
			'border_light': '#',
			'border_dark': '#',
			'design_light': '#',
			'design_dark': '#',
		},
		'brown': {
			'base_color': 'brown',
			'border_light': '#',
			'border_dark': '#',
			'design_light': '#',
			'design_dark': '#',
		}
	}
