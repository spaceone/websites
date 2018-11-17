<form xmlns:py="http://genshi.edgewall.org/" method="POST" accept-charset="UTF-8" enctype="application/x-www-form-urlencoded" name="contactform">
	<p>
	<label for="contact_tile">Title</label>
	<input name="title" type="radio" value="Mr." checked="checked">Mr.</input>
	<input name="title" type="radio" value="Mrs.">Mrs.</input>
	</p>

	<p>
	<label for="contact_name">Name</label>
	<input type="text" id="contact_name" name="name" />
	</p>

	<p>
	<label for="contact_from">E-Mail address</label>
	<input type="email" id="contact_form" name="from" required="required" />
	</p>

	<p>
	<label for="contact_website">Website</label>
	<input type="url" id="contact_website" name="website"/>
	</p>

	<p>
	<label for="contact_copy">Send me a copy</label>
	<input type="checkbox" name="copy" id="contact_copy" />
	</p>

	<p>
	<label for="contact_subject">Subject</label>
	<input type="text" name="subject" id="contact_subject"/>
	</p>

	<p>
	<label for="contact_message">Message</label>
	<textarea id="contact_message" name="message" required="required">&nbsp;</textarea>
	</p>

	<!-- TODO: captcha -->

	<p>
	<input type="submit" value="Send" />
	</p>
</form>
