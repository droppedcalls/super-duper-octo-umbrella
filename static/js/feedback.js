var form = document.getElementsByTagName('form')[0];
var ans = document.getElementsByClassName('ans');

var blank = false;

form.addEventListener('submit', (e) => {
    if (ans[0].value === '' && ans[1].value === '' && ans[2].value === '' &&
        ans[3].value === '') {
            if (blank === true) {
                err.style.color = 'red';
                e.preventDefault();
            } else {
                e.preventDefault();
                err = document.getElementById('err')
                err.innerText = 'Cannot submit blank form';
                err.style.display = 'block';
                blank = true;
            }
    }
});