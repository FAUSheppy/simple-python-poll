function goButton(){
  var tokenInput = document.getElementById('input').value
  console.log(tokenInput) 
  if(tokenInput.includes("token")){
    /* basicly if someone pasted a vote-url into the token field */
    try{
        tokenInput = tokenInput.split("token=")[1].split("&")[0]
    }catch(error){
        alert("That does not look like a token.")
        return
    }
  }

	requestURL = window.location.origin + "/checktoken?token=" + tokenInput

	var xhttp = new XMLHttpRequest();
	xhttp.onload = function() {
	    if (this.status == 200) {
          window.location.href = window.location.origin + xhttp.responseText
	    }else{
          alert("Token rejected")
      }
	};
	xhttp.open("GET", requestURL, true);
	xhttp.send();
}
