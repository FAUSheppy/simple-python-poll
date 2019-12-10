function newTokenLink(nocopy=false){
    admToken  = document.getElementById("admToken").innerText
    pollIdent = document.getElementById("pollIdent").innerText

    requestURL = window.location.origin + "/tokenget" + "?" 
                                                            + "ident=" + pollIdent
                                          + "&admToken=" + admToken
        var xhttp = new XMLHttpRequest();
        var voteTokenLinkField = document.getElementById("voteTokenLink")

        xhttp.onload = function() {
                if (xhttp.status == 200) {
                    voteTokenLinkField.value = xhttp.responseText
            if(!nocopy){
                /* Select the text field */
                voteTokenLinkField.select();
                /* Copy the text inside the text field */
                document.execCommand("copy");
            }
                }
        }

        xhttp.open("GET", requestURL, true);
        xhttp.send();
}

/* call it once to generate initial */
newTokenLink(true)
