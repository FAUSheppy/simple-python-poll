function cancle(){
	window.location.replace(window.location.origin);
}

function submitt(){
	options = document.getElementsByClassName("vote-option")
	optString = ""
	for(x in options){
		if(options[x].checked){
			if(x != 0){
				optString += ","
			}
			optString += options[x].id + "+" + options[x].checked
		}
	}
	window.location.replace(window.location.origin + "/post-vote" + "?" + "selected=" + optString)
}
