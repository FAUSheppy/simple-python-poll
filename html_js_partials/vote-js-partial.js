function cancle(){
	window.location.href = window.location.origin
}

function submitt(){
	options  = document.getElementsByClassName("vote-option")
    token    = document.getElementById("token-field")
    multi    = %s
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
