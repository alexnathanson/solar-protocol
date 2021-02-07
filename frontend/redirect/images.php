<?php

$locDir = "/home/pi/local/";

if ($_SERVER["REQUEST_METHOD"] == "GET") {
	//NOTE: nothing can be output prior to the image for this to work
	//var_dump($_GET);

	// get the file name
	$filepath= $locDir . @$_GET['file'];

	if (file_exists($filepath)){
		if(strpos($filepath, "jpg")){
			header("Content-type: image/jpg");
		} else if(strpos($filepath, "jpeg")){
			header("Content-type: image/jpeg");
		}  else if(strpos($filepath, "png")){
			header("Content-type: image/png");
		} else if(strpos($filepath, "gif")){
			header("Content-type: image/gif");
		} else {
			notFound();
			return;
		}
		header("Accept-Ranges: bytes");
		header('Content-Length: ' . filesize($filepath));
		//header("Last-Modified: Fri, 03 Mar 2004 06:32:31 GMT");
		readfile($filepath);
	} else {
		notFound();
	}
	
}

function notFound(){
	header( "HTTP/1.0 404 Not Found");
	header("Content-type: image/jpeg");
	header('Content-Length: ' . filesize("404_files.jpg"));
	header("Accept-Ranges: bytes");
	//header("Last-Modified: Fri, 03 Mar 2004 06:32:31 GMT");
	readfile("404_files.jpg");
}

?>