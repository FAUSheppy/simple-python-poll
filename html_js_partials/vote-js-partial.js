function cancle(){
	window.location.href = window.location.origin
}

function submitt(){
	options  = document.getElementsByClassName("vote-option")
    token    = document.getElementById("token-field")
    if(token){
        token = token.value
    }else{
        token = "none"
    }
    var url = new URL(window.location.href)
    pollname = url.searchParams.get("name")
    if(pollname == null){
        pollname = document.getElementById("poll-ident").className
    }
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

function showResults(){
    var url = new URL(window.location.href)
    pollname = url.searchParams.get("name")
    if(pollname == null){
        pollname = document.getElementById("poll-ident").className
    }
    window.location.href = window.location.origin + "/results" + "?name=" + pollname 
}
