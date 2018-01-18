<?php

$db_user = 'ak2hr';
$db_pass = 'tlp_rules';

//use the GET method to populate the variables
$dest=$_GET['dest'];

$database = "ak2hr"; //you'll want to edit this

$mysqli = new mysqli("127.0.0.1", $db_user, $db_pass, $database);

if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
}

$q=$mysqli->query("INSERT INTO Destinations (End_Node) VALUES ('$dest')");

$mysqli->close();
?>
