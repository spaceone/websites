# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import smtplib
import datetime
from email.mime.text import MIMEText

from circuits.http.server.resource import method
from httoop.status import UNPROCESSABLE_ENTITY

from .base import Resource

try:
	unicode
except NameError:
	unicode = str


class Graffiti(Resource):

	path = '/'
	meta_description = 'Graffiti Auftragsarbeiten von Florian Best im Kreis Diepholz, Barnstorf und Bremen'

	@method
	def GET(self, client):
		return '''
		<div style="margin:0 auto;line-height:25px;/*text-align:justify;*/">
		<div style="float: left; width: 70%;">
			<p>
				Herzlich Willkommen!<br>
				Auf dieser Internetseite stelle ich meine Graffitiarbeiten vor und
				biete <a href="/artworks/">Graffiti-Auftragsarbeiten</a> sowie <a href="/workshops/">Workshops</a> an.
			</p>
			<p>
				Schon immer war das Zeichnen - und später auch das Sprayen - eine meiner großen Leidenschaften.
				Nun, 5 Jahre nach meiner ersten Auftragsarbeit (2010), kann ich auf einige Erfahrungen zurückgreifen und biete meine Dienste an.
			</p>
			<p>
				Ganz gleich, ob Partykeller, Garagentor, Wohnzimmerwand oder Jugendzentrum - für jede Atmosphäre gestalte ich passende Motive,
				die persönlichen Vorstellungen entsprechen.
			</p>
			<p>
				Des weiteren biete ich auch Zeichnungen auf Papier und Schriftgestaltung an.
			</p>
			<p>
				Bei Interesse jeglicher Art, kann ich über das <a href="/contact/">Kontaktformular dieser Website</a> kontaktiert werden.
				Nach Absprache kann ich auch gerne per Telefon oder einem persönlichen Gespräch bereit.
			</p>
			<p>
				Mit freundlichem Gruß und viel Spaß auf dieser Website<br>
				Florian Best<br>
				“SpaceOne”
			</p>
		</div>
		<p style="float: right; width: 28%; text-align: center;">
			<a href="/images/2011_Space_DB_final1" title="Eingangshalle Bahnhof Barnstorf 2011">
				<img src="/Fotos/2011_Space_DB_final1_mini.jpg" alt="Eingangshalle Bahnhof Barnstorf 2011">
			</a>
			<a href="/images/2010_Space_JZB_final2" title="Eingangshalle Bahnhof Barnstorf 2011">
				<img src="/Fotos/2010_Space_JZB_final2_mini.jpg" alt="Eingangshalle Bahnhof Barnstorf 2011">
			</a>
			<br>
			<a href="/images/2010_JZB_final" title="Jugendzentrum Barnstorf Außenwand 2010">
				<img src="/Fotos/2010_JZB_final_mini.jpg" alt="Jugendzentrum Barnstorf Außenwand 2010">
			</a>
			<a href="/images/2010_Space_DB_final2" title="Deutsche Bahn Brücke Workshopabschlusswerk 2010">
				<img src="/Fotos/2010_Space_DB_final2_mini.jpg" alt="Deutsche Bahn Brücke Workshopabschlusswerk 2010">
			</a>
		</p>
		P.S.: Eine Auswahl meiner bisherigen Aufträge:<br>
		<ul>
			<li>Gestaltung des Musikraumes an der Christian-Hülsmeyer Schule Barnstorf</li>
			<li>Verzierung der Innen- und Außenwände im Jugendzentrum Barnstorf</li>
			<li>Verschönerung einer Bahnhofsunterführung in Barnstorf</li>
			<li>Besprühung des Innengebäude im Barnstorfer Bahnhof</li>
			<li>Leitung mehrtägiger Graffiti-Workshops mit Jugendlichen</li>
			<li>Weiterbildung zum Jugendgruppenleiter im Rahmen der “JuLeiCa”-Ausbildung</li>
		</ul>
	</div>'''

	@GET.codec('text/html')
	def _text_html(self, client):
		return client.data


