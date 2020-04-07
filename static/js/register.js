var email = document.getElementById('email');
var form = document.getElementsByTagName('form')[0];

var err = document.getElementById('email-err')

email.oninput = () => {
    if (! /.*@.*\..*$/.test(email.value)) {
        email.setCustomValidity('Please input a valid email address');
    } else {
        email.setCustomValidity('');
    }
};

form.onsubmit = () => {
    console.log(/.*@.*\..*$/.test(email.value))
    if (! /.*@.*\..*$/.test(email.value)) {
        return false;
    }
};