function cancel(){
	window.location.replace(window.location.origin);
}

function submit(){
	options = document.getElementsByClassName("option")
	optString = ""
    count = 0
	for(x in options){
		if(options[x].value){
			if(x != 0){
				optString += ","
			}
			optString += options[x].value
            count++;
		}
	}

    var question    = document.getElementById("question-input").value
    var pollName    = document.getElementById("poll-name-input").value
    var tokenNeeded = document.getElementById("token-needed-input").checked
    var multiChoice = document.getElementById("multi-possible-input").checked

    if(question == ""){
        alert("Must ask a question!")
        return
    }else if(count <= 1){
        alert("Must offer more than one option!")
        return
    }else if(pollName == ""){
        alert("Must have a poll-name!")
        return
    }
    
    var token = 0
    if(tokenNeeded){
        token = 1
    }

    var multiChoiceVar = 0
    if(multiChoice){
        multiChoiceVar = 1
    }

	window.location.href = window.location.origin + "/post-create?name=" + pollName
                    + "&options=" + optString
                    + "&" + "tokens=" + token 
                    + "&" + "multi=" + multiChoiceVar
                    + "&" + "q=" + question
}

function extend(){
	var span = document.createElement('span')
    span.innerText = "Answer: "
	var inputForm = document.createElement("input")
	inputForm.setAttribute("type", "text")
	inputForm.setAttribute("class", "option-input option")
	span.appendChild(inputForm)
	var element = document.getElementById("options-container")
    element.appendChild(span)
}

var url = new URL(window.location.href)
var pollNameInput = document.getElementById('poll-name-input')
var question = document.getElementById('question-input')
var pollname = url.searchParams.get("name")

if(pollname == "" || pollname == null){
    pollNameInput.focus();
    pollNameInput.select();
}else{
    pollNameInput.value = pollname
    question.focus();
    question.select();
}
