		<div id="headnavi"  xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">
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
				<li class="sec"><h2><a href="/saml/logout">SAML Logout</a></h2></li>
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
				<li class="sec"><h2><a href="/saml/acs/">SAML Login</a></h2></li>
			</py:if>

			</ol>
		</div>
