<html xmlns:py="http://genshi.edgewall.org/" py:strip="">
<?python from genshi import HTML ?>
	<section class="page">
		<header>
			<h1 class="title" py:content="title"/>
			<div class="creation" py:if="creation_date">
				<span py:strip="">created on</span>: ${creation_date}
			</div>
		</header>
		<article py:content="HTML(content)" />
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
	<form method="DELETE" py:if="not user.is_guest">
		<input type="button" value="Delete"/>
	</form>
</html>
