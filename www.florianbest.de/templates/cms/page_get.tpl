<html xmlns:py="http://genshi.edgewall.org/" py:strip="">
<?python from genshi import HTML ?>
<?python from markdown import markdown ?>
	<script type="text/javascript" py:if="not user.is_guest">
$(document).ready(function() {
	$('form[method="DELETE"]').submit(function(e) {
		var form = $(this);

		e.preventDefault();
		$.ajax({
			type: form.attr('method'),
			url: form.attr('action'),
			data: form.serialize()
		}).done(function(data) {
			$('#content').empty().append(data);
		}).fail(function(data) {
			$('#content').append(data.responseText)
		});
	});
});
	</script>
	<section class="page">
		<header>
			<h1 class="title" py:content="title"/>
			<div class="creation" py:if="creation_date">
				<span py:strip="">created on</span>: ${creation_date}
			</div>
		</header>
		<article py:content="HTML(markdown(content))" />
		<footer>
			<div class="author" py:if="author">
				<span py:strip="">author</span>: ${author}
			</div>
			<div class="modify_date" py:if="modify_date">
				<span py:strip="">last modified</span>: ${modify_date}
			</div>
			<div class="views" py:if="views">
				<span>page views</span>: ${views}
			</div>
		</footer>
	</section>
	<form method="DELETE" action="${url}" accept-charset="UTF-8" enctype="application/x-www-form-urlencoded" py:if="not user.is_guest">
		<input type="submit" value="Delete"/>
	</form>
	<a rel="edit-form" href="${rel['edit-form']}" py:if="not user.is_guest">
		Modify
	</a>
</html>
