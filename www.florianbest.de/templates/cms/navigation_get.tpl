<div py:if="navigation" class="navigation" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" xmlns:xi="http://www.w3.org/2001/XInclude">
<ol class="navi">
	<li class="sec"><h2><a href="/">Home</a></h2><ul>
		<li class="cat_link"><a href="/">Home</a></li>
		<li class="cat_link"><a href="/header">HTTP-Header</a></li>
		<li class="cat_link"><a href="http://graffiti.florianbest.de/">Graffiti</a></li>
		<li class="cat_link"><a href="/login">Login</a></li>
	</ul></li>
	<li class="sec"><h2><a>CMS</a></h2><ul>
	<py:for each="navi in navigation">
		<li class="cat_link"><a href="${navi['url']}">${navi['title']}</a></li>
	</py:for>
	</ul></li>
</ol>
</div>

