<?php
session_start();
require_once("checklogin.inc.php");
require_once("dbinterface.inc.php");
/* session_register("$recipes"); */
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

$loginCheck = new LoginCheck();
$loginCheck->checkLogin();
$userRole = $loginCheck->getUserRole();

print($loginCheck->getLoginHeader());

class Recipe
{
  var $id;
  var $category;
  var $name;
  var $ingredients;
  var $preparation;
  var $experience;
  var $timeNeed;
  var $numberPeople;
  var $created;
  var $owner;
  var $rights;

  function Recipe()
  {
	 $this->id=0;
	 $this->category=0;
	 $this->name=" ";
	 $this->ingredients=" ";
	 $this->preparation=" ";
	 $this->experience=" ";;
	 $this->timeNeed=" ";
	 $this->numberPeople=4;
	 $this->created=" ";
	 $this->owner=0;
	 $this->rights=0;
  }

  function setId($id)
  {
    $this->id = $id;
  }
  
  function getId()
  {
    return $this->id;
  }

  function setCategory($category)
  {
    $this->category = $category;
  }

  function getCategory()
  {
    return $this->category;
  }

  function setName($name)
  {
    $this->name = $name;
  }

  function getName()
  {
    return $this->name;
  }

  function setIngredients($ingredients)
  {
    $this->ingredients = $ingredients;
  }

  function getIngredients()
  {
    return $this->ingredients;
  }

  function setPreparation($preparation)
  {
    $this->preparation = $preparation;
  }

  function getPreparation()
  {
    return $this->preparation;
  }

  function setExperience($experience)
  {
    $this->experience = $experience;
  }

  function getExperience()
  {
    return $this->experience;
  }

  function setTimeNeed($timeNeed)
  {
    $this->timeNeed = $timeNeed;
  }

  function getTimeNeed()
  {
    return $this->timeNeed;
  }

  function setNumberPeople($numberPeople)
  {
    $this->numberPeople = $numberPeople;
  }

  function getNumberPeople()
  {
    return $this->numberPeople;
  }

  function setCreated($created)
  {
    $this->created = $created;
  }

  function getCreated()
  {
    return $this->created;
  }

  function setOwner($owner)
  {
    $this->owner = $owner;
  }

  function getOwner()
  {
    return $this->owner;
  }

  function setRights($rights)
  {
    $this->rights = $rights;
  }

  function getRights()
  {
    return $this->rights;
  }
}


//Recipe access to DB ==================================================

function getRecipe($id)
{
  global $dbConnection;
  
  $dbConnection->query("SELECT * FROM rezepte WHERE id=".$id);
  $dbRecipe = $dbConnection->getResultItems();

  $recipe = new Recipe();
  $recipe->setID($dbRecipe[0]['id']);
  $recipe->setCategory($dbRecipe[0]['category']);
  $recipe->setName($dbRecipe[0]['name']);
  $recipe->setIngredients($dbRecipe[0]['ingredients']);
  $recipe->setPreparation($dbRecipe[0]['preparation']);
  $recipe->setExperience($dbRecipe[0]['experience']);
  $recipe->setTimeNeed($dbRecipe[0]['time_need']);
  $recipe->setNumberPeople($dbRecipe[0]['number_people']);
  $recipe->setCreated($dbRecipe[0]['created']);
  $recipe->setOwner($dbRecipe[0]['owner']);
  $recipe->setRights($dbRecipe[0]['rights']);

  return $recipe;
}

