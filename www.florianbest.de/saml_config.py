# http://pysaml2.readthedocs.org/en/latest/howto/config.html

import os
import glob

from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.saml import NAME_FORMAT_URI


CONFIG = {
	"entityid": "https://www.florianbest.de/saml/metadata",
	"name_form": NAME_FORMAT_URI,
	"description": "SAML2.0 Service Provider von www.FlorianBest.de",
	"service": {
		"sp": {
			"allow_unsolicited": True,
			"want_assertions_signed": True,
			"authn_requests_signed": True,
			"logout_requests_signed": True,
			"endpoints": {
				"assertion_consumer_service": [
					('https://www.florianbest.de/saml/acs/', BINDING_HTTP_POST),
				],
				"single_logout_service": [
					('https://www.florianbest.de/saml/slo/', BINDING_HTTP_POST),
					('https://www.florianbest.de/saml/slo/', BINDING_HTTP_REDIRECT),
				],
			},
			"required_attributes": ["uid", "sn", "gn", "gecos"],
			"optional_attributes": ["objectClass", "description", "uidNumber", "gidNumber", "userPassword", "displayName", "cn", "loginShell"],
		},
	},
	"attribute_map_dir": "/usr/lib/python2.7/dist-packages/saml2/attributemaps/",
	"key_file": "/etc/letsencrypt/live/www.florianbest.de/privkey.pem",
	"cert_file": "/etc/letsencrypt/live/www.florianbest.de/cert.pem",
	"xmlsec_binary": "/usr/bin/xmlsec1",
	"metadata": {
		"local": glob.glob(os.path.join(os.path.dirname(__file__), 'idp_*.xml')),
	},
	"contact_person": [{
		"givenname": "Florian",
		"surname": "Best",
		"company": "Best",
		"mail": ["spam@florianbest.de"],
		"type": "technical",
	}, {
		"givenname": "Florian",
		"surname": "Best",
		"company": "Best",
		"mail": ["spam@florianbest.de"],
		"type": "administrative",
	}],
	"organization": {
		"name": [
			("Best", "en"),
			("Best", "de")
		],
		"display_name": ["Best"],
		"url": [
			("https://florianbest.de/en/", "en"),
			("https://florianbest.de/", "de")
		],
	},
}
