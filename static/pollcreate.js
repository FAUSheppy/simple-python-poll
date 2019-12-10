var url = new URL(window.location.href)
var pollNameInput = document.getElementById('poll-name-input')
var question = document.getElementById('question-input')

function cancel(){
    window.location.replace(window.location.origin);
}

function createButton(){
    options = document.getElementsByClassName("option")
    optString = ""
    count = 0
    for(x in options){
        
        /* exclude question */
        if(options[x].id == "question-input"){
            continue
        }

        if(options[x].value){
            if(optString != ""){
                optString += ","
            }
            optString += options[x].value
            count++;
        }
    }

    console.log(optString)

    var question    = document.getElementById("question-input").value
    var tokenNeeded = document.getElementById("token-needed-input").checked
    var multiChoice = document.getElementById("multi-possible-input").checked

    if(question == ""){
        alert("Must ask a question!")
        return
    }else if(count <= 1){
        alert("Must offer more than one option!")
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

    requestURL = window.location.origin + "/create?"
                    + "&options=" + optString
                    + "&" + "tokens=" + token 
                    + "&" + "multi=" + multiChoiceVar
                    + "&" + "q=" + question

    /* request new poll */
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var pollIdent = xhttp.responseText.split(",")[0]
            var admToken  = xhttp.responseText.split(",")[1]
            window.location.href = window.location.origin + "/viewpostcreate?"
                                                          + "pollIdent=" + pollIdent 
                                                          + "&admToken=" + admToken
        }
    };
    xhttp.open("GET", requestURL, true);
    xhttp.send();

    console.log(requestURL)
}

function extend(){
    var optionsContainer = document.getElementById("options-container")
    var inputForm        = document.createElement("input")

    inputForm.setAttribute("type",        "text")
    inputForm.setAttribute("class",       "option-input option")
    inputForm.setAttribute("placeholder", "Enter poll option..")

    optionsContainer.appendChild(inputForm)
}
