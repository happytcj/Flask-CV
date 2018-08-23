function verifySearchFields() {
    var fighter1 = document.getElementById('autocomplete1').value.toLowerCase();
    var fighter2 = document.getElementById('autocomplete2').value.toLowerCase();
    var message = '';
    
    if (fighter1 === '') {
        message = 'Please fill in field for fighter #1\n';
    }
    if (fighter2 === '') {
        message += 'Please fill in field for fighter #2\n';
    }
    if (fighter1 === fighter2) {
        message += 'Please fill in two different fighters\n';
    }

    if (message !== '') {
        alert(message);
        return false;
    }
    return true;
}