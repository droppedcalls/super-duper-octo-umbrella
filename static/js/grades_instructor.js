var tabs = document.querySelectorAll('.eval-tab')
var activeTab = tabs[0]
var defaultEval = document.querySelector('.eval-content'); //by default, first tab
defaultEval.style.display = 'block';
activeTab.style.backgroundColor = '#F54E41';

function closeconfirm(){
    document.getElementById("ins-err").style.display=" none";
}
// close the div in 5 secs
if (document.getElementById('ins-err').textContent !== null) {
    window.setTimeout("closeconfirm();", 5000);
}

function tabClick(tab) {
    var eval_grades = document.getElementById(tab.textContent);
    var inactive = [...document.querySelectorAll('.eval-content')].filter(elem => elem !== eval);
    inactive.forEach((item) => {
        item.style.display = 'none';
    })

    activeTab.style.backgroundColor = 'lightgrey';

    eval_grades.style.display = 'block';
    activeTab = tab;
    activeTab.style.backgroundColor = '#F54E41';
    document.querySelector('.new-eval').style.display = 'none';
    document.querySelector('.edit-eval').style.display = 'none';
    document.querySelectorAll('.entry-management').forEach((entry) => {
        entry.style.display = 'block';
    })
    return true;
}

for (let tab of tabs) {
    tab.onclick = () => {
        tabClick(tab);
    };
}


var add_entry = document.getElementById('add-entry');
add_entry.onclick = (e) => {
    e.preventDefault();
    document.querySelectorAll('.eval-content').forEach((entry) => {
        entry.style.display = 'none';
    })
    document.querySelectorAll('.entry-management').forEach((entry) => {
        entry.style.display = 'none';
    })
    document.querySelector('.new-eval').style.display = 'block';
}

var edit_entry = document.getElementById('edit-entry');
edit_entry.onclick = (e) => {
    e.preventDefault();
    document.querySelectorAll('.eval-content').forEach((entry) => {
        entry.style.display = 'none';
    })
    document.querySelectorAll('.entry-management').forEach((entry) => {
        entry.style.display = 'none';
    })
    document.querySelector('.edit-eval').style.display = 'block';
}

// deleting remark requests
var req_done = document.querySelectorAll('.delete')
var del_forms = document.querySelectorAll('.req-del')
req_done.forEach((button) => {
    button.onclick = () => {
        for (let form of del_forms) {
            if (button.form === form) {
                console.log(form);
                form.submit();
            }
        }
    }
})
