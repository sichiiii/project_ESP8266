

function httpGet(theUrl) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", theUrl, false); // false for synchronous request
  xmlHttp.send(null);
  const obj = JSON.parse(xmlHttp.responseText);

  window.onload = () => {
    for (let portNum = 1; portNum <= 16; portNum++) {
      if (portNum === 13 || portNum === 14) {
        continue;
      }
      [...document.querySelector('#pin_' + portNum).options]
        .filter(x => x.value === obj.ports[portNum].toString())[0]
        .setAttribute('selected', true);
    }
  };

  return JSON.stringify(obj.ports[1]);
}
