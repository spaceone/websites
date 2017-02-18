#!/bin/bash

set -e

mkdir -p i18n/de_DE/LC_MESSAGES/

xgettext \
	--force-po \
	--add-comments=i18n \
	--from-code=UTF-8 \
	--sort-output \
	--package-name="www.florianbest.de" \
	--msgid-bugs-address=i18n@florianbest.de \
	--copyright-holder="Florian Best" \
	--language python \
	--no-wrap \
	-p i18n/ \
	-d python_de \
	-- $(find -name '*.py')

msgmerge --update --sort-output i18n/messages.po i18n/python_de.po

msgfmt --check --output-file=i18n/de_DE/LC_MESSAGES/www.florianbest.de.mo i18n/messages.po
