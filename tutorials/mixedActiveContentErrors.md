# Avoiding Mixed Active Content Errors

solarprotocol.net now works with both HTTP and HTTPS. If you are building a page for solarprotocol.net that makes API calls to itself, you will need to implement something like the following code to avoid errors.

``` 
function testSSL(){
  if (window.location.protocol == 'http:'){
    return false;
  }
  else if (window.location.protocol == 'https:'){
    return true;
  }
}

if (testSSL) { 
  const response = await fetch('https://solarprotocol.net/api/v2/opendata.php?systemInfo=city');
} else {
  const response = await fetch('http://solarprotocol.net/api/v2/opendata.php?systemInfo=city');
}
```