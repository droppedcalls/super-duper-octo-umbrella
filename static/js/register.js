var elements = document.getElementsByTagName('a');
for (var i = 0; i < elements.length; i++) {
    if (elements[i].className == 'instructor') { 
         elements[i].onclick = function() { 
           document.getElementById("id-block").style.display = "none";
        }
    } else {
        elements[i].onclick = function() {
            document.getElementById("id-block").style.display = "block";
        }
    }
}
//console.log(elements);