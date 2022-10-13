<?php

//this runs on the steward's server
//it retrieves the files and sends them back to the Poe server
//in the future this could be merged with the www.php script

$locDir = "/home/pi/local/www/";
$filepath= "";

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    //NOTE: nothing can be output prior to the image for this to work
    //var_dump($_GET);

    // get the file name
    $filepath= $locDir . @$_GET['file'];

    if (file_exists($filepath)) {
        if (strpos($filepath, ".jpg")) {
            header("Content-type: image/jpg");
        } elseif (strpos($filepath, ".jpeg")) {
            header("Content-type: image/jpeg");
        } elseif (strpos($filepath, ".png")) {
            header("Content-type: image/png");
        } elseif (strpos($filepath, ".gif")) {
            header("Content-type: image/gif");
        } elseif (strpos($filepath, ".mp4")) {
            header("Content-type: video/mp4");
        } elseif (strpos($filepath, ".pdf")) {
            header("Content-type: application/pdf");
        } else {
            notFound();
            return;
        }
        serveImg();
    } else {
        notFound();
    }
}

function serveImg()
{
    global $filepath;

    header("Accept-Ranges: bytes");
    header('Content-Length: ' . filesize($filepath));
    //header("Last-Modified: Fri, 03 Mar 2004 06:32:31 GMT");
    readfile($filepath);
}

function notFound()
{
    header("HTTP/1.0 404 Not Found");
    header("Content-type: image/jpeg");
    header('Content-Length: ' . filesize("404_files.jpg"));
    header("Accept-Ranges: bytes");
    //header("Last-Modified: Fri, 03 Mar 2004 06:32:31 GMT");
    readfile("404_files.jpg");
}