class Kunstwerke(Resource):

	path = '/artworks/'
	meta_description = 'Graffiti Auftragsarbeiten / Kunstwerke von Florian Best'

	images = (
		('2018_Space_Workshop1_final1', dict(title='')),
		('2018_Space_Workshop1_final2', dict(title='Space - Juli 2018 -  Abschlusswerk Graffiti Workshop in Barnstorf')),
		('2018_Space_Workshop2_final1', dict(title='Space - Juli 2018 -  Abschlusswerk Graffiti Workshop in Barnstorf')),
		('2011_Space_DB_final1', dict(title='Space - Juli 2011 - in der Eingangshalle vom Bahnhof Barnstorf')),
		('2011_Space_DB_final2', dict(title='')),
		('2010_Space_DB_final', dict(
			content='Space - Juni 2010 - Deutsche Bahn Brücke in Barnstorf <br> Abschlusswerk meines Graffiti Workshops',
			title='Deutsche Bahn Brücke'
		)),
		('2010_Space_DB_final2', dict(title='')),
		('2010_Space_DB_43', dict(title='')),
		('2010_Space_JZB_final2', dict(title='Space - 2010 - Jugendzentrum Barnstorf<br><br>')),
		('2010_JZB_final', dict(title='JZB - 2010 - Eingang des Jugendzentrum Barnstorf')),
		('2010_JZB_6', dict(title='')),
		('2018_Tux', dict(title='Linux Tux')),
		('2018_CafeFreiraumLeinwand', dict(title='Leinwand für das Cafe Freiraum Projekt in Diepholz')),
	)

	@method
	def GET(self, client):
		return [dict(url=url, title=image['title'], content=image.get('content', image['title'])) for url, image in self.images]

	@GET.codec('text/html')
	def _text_html(self, client):
		return '<p>%s</p>' % ('\n'.join(
			'''
				<span class="bordered">
					<a href="/Fotos/%(url)s.jpg" title="%(title)s">
						<img src="/Fotos/%(url)s_thumb.jpg" alt="%(title)s" title="%(title)s" >
					</a>
					<br>%(content)s
				</span>
				<br>
			''' % x for x in client.data
		))


class Images(Resource):

	path = '/images/{image}'
	meta_description = 'Graffiti Auftragsarbeit'

	def identify(self, client, path_segments):
		if path_segments['image'] in Kunstwerke.images:
			return self

	@method
	def GET(self, client):
		image = client.path_segments['image']
		image = dict(url=image)
		image.update(Kunstwerke.images[image['url']])
		return image

	@GET.codec('text/html')
	def _text_html(self, client):
		return '''<span class="bordered">
			<a href="/Fotos/%(url)s.jpg">
				<img src="/Fotos/%(url)s_thumb.jpg" alt="%(title)s" title="%(title)s">
			</a>
			<br>%(title)s
		</span><br>''' % client.data


