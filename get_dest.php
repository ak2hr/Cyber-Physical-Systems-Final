<?php    
	
$db_user = 'ak2hr';
$db_pass = 'tlp_rules';

$database = "ak2hr"; 

$mysqli = new mysqli("127.0.0.1", $db_user, $db_pass, $database);

$id=$_GET['id']; 

if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
}

$q=$mysqli->query("SELECT * FROM Destinations WHERE id = ('$id')");

//then echo (print) the values
//note the use of the associative array!
while($r=$q->fetch_assoc()){
    echo "id: " . $r['id'] . "; Dest: " . $r['End_Node'] . "\n";
}


$mysqli->close();
?> 