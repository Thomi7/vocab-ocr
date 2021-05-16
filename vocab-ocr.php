<?php

$hash=hash_file('md5', 'php://input');
$file="/data/test/$hash";
file_put_contents($file, file_get_contents('php://input'));

header("Content-Type: application/vnd.ms-excel");
header("Content-Transfer-Encoding: Binary");
readfile("/data/test/out.xls");

?>
