% if "link" in data: # this will be shown after file will be uploaded
    <script>
    function copyTextFunction() {
      <!-- We can copy innerText or InnerHTML ... -->
      navigator.clipboard.writeText(document.getElementById("new_link").innerText); }
    </script>

    <b>Link na nově nahraný soubor je:</b><br><br>

    <a href="/files/${data["link"]}" id="new_link">/files/${data["link"]}</a>

    <!-- The button used to copy the text -->
    <button onclick="copyTextFunction()">Copy link</button> 

    <br><br>
    <a href="/upload">Nahrát další soubor.</a>
% else: # this is the default view
    <p>Click on the "Browse..." button to upload a file:</p>
    <p>
    <form method="post" action="/upload" enctype="multipart/form-data">
      <input type="file" id="myFile" name="filename">
      <input type="submit" value="Upload">
    </form>
    </p>
% endif
