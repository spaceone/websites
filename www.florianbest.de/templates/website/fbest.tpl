<html lang="${language}" dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">
<head>
	<title py:content="title" />
	<base py:if="base" href="${base}" />
	<meta py:for="meta_entry in meta" py:attrs="{meta_entry.var: meta_entry.value}" content="${meta_entry.content}" />
	<link py:for="link in links" rel="${link.rel}" type="${link.type}" href="${link.href}" />
</head>
<?python from genshi import HTML ?>
<body py:content="HTML(content)">
</body>
</html>
