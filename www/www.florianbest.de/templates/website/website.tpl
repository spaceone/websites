<html lang="${language}" dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">
<?python from genshi import HTML ?>
<head>
	<title py:content="title" />
	<base py:if="base" href="${base}" />

	<py:for each="imeta in meta">
	<meta py:attrs="{imeta.var: imeta.value}" content="${imeta.content}" />
	</py:for>

	<!---<py:comment>
	<link rel="alternate stylesheet" href="/css/${sf.design}/print.css" title="PrintView" type="text/css"/>
	<link rel="stylesheet" href="/css/${sf.design}/print.css" type="text/css" media="print"/>
	</py:comment>-->

	<py:for each="link in links">
	<link rel="${link.rel}" type="${link.type}" href="${link.href}" />
	</py:for>

	<!--<py:comment>-->
<!--	[if lt IE 8]>
		<link rel="stylesheet" type="text/css" href="/css/${sf.design}/ie.css" />
	${HTML(u'%s' % (chr(60),))}![endif]-->
	<!--</py:comment>-->

	<style py:if="inline_stylesheet">
	<![CDATA[
		${inline_stylesheet}
	]]>
	</style>
</head>
<body>
	<!-- @start margin -->
	<div id="margin">
		<!-- @start profile -->
		<div id="profile" py:if="False">
			<p py:if="user.is_logged_in" class="fl">
				Hi ${user.ProfileLink};
				unseen:
				<a href="/pm">MSG's: <!-- {GWF_Notice::getUnreadPM($$user)}--></a>,
				<a href="/news">News: <!-- {GWF_Notice::getUnreadNews($$user)}--></a>,
				<a href="/forum">Forum: <!-- {GWF_Notice::getUnreadForum($$user, true)}--></a>,
				<a href="/links">Links<!-- {GWF_Notice::getUnreadLinks($$user)}--></a>
				<a href="/chall">Challenges: <!-- {GWF_Notice::getUnreadChallenges($$user)}--></a>
				<a href="/pagebuilder/news">Articles: <!-- {GWF_Notice::getUnreadPageBuilder($$user)}--></a>
				<a href="/comments/news">Comments: <!-- {GWF_Notice::getUnreadComments($$user)}--></a>
				<p class="fr">Last Login: <span class="color">{GWF_Time::displayTimestamp($$user->getVar('user_lastlogin'))}</span></p>
			</p>
			<!--{if ! $$user->isLoggedIn()}
			{GWF_Module::loadModuleDB('Login', true, true)->getMethod('Form')->setTemplate('shortlogin.tpl')->execute()}
			{/if}-->

			<p py:if="False" class="fr" style="width: auto;">
				<a href="$${SF->getIndex('print')}print"><img src="/images/SF/printer.png" alt="Druckansicht" title="Druckansicht"/></a>
				<a href="$${SF->getIndex('plain')}plain"><img src="/images/SF/paper.png" alt="HTML-Quelltext" title="Quelltext anzeigen"/></a>
				<a href="de/"><img src="/images/${iconset}/country/Germany.png" alt="[DE]" title="${_('change_language')}"/></a>
				<a href="en/"><img src="/images/${iconset}/country/UnitedStates.png" alt="[EN]" title="${_('change_language')}"/></a>
			</p>
		</div>
		<!-- @end profile -->
		<!-- @start logo -->
		<div id="logo">
			<span>
				 - the perfection of WebApplication -
			</span>
		</div>
		<!-- @end logo -->
		<!-- @start headnavi -->
		<div id="headnavi">
			<ol class="navi">
			<py:if test="user.is_logged_in">
				<li class="sec">
					<h2><a href="$${user->getProfileHREF()}">[$${user->display('user_name')}]</a></h2>
					<ul>
						<li class="cat"><h2>Settings:</h2></li>
						<li class="cat"><h2><a href="/account">Account</a></h2></li>
						<li class="cat"><h2><a href="/profile_settings">Profile</a></h2></li>
						<li class="cat"><h2><a href="/forum/options">Forum</a></h2></li>
						<li class="cat"><h2><a href="/pm/options">PM</a></h2></li>
					</ul>
				</li>
				<li py:if="user.is_admin" class="sec">
					<h2><a href="/nanny">[Admin]</a></h2>
					<ul>
						<li class="cat"><h2><a href="/nanny">Admin</a></h2></li>
						<li class="cat"><h2><a href="/Admin/Users">Benutzer</a></h2></li>
						<li class="cat"><h2><a href="/Admin/Groups">Gruppen</a></h2></li>
						<li class="cat"><h2><a href="/Admin/LoginAs?username=">Einloggen als</a></h2></li>
						<li class="cat"><h2><a href="/PageBuilder/Admin">CMS</a></h2></li>
					</ul>
				</li>
				<li class="sec">
					<h2><a href="/nanny">[Modules]</a></h2>
					<ul>
						<li class="cat"><h2><a href="/links">Links<!-- {GWF_Notice::getUnreadLinks($$user)}--></a></h2></li>
						<li class="cat"><h2><a href="/Links/Add?tag=">Link hinzufügen</a></h2></li>
						<li class="cat"><h2><a href="/forum">Forum<!-- {GWF_Notice::getUnreadForum($$user)}--></a></h2></li>
						<li class="cat"><h2><a href="/Forum/Unread">ungelesene</a></h2></li>
						<li class="cat"><h2><a href="/pm">PM<!-- {GWF_Notice::getUnreadPM($$user)}--></a></h2></li>
						<li class="cat"><h2><a href="/news">News<!-- {GWF_Notice::getUnreadNews($$user)}--></a></h2></li>
					</ul>
				</li>
				<li class="sec"><h2><a href="/logout">Logout</a></h2></li>
			</py:if>
			<py:if test="user.is_guest">
				<!--<li class="sec"><h2><a href="/news">News {GWF_Notice::getUnreadNews($$user)}</a></h2></li>
				<li class="sec"><h2><a href="/links">Links</a></h2></li>
				<li class="sec"><h2><a href="/forum">Forum</a></h2></li>
				<li class="sec"><h2><a href="/register">Register</a></h2></li>-->
				<li class="sec"><h2><a href="/">Home</a></h2></li>
				<li class="sec"><h2><a href="/header">HTTP-Header</a></h2></li>
				<li class="sec"><h2><a href="http://graffiti.florianbest.de/">Graffiti</a></h2></li>
				<li class="sec"><h2><a href="/login">Login</a></h2></li>
			</py:if>

			</ol>
