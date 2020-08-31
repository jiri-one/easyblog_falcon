<%inherit file="base.mako"/>

<div class="comment_title">Přihlaste se prosím:</div>
<div class="comment_form">
<form method="post" action="" accept-charset="UTF-8">
	<label for="login">Uživatelské jméno:</label><br>
	<input type="text" name="login" placeholder="Login name"><br>
	<label for="password">Heslo:</label><br>
	<input type="password" name="password" placeholder="Password"><br>
	<input type="checkbox" onclick="showPassword()">Show Password<br>
	<input type="submit" value="Odeslat">
</form>
</div>
<script>
function showPassword() {
var x = document.getElementsByName("password")[0];
if (x.type === "password") {
	x.type = "text";
} else {
	x.type = "password";
}
}
</script>