class Workshopangebot(Resource):

	path = '/workshops/'
	meta_description = 'Graffiti Workshop Angebot in Bremen, Diepholz, Barnstorf von Florian Best'

	@method
	def GET(self, client):
		return '''
		Hier skizziere ich ungefähr meinen Workshopaufbau, zur Inspiration stelle ich einige Graffiti Hefte zur Verfügung.

	<p>
		<h3>1. Tag - Graffiti kennenlernen und Zeichnen üben</h3>
		<ul>
			<li>Graffiti vorstellen + mein Bezug dazu</li>
			<li>Welches Interesse besteht an der Teilnahme?</li>
			<li>Wer hatte schon mit Graffiti oder Kunst zu tun.</li>
			<li>Wünsche und Fragen klären</li>
			<li>Handschrift ansehen</li>
			<li>Bleistifthaltung lernen</li>
			<li>Buchstaben:</li>
			<li>Grundaufbau -> woraus bestehen Buchstaben?,</li>
			<li>Dreiecke, Rechtecke, Quadrate, Kreise, Halbkreise, Linien üben</li>
			<li>Einteilung von Buchstaben in sinngemäße Balken</li>
		</ul>
	</p>

	<p>
		Übung:
		<ul>
			<li>Zeichnung von Buchstaben mit Bleistift (!), ohne Lineal & Geodreieck,</li>
			<li>Proportioneneinteilung mittels Einteilung des Blatts durch Linie,</li>
			<li>Schräge und krumme Linien sind erstmal nicht schlimm.</li>
			<li>gerade Linien üben,</li>
			<li>stabile Buchstaben</li>
			<li>niemals kritzeln (!),</li>
			<li>nicht durchstreichen,</li>
			<li>gleichmäßigkeit und synchrone Buchstaben,</li>
			<li>Gefühl für Buchstaben entwickeln,</li>
			<li>mit Fineliner fertige buchstaben nachziehen.</li>
			<li>Kugelschreiber sind für kritzeleien!</li>
		</ul>
	</p>

	<p>
		Buchstaben (metamorphose):
		<ol>
			<li>Erweiterung, kaligraphische und schöne buchstaben, eindrucksvoll wirken lassen, Blockige Buchstaben</li>
			<li>abstrakter werden, strecken, ziehen, transformieren, dicke und dünne bearbeiten, wichtigkeit der einzelnen Buchstabenteile</li>
			<li>4-fach Linien, modellieren, dinge anhängen, Elemente repertuare lernen, Pfeile ausdrucksvoll wirken lassen, das Auge schulen (!)</li>
			<li>mit Filzstift nachziehen</li>
		</ol>

		freiwillige Hausaufgabe: Üben, lernen, skizzieren.
	</p>

	<p>
		<h3>2. Tag - Spitzname als Graffiti umsetzten</h3>
		<ul>
			<li>Spitzname skizzieren</li>
			<li>verschiedene Graffiti am PC angucken und kommentieren</li>
			<li>3D-Style, Blöcke, Schatten, Highlights, 2nd Outlines, Backgrounds</li>
			<li>Taggen, Bubble Style & verscheidene Styles</li>
			<li>Skizzen fertigstellen</li>
			<li>Hintergrund ausdenken, farbig ausfüllen, eventuell Charakter/Figuren ausdenken</li>
		</ul>

		Wand streichen bzw. zum Sprühen vorbereiten
	</p>

	<p>
		<h3>3 - n. Tag - Sprühen:</h3>
		<ul>
			<li>Spraydosen → Unterschiede</li>
			<li>wie Sprühe ich?, Abstand zur Wand, Handhaltung, Linien ziehen, wo/wie absetzen?</li>
			<li>Caps: stärken, größe, dick, dünn, usw.</li>
			<li>Sprüheffekte</li>
			<li>wozu dient das schütteln der Dosen?: Vermeidung, dass Caps verstopfen und damit die Farbe gut pigmentiert ist</li>
		</ul>
	</p>

	<ol>
		<li>Grundbau der Buchstaben, dann modellieren (Grundlinien mit heller Farbe (z.B. himalayablau))</li>
		<li>modell nachziehen (beige oder hellgelb)</li>
		<li>Fill in</li>
		<li>Blöcke, 3D, Schatten, highlights, effekte</li>
		<li>Hintergrund</li>
		<li>Outline</li>
		<li>2nd Outline</li>
		<li>1st Outline nachziehen</li>
	</ol>
	'''

	@GET.codec('text/html')
	def _text_html(self, client):
		return client.data


class Zeitungsartikel(Resource):

	path = '/zeitungsartikel/'
	meta_description = 'Zeitungsartikel und Presseinformationen über Graffiti von Florian Best'

	@method
	def GET(self, client):
		return [{
			'src': '/zeitungsartikel/graffiti-in-neuem-glanz.jpg',
			'title': 'Graffiti in neuem Glanz',
			'source': 'Kreiszeitung Diepholz, 05. Dezember 2013, Seite 13',
		}, {
			'src': '/zeitungsartikel/sprayer-ganz-legal-im-bahnhof.jpg',
			'title': 'Sprayer ganz legal im Bahnhof',
			'source': 'Barnstorfer Wochenblatt, 13. Juli 2011, Titelseite',
		}, {
			'src': '/zeitungsartikel/techniken-der-graffiti-kunst.jpg',
			'title': 'Techniken der Graffiti Kunst',
			'source': 'Kreiszeitung Sommer 2010',
		}]

	@GET.codec('text/html')
	def _text_html(self, client):
		return '<p>%s</p>' % '\n'.join('''
			<span class="bordered">
				<img src="%(src)s" alt="%(title)s" title="%(title)s">
				<br>Quelle: %(source)s
			</span>''' % data for data in client.data)


