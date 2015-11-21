# -*- coding: utf-8 -*-

import re
import copy


class SanitizeError(ValueError):
	pass

# TODO: TypeValidator for python types


# TODO: add mechanism to depend on other values
class Sanitizer(object):
	u"""Base class for every sanitizer"""

	def __init__(self, **kwargs):
		u"""Init Sanitizer
			:param required: Is the value required
			:param default: A default fallback value if the value is not set
		"""
		# FIXME: rethink this
		self.required = kwargs.get('required', True)
		self.default = kwargs.get('default', None)

	def sanitize(self, value):
		u"""
		:raises: :class:`~SanitizeError`
		"""

		# the value is invalid, try to sanitize it
		try:
			value = self._sanitize(value)
		except SanitizeError:
			if not self.required:
				return self.default
			raise
		return value

	def _sanitize(self, value):
		return value

	def raise_validation_error(self, message):
		u"""Raise a validation error.

		:param str message: the exception message.
		:raises: :class:`~SanitizeError`
		"""
		raise SanitizeError(message)


class ListValidator(Sanitizer):
	u"""A list-validator"""

	def sanitize(self, value):
		u"""Checks if the given value is an instance of list

		:param value: the value to validate.
		"""
		if not isinstance(value, (list)):
			raise SanitizeError('Value is not of type "list"')
		return value


class DictValidator(Sanitizer):
	u"""A dict validator"""

	def sanitize(self, value):
		u"""Checks if the given value is an instance of dict

		:param value: the value to validate.
		"""
		if not isinstance(value, dict):
			raise SanitizeError('Value is not of type "dict"')
		return value


class DictSanitizer(Sanitizer):
	u"""makes sure the value is a dict and validates its fields.

		:param sanitizers: sanitizer to apply to the content of the sanitized dict
		:type sanitizers: a dict of :class:`~Sanitizer`

		:param allow_other_keys: indicates whether the sanitized dict may contain other keys than those existing in :attr:`sanitizers`
		:type allow_other_keys: bool
	"""
	def __init__(self, sanitizers, allow_other_keys=False, **kwargs):
		super(DictSanitizer, self).__init__(**kwargs)
		self.sanitizers = sanitizers
		self.allow_other_keys = allow_other_keys

	def _sanitize(self, value):
		if not isinstance(value, dict):
			raise SanitizeError('is not a dict')
			#self.raise_formatted_validation_error(_('Not a "dict"'), name, type(value).__name__)

		if not self.allow_other_keys and any(key not in self.sanitizers for key in value):
			raise SanitizeError('Has more than the allowed keys')
			#self.raise_validation_error(_('Has more than the allowed keys'))

		altered_value = copy.deepcopy(value)

		errors = []
		for attr, sanitizer in self.sanitizers.iteritems():
			try:
				altered_value[attr] = sanitizer.sanitize(value.get(attr))
			except SanitizeError as e:
				errors.append((e, attr))
		if errors:
			raise SanitizeError(errors)

		return altered_value

	def __add__(self, other):
		new = copy.deepcopy(self)
		new.sanitizers.update(other.sanitizers)
		return new


class StringValidator(Sanitizer):
	u"""A string validator"""

	def __init__(self, regex_pattern=None, re_flags=0, minimum=None, maximum=None, **kwargs):
		u"""
			:param regex_pattern: a regular expression which have to match when validating
			:type regex_pattern: a re.pattern_type or a string which will be compiled with the flags given in `re_flags`
			:param re_flags: optional flags when compiling regex pattern
			:param minimum: the minimum length of the string
			:param maximum: the maximum length of the string
		"""
		super(StringValidator, self).__init__(**kwargs)

		# compile pattern
		if isinstance(regex_pattern, basestring):
			regex_pattern = re.compile(regex_pattern, flags=re_flags)
		self.regex_pattern = regex_pattern

		self.minimum = minimum
		self.maximum = maximum

	def sanitize(self, value):
		u"""Checks if the given value is an instance of str

		:param value: the value to validate.
		"""
		if not isinstance(value, basestring):
			self.raise_validation_error('Value is not a string')

		if not isinstance(value, unicode):
			# force UTF-8 ?!
			value = value.decode('utf-8')

		if self.minimum is not None and len(value) < self.minimum:
			self.raise_validation_error('Value is too short, it has to be at least of length %(minimum)d')

		if self.maximum is not None and len(value) > self.maximum:
			self.raise_validation_error('Value is too long, it has to be at most of length %(maximum)d')

		if self.regex_pattern and not self.regex_pattern.search(value):
			self.raise_validation_error('Value is invalid')

		return value


