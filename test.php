<?php

// function for responding to json format
function sendJsonResponse($arr)
{
  header('Content-Type: application/json');
  header("Access-Control-Allow-Origin: *");
  header("Access-Control-Allow-Origin: *");
  header("Access-Control-Allow-Credentials: true");
  header("Access-Control-Allow-Methods: GET,HEAD,OPTIONS,POST,PUT");
  header("Access-Control-Allow-Headers: Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers");
  echo json_encode($arr);
}

$PATH = '<PATH_ON_SERVER_FOR_FILE_UPDATED_BY_CRON>'; // For example: '/var/www/html/net_use.txt';
$res = ["success" => true, 'data' => []];
try {
	if(!file_exists($PATH)) {
		sendJsonResponse([
			'success' => false,
			'message' => "File not found !"
		]);
		exit();
	}
	$handle = fopen($PATH, "r");
	if ($handle) {
		$prev = null;
		$min = null;
		$max = null;
		while (($line = fgets($handle)) !== false) {
			// process the line read.
			$line = trim($line);
			$arr = explode(":", $line);
			if (count($arr) === 2) {
				$t = (int)($arr[0]);
				$v = (int)($arr[1]);

				$min = $min == null || $t < $min ? $t: $min;
				$max = $max == null || $t > $max ? $t: $max;

				/* Check to add record or not */
				if ($v !== $prev)
				{
					array_push($res['data'], compact('t', 'v'));
					$prev = $v;
				}
			}
		}
		$res['min'] = $min;
		$res['max'] = $max;
		fclose($handle);
	} else {
		// error opening the file.
		sendJsonResponse([
			'success' => false,
			'message' => "File could not open !"
		]);
	} 
} catch(Exception $ex)
{
	sendJsonResponse([
		'success' => false,
		'message' => $ex->getMessage()
	]);
}
sendJsonResponse($res);
?>