class Kontakt(Resource):

	path = '/contact/'
	meta_description = 'Kontaktaufnahme zu Florian Best für Graffiti Auftragsarbeiten und Workshops oder Presse und anderes Interesse'

	@method
	def GET(self, client):
		return """Kontakt per Formular oder E-Mail-Adresse: graffiti at florianbest punkt de
<br/>
<br/>
<br/>
<form method="POST" accept-charset="UTF-8" enctype="application/x-www-form-urlencoded" name="contactform">
	<p>
	<label for="contact_tile">Title</label>
	<input name="title" type="radio" value="Mr." checked="checked">Mr.</input>
	<input name="title" type="radio" value="Mrs.">Mrs.</input>
	</p>

	<p>
	<label for="contact_name">Name</label>
	<input type="text" id="contact_name" name="name" />
	</p>

	<p>
	<label for="contact_from">E-Mail address</label>
	<input type="email" id="contact_form" name="from" required="required" />
	</p>

	<p>
	<label for="contact_website">Website</label>
	<input type="url" id="contact_website" name="website"/>
	</p>

	<p>
	<label for="contact_copy">Send me a copy</label>
	<input type="checkbox" name="copy" id="contact_copy" />
	</p>

	<p>
	<label for="contact_subject">Subject</label>
	<input type="text" name="subject" id="contact_subject"/>
	</p>

	<p>
	<label for="contact_message">Message</label>
	<textarea id="contact_message" name="message" required="required">&nbsp;</textarea>
	</p>

	<!-- TODO: captcha -->

	<p>
	<input type="submit" value="Send" />
	</p>
</form>""".encode('utf-8')
	GET.codec('text/html')

	@method
	def POST(self, client):
		def escape(s):
			return repr(s).lstrip('u')[1:-1]

		default_sender = unicode('bm9yZXBseUBmbG9yaWFuYmVzdC5kZQ=='.decode('base64'))
		receiver = unicode('Z3JhZmZpdGlAZmxvcmlhbmJlc3QuZGU='.decode('base64'))
		data = {}
		for key, val in dict(client.request.body.data).items():
			if isinstance(val, unicode):
				val = val.encode('latin-1', 'replace').decode('utf-8', 'replace')
			data[key] = val
		data.setdefault('copy', False)
		copy = data['copy'] == 'on'
		subject = escape(data.get('subject', u''))
		sender = escape(data.get('from', default_sender))
		if u'@' not in sender:
			copy = False
			sender = default_sender
		if data.get('name') and '<' not in data['name'] and '>' not in data['name']:
			sender = u'%s <%s>' % (escape(data['name']), sender)
			sender = sender.replace(u',', '')

		text = u'''Graffiti Contact form:
%s %s <%s> wrote a message via the contact form.
Website: %s
Copy: %s
Subject: %s
HTTP-Request: %s
IP-Address: %s
Hostname: %s
Date: %s
Message: %s
		'''
		try:
			text = text % (
				data['title'], data['name'], data['from'], data['website'], data['copy'],
				data['subject'], '\n'.join('%s: %s' % (escape(key), escape(val)) for key, val in client.request.headers.items()), client.remote.ip,
				client.remote.name, datetime.datetime.now().isoformat(), data['message']
			)
		except KeyError as exc:
			raise UNPROCESSABLE_ENTITY('Missing field: %r' % (str(exc),))

		message = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
		message['From'] = sender
		message['To'] = receiver
		message['Subject'] = subject
		if copy:
			message['CC'] = sender

		connection = smtplib.SMTP('localhost')
		connection.sendmail(sender, [receiver], message.as_string())
		connection.quit()
		return 'Vielen Dank für die E-Mail! Ich werde sobald wie möglich antworten.'
	POST.accept('application/x-www-form-urlencoded')
	POST.codec('text/html')


class Robots(Resource):

	path = '/robots.txt'

	@method
	def GET(self, client):
		return 'User-agent: *\nDisallow: /contact/'
	GET.codec('text/plain')

#class InAktion(Resource): pass
#class ProjektBewerbung(Resource): pass
#class MeineAnfaenge(Resource): pass
