<html xmlns:py="http://genshi.edgewall.org/" py:strip="">
<style type="text/css">td { border: thin solid #000; }</style>

<table style="border: 1px solid #000000" py:if="headers or params">
	<tr py:if="infos">
		<th>name</th>
		<th>information</th>
	</tr>

	<tr py:for="var, value in infos">
		<td>${var}</td>
		<td>
			<img style="height: 15px;" src="/images/SF/client/${value.image}.png" py:if="var in ('Operating System', 'Internet Service Provider', 'Browser')"/>
			${value}
		</td>
	</tr>
	<tr>
		<td colspan="2">&nbsp;</td>
	</tr>

	<tr py:if="headers">
		<th>header name</th>
		<th>header value</th>
	</tr>

	<tr py:for="var, value in headers">
		<td>${var}</td>
		<td>${value}</td>
	</tr>

	<tr>
		<td colspan="2">&nbsp;</td>
	</tr>

	<tr py:if="params">
		<th>querystring param name</th>
		<th>param value</th>
	</tr>

	<tr py:for="var, value in params">
		<td>${var}</td>
		<td>${value}</td>
	</tr>

</table>

</html>
