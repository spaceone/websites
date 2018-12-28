<html xmlns:py="http://genshi.edgewall.org/" py:strip="">
	<form method="POST" action="${rel['create-form']}" rel="create-form" accept-charset="UTF-8" enctype="application/x-www-form-urlencoded">
		<py:for each="field in fields">
			<py:choose test="field['type']">
		<p>
			<label for="${field['attrs']['name']}" title="${field['description']}">${field['label']}</label>
			<textarea py:when="'textarea'" py:content="field['content']" py:attrs="field['attrs']"/>
			<input py:otherwise="" py:content="field['content']" py:attrs="field['attrs']"/>
		</p>
			</py:choose>
		</py:for>
		<input type="submit" value="Create" />
	</form>
</html>

