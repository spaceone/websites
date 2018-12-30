<html xmlns:py="http://genshi.edgewall.org/" py:strip="">
<style type="text/css">td { border: thin solid #000; }</style>

<table style="border: 1px solid #000000" py:if="headers or params">
	<tr py:if="infos">
		<th>Name</th>
		<th>Information</th>
	</tr>

	<tr py:for="var, val in infos">
		<td>${var}</td>
		<td>
			<py:for each="value in (val if isinstance(val, list) else [val])">
				<img style="height: 15px;" src="/images/${value.image}.png" title="${value}" alt="${value}" py:if="hasattr(value, 'image')"/>
				${value}
			</py:for>
		</td>
	</tr>
	<tr>
		<td>Screen resolution</td>
		<td>
			<script type="text/javascript">document.write(screen.width + 'x' + screen.height);</script>
			<noscript>Unknown</noscript>
		</td>
	</tr>
	<tr>
		<td colspan="2">&nbsp;</td>
	</tr>

	<tr py:if="headers">
		<th>Header name</th>
		<th>Header value</th>
	</tr>

	<tr py:for="var, value in headers">
		<td>${var}</td>
		<td>${value}</td>
	</tr>

	<tr>
		<td colspan="2">&nbsp;</td>
	</tr>

	<tr py:if="params">
		<th>Querystring param name</th>
		<th>Param value</th>
	</tr>

	<tr py:for="var, value in params">
		<td>${var}</td>
		<td>${value}</td>
	</tr>

	<tr>
		<td colspan="2">&nbsp;</td>
	</tr>

	<tr py:if="server">
		<th>Server information</th>
		<th></th>
	</tr>

	<tr py:for="var, value in server">
		<td>${var}</td>
		<td>${value}</td>
	</tr>

</table>

</html>
