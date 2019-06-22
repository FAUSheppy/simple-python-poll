function cancel(){
	window.location.href = window.location.origin
}

function submit(){
  options  = document.getElementsByClassName("vote-option")
  token    = document.getElementById("token-field")
  multi    = true
  if(token){
      token = token.value
  }else{
      token = "none"
  }
  var url = new URL(window.location.href)
  pollname = url.searchParams.get("ident")
  if(pollname == null){
      pollname = document.getElementById("poll-ident").className
  }
	optString = ""
    count = 0
	for(x in options){
		if(options[x].checked){
			if(x != 0){
				optString += ","
			}
			optString += options[x].id
            count++
		}
	}

  /* check if at least one selcted */
  if(count == 0){
      alert("Must select at least one option")
      return
  }

  /* check if multi choice */
  if(count > 1 && !multi){
      alert("Can only select ONE option!")
      return
  }
	var xhttp = new XMLHttpRequest();
	xhttp.onload = function() {
		if (xhttp.status == 200) {
        	window.location.href = window.location.origin + "/viewresults?ident=" + pollname
		}else{
            alert("Token rejected")
    	}
	};
  requestURL = window.location.origin + "/vote" + "?" 
									                  + "ident=" + pollname
                                  	+ "&token=" + token
                                  	+ "&selected=" + optString
	xhttp.open("GET", requestURL, true);
	xhttp.send();
}

function showResults(){
    var url = new URL(window.location.href)
    pollIdent = url.searchParams.get("ident")
    if(pollIdent == null){
        pollIdent = document.getElementById("poll-ident").className
    }
    window.location.href = window.location.origin + "/viewresults" + "?ident=" + pollIdent 
}
