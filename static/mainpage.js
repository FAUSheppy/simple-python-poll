function create(){
	window.location.href = window.location.origin + "/create?pollname=" + input;
}
function submit(){
	input = document.getElementById("input").value
    if(input == ""){
        alert("Must give name of or token for a poll!")
        return
    }
	window.location.href = window.location.origin + "/poll?ident=" + input;
}
var input = document.getElementById('input')
input.focus();
input.select();
