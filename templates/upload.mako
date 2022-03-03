<%inherit file="base.mako"/>

<p>Click on the "Choose File" button to upload a file:</p>

<form method="post" action="/upload" enctype="multipart/form-data">
  <input type="file" id="myFile" name="filename">
  <input type="submit">
</form>
