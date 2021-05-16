<?php

$from_lang="eng";
$to_lang="deu";

if (getallheaders()["from-lang"] = "fr") {
    $from_lang="fra";
}

# store image in tmp folder of its md5 hash
$hash=hash_file('md5', 'php://input');
$tmp_folder="/tmp/$hash";
shell_exec("rm -rf $tmp_folder");
mkdir($tmp_folder);
file_put_contents("$tmp_folder/input", file_get_contents('php://input'));

shell_exec("/usr/bin/vocab-ocr.sh \"$tmp_folder\" \"input\" \"$from_lang\" \"$to_lang\"");

header("Content-Type: text/csv");
header("Content-Transfer-Encoding: Binary");
readfile("$tmp_folder/out.csv");

?>
