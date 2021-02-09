<?php
namespace Upload;
//based on: https://www.w3schools.com/php/php_file_upload.asp

function uploadIt(){

  if(isset($_POST["directory"])) {
    $target_dir = $_POST["directory"];

    $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

    $uploadOk = 1;


    if(strpos(mime_content_type($target_file),"image")!== false ){
      imageUpload($target_file);
    } else if (strpos(mime_content_type($target_file),"text")!== false ){
      textUpload($target_file);
    }
/*
    $imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

    // Check if image file is a actual image or fake image
    if(isset($_POST["submit"])) {
      $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
      if($check !== false) {
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
      } else {
        echo "File is not an image.";
        $uploadOk = 0;
      }
    }*/

    // Check if file already exists
    //this might need a condition to delete the old file...
    if (isset($_POST["replace"]) == 0 && file_exists($target_file)) {
      echo "Sorry, file already exists.";
      $uploadOk = 0;
    }

    // Check file size
    if ($_FILES["fileToUpload"]["size"] > 500000) {
      echo "Sorry, your file is too large.";
      $uploadOk = 0;
    }

    // Check if $uploadOk is set to 0 by an error
    if ($uploadOk == 0) {
      echo "Sorry, your file was not uploaded.";
    // if everything is ok, try to upload file
    } else {
      if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo "The file ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " has been uploaded.";
      } else {
        echo "Sorry, there was an error uploading your file.";
      }
    }
  }
}

function imageUpload($iF){
  //supported file types jpg, jpeg, png, gif

  global $uploadOk;


    $imageFileType = strtolower(pathinfo($iF,PATHINFO_EXTENSION));

    // Check if image file is a actual image or fake image
    if(isset($_POST["submit"])) {
      $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
      if($check !== false) {
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
      } else {
        echo "File is not an image.";
        $uploadOk = 0;
      }
    }

  //check for image mimetype
    // Allow certain file formats
    if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
    && $imageFileType != "gif" ) {
      echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
      $uploadOk = 0;
    }
}

function textUpload(){
  //supported file types html, css
  // php is disable on server for this directory
  global $uploadOk;

  // Allow certain file formats
  if($imageFileType != "html" && $imageFileType != "css") {
    echo "Sorry, only HTML and CSS files are allowed.";
    $uploadOk = 0;
  }
}

?>
