# -*- coding: utf-8 -*-

from six.moves.configparser import ConfigParser
import os.path
import ast


class HTML(object):
	pass


class Meta(HTML):

	def __init__(self, value, content, http_equiv=False):
		self.var = 'http-equiv' if http_equiv else 'name'
		self.value = value
		self.content = content

	def __repr__(self):
		return '<meta %s=%r content=%r />' % (self.var, self.value, self.content)


class Link(HTML):

	def __init__(self, rel, type, href, **attrs):
		self.rel = rel
		self.type = type
		self.href = href
		self.attrs = attrs


class CSS(Link):

	def __init__(self, href, **attrs):
		super(CSS, self).__init__('stylesheet', 'text/css', href, **attrs)


class JavaScript(HTML):

	def __init__(self, href=None, type='text/javascript', **attrs):
		self.attrs = {'src': href, 'type': type}
		self.content = attrs.pop('content', None)


def config():
	c = ConfigParser()
	c.read(os.path.join(os.path.dirname(__file__), 'config.cfg'))
	config = dict((x, ast.literal_eval(y)) for x, y in c.items('website'))
	config['meta'] = [Meta(x, ast.literal_eval(y)) for x, y in c.items('website_meta')]
	config['meta'] += [Meta(x, ast.literal_eval(y), True) for x, y in c.items('website_meta_http')]

	links = dict((x, ast.literal_eval(y.replace('$', '%'))) for x, y in c.items('website_links'))
	config['links'] = []
	config['links'] += [Link(**dict((y, z % config) for y, z in x.items())) for x in links.get('links', [])]
	config['links'] += [CSS(x % config) for x in links['stylesheet']]
	config['links'] += [Link('icon', links['icon_type'], x % config) for x in links['icon']]
#	import pdb; pdb.set_trace()
	return config
