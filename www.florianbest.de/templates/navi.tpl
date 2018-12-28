<div py:if="navigation" id="${side}" class="navigation" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" xmlns:xi="http://www.w3.org/2001/XInclude">
<p class="top" style="background-image: url('/images/${design}/${layout}/navi${side}head.png');">
<!--	<a href="${SF->getIndex($side)}${side}=hidden"><img src="${root}img/${iconset}/sub.png" alt="[-]" title="Hide Navigation"></a>-->
</p>
<!--<hr/>-->
<ol class="navi">
${navigation}
	<li class="sec"><h2><a href="/">Home</a></h2><ul>
		<li class="cat_link"><a href="/">Home</a></li>
		<li class="cat_link"><a href="/header">HTTP-Header</a></li>
		<li class="cat_link"><a href="http://graffiti.florianbest.de/">Graffiti</a></li>
		<li class="cat_link"><a href="/login">Login</a></li>
	</ul></li>
</ol>
<!--<hr/>-->
<p class="bottom"></p>
</div>
