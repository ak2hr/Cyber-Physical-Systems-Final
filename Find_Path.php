<?php

$prev=$_GET['prev'];
$start=$_GET['start'];
$dest=$_GET['dest'];

$output = shell_exec("python Robo_Path.py $prev $start $dest");
echo "<pre>$output</pre>";

?>