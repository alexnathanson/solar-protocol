<?php
namespace Upload;
//based on: https://www.w3schools.com/php/php_file_upload.asp

$maxFileSizeBytes = 500000;
$uploadStatus = "";

function uploadIt(){
  global $uploadStatus;

  if(isset($_POST["directory"])) {
    $target_dir = $_POST["directory"];

    $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

    $uploadOk = 1;


    if(strpos(mime_content_type($_FILES["fileToUpload"]["tmp_name"]),"image")!== false ){
      imageUpload($target_file);
    } else if (strpos(mime_content_type($_FILES["fileToUpload"]["tmp_name"]),"text")!== false ){
      textUpload($target_file);
    } else if (strpos(mime_content_type($_FILES["fileToUpload"]["tmp_name"]),"pdf")!== false ){
      pdfUpload($target_file);
    }

    // Check if file already exists
    //this might need a condition to delete the old file...
    if (isset($_POST["replace"]) == 0 && file_exists($target_file)) {
      $uploadStatus .= "<br>File already exists.";
      $uploadOk = 0;
    }

    // Check file size
    if ($_FILES["fileToUpload"]["size"] > $GLOBALS["maxFileSizeBytes"]) {
      $uploadStatus .= "<br>Your file is too large.";
      $uploadOk = 0;
    }

    // Check if $uploadOk is set to 0 by an error
    if ($uploadOk == 0) {
      $uploadStatus .=  "<br>Sorry, your file was not uploaded.";
    // if everything is ok, try to upload file
    } else {
      if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        $uploadStatus .=  "<br>The file ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " has been uploaded.";
      } else {
        $uploadStatus .=  "<br>Sorry, there was an error uploading your file.";
      }
    }
  } else {
    $uploadStatus .= "<br>Directory not selected. File not uploaded.";
  }
}

function imageUpload($iF){
  //supported file types jpg, jpeg, png, gif

  global $uploadOk, $uploadStatus;


  $imageFileType = strtolower(pathinfo($iF,PATHINFO_EXTENSION));

  // Check if image file is a actual image or fake image
  if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
      //echo $check["mime"];
      $uploadOk = 1;
    } else {
      $uploadStatus .= "<br>File is not an image.";
      $uploadOk = 0;
    }

    #not working yet!
    if(isset($_POST["dither"])){
      $target = "temp/" . $_FILES['new_image']['name'];
      $src = $_FILES["fileToUpload"]["tmp_name"];

      move_uploaded_file($src, $target);

      $dst = imagetruecolortopalette($src, true, 255); 
      imagedestroy($src);
      imagejpeg($dst,$_FILES["fileToUpload"]["tmp_name"]);
      //imagedestroy($dst);
      move_uploaded_file($src, $_FILES["fileToUpload"]["tmp_name"]);
    }  


    if(isset($_POST["rename"])){
      /*move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], "$uploads_dir/$name");*/

      $tmp_name = $_FILES["fileToUpload"]["tmp_name"];
      // basename() may prevent filesystem traversal attacks;
      // further validation/sanitation of the filename may be appropriate
      //$name = basename($_FILES["fileToUpload"]["name"]);
      move_uploaded_file($tmp_name, $_POST["directory"] . $_POST["rename"] . "." . $imageFileType);
    }


  }

  //check for image mimetype
  // Allow certain file formats
  if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
  && $imageFileType != "gif" ) {
    $uploadStatus .=  "<br>Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
    $uploadOk = 0;
  }
}

function textUpload($tF){
  //supported file types html, css
  // php is disable on server for this directory
  global $uploadOk, $uploadStatus;

  $textFileType = strtolower(pathinfo($tF,PATHINFO_EXTENSION));

  // Allow certain file formats
  if($textFileType != "html" && $textFileType != "css") {
    $uploadStatus .= "<br>Sorry, only HTML and CSS files are allowed.";
    $uploadOk = 0;
  }
}

function pdfUpload($tF){
  //supported file types: pdf
  // php is disable on server for this directory
  global $uploadOk, $uploadStatus;

  $textFileType = strtolower(pathinfo($tF,PATHINFO_EXTENSION));

  // Allow certain file formats
  if($textFileType != "pdf") {
    $uploadStatus .= "<br>Sorry, not a pdf.";
    $uploadOk = 0;
  }
}

?>
