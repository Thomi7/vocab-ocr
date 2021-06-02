<?php

require_once 'System.php';

$installed_langs = explode("\n", shell_exec("tesseract --list-langs | tail -n +2"));
array_pop($installed_langs); // pop empty string

// validate left lang
$left_lang = 'eng';
if (in_array($_POST['left-lang'], $installed_langs)) {
    $left_lang = $_POST['left-lang'];
}

// validate right lang
$right_lang = 'deu';
if (in_array($_POST['right-lang'], $installed_langs)) {
    $left_lang = $_POST['right-lang'];
}

// validate mode
$modes = ['default', 'greenwich'];
$mode='default';
if (in_array($_POST['mode'], $modes)) {
    $mode = $_POST['mode'];
}

if (!empty(array_filter($_FILES['files']['name']))) {
    // prepare tmp folder
    $tmp_dir=System::mktemp('-d vocab-ocr-');

    // save files to tmp directory
    $file_counter=0;
    foreach ($_FILES['files']['tmp_name'] as $key => $value) {
        $file_tmpname=$_FILES['files']['tmp_name'][$key];
        $file_counter+=1;
        move_uploaded_file("$file_tmpname", "$tmp_dir/input$file_counter")
            or exit("Error: file \"{$_FILES['files']['name'][$key]}\" couldn't be received");
    }

    // process to csv
    $csv = shell_exec("vocab-ocr \"$tmp_dir\" \"$left_lang\" \"$right_lang\" \"$mode\"");

    // return csv
    header('Content-Type: text/csv');
    $date = date('Y-m-d_H-i-s');
    header("Content-Disposition: attachment; filename=\"$left_lang\_$right_lang\_$date.csv\"");
    echo "$csv";
} else {
    exit('Error: no files submitted');
}

?>
