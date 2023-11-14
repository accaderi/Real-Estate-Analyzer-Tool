if (settings['web_browser'] === 'msedgedriver.exe'){
    document.getElementById('web_browser').selectedIndex = 1;
}

if (settings['mapbox_api']){
    document.getElementById('mapbox_api').type = 'password';
    document.getElementById('mapbox_api').value = settings['mapbox_api'];
}

if (settings['ingatlancom_user'][0]){
    document.getElementById('userName').value = settings['ingatlancom_user'][0];
    document.getElementById('passWord').value = settings['ingatlancom_user'][1];
}

function check_webad_search() {
    var modal_v = 0;

    if ((userName.value.length === 0 && passWord.value.length > 0) ||
        (userName.value.length > 0 && passWord.value.length === 0)
      ) {
        modal_v = 1;
        document.getElementById('modal-body').innerHTML =
          'Please fill out the Username and the Password field too!';
        document.getElementById('bck').innerHTML = 'Gotcha';
        document.getElementById('cont').style.display = 'none';
        console.log('mod2 fill out', modal_v);
      }

    if (modal_v === 0) {
        document.getElementById('settings_form').submit();
    } else {
        var myModal = new bootstrap.Modal('#Modal_1');
      myModal.show();
    }

}