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

	// if entry does not exist yet
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
		$port = $port+1;
		$conn_port = random_int(60000, 65534);
		$ret = array("port" => $port, "connection_port" => $conn_port);

		$sql3 = "INSERT INTO ports (ip, port, connection_port) VALUES ('".$ip."','".$port."','". $conn_port."')";

		if (!$xx = $mysqli->query($sql3)) {
		  // Handle error
		  echo "Sorry, this website is experiencing problems.";
		  echo "Error: Query failed to execute, here is why: \n";
		  echo "Query: " . $sql . "\n";
		  echo "Errno: " . $mysqli->errno . "\n";
		  echo "Error: " . $mysqli->error . "\n";
		  exit;
		}

		echo $port.":".$conn_port;
		return $ret;
	}

	//return information that exists
	while ($row = $result->fetch_assoc()) {     

	   echo $row['port'].":".$row["connection_port"]; 

	}
}

function spawnTheMaster($array){
	exec('sudo nohup python3 master.py -m 0.0.0.0:'.$array["port"].' -c 0.0.0.0:'.$array["conn_port"].' > /dev/null 2>&1 &');
}
 

// run query and output results 
$portArray = outputQueryResults($mysqli); 

// close database connection 
mysqli_close($mysqli);

//spawn the master server
spawnTheMaster($portArray);


?>