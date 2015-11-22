# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time
from datetime import datetime

from httoop import Date, NOT_FOUND, SEE_OTHER

from circuits.http.server.resource import method
from circuits.http.utils import httphandler, is_user

from .db import Column, String, Integer, DateTime, hybrid_property, SQLResource
from .base import Resource
from .validators import StringValidator, BoolSanitizer


class URLSanitizer(StringValidator):

	def sanitize(self, value):
		value = str(value)
		# FIXME: urldecode
		if not value.startswith('/'):
			value = '/%s' % value
		return value


# TODO: use sqlalchemies hybrid property for the option bits
class Page(Resource, SQLResource):
	u"""A Page"""

#	path = '/pages{url:/.*}'
	path = '{start:(/pages)?}{url:/.*}'
	# TODO: get idproperties from python-routes dispatcher
	idproperties = ('url',)

	# option bits
	(ENABLED, INDEXED, FOLLOW) = 0x01, 0x02, 0x04

	# column definements
	id = Column(Integer, primary_key=True, autoincrement=True)
	url = Column(String(256), nullable=False, unique=True)
	title = Column(String(256), default="", nullable=False)
##	other_id = Column(Integer) # The real ID of the resource, e.g. to translate it or put it into another content-type form
##	language = Column(String, default="", nullable=False)
	author = Column(String(32), nullable=False) # TODO: we could join into SQLUser here but this would be a dependency on it which we (at currently state) may not want?
	groups = Column(String, default="", nullable=False) # TODO: implement
	creation_date = Column(DateTime, default=lambda: datetime.now(), nullable=False)
	modify_date = Column(DateTime, default=lambda: datetime.now(), nullable=False)
	meta_tags = Column(String(256), default="", nullable=False)
	meta_description = Column(String(256), default="", nullable=False)
	content = Column(String, default="", nullable=False)
	views = Column(Integer, default=0, nullable=False)
	options = Column(Integer, default=ENABLED, nullable=False)
	indexed = type('Column', (object,), dict(default=False, type=type('type', (object,), dict(python_type=bool))))()
	follow = type('Column', (object,), dict(default=False, type=type('type', (object,), dict(python_type=bool))))()

	# TODO: create an wrapper arround Column, to add also the following properties: readonly, description, label, etc.

	# descriptions
	author.description = 'The author of this page'
	groups.description = 'groups which are allowed to access this page'
	creation_date.description = 'when the page was created'
	modify_date.description = 'when the page was last modified'
	url.description = 'the path of this page'
	title.description = 'the title of this page'
	meta_tags.description = 'HTML meta tags'
	meta_description.description = 'HTML meta description'
	content.description = 'The content of this page as HTML'
	views.description = "how often the page was visited (GET)"
	indexed.description = 'conforms <meta name="robots" content="(no)?index"/>'
	follow.description = 'conforms <meta name="robots" content="(no)?follow"/>'

	# readonly
	author.readonly = True
	creation_date.readonly = True
	modify_date.readonly = True
	views.readonly = True
	id.readonly = True
##	other_id.readonly = True
	options.readonly = True

	# sanitizer
	validate_url = URLSanitizer()
	validate_author = validate_language = validate_groups =\
		validate_title = validate_meta_tags = \
		validate_meta_description = validate_content = StringValidator()
	validate_indexed = validate_follow = BoolSanitizer()

#	# FIXME: is not being added to __dict__
#	@hybrid_property
#	def indexed(self):
#		if isinstance(self, type):
#			return None
#		return self.option_enabled(Page.INDEXED)

	@property
	def columns(self):
		# manipulate the scheme
		# TODO: make this generic, how??? hybrid_property and mixin from sqlalchemy did not add the values into __dict__.. we can do this by hand
		columns = super(Page, self).columns
		# add columns for the options of this page
		columns.update(dict(
			indexed = self.indexed,
			follow = self.follow
		))
		# remove the hidden properties from our schema
		columns.pop('options')
		columns.pop('id')
##		columns.pop('other_id')
		return columns

	def identify(self, client, path_segments):
		url_ = path_segments['url']
		for url in (url_.rstrip('/'), '%s/' % (url_.rstrip('/'),)):
			try:
				client.obj = super(Page, self).GET(client, url=url)
			except NOT_FOUND:
				pass
			else:
				if url_ != url:
					raise SEE_OTHER(url)
				break
		else:
			return
		return self

	def last_modified(self, client):
		if not client.obj or client.obj.modify_date is None:
			return
		return Date(time.mktime(client.obj.modify_date.timetuple()))

	@method
	def GET(self, client, _, url, **params):
		obj = super(Page, self).GET(client, url=url)
		obj.views += 1 # increment page views for every request

		values = obj.as_dict()

		# translate options
		values['indexed'] = obj.option_enabled(Page.INDEXED)
		values['follow'] = obj.option_enabled(Page.FOLLOW)

		# format dates
		if values['modify_date']:
			values['modify_date'] = values['modify_date'].strftime('%Y-%m-%d %H:%M:%S')
		if values['creation_date']:
			values['creation_date'] = values['creation_date'].strftime('%Y-%m-%d %H:%M:%S')

		# remvove hidden properties # TODO: make this generic
		values.pop('options', None)
		values.pop('id', None)
##		values.pop('other_id', None)

		try:
			client.domain.session.commit()
		finally:
			return values
	GET.codec('application/json', 0.9)

	@method
	def PUT(self, client, _, url):
		# remove immutable things
		client.request.body.data.pop('views')
		client.request.body.data.pop('creation_date')
		client.request.body.data['author'] = client.user.username  # FIXME: only when adding otherwise keep the current value
		client.request.body.data['modify_date'] = datetime.now()

		options = Page.ENABLED
		if client.request.body.data.pop('follow', False):
			options |= Page.FOLLOW
		if client.request.body.data.pop('indexed', False):
			options |= Page.INDEXED
		client.request.body.data['options'] = options

		super(Page, self).PUT(client, url=url)
		if client.response.status == 201:
			return _('The resource %r has successfully been created.') % url
		return _('The resource %r has successfully been modified.') % url
	PUT.conditions(is_user('root'))
	PUT.codec('application/json', 0.9)

	@method
	def DELETE(self, client, _, url, **params):
		super(Page, self).DELETE(client, url=url)
		return _('The resource %r has successfully been removed.') % url
	DELETE.conditions(is_user('root'))

	OPTIONS = method(SQLResource.OPTIONS)
	OPTIONS.codec('application/json', 0.9)

	@httphandler('cms.install', priority=0.6)
	def _on_page_install(self, session):
		# insert a default page when installing
		p = self.__class__(
			author='SF',
			url='/index',
			title='Welcome to SF CMS index',
			meta_tags='SF, CMS, Index',
			meta_description='',
			content='This is the index of the SpaceFramework CMS Module',
			options=Page.INDEXED|Page.ENABLED|Page.FOLLOW
		)
		session.add(p)
		session.commit()

	def __repr__(self):
		return '<Page title=%r url=%r (%d)>' % (self.title, self.url, len(self.content) if self.content else 0)


class Navigation(Resource):
	path = '/navigation'

	@method
	def GET(self, client):
		result = client.domain.session.query(Page.url, Page.title).all() # TODO: permission
		return dict(navigation=dict((ipage.url, ipage.title) for ipage in result))
	GET.codec('application/json', 0.9)
