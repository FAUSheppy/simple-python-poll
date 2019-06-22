function goButton(){
    var tokenInput = document.getElementById('input').value
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
