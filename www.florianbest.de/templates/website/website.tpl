<html lang="${language}" dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" xmlns:xi="http://www.w3.org/2001/XInclude">
<?python from genshi import HTML ?>
<head>
	<title py:content="title" />
	<base py:if="False and base" href="${base}" />

	<py:for each="imeta in meta">
	<meta py:attrs="{imeta.var: imeta.value}" content="${imeta.content}" />
	</py:for>

	<py:for each="link in links">
	<link rel="${link.rel}" type="${link.type}" href="${link.href}" py:attrs="link.attrs"/>
	</py:for>

	<style py:if="inline_stylesheet">
	<![CDATA[
		${inline_stylesheet}
	]]>
	</style>
</head>
<body>
	<div id="margin">
		<xi:include href="../profile.tpl" />
		<xi:include href="../logo.tpl" />
		<xi:include href="../headnavi.tpl" />

		<div id="body">
			<py:with py:if="navigation" vars="side='left'">
				<xi:include href="../navi.tpl" />
			</py:with>
			<div id="middle" style="/*margin: 0 20px; background-color: #1C1C1C;*/">
				<xi:include href="../shell.tpl" />
				<div id="content" class="inhalt">
					<xi:include py:if="False" href="../errors.tpl" />
					${HTML(content)}
				</div>
				<hr/>
				<p class="bottom">
					<a class="backbutton" href="#" onclick="window.history.back();" title="">${_('back')}</a>
				</p>
			</div>
			<py:with py:if="naviright" vars="side='naviright'">
				<xi:include href="../navi.tpl" />
			</py:with>
		</div>
		<!-- @start copyright -->
		<div py:if="False" id="copyright">
			<p class="copyright">
				SPACE-Framework is copyright by
				<a href="/profile/space" title="space's profile">Florian Best</a>
			</p>
			<py:if test="details">
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
			<p py:if="False and not details" class="copyright fr">
				<a href="$${SF->getIndex('details')}details=hidden"><img style="margin: 10px 0; height: 10px;" src="/images/${iconset}/sub.png" alt="[+]" title="Hide Details"/></a>
			</p>
		</div>
		<!-- @end copyright -->
		<!-- @start details -->
		<div py:if="details" id="details">
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
<!--			<a href="/disclaimer/">${_('disclaimer')}</a>
			<a href="/sitemap/">${_('sitemap')}</a>
			<a href="/roadmap/">${_('roadmap')}</a>
			<a href="/changelog/">${_('changelog')}</a>
			<a href="/credits/">${_('credits')}</a>
			<a href="/helpdesk/">${_('helpdesk')}</a>
			<a href="/todo/">${_('todo')}</a>
			<a href="/project/">${_('project')}</a>-->
			<a href="https://github.com/spaceone/websites/blob/private/${source}" rel="nofollow noreferrer" target="_blank">view page source</a>
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
