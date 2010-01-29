<?php
session_start();

require_once("checklogin.inc.php");
require_once("dbinterface.inc.php");
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
       "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>Rezeptdatenbank</title>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
</head>
<body>

<?php

function printCreateUserForm()
{
        print("<form action=admin.php?action=createDbUser method=post>\n");
        print("Name: <input name=name size=25><br>\n");
        print("Login: <input name=user size=15><br>\n");
        print("Password: <input name=passwd size=15 type=password><br>\n");
        print("Confirm: <input name=confirm size=15 type=password><br>\n");
        print("Rights: <select name=role size=1>\n");
        print("<option value=0 selected=\"selected\">Guest</option>\n");
        print("<option value=5>User</option>\n");
        print("<option value=10>Admin</option>\n");
        print("</select>\n");
        print("<input type=submit value=Create> <input type=reset value=Cancel>\n");
	print("</form>\n");
}

function printUserList()
{
	global $dbConnection;

	$dbConnection->query("SELECT * FROM users");
	$dbUsers = $dbConnection->getResultItems();

	print("<table border=1 cellspacing=0 cellpadding=2>\n");
	for($userCounter = 0; $userCounter < $dbConnection->getResultNumber(); $userCounter++)
	{
		print("<tr>\n");
		print("<td> ".$dbUsers[$userCounter]['login']." </td><td> ".$dbUsers[$userCounter]['name']." </td>\n");
		print("<td> ".$dbUsers[$userCounter]['role']." </td>\n");
		print("<td> <a href=admin.php?action=editUser&uid=".$dbUsers[$userCounter]['uid'].">Edit</a> </td>\n");
		print("<td> <a href=admin.php?action=deleteUser&uid=".$dbUsers[$userCounter]['uid'].">Delete</a> </td>\n");
		print("</tr>\n");
	}
	print("</table><br><br>\n");

	print("<a href=admin.php?action=createUser>Create user account</a><br>\n");
}

function printEditUserForm($uid)
{
	global $dbConnection;
	global $loginCheck;

	$dbConnection->query("SELECT * FROM users WHERE uid='".$uid."'");
	$dbUser = $dbConnection->getResultItems();
	print("Edit user account of ".$dbUser[0]['login']."<br><br>\n");
	print("<form action=admin.php?action=editDbUser&uid=".$uid." method=post>\n");
	print("Name: <input name=name size=25 value=\"".$dbUser[0]['name']."\"><br>\n");
	print("Password: <input name=passwd size=15 type=password><br>\n");
	print("Confirm: <input name=confirm size=15 type=password><br>\n");
	if($loginCheck->getUserRole() == 10)
	{
		print("Rights: <select name=role size=1>\n");
		print("<option value=0");
		if($dbUser[0]['role'] == 0)
		{
			print(" selected=\"selected\"");
		}
		print(">Guest</option>\n");
		print("<option value=5");
		if($dbUser[0]['role'] == 5)
		{
			print(" selected=\"selected\"");
		}
		print(">User</option>\n");
		print("<option value=10");
		if($dbUser[0]['role'] == 10)
		{
			print(" selected=\"selected\"");
		}
		print(">Admin</option>\n");
		print("</select><br>\n");
	}
	print("<input type=submit value=Change> <input type=reset value=Cancel>\n");
	print("</form>\n");
}

function createDbUser()
{
	global $dbConnection;

	if($_POST["passwd"] != $_POST["confirm"])
        {
		echo "ERROR: Password was not the same !!";
		echo "<a href=admin.php?action=createUser>Again</a>";
	}
	else
	{
		$dbConnection->query("SELECT * FROM users WHERE login='".$_POST["user"]."'");
		$query = $dbConnection->getResultNumber();
		if($query == 0)
		{
			$result = $dbConnection->query("INSERT INTO users
					(passwd, login, name, role, created) VALUES
					('".sha1($_POST["passwd"])."','".
						$_POST["user"]."','".
						$_POST["name"]."','".
						$_POST["role"]."',
						CURRENT_TIMESTAMP )");
			if(!$result)
			{
				print("Database error: could not add user.<br>\n");
				printCreateUser();
			}
		}
		else
		{
			print("Error, user already exists, please choose another login name.<br>\n");
			printCreateUser();
		}
	}
}

function deleteUser($uid)
{
	global $dbConnection;

	if($dbConnection->query("DELETE FROM users WHERE uid='".$uid."'"))
	{
		print("User deleted.<br>\n");
		printUserList();
	}
}

function editDbUser($uid)
{
	global $dbConnection;

	if($_POST['passwd'] == "")
	{
		print("Passwd is empty!<br>");
		$dbConnection->query("UPDATE users SET name='".$_POST['name'].
							"', role='".$_POST['role'].
							"' WHERE uid='".$uid."'");
	}
	else
	{
                if($_POST["passwd"] == $_POST["confirm"])
		{
			print("Passwd is filled!<br>");
			$dbConnection->query("UPDATE users SET name='".$_POST['name'].
							"', role='".$_POST['role'].
							"', passwd='".sha1($_POST['passwd']).
							"' WHERE uid='".$uid."'");
		}
		else
		{
			print("Password was not confirmed correctly<br><br>\n");
		}
	}
}


//************************//
// Main program           //
//************************//

$loginCheck = new LoginCheck();
$loginCheck->checkLogin();

print($loginCheck->getLoginHeader());


$dbConnection = new DbInterface();
if($dbConnection->connect())
{
	if($loginCheck->getUserRole() < 10)
	{
		switch($_GET['action'])
		{
			case "editDbUser":
			{
				editDbUser($_GET['uid']);
				break;
			}
			default:
			{
				if($_SESSION['SessionID'])
				{
					$dbConnection->query("SELECT * FROM sessions WHERE sid='".$_SESSION['SessionID']."'");
					$dbSession = $dbConnection->getResultItems();
					printEditUserForm($dbSession[0]['uid']);
				}
				else
				{
			  		print("You don't have enough rights to enter this page.<br>\n");
				}
			}
		}
        print("</body>\n");
        print("</html>\n");
	
		exit;
	}

	switch($_GET['action'])
	{
		case "createUser":
		{
			print("<h1>Create user</h1>\n");
			printCreateUserForm();
			break;
		}
		case "createDbUser":
		{
			createDbUser();
			break;
		}
		case "deleteUser":
		{
			deleteUser($_GET['uid']);
			break;
		}
		case "editUser":
		{
			print("<h1>Edit user</h1>\n");
			printEditUserForm($_GET['uid']);
			break;
		}
		case "editDbUser":
		{
			editDbUser($_GET['uid']);
			break;
		}
		default:
		{
			print("<h1>User administration</h1>\n");
			printUserList();
		}
	}
	$dbConnection->disconnect();
}
else
{
	print("Could not connect to the database.<br>\n");
}

?>
</body>
</html>
