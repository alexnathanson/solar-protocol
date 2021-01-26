const params = new URLSearchParams(window.location.search);

//example http://solarprotocol.net/api/v1/chargecontroller.php?file=list
let result = JSON.parse(httpGet('http://solarprotocol.net/api/v1/chargecontroller.php?' + params.get("key") + "=" + params.get("value")));

console.log(result);

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}