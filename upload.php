<?php

$root_dir = "/tmp";

$from_lang="eng";
$to_lang="deu";

if ($_POST["from-lang"] == "fr") {
    $from_lang="fra";
} else if ($_POST["from-lang"] == "es") {
    $from_lang="spa";
}

if (!empty(array_filter($_FILES['files']['name']))) {
    // concatenate file hashes
    $hash_concat="";
    foreach ($_FILES['files']['tmp_name'] as $key => $value) {
        $file_tmpname=$_FILES['files']['tmp_name'][$key];
        $file_hash=hash_file('md5', $file_tmpname);
        $hash_concat.=$hash1;
    }

    // calculate hash folder from random string and file hashes
    $tmp_folder="/tmp/".hash('md5', uniqid().$hash_concat);

    // prepare tmp folder
    shell_exec("rm -rf \"$tmp_folder\"");
    mkdir($tmp_folder);

    // save files to tmp directory
    $file_counter=0;
    foreach ($_FILES['files']['tmp_name'] as $key => $value) {
        $file_tmpname=$_FILES['files']['tmp_name'][$key];
        $file_counter+=1;
        move_uploaded_file("$file_tmpname", "$tmp_folder/input$file_counter")
            or exit("Error: file \"{$_FILES['files']['name'][$key]}\" couldn't be received");
    }

    // process image files
    shell_exec("vocab-ocr-multiple \"$tmp_folder\" \"input\" \"$from_lang\" \"$to_lang\" $file_counter");

    // return csv
    header("Content-Type: text/csv");
    header('Content-Disposition: attachment; filename="vocab.csv"');
    readfile("$tmp_folder/concat.csv");

    // clear processed data
    shell_exec("rm -rf \"$tmp_folder\"");
} else {
    exit("Error: no files submitted");
}

?>
