<?php

$hash=hash_file('md5', 'php://input');
$tmp_folder="/tmp/$hash";

shell_exec("rm -rf $tmp_folder");
mkdir($tmp_folder);
file_put_contents("$tmp_folder/in", file_get_contents('php://input'));

shell_exec("/usr/bin/vocab-ocr.sh \"$tmp_folder\" \"in\"");

header("Content-Type: text/csv");
header("Content-Transfer-Encoding: Binary");
readfile("$tmp_folder/out.csv");

?>
