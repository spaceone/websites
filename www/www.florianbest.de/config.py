class HTML(object): pass


class Meta(HTML):
	def __init__(self, value, content, http_equiv=False):
		self.var = 'http-equiv' if http_equiv else 'name'
		self.value = value
		self.content = content

	def __repr__(self):
		return '<meta %s=%r content=%r />' % (self.var, self.value, self.content)


class Link(HTML):
	def __init__(self, rel, type, href):
		self.rel = rel
		self.type = type
		self.href = href


class CSS(Link):
	def __init__(self, href):
		super(CSS, self).__init__('stylesheet', 'text/css', href)


def config():
	c = ConfigParser()
	c.read('config.cfg')
	config = dict((x, ast.literal_eval(y)) for x, y in c.items('website'))
	config.update(dict(
		sf=type('', (object,), {'design': 'SF', 'layout': 'space', 'layoutcolor': 'green', 'display': type('', (object,), {'navileft':False, 'shell': False, 'naviright': False, 'details': False})})
		user=type('USER', (object,), {'is_logged_in' : False, 'is_guest':True})
		_=lambda x:x
	))
	config['meta'] = [Meta(x, ast.literal_eval(y)) for x, y in c.items('website_meta')]
	config['meta'] += [Meta(x, ast.literal_eval(y), True) for x, y in c.items('website_meta_http')]

	links = [(x, ast.literal_eval(y.replace('$', '%'))) for x, y in c.items('website_links')]
	config['links'] = []
	config['links'] += [CSS(x % config) for x in links['stylesheet']]
	config['links'] += [Link('icon', links['icon_type'], x % config) for x in links['icon']]
	return config
