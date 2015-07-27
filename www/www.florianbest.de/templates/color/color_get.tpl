.top {
	background-image:url('/images/${design}/${layout}/contenthead.png');
}

/*- ------------------------ MAIN THINGS AND ID's ------------------------*/
div#margin { /* BORDER HIGHLIGHT EFECT*/
	background-color: ${border_light};
	border: thin solid ${border_dark};
}
div#logo {
	background: #131313 url('/images/${design}/${layout}/${base_color}/header.png') no-repeat center right;
	border-top: thin groove ${design_dark};
}
div#logo span {
	background-color: ${design_light};
}
/*div#footer*/
div#profile,
div#body {
	border-top: thin groove ${design_dark};
}

.navigation hr,
#inhalt hr,
textarea,
input,
div.sitenav {
	background-color: ${design_dark};
}
/*p.bottom,
p.top,*/
#sitenav a:hover span,
fieldset,
fieldset legend {
	border: thin solid ${design_light};
}
fieldset
{
	background:transparent url('/images/${design}/${layout}/${base_color}/trans.png');
}

/* ------------------------------ LAYOUT ---------------------------- */
.color,
#inhalt p:first-letter {
	color: ${design_dark};
}
a,
a.backbutton,
div#profile a,
div#copyright a,
div#details a,
div#footer,
.inhalt a,
.inhalt a:visited,
.inhalt a:active,
.inhalt a:hover,
.navigation a:hover {
	color: ${design_light};
}

hr {
	border-bottom: thin solid ${design_dark}!important;
}

/*--------------------------- HEADNAV -------------------------------*/
ol.navi h2 > a:first-letter,
div#headnavi > ol.navi > li.sec > ul > li:hover > a,
div#headnavi > ol.navi > li.sec > ul > li > ul li:hover > a,
div#headnavi * a:hover,
div#headnavi > ol.navi > li.sec > h2 > a:first-letter,
div#headnavi > ol.navi > li.sec > h2:hover {
	color: ${design_dark} !important;
}

div#headnavi > ol.navi > li > ul,
div#headnavi > ol.navi > li > ul > li > ul {
	border: thin solid ${design_dark};
}
div#headnavi > ol.navi > li > ul > li.sub:after {
	background-color: ${border_light};
}
div#headnavi > ol.navi > li > ul > li > ul > li {
	border-top: thin solid ${design_light};
	border-bottom: thin solid ${design_dark};
	border-left: thin solid #1c1c1c;
	border-right: thin solid #131313;
}
div#headnavi > ol.navi > li > ul > li.sub:hover:after {
	background-color: ${design_dark};
}

/*--------------------------- NAVIGATION ---------------------------*/

div.navigation li.subcat_link,
div.navigation li.sec_link,
div.navigation li.cat_link {
	list-style-image:url('/images/${design}/${layout}/${base_color}/round.png');
}
div.navigation li.subcat_link:hover,
div.navigation li.sec_link:hover,
div.navigation li.cat_link:hover {
	list-style-image:url('/images/${design}/${layout}/${base_color}/navi.png');
}
div.navigation li.cat, div.navigation li.subcat {
	list-style-image:url('/images/${design}/${layout}/${base_color}/navi.png');
}
div.navigation li.cat:hover, div.navigation li.subcat:hover {
	list-style-image:url('/images/${design}/${layout}/${base_color}/down.png');
}
div.navigation li.subcat:hover > ul {
	list-style-image:url('/images/${design}/${layout}/${base_color}/down.png');
}
/*
div.navigation > ol.navi > li.sec > ul > li.cat > ul > li:hover:before {
	content: url('/images/${design}/${layout}/${base_color}/navi.png');
}
*/
div.navigation > ol.navi > li.sec > ul > li.cat:hover { list-style-image:url('/images/${design}/${layout}/${base_color}/down.png');
}

div.navigation > ol.navi > li.sec > ul > li.cat > ul > li { list-style-image:url('/images/${design}/${layout}/${base_color}/round.png');
}

div.navigation > ol.navi > li.sec > ul > li.cat > ul > li:hover,
div.navigation > ol.navi > li.sec > ul > li.cat { list-style-image: url('/images/${design}/${layout}/${base_color}/navi.png');
}

div.navigation > ol.navi > li.sec > ul > li.cat:target > ul {
	border: thin solid ${design_dark};
	border-right: thin solid ${design_light};
}
div.navigation > ol.navi > li.sec > ul > li.cat:target {
	background-color: ${design_light};
}
div.navigation > ol.navi > li.sec > ul > li.cat:hover > ul {
	border: thin solid ${design_light};
	border-right: thin solid ${design_dark};
}

div.navigation > ol.navi > li.sec > ul > li.cat:hover {
	background-color: ${design_dark};
}
