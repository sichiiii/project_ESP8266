

function httpGet(theUrl){
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
  xmlHttp.send( null );
  const obj = JSON.parse(xmlHttp.responseText);
  const obj1 = obj.ports
  window.onload = () => {
    [...document.querySelector('#pin_1').options]
      .filter(x => x.value === obj.ports[1].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_2').options]
      .filter(x => x.value === obj.ports[2].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_3').options]
      .filter(x => x.value === obj.ports[3].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_3').options]
      .filter(x => x.value === obj.ports[3].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_4').options]
      .filter(x => x.value === obj.ports[4].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_5').options]
      .filter(x => x.value === obj.ports[5].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_6').options]
      .filter(x => x.value === obj.ports[6].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_7').options]
      .filter(x => x.value === obj.ports[7].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_8').options]
      .filter(x => x.value === obj.ports[8].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_9').options]
      .filter(x => x.value === obj.ports[9].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_10').options]
      .filter(x => x.value === obj.ports[10].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_11').options]
      .filter(x => x.value === obj.ports[11].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_12').options]
      .filter(x => x.value === obj.ports[12].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_15').options]
      .filter(x => x.value === obj.ports[15].toString())[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_16').options]
      .filter(x => x.value === obj.ports[16].toString())[0]
      .setAttribute('selected', true);
  };
  
  return JSON.stringify(obj.ports[1]);
}
