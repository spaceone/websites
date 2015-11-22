		<div id="profile" py:if="False" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">
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

