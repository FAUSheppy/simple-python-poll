function cancle(){
	window.location.href = window.location.origin;
}

function submitt(){
	options  = document.getElementsByClassName("vote-option")
    token    = document.getElementById("token-field").value
    pollname = document.getElementById("poll-name").innerText
	optString = ""
	for(x in options){
		if(options[x].checked){
			if(x != 0){
				optString += ","
			}
			optString += options[x].id
		}
	}
	window.location.href = window.location.origin + "/post-vote" + "?" + "name=" + pollname
                                    + "&" + "token=" + token
                                    + "&" + "selected=" + optString
}
