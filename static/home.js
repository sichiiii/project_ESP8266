window.onload = () => {
    [...document.querySelector('#pin_7').options]
      .filter(x => x.value === "1")[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_8').options]
      .filter(x => x.value === "1")[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_9').options]
      .filter(x => x.value === "1")[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_10').options]
      .filter(x => x.value === "1")[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_11').options]
      .filter(x => x.value === "1")[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_12').options]
      .filter(x => x.value === "1")[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_15').options]
      .filter(x => x.value === "1")[0]
      .setAttribute('selected', true);
    [...document.querySelector('#pin_16').options]
      .filter(x => x.value === "1")[0]
      .setAttribute('selected', true);
  };

function httpGet(theUrl){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
alert(httpGet("http://localhost:8090/check"));

  