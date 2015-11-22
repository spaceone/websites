				<div py:if="shell" id="smallshell" class="shell" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">
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
