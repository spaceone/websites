<html xmlns:py="http://genshi.edgewall.org/" py:strip="">
<h1>HTTP Error ${status} - ${reason}</h1>
<p py:if="description">${description}</p>
<!--!
<?python from genshi import HTML ?>
<p py:if="traceback">
	<br py:for="line in traceback.splitlines()" py:content="line.replace(' ', HTML('&nbsp;'))"/>
</p>-->
<pre py:if="status >= 500 and traceback" py:content="traceback"/>
</html>
