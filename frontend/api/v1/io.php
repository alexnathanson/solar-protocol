<?php

// This is for private file sharing (password protected) data.

/**
 * all methods PW protected
 * post arbitrary files, log meta data about transaction
 * get file list, meta data, individual files
**/

// If you change this value, the client keys need to match
$hash = '$2y$10$mCxhv3NC4/lkSycnD85XLuw/AYBCxw1ElmCqeksR.f88BTZoXXuca';

$api_key= "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $api_key = test_input($_POST["api_key"]);

    //check if key is correct
    if (verifyPW($api_key, $hash)) {
        //do password protected stuff here
    }
}
