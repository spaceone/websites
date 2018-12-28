# -*- coding: utf-8 -*-

import os

from httoop import TEMPORARY_REDIRECT, SEE_OTHER, BAD_REQUEST, MULTIPLE_CHOICES, URI

from circuits.http.server.resource import method
from circuits.http.server.saml.service_provider import ServiceProvider, SamlLogoutRequest
from circuits.http.server.saml.events import single_sign_on, saml_logout_request, saml_logout_response, saml_global_logout
from circuits.http.server.saml.models import SamlAuthnRequest, MultipleIdentityProvider

from .base import _Resource, Resource

SESSION = {}


class _Resource(_Resource):

	def init(self, saml, **kwargs):
		self.saml = saml


class Resource(Resource):

	def init(self, saml, **kwargs):
		self.saml = saml


class Metadata(_Resource):

	path = 'metadata'

	@method
	def GET(self, client, _, **params):
		return self.saml.get_metadata()

	@GET.codec('application/xml', charset='utf-8')
	def _application_xml(self, client):
		return client.data


class AssertionConsumerService(Resource):

	path = 'acs/'

	@method
	def GET(self, client, **params):
		# TODO: check if already logged in
		preferred_identity_provider = params.get('identity_provider')
		reply_binding, service_provider_url = None, str(client.request.uri)
		#reply_binding, service_provider_url = self.saml.select_service_provider(client)
		state = object()  # we can store various state here
		response = single_sign_on(SamlAuthnRequest(
			state=state,
			service_provider_url=service_provider_url,
			reply_binding=reply_binding,
			preferred_identity_provider=preferred_identity_provider,
		))
		self.fire(response, self.saml.channel)
		yield self.wait(response)
		if response.value.errors:
			exc = response.value.value[1]
			if isinstance(exc, MultipleIdentityProvider):
				urls = []
				for idp in exc.idps:
					uri = URI(client.request.uri)
					uri.query = {'identity_provider': idp}
					urls.append(bytes(uri))
				raise MULTIPLE_CHOICES(urls, str(exc))
			raise exc
		yield response.value.value.apply(client)

	@GET.codec('*/*')
	def _get_codec(self, client):
		return client.data

	@method
	def POST(self, client, _, **params):
		response = self.saml.parse_authn_respone(client)
		if not response:
			# The request doesn't contain a SAML message. Force redirection that it gets one
			raise TEMPORARY_REDIRECT('/saml/acs/')

		SESSION['SAML'] = response
		print '#### RECEIVED the following attributes!!!!', response
		# TODO: set cookie

		# successful login
		raise SEE_OTHER('/')
	POST.accept('application/x-www-form-urlencoded')

	@POST.codec('*/*')
	def _post_codec(self, client):
		return client.data


class SamlLogout(Resource):

	path = 'logout'

	@method
	def GET(self, client):
		if not SESSION['SAML']:
			# already logged out
			raise SEE_OTHER('/logout')

		response = yield self.call(saml_global_logout(SESSION['SAML'].name_id), self.saml.channel)
		if response.value is not None:
			# inform the identiy provider about the logout
			yield response.value.apply(client)
			return

		# successful logout
		SESSION.pop('SAML')
		raise SEE_OTHER('/logout')


class SingleLogoutService(Resource):

	path = 'slo/'

	def slo(self, client):
		request = self.saml.parse_saml_logout(client)
		if not request:
			raise BAD_REQUEST('The HTTP request is missing required SAML parameter.')

		if isinstance(request, SamlLogoutRequest):
			response = yield self.call(saml_logout_request(SESSION['SAML'].name_id, request), self.saml.channel)
			yield response.value.apply(client)
			return

		yield self.call(saml_logout_response(request), self.saml.channel)
		# successful logout, redirect to a nice page
		SESSION.pop('SAML')
		raise SEE_OTHER('/logout')

	GET = method('GET')(slo)
	POST = method('POST')(slo)
	POST.accept('application/x-www-form-urlencoded')


class SAML(Resource):

	path = '/saml'

	def website_template_path(self, client):
		return self.parent.website_template_path(client)

	@method
	def GET(self, client):
		raise SEE_OTHER('/saml/acs/')

	def init(self, **kw):
		self.saml = ServiceProvider(configfile=os.path.join(os.path.dirname(__file__), 'saml_config.py'), channel='saml')
		self += self.saml
		self += Metadata(channel='saml-metadata', saml=self.saml)
		self += AssertionConsumerService(channel='saml-acs', saml=self.saml)
		self += SamlLogout(channel='saml-logout', saml=self.saml)
		self += SingleLogoutService(channel='saml-slo', saml=self.saml)
