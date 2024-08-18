
spProtocol = window.location.protocol;

let result = JSON.parse(getAPI(spProtocol + '//solarprotocol.net/api/v2/opendata.php?systemInfo=name'));
let battery = JSON.parse(getAPI(spProtocol + '//solarprotocol.net/api/v2/opendata.php?value=battery-percentage'));

console.log(result);

var state;

if (result.name != "Solar Power for Artists") {
  state = "off";
} else if (battery["battery-percentage"] <= 0.5){
  state = "low";
} else {
  state = "on";
}

function getAPI(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}