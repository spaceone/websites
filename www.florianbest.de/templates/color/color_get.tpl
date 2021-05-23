:root {
	--base-color: ${base_color};
	--design-dark: ${design_dark};
	--design-light: ${design_light};
	--border-dark: ${border_dark};
	--border-light: ${border_light};
}

.top {
	background-image: url('/images/${design}/${layout}/contenthead.png');
}
div#logo {
	background: #131313 url('/images/${design}/${layout}/${base_color}/header.png') no-repeat center right;
}
fieldset
{
	background: transparent url('/images/${design}/${layout}/${base_color}/trans.png');
}

/*--------------------------- NAVIGATION ---------------------------*/
div.navigation li.subcat_link,
div.navigation li.sec_link,
div.navigation li.cat_link {
	list-style-image: url('/images/${design}/${layout}/${base_color}/round.png');
}
div.navigation li.subcat_link:hover,
div.navigation li.sec_link:hover,
div.navigation li.cat_link:hover {
	list-style-image: url('/images/${design}/${layout}/${base_color}/navi.png');
}
div.navigation li.cat, div.navigation li.subcat {
	list-style-image: url('/images/${design}/${layout}/${base_color}/navi.png');
}
div.navigation li.cat:hover, div.navigation li.subcat:hover {
	list-style-image: url('/images/${design}/${layout}/${base_color}/down.png');
}
div.navigation li.subcat:hover > ul {
	list-style-image: url('/images/${design}/${layout}/${base_color}/down.png');
}
/*
div.navigation > ol.navi > li.sec > ul > li.cat > ul > li:hover:before {
	content: url('/images/${design}/${layout}/${base_color}/navi.png');
}
*/
div.navigation > ol.navi > li.sec > ul > li.cat:hover {
	list-style-image: url('/images/${design}/${layout}/${base_color}/down.png');
}

div.navigation > ol.navi > li.sec > ul > li.cat > ul > li {
	list-style-image: url('/images/${design}/${layout}/${base_color}/round.png');
}

div.navigation > ol.navi > li.sec > ul > li.cat > ul > li:hover,
div.navigation > ol.navi > li.sec > ul > li.cat {
	list-style-image: url('/images/${design}/${layout}/${base_color}/navi.png');
}
