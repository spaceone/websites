<div py:if="pages" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" xmlns:xi="http://www.w3.org/2001/XInclude">
<ul>
	<py:for each="page in pages">
		<li><a href="${page['url']}">${page['title']}</a></li>
	</py:for>
</ul>
<a href="${rel['create-form']}" rel="create-form">Create Page</a>
</div>
