<?php
session_start();
//require_once("checklogin.inc.php");
require_once("dbinterface.inc.php");

//$loginCheck = new LoginCheck();
//$loginCheck->checkLogin();

$action = $_GET["action"];

//$loginCheck = new LoginCheck();

switch($action)
  {
  case "":
	 {
		print("<form action=login.php?action=login method=post>\n");
		print("Username: <input name=user size=15><br>\n");
		print("Password: <input name=passwd size=15 type=password><br>\n");
		print("<input type=submit value=Login> <input type=reset value=Cancel>\n");
		print("</form>\n");
		break;
	 } 
  case "login":
 	{
		$dbConnection = new DbInterface();
	 
		if($dbConnection->connect())
		{
		  $dbConnection->query("SELECT * FROM users WHERE login='".$_POST["user"]."'");
		  $query = $dbConnection->getResultNumber();

		  if($query == 0)
			 {
				echo "User does not exist. <a href=login.php?action=create>Create</a>";
			 }
		  else if($query > 1)
			 {
				echo "ERROR: Many users with this name exist !!";
			 }
		  else
			 {
				$dbUser = $dbConnection->getResultItems();
				
				if (sha1($_POST["passwd"]) == $dbUser[0]['passwd'])
				  {
					 $sessionId = md5(uniqid(rand()));
					 $ipAddr = getenv('REMOTE_ADDR');
					 $browserAgent = getenv('HTTP_USER_AGENT');

					 $qResult = $dbConnection->query("INSERT INTO sessions (sid, ip, browser, uid, login_time, expires) VALUES 
                                               ('".$sessionId."','"
																.$ipAddr."','"
																.$browserAgent."','"
																.$dbUser[0]['uid']."', 
                                                CURRENT_TIMESTAMP, '"
																.(time() + (30 * 60))."')");
					 if(!$qResult)
						{
						  echo "ERROR: could not start user session (DB error)<br>";
						}
					 else
						{
						  $hostname = $_SERVER['HTTP_HOST'];
						  $path = dirname($_SERVER['PHP_SELF']);

						  $_SESSION['SessionID'] = $sessionId;
						  header('Location: https://'.$hostname.($path == '/' ? '' : $path).'/rezepte.php');
						  //header('Location: http://'.$hostname.($path == '/' ? '' : $path).'/admin.php');
						}
				  }
				else
				  {
					 echo "Wrong password :-(<br>";
				  }
			 }
		  
		  $dbConnection->disconnect();
		}
		break;
	 }
  case "logout":
	 {
		$dbConnection = new DbInterface();

		if($dbConnection->connect())
		  {
			 $query = $dbConnection->query("DELETE FROM sessions WHERE sid='".$_SESSION['SessionID']."'");
			 if($query)
				{
				  $_SESSION['SessionID'] = "";
				  $hostname = $_SERVER['HTTP_HOST'];
				  $path = dirname($_SERVER['PHP_SELF']);
				  header('Location: https://'.$hostname.($path == '/' ? '' : $path).'/rezepte.php');
				}
		  }
		break;
	 }
  }


?>

</body>
</html>