class StringSanitizer(StringValidator):
	u"""IntSanitizer makes sure that the value is a string and sanitizes it"""

	def sanitize(self, value):
		if not isinstance(value, basestring):
			value = str(value)
		return super(StringSanitizer, self).sanitize(value)


# TODO: choiceSanitizer
class SortValidator(Sanitizer):
	def _sanitize(self, value):
		if value not in ('ASC', 'DESC'):
			raise SanitizeError
		return value


class OrderBySanitizer(Sanitizer):
	def _sanitize(self, value, name):
		if not isinstance(value, list):
			value = str(value).split(',')
		return value


class IntValidator(Sanitizer):
	"""A int validator"""

	def sanitize(self, value):
		u"""Checks if the given value is an instance of int.

		:param value: the value to validate.
		"""
		return isinstance(value, int)


class IntSanitizer(IntValidator):
	u"""IntSanitizer makes sure that the value is a int or tries to cast it"""

	def _sanitize(self, value, name):
		try:
			value = int(value)
			if not isinstance(value, int):
				raise ValueError
			return value
		except:
			raise SanitizeError


class FloatValidator(Sanitizer):
	"""A float validator"""

	def sanitize(self, value):
		u"""Checks if the given value is an instance of float.

		:param value: the value to validate.
		"""
		return isinstance(value, long)


class FloatSanitizer(FloatValidator):
	u"""FloatSanitizer makes sure that the value is a float and sanitizes it"""

	def _sanitize(self, value, name):
		try:
			return long(value)
		except:
			raise SanitizeError


class BoolValidator(Sanitizer):
	"""A boolean validator"""

	def sanitize(self, value):
		u"""Checks if the given value is an instance of bool.

		:param value: the value to validate.
		"""
		return isinstance(value, bool)


class BoolSanitizer(BoolValidator):
	u"""BoolSanitizer makes sure that the value is a bool or casts it"""

	def _sanitize(self, value, name):
		return bool(value)


# pseudo validators
class ChoiceValidator(Sanitizer):
	pass


'''
class ListSanitizer(Sanitizer):
	u"""ListSanitizer makes sure that the value is a list and sanitizes its elements.

	You can give the same parameters as the base class.
	Plus:

	:param sanitizer: sanitizes each of the sanitized list's elements
	:param int min_elements: must have at least this number of elements
	:param int max_elements: must have at most this number of elements
	:type sanitizer: :class:`~Sanitizer`
	"""
	def __init__(self, sanitizer, min_elements=None, max_elements=None, **kwargs):
		super(ListSanitizer, self).__init__(**kwargs)
		self.sanitizer = sanitizer
		self.min_elements = min_elements
		self.max_elements = max_elements

	def _sanitize(self, value, name, further_arguments):
		if not isinstance(value, list):
			self.raise_formatted_validation_error(_('Not a "list"'), name, type(value).__name__)

		if self.min_elements is not None and len(value) < self.min_elements:
			self.raise_validation_error(_('Must have at least %(min_elements)d elements'))
		if self.max_elements is not None and len(value) > self.max_elements:
			self.raise_validation_error(_('Must have at most %(max_elements)d elements'))

		multi_error = MultiValidationError()
		altered_value = []
		for i, item in enumerate(value):
			name = 'Element #%d' % i
			try:
				altered_value.append(self.sanitizer.sanitize(name, {name : item}))
			except ValidationError as e:
				multi_error.add_error(e, i)
		if multi_error.has_errors():
			raise multi_error
		return altered_value
'''

