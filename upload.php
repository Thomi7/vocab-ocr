<?php

require_once 'System.php';

$from_lang='eng';
$to_lang='deu';

if ($_POST['from-lang'] == 'fr') {
    $from_lang='fra';
} else if ($_POST['from-lang'] == 'es') {
    $from_lang='spa';
}

$mode='default';
if ($_POST['mode'] == 'greenwich') {
    $mode='greenwich';
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

    // return csv
    header('Content-Type: text/csv');
    $date = date('Y-m-d_H-i-s');
    header("Content-Disposition: attachment; filename=\"$from_lang\_$to_lang\_$date.csv\"");
    $csv = shell_exec("vocab-ocr \"$tmp_dir\" \"$from_lang\" \"$to_lang\" \"$mode\"");
    echo "$csv";
} else {
    exit('Error: no files submitted');
}

?>
