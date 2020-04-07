const closed = '\u25B6';
const open = '\u25BC';

var q = document.getElementsByClassName('question');

function showContent(elem) {
    var indicator = elem.getElementsByClassName('indicator')[0];
    if (indicator === closed) {
        indicator.textContent = open;
        elem.getElementsByClassName('ans-list')[0].style.display = block;
    } else if (indicator === open) {
        indicator.textContent = closed;
        elem.getElementsByClassName('ans-list')[0].style.display = block;
    }
}

for (let elem of q) {
    elem.onclick = () => {
        var indicator = elem.getElementsByClassName('indicator')[0];
        if (indicator.textContent === closed) {
            indicator.textContent = open;
            elem.getElementsByClassName('ans-list')[0].style.display = 'block';
        } else if (indicator.textContent === open) {
            indicator.textContent = closed;
            elem.getElementsByClassName('ans-list')[0].style.display = 'none';
        }
    };
}