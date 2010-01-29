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
function printFooter()
{
  print("<br/><br/><a href=\"rezepte.php\">Rezeptliste</a><br/>\n");
}

function printCreateCategoryForm()
{
        print("<form action=category.php?action=createDbCategory method=post>\n");
        print("Name: <input name=name size=25><br>\n");
        print("<input type=submit value=Create> <input type=reset value=Cancel>\n");
		  print("</form>\n");
		  printFooter();
}

function printCategoryList()
{
	global $dbConnection;

	$dbConnection->query("SELECT * FROM categories ORDER BY name");
	$dbCategories = $dbConnection->getResultItems();

	print("<table border=1 cellspacing=0 cellpadding=2>\n");
	for($catCounter = 0; $catCounter < $dbConnection->getResultNumber(); $catCounter++)
	{
		print("<tr>\n");
		print("<td> ".$dbCategories[$catCounter]['name']."</td>\n");
		print("<td> <a href=category.php?action=editCategory&cid=".$dbCategories[$catCounter]['cid'].">Edit</a> </td>\n");
		print("<td> <a href=category.php?action=deleteCategory&cid=".$dbCategories[$catCounter]['cid'].">Delete</a> </td>\n");
		print("</tr>\n");
	}
	print("</table><br><br>\n");

	print("<a href=category.php?action=createCategory>Create category</a><br>\n");
	printFooter();
}

function printEditCategoryForm($cid)
{
	global $dbConnection;
	global $loginCheck;

	$dbConnection->query("SELECT * FROM categories WHERE cid='".$cid."'");
	$dbCategories = $dbConnection->getResultItems();
	print("Edit user account of ".$dbCategories[0]['name']."<br><br>\n");
	print("<form action=category.php?action=editDbCategory&cid=".$cid." method=post>\n");
	print("Name: <input name=name size=25 value=\"".$dbCategories[0]['name']."\"><br>\n");
	print("<input type=submit value=Change> <input type=reset value=Cancel>\n");
	print("</form>\n");
	printFooter();
}

function createDbCategory()
{
	global $dbConnection;

	{
		$dbConnection->query("SELECT * FROM categories WHERE name='".$_POST["name"]."'");
		$query = $dbConnection->getResultNumber();
		if($query == 0)
		{
			$result = $dbConnection->query("INSERT INTO categories
					(name) VALUES
					('".$_POST["name"]."')");
			if(!$result)
			{
				print("Database error: could not add category.<br>\n");
				printCreateCategory();
			}
		}
		else
		{
			print("Error, category already exists, please choose another name.<br>\n");
			printCreateCategory();
		}
	}
}

function deleteCategory($cid)
{
	global $dbConnection;

	$dbConnection->query("UPDATE rezepte SET category='0' WHERE category='".$cid."'");

	if($dbConnection->query("DELETE FROM categories WHERE cid='".$cid."'"))
	{
		print("Category deleted.<br>\n");
		printCategoryList();
	}
}

function editDbCategory($cid)
{
	global $dbConnection;

	print("Name is empty!<br>");
	$dbConnection->query("UPDATE categories SET name='".$_POST['name'].
							"' WHERE cid='".$cid."'");
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
	switch($_GET['action'])
	{
		case "createCategory":
		{
			print("<h1>Create category</h1>\n");
			printCreateCategoryForm();
			break;
		}
		case "createDbCategory":
		{
			createDbCategory();
			break;
		}
		case "deleteCategory":
		{
			deleteCategory($_GET['cid']);
			break;
		}
		case "editCategory":
		{
			print("<h1>Edit category</h1>\n");
			printEditCategoryForm($_GET['cid']);
			break;
		}
		case "editDbCategory":
		{
			editDbCategory($_GET['cid']);
			break;
		}
		default:
		{
			print("<h1>Category administration</h1>\n");
			printCategoryList();
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

