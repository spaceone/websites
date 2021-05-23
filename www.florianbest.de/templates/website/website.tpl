<html lang="${language}" dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" xmlns:xi="http://www.w3.org/2001/XInclude">
<?python from genshi import HTML ?>
<head>
	<title py:content="title" />
	<base py:if="False and base" href="${base}" />

	<py:for each="imeta in meta">
	<meta py:attrs="{imeta.var: imeta.value}" content="${imeta.content}" />
	</py:for>

	<py:for each="link in links">
	<link rel="${link.rel}" type="${link.type}" href="${link.href}" py:attrs="link.attrs"/>
	</py:for>

	<py:for each="script in scripts">
	<script type="${script.type}" py:attrs="script.attrs" py:content="script.content or '&nbsp;'">
		<!-- genshi bug -->
	</script>
	</py:for>

	<style py:if="inline_stylesheet">
	<![CDATA[
		${inline_stylesheet}
	]]>
	</style>
</head>
<body>
	<div id="margin">
		<xi:include href="../profile.tpl" />
		<xi:include href="../logo.tpl" />
		<xi:include href="../headnavi.tpl" />

		<div id="body">
			<py:with py:if="navigation" vars="side='left'">
				<xi:include href="../navi.tpl" />
			</py:with>
			<div id="middle" style="/*margin: 0 20px; background-color: #1C1C1C;*/">
				<xi:include href="../shell.tpl" />
				<div id="content">
					<xi:include py:if="False" href="../errors.tpl" />
					${HTML(content)}
				</div>
				<hr/>
				<p class="bottom">
					<a class="backbutton" href="#" onclick="window.history.back();" title="">${_('back')}</a>
				</p>
			</div>
			<py:with py:if="naviright" vars="side='naviright'">
				<xi:include href="../navi.tpl" />
			</py:with>
		</div>
		<div id="footer">
			<!--<hr style="margin: 0 auto;"/>-->
			<a href="/contact/">${_('contact')}</a>
			<a href="/impress/">${_('impress')}</a>
			<a href="/disclaimer/" py:if="not user.is_guest">${_('disclaimer')}</a>
			<a href="/sitemap/" py:if="not user.is_guest">${_('sitemap')}</a>
			<a href="/credits/" py:if="not user.is_guest">${_('credits')}</a>
			<a href="/todo/" py:if="not user.is_guest">${_('todo')}</a>
			<a href="https://github.com/spaceone/websites/blob/private/${source}" rel="noopener nofollow noreferrer" target="_blank">view page source</a>
			<a href="#" class="last">${_('bookmark')}</a>
		</div>
	</div>
	<!-- @end margin -->
	<p style="text-align: center;">
		Valid <a href="http://validator.w3.org/check?uri=referer">HTML5</a> and <a href="http://jigsaw.w3.org/css-validator/check/referer?profile=css3">CSS 3</a>
	</p>
</body>
</html>
