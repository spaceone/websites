# -*- coding: utf-8 -*-
"""wrapper for sqlalchemy"""

from sqlalchemy import ForeignKey, Column, create_engine
from sqlalchemy.types import Boolean, Date, DateTime, Enum, Float, String, Integer, Numeric, Text, Time, Unicode, UnicodeText, NullType, PickleType
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from httoop import NOT_FOUND, CREATED, GONE
Base = declarative_base()


def base(cls):
	return declarative_base(cls=cls)


# FIXME: sqlalchemy really does not like this
def metabase(cls=None):
	import abc
	return declarative_base(cls=cls, metaclass=abc.ABCMeta)


@base
class SQLResource(object):
	u"""

	"""
	idproperties = ()  # TODO: get from uri_dispatcher
	__abstract__ = True

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()

	@property
	def options(self):
		return 0

#	@property
#	def installed(self):
#		return self.__table__.exists(bind=self.session.bind)
#
#	@handler('install')
#	def _on_sql_install(self):
#		return self.__table__.create(bind=self.session.bind)
#
#	@handler('uninstall')
#	def _on_sql_uninstall(self):
#		return self.__table__.drop(bind=self.session.bind)

	def option_enabled(self, bits):
		return (self.options & bits) == bits

	def enable_options(self, bits):
		self.options = self.options | bits

	def disable_options(self, bits):
		self.options = self.options & (~bits)

	def as_dict(self):
		columns = self.columns
		return dict((key, val) for key, val in self.__dict__.items() if key in columns)

	@property
	def columns(self):
		return dict(self.__table__.columns)

	@property
	def schema(self):
		schema = dict()  #Schema()
		for name, column in dict(self.columns).items():
			schema[name] = dict(
				column=column,
				default=getattr(column.default, 'arg', None),
				label=getattr(column, '_label', name),
				description=getattr(column, 'description', ""),
				validator=getattr(self, 'validate_%s' % name, None),
				readonly=getattr(column, 'readonly', False),
				type=column.type.python_type
			)
			if hasattr(schema[name]['default'], '__call__'):
				schema[name]['default'] = str(schema[name]['default'](None))
		return schema

	def x_sql_schema_text(self):
		# TODO: mimetype text/x-sql-schema which is the CREATE TABLE statement
		pass

	def GET(self, client, **params):
		props = dict([(prop, params[prop]) for prop in self.idproperties])
		query = client.domain.session.query(self.__class__).filter_by(**props)
		try:
			obj = query.one()
		except NoResultFound:
			raise NOT_FOUND(client.request.uri.path)
		return obj

	def PUT(self, client, **params):
		session = client.domain.session
		props = dict([(prop, params[prop]) for prop in self.idproperties])
		query = session.query(self.__class__).filter_by(**props)
		# TODO: can i use merge?
		try:
			obj = query.one()
		except NoResultFound:
			exists = False
			obj = self.__class__(**client.request.body.data)  # FIXME
			session.add(obj)
		else:
			exists = True
			for key, value in client.request.body.data.iteritems():
				setattr(obj, key, value)

		session.commit()

		if not exists:
			client.response.status = CREATED.status
			client.response.headers['Location'] = client.request.uri.path

		return obj

	def DELETE(self, client, **params):
		session = client.domain.session
		obj = SQLResource.GET(self, client, **params)
		if obj is None:  # obj.DELETED
			# TODO: is there a possibility to detect if the resource had exists?
			raise GONE()
		session.delete(obj)
		session.commit()

	# A POST request is allowed here to add, modify or delete a resource????

	def OPTIONS(self, client, **params):
		schema = dict()
		for name, value in self.schema.iteritems():
			schema[name] = dict(
				default=value['default'],
				label=value['label'].title(),
				description=value['description'],
				readonly=value['readonly'],
				type=value['type'].__name__
			)
		return schema
