<?php

/*	$app->get('/clientindex', function ($request, $response, $args) {
	    $file = '../public/index.html';
	    if (file_exists($file)) {
	        return $response->write(file_get_contents($file));
	    } else {
	        throw new \Slim\Exception\NotFoundException($request, $response);
	    }
	})*/


	if ($_SERVER["REQUEST_METHOD"] == "GET") {
		var_dump($_GET);
	}



?>