<!--GWF_Navigation::getPageMenu()|indent:3:"\t"-->
<!--GWF_Module::loadModuleDB('Navigation')->execute()->getPageMenu()|indent:3:"\t"-->
		</div>
		<!-- @end headnavi -->
		<!-- @start body -->
		<div id="body">
			<!--@start left -->
			<div py:if="sf.display.navileft" id="left" class="navigation">
{include file="tpl/$${design}/navi.tpl" assign='navi_left' side='navileft' navigation="{SF_Navigation::display_navigation(SF_Navigation::SIDE_LEFT)}"}
$${navi_left|indent:4:"\t"}
			</div>
			<div py:if="False and not sf.display.navileft" id="left">
				<a href="$${SF->getIndex('navileft')}navileft=shown"><img style="margin: 10px 0; height: 10px;" src="/images/${iconset}/add.png" alt="[+]" title="Show Navigation"/></a>
			</div>
			<!-- @end left -->
			<!-- @start middle -->
			<div id="middle" style="margin: 0 20px; background-color: #1C1C1C;">
				<!-- @start shell -->
				<div py:if="sf.display.shell" id="smallshell" class="shell">
					<span class="fr">
						<a href="$${SF->getIndex('shell')}shell=hidden"><img style="margin: 10px 0; height: 10px;" src="/images/${iconset}/sub.png" alt="[-]" title="Hide Shell"/></a>
					</span><br/>
					<!--{assign var="month" val="$$SF->langA('monthnames', date('n'))"}
					{array( $$SF->langA('daynames', date('w')), date('w'), $$month, date('n'), date('Y')))}|-->
					<pre class="logo" id="shell_logo">
    					.--.      _____________________________________________________________
   					   |o_o |    /    WELCOME TO       $${_(SF::greeting())}                            \
   					   |:_/ | --&lt;|       WWW.FLORIAN     $${_('today_is_the', array( $$SF->langA('daynames', date('w')), date('w'), $$SF->langA('monthnames', date('n')), date('n'), date('Y')))}|
  					  //   \ \   \           BEST.DE !!!  Es ist {date('G:i:s')} Uhr                   /
 					 (|     | )   --------------------------------------------------------------
					/'\_   _/`\ type in ´help´ for
					\___)=(___/  a list of commands!
					</pre>
					$${logo}
					<form method="GET" action="index.php">
						<p class="shell">
							<span class="bold shell_{if $$user->isAdmin()}admin{else}user{/if}">$${user->displayUsername()}@$${smarty.server.SERVER_NAME}</span>
							<span class="bold shell_dir">$${smarty.server.REQUEST_URI|escape}{if $$user->isAdmin()} # {else} $$ {/if}</span>
							<input type="text" size="8" value="cmd" name="cmd" class="shell border"/>
							<input type="hidden" name="mo" value="SF"/>
							<input type="hidden" name="me" value="Shell"/>
							<input type="submit" value=" " name="submit" class="shell"/>
							<br/><br/>
						</p>
					</form>
				</div>
				<!-- @end shell -->
				<span py:if="False and not sf.display.shell" class="fr">
					<a href="$${SF->getIndex('shell')}shell=shown"><img style="margin: 10px 0; height: 10px;" src="/images/${iconset}/add.png" alt="[+]" title="Show Shell"/></a>
				</span>
				<!-- @start content -->
				<div id="content" class="inhalt {if $$SF->getMoMe('SF_Shell')}shell{/if}">
				<!-- @begin errormessages -->
<!-- ${errors}-->
				<!-- @end errormessages -->
					${HTML(content)}
				</div>
				<!-- @end content -->
				<hr/>
				<!--<p class="bottom">
					<a class="backbutton" href="{GWF_Session::getLastURL()|escape}" title="{GWF_Session::getLastURL()|escape}">${_('back')} ({GWF_Session::getLastURL()|escape})</a>
				</p>-->
			</div>
			<!-- @end middle -->
			<!-- @start right -->
			<div py:if="sf.display.naviright" id="right" class="navigation">
{include file="tpl/$${design}/navi.tpl" assign='navi_right' side='naviright' navigation="{SF_Navigation::display_navigation(SF_Navigation::SIDE_LEFT)}"}
$${navi_right|indent:4:"\t"}
			</div>
			<div py:if="False and not sf.display.naviright" id="right">
				<a href="$${SF->getIndex('naviright')}naviright=shown"><img style="margin: 10px 0; height: 10px;" src="/images/${iconset}/add.png" alt="[+]" title="Show Navigation"/></a>
			</div>
		<!-- @end right -->
		</div>
		<!-- @end body -->
		<!-- @start copyright -->
		<div py:if="False" id="copyright">
			<p class="copyright">
				SPACE-Framework is copyright by
				<a href="/profile/space" title="space's profile">Florian Best</a>
			</p>
			<py:if test="sf.display.details">
			<!-- @start shortdetails -->
			<p class="copyright fl" style="text-align: left; width: 50%;">
				$${user->displayProfileLink()}
				{GWF_ClientInfo::imgCountry()}{GWF_ClientInfo::getIPAddress()};
				{GWF_ClientInfo::imgOperatingSystem()}{GWF_ClientInfo::displayOperatingSystem()};
				{GWF_ClientInfo::imgBrowser()}{GWF_ClientInfo::displayBrowser()};
				{GWF_ClientInfo::imgProvider()}{GWF_ClientInfo::displayProvider()}
			</p>
			<p class="copyright fl" style="text-align: right; width: 50%;">
				<py:for each="dc in ('red', 'blue', 'green', 'orange')">
				<a title="$${_('designcolor', $$SF->lang($$dc))}" href="$${SF->getIndex('layoutcolor')}layoutcolor=$${dc}">
					<img src="/images/SF/circle_${dc}.png" alt="$${_('designcolor', $$SF->lang($$dc))}"/>
				</a>
				</py:for>
				<a href="$${SF->getIndex('details')}details=shown">
					<img src="/images/${iconset}/add.png" alt="[+]" title="Show Details"/>
				</a>
			</p>
			</py:if>
			<p py:if="False and not sf.display.details" class="copyright fr">
				<a href="$${SF->getIndex('details')}details=hidden"><img style="margin: 10px 0; height: 10px;" src="/images/${iconset}/sub.png" alt="[+]" title="Hide Details"/></a>
			</p>
		</div>
		<!-- @end copyright -->
		<!-- @start details -->
		<div py:if="sf.display.details" id="details">
			<table>
				<tr>
					<th>$${_('visitor')|upper}</th>
					<th>$${_('surfer_infos')|upper}</th>
					<!--<th>$${_('statistics')|upper}</th>
			<th>$${_('server')|upper}</th>
					<th>$${_('donations')|upper}</th>-->
				</tr>
				<tr>
					<td>
						${_('ct_online_atm')}, array(GWF_Notice::getOnlineUsers()))}<br/>
						${_('ct_vis_total')}<br/>
						${_('ct_vis_today')}<br/>
						${_('ct_vis_yesterday')}<br/>
						${_('ct_online_today')}<br/>
						${_('ct_online_total')}<br/>
					</td>
					<td>
            			<!--$$lang['screen_resolution']}: <span class="color"><script language="JavaScript">document.write(screen.width+'x'+screen.height);</script> Pixel</span><br/>-->
						<span class="color">${_('country')}, array(GWF_ClientInfo::imgCountryByIP(), GWF_ClientInfo::displayCountryByIP()))}</span><br/>
						<span class="color">${_('ip')}, array(GWF_ClientInfo::getIPAddress()))}</span><br/>
						<span class="color">${_('operating_system')}, array(GWF_ClientInfo::imgOperatingSystem(), GWF_ClientInfo::displayOperatingSystem()))}</span><br/>
						<span class="color">${_('browser')}, array(GWF_ClientInfo::imgBrowser(), GWF_ClientInfo::displayBrowser()))}</span><br/>
						<span class="color">${_('provider')}, array(GWF_ClientInfo::imgProvider(), GWF_ClientInfo::displayProvider()))}</span><br/>
						<span class="color">${_('hostname')}, array(GWF_ClientInfo::getHostname()))}</span><br/>
						<span class="color">${_('referer')}, array(GWF_ClientInfo::getReferer()))}</span><br/>
						<span class="color">${_('user_agent')}, array(GWF_ClientInfo::getUserAgent()))}</span>
					</td>
			<!--TODO: challenges-->
			<!--TODO: switch Design-->
			<!--TODO: statistics -->
			<!--TODO: new layout -->
				</tr>
			</table>
		</div>
		<!-- @end details -->
		<!-- @start footer -->
		<div id="footer">
			<!-- TODO: generic -->
			<!--<hr style="margin: 0 auto;"/>-->
			<a href="/contact/">${_('contact')}</a>
			<a href="/impress/">${_('impress')}</a>
			<a href="/disclaimer/">${_('disclaimer')}</a>
			<a href="/sitemap/">${_('sitemap')}</a>
			<a href="/roadmap/">${_('roadmap')}</a>
			<a href="/changelog/">${_('changelog')}</a>
			<a href="/credits/">${_('credits')}</a>
			<a href="/helpdesk/">${_('helpdesk')}</a>
			<a href="/todo/">${_('todo')}</a>
			<a href="/project/">${_('project')}</a>
			<a href="#" class="last">${_('bookmark')}</a>
		</div>
		<!-- @end footer -->
	</div>
	<!-- @end margin -->
	<!-- @start debug-->
	<p style="text-align: center;">
	<!--!	SQL: $${timings['t_sql']|string_format:"%.03f"}s ($${timings['queries']} Queries);
		PHP: $${timings['t_php']|string_format:"%.03f"}s;
		TOTAL: $${timings['t_total']|string_format:"%.03f"}s;<br/>
		MEM PHP: $${timings['mem_php']|filesize:"2":"1024"};
		MEM USER: $${timings['mem_user']|filesize:"2":"1024"};
		MEM TOTAL: $${timings['mem_total']|filesize:"2":"1024"};<br/>
		SPACE FREE: $${timings['space_free']|filesize:"2":"1024"}
		SPACE USED: $${timings['space_used']|filesize:"2":"1024"}
		SPACE TOTAL: $${timings['space_total']|filesize:"2":"1024"}<br/>
		<br/>-->
		Valid <a href="http://validator.w3.org/check?uri=referer">HTML5</a> and <a href="http://jigsaw.w3.org/css-validator/check/referer?profile=css3">CSS 3</a>
	</p>
	<!-- @end debug -->
</body>
</html>
