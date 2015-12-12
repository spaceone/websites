# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from circuits.http.server.resource import method

from .base import Resource


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
				Nun, 5 Jahre nach meiner ersten Auftragsarbeit, kann ich auf einige Erfahrungen zurückgreifen und biete meine Dienste an.
			</p>
			<p>
				Ganz gleich, ob Partykeller, Garagentor oder Wohnzimmerwand - für jede Atmosphäre gestalte ich passende Motive,
				die persönlichen Vorstellungen entsprechen.
			</p>
			<p>
				Des weiteren biete ich auch Zeichnungen auf Papier, Graffiti-body-painting und Schriftgestaltung an.
			</p>
			<p>
				Bei Interesse jeglicher Art, kann ich über das <a href="/contact/">Kontaktformular dieser Website</a> kontaktiert werden.
				Nach Absprache bin ich auch gerne bereit für Telefonate oder persönliche Gespräche.
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

	images = {
		'2011_Space_DB_final1': dict(title='Space - Juli 2011 - in der Eingangshalle vom Bahnhof Barnstorf'),
		'2011_Space_DB_final2': dict(title=''),
		'2010_Space_DB_final': dict(
			content='Space - Juni 2010 - Deutsche Bahn Brücke in Barnstorf <br> Abschlusswerk meines Graffiti Workshops',
			title='Deutsche Bahn Brücke'
		),
		'2010_Space_DB_final2': dict(title=''),
		'2010_Space_DB_43': dict(title=''),
		'2010_Space_JZB_final2': dict(title='Space - 2010 - Jugendzentrum Barnstorf<br><br>'),
		'2010_JZB_final': dict(title='JZB - 2010 - Eingang des Jugendzentrum Barnstorf'),
		'2010_JZB_6': dict(title='')
	}

	@method
	def GET(self, client):
		return [dict(url=url, title=image['title'], content=image.get('content', image['title'])) for url, image in self.images.items()]

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
			<li>Welches Interesse besteht an der Teilnahme?
			<li>Wer hatte schon mit Graffiti oder Kunst zu tun.
			<li>Wünsche und Fragen klären</li>
			<li>Handschrift ansehen</li>
			<li>Bleistifthaltung lernen</li>
			<li>Buchstaben:
			<li>Grundaufbau -> woraus bestehen Buchstaben?,
			<li>Dreiecke, Rechtecke, Quadrate, Kreise, Halbkreise, Linien üben
			<li>Einteilung von Buchstaben in sinngemäße Balken</li>
		</ul>
	</p>

	<p>
		Übung:
		<ul>
			<li>Zeichnung von Buchstaben mit Bleistift (!), ohne Lineal & Geodreieck,
			<li>Proportioneneinteilung mittels Einteilung des Blatts durch Linie,
			<li>Schräge und krumme Linien sind erstmal nicht schlimm.
			<li>gerade Linien üben,
			<li>stabile Buchstaben
			<li>niemals kritzeln (!),
			<li>nicht durchstreichen,
			<li>gleichmäßigkeit und synchrone Buchstaben,
			<li>Gefühl für Buchstaben entwickeln,
			<li>mit Fineliner fertige buchstaben nachziehen.
			<li>Kugelschreiber sind für kritzeleien!
		</ul>
	</p>

	<p>
		Buchstaben (metamorphose):
		<ol>
			<li>Erweiterung, kaligraphische und schöne buchstaben, eindrucksvoll wirken lassen, Blockige Buchstaben
			<li>abstrakter werden, strecken, ziehen, transformieren, dicke und dünne bearbeiten, wichtigkeit der einzelnen Buchstabenteile
			<li>4-fach Linien, modellieren, dinge anhängen, Elemente repertuare lernen, Pfeile ausdrucksvoll wirken lassen, das Auge schulen (!)
			<li>mit Filzstift nachziehen
		</ol>

		freiwillige Hausaufgabe: Üben, lernen, skizzieren.
	</p>

	<p>
		<h3>2. Tag - Spitzname als Graffiti umsetzten</h3>
		<ul>
			<li>Spitzname skizzieren
			<li>verschiedene Graffiti am PC angucken und kommentieren
			<li>3D-Style, Blöcke, Schatten, Highlights, 2nd Outlines, Backgrounds
			<li>Taggen, Bubble Style & verscheidene Styles
			<li>Skizzen fertigstellen
			<li>Hintergrund ausdenken, farbig ausfüllen, eventuell Charakter/Figuren ausdenken
		</ul>

		Wand streichen bzw. zum Sprühen vorbereiten
	</p>

	<p>
		<h3>3 - n. Tag - Sprühen:</h3>
		<ul>
			<li>Spraydosen → Unterschiede
			<li>wie Sprühe ich?, Abstand zur Wand, Handhaltung, Linien ziehen, wo/wie absetzen?
			<li>Caps: stärken, größe, dick, dünn, usw.
			<li>Sprüheffekte
			<li>wozu dient das schütteln der Dosen?: Vermeidung, dass Caps verstopfen und damit die Farbe gut pigmentiert ist
		</ul>
	</p>

	<ol>
		<li>Grundbau der Buchstaben, dann modellieren (Grundlinien mit heller Farbe (z.B. himalayablau))
		<li>modell nachziehen (beige oder hellgelb)
		<li>Fill in
		<li>Blöcke, 3D, Schatten, highlights, effekte
		<li>Hintergrund
		<li>Outline
		<li>2nd Outline
		<li>1st Outline nachziehen
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
		return '''<br>Formular wird gerade überarbeitet:
			vorläufige E-Mail-Adresse: graffiti at florianbest punkt de<br><br><br><br>'''.encode('utf-8')
	GET.codec('text/html')


class Robots(Resource):

	path = '/robots.txt'

	@method
	def GET(self, client):
		return 'User-agent: *\nDisallow: /contact/'
	GET.codec('text/plain')

#class InAktion(Resource): pass
#class ProjektBewerbung(Resource): pass
#class MeineAnfaenge(Resource): pass
