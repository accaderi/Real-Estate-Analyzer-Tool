document.getElementById('webaddress').addEventListener('input', submitcheck);
document.getElementById('search').addEventListener('input', submitcheck);

let submitBtn = document.getElementById('subSubmit');
let submitBtn_web = document.getElementById('subSubmit_web');

let sel_sale_input = document.getElementById('salerent');

country_radios = document.querySelectorAll('input[name="btnradio"]');
console.log(country_radios);

const conditionMetForSaleBtn = sessionStorage.getItem('conditionMetForSaleBtn');
if (conditionMetForSaleBtn === 'true') {
  sel_sale_input.value = false; // originally it was "0"
  sel_sale_input.disabled = true;
}

country_radios.forEach(element => {
  element.addEventListener('change', function() {

    if (country_radios[1].checked || country_radios[2].checked)
    {
      console.log('stg');
      sel_sale_input.value = 0
      sel_sale_input.disabled = true;
      sessionStorage.setItem('conditionMetForSaleBtn', 'true');
    }
    else
    {
      sel_sale_input.disabled = false;
      sessionStorage.removeItem('conditionMetForSaleBtn');
    }

  });
});


function submitcheck() {
  var addr = document.getElementById('webaddress').value.length;
  var sear = document.getElementById('search').value.length;

  const conditionMetForScrapBtn = sessionStorage.getItem('conditionMetForScrapBtn');
if (conditionMetForScrapBtn === 'true') {
  sel_sale_input.disabled = false;
}
  
  if (addr > 0) {
    submitBtn_web.disabled = false;
    sessionStorage.setItem('conditionMetForScrapBtn', 'true');
  } else {
    submitBtn_web.disabled = true;
    sessionStorage.removeItem('conditionMetForScrapBtn');
  }
  
  if (sear > 0) {
    submitBtn.disabled = false;
    sessionStorage.setItem('conditionMetForScrapBtn', 'true');
  } else {
    submitBtn.disabled = true;
    sessionStorage.removeItem('conditionMetForScrapBtn');
  }
}


function check_webad_search() {
  var modal_v = 0;

  if (webaddress.value.length != 0 && search.value.length != 0) {
    modal_v = 1;
    document.getElementById('modal-body').innerHTML =
      'Both webaddress and search criterias found,\
        webaddress takes precedence and search ignored!<br>\
        Note: In order to use the search function leave the webaddress field blank.';
    console.log('mod 1 both');
  } 
  
  if (
      document.getElementById('btnradio1').checked &&
      document.getElementById('flexCheckChecked').checked
    ) {
      modal_v = 0;
    }

    if (
        webaddress.value.includes('immobilienscout24.de') &&
        (webaddress.value.includes('haus') ||
        webaddress.value.includes('wohnung') ||
        webaddress.value.includes('miete') ||
        webaddress.value.includes('kaufe')) ||
        webaddress.value.includes('ingatlan.com') &&
        (webaddress.value.includes('haz') ||
        webaddress.value.includes('lakas') ||
        webaddress.value.includes('elado') ||
        webaddress.value.includes('kiado'))
    ) {
      modal_v = 0;
    } else if (webaddress.value) {
      modal_v = 2;
      document.getElementById('modal-body').innerHTML =
        'Either not supported webpage or not supported options, sorry!';
      console.log('mod2 fill out not supported', modal_v);
    }
    
    if (modal_v === 0) {
      document.getElementById('mainform').submit();
      submitBtn_web.disabled = true;
      submitBtn.disabled = true;
    } else {
      if (modal_v === 1) {
        document.getElementById('bck').style.display = 'Back';
        document.getElementById('cont').style.display = 'Start scrapping';
        console.log('mod1 btns');
      } else if (modal_v === 2) {
        document.getElementById('bck').innerHTML = 'Gotcha';
        document.getElementById('cont').style.display = 'none';
        console.log('mod2 got');
      }
      var myModal = new bootstrap.Modal('#Modal_1');
      myModal.show();
    }
    
  }