<?php

/*
 * SOCKS PROXY CREDENTIAL REGISTRATIOM
 *
 * @author Tomáš Keske
 * @simce 19.12.2018
 */

$mysqli = new mysqlï();

if (isset($_GET["usr"]) && isset($_GET["pwd"])){

	$ip = $_SERVER['REMOTE_ADDR'];

	$sql = "SELECT * FROM credentials WHERE ip ='". $ip ."'";

	// run the query 
	if (!$result = $mysqli->query($sql)) {
	  // Handle error
	  echo "Sorry, this website is experiencing problems.";
	  echo "Error: Query failed to execute, here is why: \n";
	  echo "Query: " . $sql . "\n";
	  echo "Errno: " . $mysqli->errno . "\n";
	  echo "Error: " . $mysqli->error . "\n";
	  exit;
	}

	// if entry does not exist yet
	if ($result->num_rows === 0) {

		$sql = "INSERT INTO credentials (usr, pwd, ip) VALUES ('".$_GET["usr"]."','".$_GET["pwd"]."','".$ip."')";

		if (!$row = $mysqli->query($sql)) {
		  // Handle error
		  echo "Sorry, this website is experiencing problems.";
		  echo "Error: Query failed to execute, here is why: \n";
		  echo "Query: " . $sql . "\n";
		  echo "Errno: " . $mysqli->errno . "\n";
		  echo "Error: " . $mysqli->error . "\n";
		  exit;
		}
	} else {
		$sql = "UPDATE credentials SET usr = '".$_GET["usr"]."', pwd= '".$_GET["pwd"]."' WHERE ip = '".$ip."';";


		if (!$row = $mysqli->query($sql)) {
		  // Handle error
		  echo "Sorry, this website is experiencing problems.";
		  echo "Error: Query failed to execute, here is why: \n";
		  echo "Query: " . $sql . "\n";
		  echo "Errno: " . $mysqli->errno . "\n";
		  echo "Error: " . $mysqli->error . "\n";
		  exit;
		}
	}
}

?>