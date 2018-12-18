<?php

// Connect to database server and database
$mysqli = new mysqli();

// If connection attempt failed, let us know
if ($mysqli->connect_errno) {
  echo "Sorry, this website is experiencing problems.";
  echo "Error: Failed to make a MySQL connection, here is why: \n";
  echo "Errno: " . $mysqli->connect_errno . "\n";
  echo "Error: " . $mysqli->connect_error . "\n";
  exit;
}

function outputQueryResults($mysqli) { 

	$ip = $_SERVER['REMOTE_ADDR'];

	$sql = "SELECT * FROM ports WHERE ip ='". $ip ."'";

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

	// If zero rows....
	if ($result->num_rows === 0) {
	    
	    $sql2 = "SELECT * FROM ports WHERE id=(SELECT MAX(id) FROM ports)";
	    
		if (!$result = $mysqli->query($sql2)) {
		  // Handle error
		  echo "Sorry, this website is experiencing problems.";
		  echo "Error: Query failed to execute, here is why: \n";
		  echo "Query: " . $sql . "\n";
		  echo "Errno: " . $mysqli->errno . "\n";
		  echo "Error: " . $mysqli->error . "\n";
		  exit;
		}

		while ($row = $result->fetch_assoc()) {     

		   $port = $row['port']; 

		}

		$port = intval($port);
		$port = $port++;

		$sql3 = "INSERT INTO ports (ip, port) VALUES ('".$ip."','".$port."')";

		if (!$xx = $mysqli->query($sql3)) {
		  // Handle error
		  echo "Sorry, this website is experiencing problems.";
		  echo "Error: Query failed to execute, here is why: \n";
		  echo "Query: " . $sql . "\n";
		  echo "Errno: " . $mysqli->errno . "\n";
		  echo "Error: " . $mysqli->error . "\n";
		  exit;
		}

		while ($row = $xx->fetch_assoc()) {     

		   var_dump($row); 

		}
	}

	//output data in HTML table 
	while ($row = $result->fetch_assoc()) {     

	   echo $row['port']; 

	}
}
 

// run query and output results 
outputQueryResults($mysqli); 

// close database connection 
mysqli_close($mysqli);

 

?>