function getAllRecipes($category)
{
  global $dbConnection;

  if($category < 0)
	 {
		$queryResult = $dbConnection->query("SELECT * FROM rezepte ORDER BY name");
	 }
  else
	 {
		$queryResult = $dbConnection->query("SELECT * FROM rezepte WHERE category='".$category."' ORDER BY name");
	 }
  $numberResults = $dbConnection->getResultNumber();
  $dbRecipes = $dbConnection->getResultItems();
  for($rowCounter=0; $rowCounter < $numberResults; $rowCounter++)
	 {
		//$recipe = pg_fetch_object($queryResult, $rowCounter);
		//print("testName: ". $recipe->name ."<br>\n");
		$recipeArray[$rowCounter] = new Recipe();
		$recipeArray[$rowCounter]->setID($dbRecipes[$rowCounter]['id']);
		$recipeArray[$rowCounter]->setCategory($dbRecipes[$rowCounter]['category']);
		$recipeArray[$rowCounter]->setName($dbRecipes[$rowCounter]['name']);
		$recipeArray[$rowCounter]->setIngredients($dbRecipes[$rowCounter]['ingredients']);
		$recipeArray[$rowCounter]->setPreparation($dbRecipes[$rowCounter]['preparation']);
		$recipeArray[$rowCounter]->setExperience($dbRecipes[$rowCounter]['experience']);
		$recipeArray[$rowCounter]->setTimeNeed($dbRecipes[$rowCounter]['time_need']);
		$recipeArray[$rowCounter]->setNumberPeople($dbRecipes[$rowCounter]['number_people']);
		$recipeArray[$rowCounter]->setCreated($dbRecipes[$rowCounter]['created']);
		$recipeArray[$rowCounter]->setOwner($dbRecipes[$rowCounter]['owner']);
		$recipeArray[$rowCounter]->setRights($dbRecipes[$rowCounter]['rights']);
	 }
  return $recipeArray;
}

