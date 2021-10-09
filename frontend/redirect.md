# htaccess and redirection

Redirection for pretty URLs and security purposes happens between the htaccess file and the php files in the redirect directory

## htaccess

* L = do not proceed further if this rewrite rule is accepted
* QSA = append query string
* R = issues redirect

<p>
directories without a trailing / are redirected to the same URL with a trailing /
</p>
<p>
requests coming through solarprotocol.net/network are routed to the network.php page, which makes the request from the steward's server i.e. 123.123.123.123/local
</p>
<p>
requestions coming through local (123.123.123.123/local) are routed to either www.php for css and html or images.php for media
</p>

## network.php

## www.php

## images.php

## resources
 * a good list of htaccess syntax: https://www.alvinpoh.com/essential-htaccess-tips-and-tricks/
 * this tester is helpful for confirm the htaccess file is doing what you intend: https://htaccess.madewithlove.be/
