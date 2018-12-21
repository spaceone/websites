<!DOCTYPE html>
<html lang="de" dir="ltr" xmlns:py="http://genshi.edgewall.org/">
<head>
	<title>Graffiti - www.FlorianBest.de</title>
	<base href="${base}"/>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

	<meta name="author" content="Florian Best"/>
	<meta name="robots" content="index, follow"/>
	<meta name="googlebot" content="index, follow"/>

	<meta name="description" content="Graffiti Auftragsarbeiten von Florian Best im Kreis Diepholz, Barnstorf, Bremen"/>

	<link rel="shortcut icon" type="image/x-icon" href="/favicon.ico"/>
	<link rel="stylesheet" type="text/css" href="/css/design.css"/>
	<link rel="stylesheet" type="text/css" href="/css/layout.css"/>
	<link rel="stylesheet" type="text/css" href="/css/format.css"/>
</head>
<body>
	<div id="margin">
		<div id="logo">&nbsp;</div>
		<div id="body">
			<div id="left" class="navigation">
			</div>
			<div id="content">
				<h1>HTTP Error ${status} - ${reason}</h1>
				<p py:if="description">${description}</p>
				<!--!
				<?python from genshi import HTML ?>
				<p py:if="traceback">
					<br py:for="line in traceback.splitlines()" py:content="line.replace(' ', HTML('&nbsp;'))"/>
				</p>-->
				<pre py:if="status >= 500 and traceback" py:content="traceback"/>
			</div>
		</div>
	</div>
	<p style="text-align: center;">
		Valid <a href="http://validator.w3.org/check?uri=referer">HTML5</a> and
		<a href="http://jigsaw.w3.org/css-validator/check/referer?profile=css3">CSS 3</a>
	</p>
</body>
</html>