function addRecipe($recipe)
{
  global $dbConnection;

  $dbConnection->query("INSERT INTO rezepte 
	(category,name,ingredients,preparation,experience,time_need,number_people,created,owner,rights) VALUES ('"
							 . $recipe->getCategory() ."','"
							 . $recipe->getName() ."','"
							 . $recipe->getIngredients() ."','"
							 . $recipe->getPreparation() ."','"
							 . $recipe->getExperience() ."','"
							 . $recipe->getTimeNeed() ."',"
							 . $recipe->getNumberPeople() .",CURRENT_TIMESTAMP,"
							 . $recipe->getOwner() .","
							 . $recipe->getRights() .")");
}

function modifyRecipe($recipe)
{
  global $dbConnection;

  $dbConnection->query("UPDATE rezepte SET category="
							 . $recipe->getCategory() .", name='"
							 . $recipe->getName() ."', ingredients='"
							 . $recipe->getIngredients() ."', preparation='"
							 . $recipe->getPreparation() ."', experience='"
							 . $recipe->getExperience() ."', time_need='"
							 . $recipe->getTimeNeed() ."', number_people="
							 . $recipe->getNumberPeople() .", owner="
							 . $recipe->getOwner() .", rights="
							 . $recipe->getRights() ." WHERE id="
							 . $recipe->getId()
							 );
}

?>
<h1>Rezeptdatenbank</h1>
<?php

$dbConnection = new DbInterface();
//$dbConnection = new DatabaseConnection();
if(!$dbConnection->connect())
{
  print("Error: Could not connect to database<br>\n");
  exit;
} else {
  //print("Successfully connected to database<br>\n");
}

if(isset($_GET["viewRecipe"]))
{
  global $dbConnection;

  $recipe = getRecipe($_GET["viewRecipe"]);

  if($recipe->getCategory() >= 0)
	 {
		$dbConnection->query("SELECT * FROM categories WHERE cid='".$recipe->getCategory()."'");
		$dbCategory = $dbConnection->getResultItems();
		$category = $dbCategory[0]['name'];
	 }
  else
	 {
		$category = "Keine";
	 }

  ?>
	 <table border="0" bgcolor="#0000A0" cellspacing="3">
		 <tr><td>
		 <table width="600" border="0" bgcolor="#DCDCFF" cellspacing="10">
		 <tr>
		 <td>
  <?php
		 print("Kategorie: ".$category."<br>\n");
  ?>
					<h3>
					<?php print($recipe->getName()); ?>
					</h3>
				</td>
			</tr><tr>
				<td><br>
					<b>Zutaten</b>
				</td>
			</tr><tr>
				<td>
					<?php print(nl2br($recipe->getIngredients())); ?>
				</td>
			</tr><tr>
				<td><br>
					<b>Zubereitung</b>
				</td>
			</tr><tr>
				<td>
					<?php print(nl2br($recipe->getPreparation())); ?>
				</td>
			</tr><tr>
				<td><br>
					<b>Anzahl Personen: </b>
					<?php print(nl2br($recipe->getNumberPeople())); ?>
				</td>
			</tr><tr>
				<td><hr><br>
					<?php print("vom: ". $recipe->getCreated()); ?>
				</td>
			</tr>
		</table>
		</td></tr>
	</table>
	<br><br>
	<?php 
	if($userRole > 4)
	  {
		 print("<a href=\"rezepte.php?modifyRecipe=". $recipe->getId() ."\">Rezept ändern</a><br>\n");
		 print("<a href=\"rezepte.php?addRecipe=1\">Rezept hinzufügen</a><br>\n");
	  }
  print("<a href=\"rezepte.php\">Rezeptliste</a>\n");

} else if(isset($_GET["modifyRecipe"]) && ($userRole > 4)) {
	if(isset($_POST["Name"]))
	{
	  $dbConnection->query("SELECT * FROM categories WHERE name='".$_POST["Category"]."'");
	  $dbCategory = $dbConnection->getResultItems();

	  $recipe = new Recipe();
	  $recipe->setId($_GET["modifyRecipe"]);
	  $recipe->setCategory($dbCategory[0]['cid']);
	  $recipe->setName($_POST["Name"]);
	  $recipe->setIngredients($_POST["Ingredients"]);
	  $recipe->setPreparation($_POST["Preparation"]);
	  $recipe->setNumberPeople($_POST["NumberPeople"]);
	  modifyRecipe($recipe);
	  print("Rezept wurde geändert.<br><br>\n");
	  ?>
		<br><br>
		<a href="rezepte.php?addRecipe=1">Rezept hinzufügen</a><br>
		<a href="rezepte.php">Rezeptliste</a>
	  <?php
		
	} else {
	  $recipe = getRecipe($_GET["modifyRecipe"]);
	  
	  if($recipe->getCategory())
		 {
			$dbConnection->query("SELECT * FROM categories WHERE cid='".$recipe->getCategory()."'");
			$dbCategory = $dbConnection->getResultItems();
			$catId = $dbCategory[0]['cid'];
		 }
	  else
		 {
			$catId = 0;
		 }

		?>
		<table border="0" bgcolor="#0000A0" cellspacing="3">
		<tr><td>
		<table width="200" border="0" bgcolor="#DCDCFF" cellspacing="10">
			<tr><td>
			   <?php print("<form action=\"rezepte.php?modifyRecipe=". $_GET["modifyRecipe"] ."\" method=\"post\">"); ?>
			   <p>Kategorie: 
				<select name="Category" size="1">
				<?php
         	$dbConnection->query("SELECT * FROM categories ORDER BY name");
				$dbCategories = $dbConnection->getResultItems();

				for($catCounter = 0; $catCounter < $dbConnection->getResultNumber(); $catCounter++)
				  {
					 if($dbCategories[$catCounter]['cid'] == $catId)
						{
						  print("<option selected>".$dbCategories[$catCounter]['name']. "</option><br/>\n");
						}
					 else
						{
						  print("<option>".$dbCategories[$catCounter]['name']. "</option><br/>\n");
						}
				  }
				?>
				</select></p>

			   <p>Name: <br>
				<?php print("<input name=\"Name\" size=\"50\" maxlength=\"50\" value=\"". $recipe->getName() ."\">"); ?>
				</p>
				<p>Zutaten: <br>
				<textarea name="Ingredients" rows="7" cols="50"><?php print($recipe->getIngredients()) ?></textarea></p>
				<p>Zubereitung: <br>
				<textarea name="Preparation" rows="10" cols="50"><?php print($recipe->getPreparation()) ?></textarea></p>
				<p>Anzahl Personen: <input name="NumberPeople" size="2" maxlength="2" value=<?php print("\"". $recipe->getNumberPeople() ."\""); ?>></p>
				<br>
				<p><input name="Ok" type="submit" value="Rezept ändern">
				<input name="Cancel" type="reset" value="Zurücksetzen"></p>
			</td></tr>
		</table>
		</td></tr>
		</table><br><br>
		<a href="rezepte.php">Rezeptliste</a>
		<?php
	}

 } else if(isset($_GET["addRecipe"]) && ($userRole > 4)) {
	if(isset($_POST["Name"]))
	{
	  $dbConnection->query("SELECT * FROM categories WHERE name='".$_POST["Category"]."'");
	  $dbCategory = $dbConnection->getResultItems();

	  $recipe = new Recipe();
	  $recipe->setName($_POST["Name"]);
	  $recipe->setCategory($dbCategory[0]['cid']);
	  $recipe->setIngredients($_POST["Ingredients"]);
	  $recipe->setPreparation($_POST["Preparation"]);
	  $recipe->setNumberPeople($_POST["NumberPeople"]);
	  addRecipe($recipe);
	  print("Rezept wurde hinzugefügt.<br><br>\n");
	  ?>
		<br><br>
		<a href="rezepte.php?addRecipe=1">Rezept hinzufügen</a><br>
		<a href="rezepte.php">Rezeptliste</a>
	  <?php

	} else {

		?>
		<table border="0" bgcolor="#0000A0" cellspacing="3">
		<tr><td>
		<table width="200" border="0" bgcolor="#DCDCFF" cellspacing="10">
			<tr><td>
				<form action="rezepte.php?addRecipe=1" method="post">
			   <p>Kategorie: 
				<select name="Category" size="1">
				<?php
         	$dbConnection->query("SELECT * FROM categories ORDER BY name");
				$dbCategories = $dbConnection->getResultItems();

				for($catCounter = 0; $catCounter < $dbConnection->getResultNumber(); $catCounter++)
				  if($dbCategories[$catCounter]['cid'] == 0)
					 {
						print("<option selected>".$dbCategories[$catCounter]['name']. "</option><br/>\n");
					 }
				  else
					 {
						print("<option>".$dbCategories[$catCounter]['name']. "</option><br/>\n");
					 }
				?>
				</select></p>
				<p>Name: <br>
				<input name="Name" size="50" maxlength="50"></p>
				<p>Zutaten: <br>
				<textarea name="Ingredients" rows="7" cols="50"></textarea></p>
				<p>Zubereitung: <br>
				<textarea name="Preparation" rows="10" cols="50"></textarea></p>
				<p>Anzahl Personen: <input name="NumberPeople" size="2" maxlength="2" value="4"></p>
				<br>
				<p><input name="Ok" type="submit" value="Rezept hinzufügen">
				<input name="Cancel" type="reset" value="Zurücksetzen"></p>
				</form>
			</td></tr>
		</table>
		</td></tr>
		</table><br><br>
		<a href="rezepte.php">Rezeptliste</a>
		<?php
	}

} else {

  ?>
  <form action="rezepte.php" method="post">
  <p>Kategorie: 
  <select name="Category" size="1">
  <option selected>Alle</option>
  <?php
  $dbConnection->query("SELECT * FROM categories ORDER BY name");
  $dbCategories = $dbConnection->getResultItems();
  
  for($catCounter = 0; $catCounter < $dbConnection->getResultNumber(); $catCounter++)
	 {
		print("<option>".$dbCategories[$catCounter]['name']. "</option><br/>\n");
	 }
  ?>
  </select></p>
  <p><input name="Update" type="submit" value="Aktualisieren"></p>
  </form>

  <?php

  $catId = -1;
  if(isset($_POST["Category"]))
	 {
		if($_POST["Category"] != "Alle")
		  {
			 $dbConnection->query("SELECT * FROM categories WHERE name='".$_POST["Category"]."'");
			 $dbCategory = $dbConnection->getResultItems();
		
			 $catId = $dbCategory[0]['cid'];
		  }
	 }
  $recipes = getAllRecipes($catId);

	?>
	<table border="0" bgcolor="#0000A0" cellspacing="3">
	<tr><td>
	<table width="600" border="0" bgcolor="#DCDCFF" cellspacing="10">
		<tr><td>
			<b>Liste aller Rezepte:</b><br>
		</td>
		</tr><tr>
		<td><ul>
	<?php

  for($i=0; $i < count($recipes); $i++)
  {
	 print("<li>\n");
    print("<a href=rezepte.php?viewRecipe=". $recipes[$i]->getId() .">". $recipes[$i]->getName() ."</a>\n");
    print("</li>\n");
  }

	
	?>
		</ul></td></tr>
	</table>
	</td></tr>
	</table><br><br>
	<?php
	if($userRole > 4)
	  {
		 print("<a href=\"rezepte.php?addRecipe=1\">Rezept hinzufügen</a><br>\n");
	  }
}

if(!$dbConnection->disconnect())
{
  print("Error: Could not disconnect to database<br>\n");
} else {
  //print("Successfully disconnected from database<br>\n");
}

?>

</body>
</html>
