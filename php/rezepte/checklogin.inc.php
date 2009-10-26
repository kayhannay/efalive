<?php
require("dbinterface.inc.php");

class LoginCheck
{
  var $validUser;
  var $loginHeader;
  var $userName;
  var $userRole;

  function LoginCheck()
  {
	 $this->validUser = 0;
	 $this->loginHeader = "";
         $this->userName = "";
         $this->userRole = 0;
  }

  function checkLogin()
  {
	 $retVal = 0;

	 $dbConnection = new DbInterface();

	 if($dbConnection->connect())
		{
		  /* Delete all expired sessions */
		  $dbConnection->query("DELETE FROM sessions WHERE expires<".time());
		
		  /* Fetch session for the given session ID from the database */
		  $dbConnection->query("SELECT * FROM sessions WHERE sid='".$_SESSION['SessionID']."'");
		  $query = $dbConnection->getResultNumber();

		  if($query == 0)
			 {
				$this->loginHeader = $this->loginHeader."<a href=login.php>login</a><br>";
			 }
		  else if($query > 1)
			 {
				$this->loginHeader = $this->loginHeader."ERROR: Many sessions with this ID exist !!<br>";
			 }
		  else
			 {
				$dbSessions = $dbConnection->getResultItems();
				
				if(($dbSessions[0]['ip'] != getenv('REMOTE_ADDR')) || ($dbSessions[0]['browser'] != getenv('HTTP_USER_AGENT')))
				  {
					 $dbConnection->query("DELETE FROM sessions WHERE sid='".$dbSessions[0]['sid']."'");
					 $this->loginHeader = $this->loginHeader."ERROR: session closed for security reasons<br>";
				  }
				else
				  {
					 $dbConnection->query("UPDATE sessions SET expires='".(time() + (60 * 30))."' WHERE sid='".$dbSessions[0]['sid']."'");
					 //echo "Session is OK.<br>";
					 $query = $dbConnection->query("SELECT * FROM users WHERE uid='".$dbSessions[0]['uid']."'");
					 
					 if($query)
						{
						  $dbUser = $dbConnection->getResultItems();
						  $this->userName = $dbUser[0]['name'];
						  $this->userRole = $dbUser[0]['role'];
						  $this->loginHeader = $this->loginHeader."Logged in as ".$dbUser[0]['name']." [".$dbUser[0]['login']."] | ";
						}
					 $this->loginHeader = $this->loginHeader."<a href=login.php?action=logout>logout</a> ";
					 switch($this->userRole)
					 {
					   case 0:
					     {
						$this->loginHeader = $this->loginHeader."| <a href=admin.php>Account</a>";
						break;
					     }
					   case 5:
					     {
						$this->loginHeader = $this->loginHeader."| <a href=admin.php>Account</a> | <a href=category.php>Categories</a>";
						break;
					     }
					   case 10:
					     {
						$this->loginHeader = $this->loginHeader."| <a href=admin.php>Administration</a> | <a href=category.php>Categories</a>";
						break;
					     }
					   default:
					     {
					     }
					 }
					 $this->loginHeader = $this->loginHeader."<br>";
					 $retVal = 1;
					 $this->validUser = 1;
				  }
			 }
		  $dbConnection->disconnect();
		}
	 else
		{
		  $this->loginHeader = $this->loginHeader."ERROR: Connection to database failed!<br>";
		}

	 return $retVal;
  }

  function isValidUser()
  {
	 return $this->validUser;
  }

  function getLoginHeader()
  {
	 return $this->loginHeader;
  }

  function getUserName()
  {
	return $this->userName;
  }

  function getUserRole()
  {
	return $this->userRole;
  }
}
?>