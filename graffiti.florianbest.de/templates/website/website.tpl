<!DOCTYPE html>
<html lang="de" dir="ltr">
<head>
	<title>${title} - Graffiti von Florian Best</title>
	<base href="${base}"/>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

	<meta name="author" content="Florian Best"/>
	<meta name="robots" content="${meta_robots}"/>

	<meta name="description" content="${meta_description}"/>

	<link rel="shortcut icon" type="image/x-icon" href="/favicon.ico"/>
	<link rel="stylesheet" type="text/css" href="/css/graffiti.css"/>
</head>
<?python from genshi import HTML ?>
<body>
	<div id="margin">
		<div id="logo">&nbsp;</div>
		<div id="navigation">
			${HTML(navigation)}
		</div>
		<div id="content">
			<br/><h1>${title}</h1><br/>
			${HTML(content)}
		</div>
	</div>
	<p id="footer">
		Valid <a rel="nofollow" href="http://validator.w3.org/check?uri=referer">HTML5</a> and
		<a rel="nofollow" href="http://jigsaw.w3.org/css-validator/check/referer?profile=css3">CSS 3</a>
		| &copy; 2014 by Florian Best | <a href="/contact/" rel="nofollow">Impressum</a>
	</p>
</body>
</html>
