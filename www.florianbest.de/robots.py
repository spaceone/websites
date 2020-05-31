# -*- coding: utf-8 -*-

import itertools
import operator

from circuits.http.server.resource import method
from .base import _Resource


class Robots(_Resource):
	"""This is the robots file for this domain located under /robots.txt

		.. seealso:: http://www.robotstxt.org/norobots-rfc.txt
	"""

	path = '/robots.txt'

	@method
	def GET(self, client, _, **params):
		robots = self.group_by_value(getattr(client.domain, 'robots', {}))
		return bytes(RobotEntries([RobotEntry(agents, *rules) for agents, rules in robots.items()]))
	GET.codec('text/plain', charset='utf-8')

	# TODO: move into RobotEntries.__str__
	def group_by_value(self, d):
		new_d = {}
		sorted_items = sorted(d.items(), key=operator.itemgetter(1))
		for value, group in itertools.groupby(sorted_items, key=operator.itemgetter(1)):
			key = tuple(item[0] for item in group)
			new_d[key] = value
		return new_d


class RobotEntry(object):

	def __init__(self, user_agents, disallow=None, allow=None):
		self.user_agents = user_agents
		self.allow = set(allow or [])
		self.disallow = set(disallow or [])

	def __str__(self):
		return '%s\n%s\n%s' % (
			'\n'.join('User-agent: %s' % u for u in self.user_agents),
			'\n'.join('Disallow: %s' % d for d in self.disallow),
			'\n'.join('Allow: %s' % d for d in self.allow),
		)


class RobotEntries(list):

	def __str__(self):
		return '\n\n'.join(str(r) for r in self)
