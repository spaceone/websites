<html xmlns:py="http://genshi.edgewall.org/" py:strip="">
	<?python from genshi import HTML ?>
	<?python from markdown import markdown ?>
	<noscript>
		This formular requires Javascript. Please enable it!
	</noscript>
	<script type="text/javascript">
$(document).ready(function() {
	$('form[rel="edit-form"]').submit(function(e) {
		var form = $(this);

		e.preventDefault();
		$.ajax({
			type: form.attr('method'),
			url: form.attr('action'),
			data: form.serialize()
		}).done(function(data) {
			location.reload();
		}).fail(function(data) {
			$('#content').append(data.responseText)
		});

		e.preventDefault();
	});
});
	</script>
	<hr/>
	<article py:content="HTML(markdown(page['content']))" />
	<p>
		<a href="${page['url']}">View page</a>
	</p>
	<hr/>
	<form method="PUT" action="${page['url']}" rel="edit-form" accept-charset="UTF-8" enctype="application/x-www-form-urlencoded">
		<py:for each="field in fields">
			<py:choose test="field['type']">
		<p>
			<label for="${field['attrs']['name']}">${field['label']}</label>
			<textarea py:when="'textarea'" py:content="field['content']" py:attrs="field['attrs']"/>
			<input py:otherwise="" py:content="field['content']" py:attrs="field['attrs']"/>
		</p>
			</py:choose>
		</py:for>
		<input type="submit" value="Modify" />
	</form>
	<form method="DELETE" action="${page['url']}" accept-charset="UTF-8" enctype="application/x-www-form-urlencoded">
		<input type="submit" value="Remove" />
	</form>
</html>
