
console.log(httpGet('http://solarprotocol.net/api/v1/api.php?value=PV-voltage'));

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}