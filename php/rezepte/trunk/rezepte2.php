<?php
session_start();
require_once("checklogin.inc.php");
require_once("dbinterface.inc.php");
/* session_register("$recipes"); */
?>
<html>
<head>
<title>Rezeptdatenbank</title>
</head>
<body>

<?php

$loginCheck = new LoginCheck();
$loginCheck->checkLogin();
$userRole = $loginCheck->getUserRole();

print($loginCheck->getLoginHeader());


class DatabaseConnection
{
  var $dbConnection;

  var $table;
  
  function DatabaseConnection()
  {
	$this->dbConnection = new DbInterface();
  }

  function connect()
  {
    return $this->dbConnection->connect();
  }
  
  function disconnect()
  {
    return $this->dbConnection->disconnect();
  }

  function getAllRecipes()
  {
    $queryResult = $this->dbConnection->query("SELECT * FROM rezepte");
    $numberResults = $this->dbConnection->getResultNumber();
    $dbRecipes = $this->dbConnection->getResultItems();
    for($rowCounter=0; $rowCounter < $numberResults; $rowCounter++)
      {
	//$recipe = pg_fetch_object($queryResult, $rowCounter);
	//print("testName: ". $recipe->name ."<br>\n");
	$this->recipeArray[$rowCounter] = new Recipe();
	$this->recipeArray[$rowCounter]->setID($dbRecipes[$rowCounter]['id']);
	$this->recipeArray[$rowCounter]->setCategory($dbRecipes[$rowCounter]['category']);
	$this->recipeArray[$rowCounter]->setName($dbRecipes[$rowCounter]['name']);
	$this->recipeArray[$rowCounter]->setIngredients($dbRecipes[$rowCounter]['ingredients']);
	$this->recipeArray[$rowCounter]->setPreparation($dbRecipes[$rowCounter]['preparation']);
	$this->recipeArray[$rowCounter]->setExperience($dbRecipes[$rowCounter]['experience']);
	$this->recipeArray[$rowCounter]->setTimeNeed($dbRecipes[$rowCounter]['time_need']);
	$this->recipeArray[$rowCounter]->setNumberPeople($dbRecipes[$rowCounter]['number_people']);
	$this->recipeArray[$rowCounter]->setCreated($dbRecipes[$rowCounter]['created']);
	$this->recipeArray[$rowCounter]->setOwner($dbRecipes[$rowCounter]['owner']);
	$this->recipeArray[$rowCounter]->setRights($dbRecipes[$rowCounter]['rights']);
      }
    return $this->recipeArray;
  }

  function getRecipe($id)
  {
	$this->dbConnection->query("SELECT * FROM rezepte WHERE id=".$id);

	$dbRecipe = $this->dbConnection->getResultItems();

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

  function addRecipe($recipe)
  {
    $this->dbConnection->query("INSERT INTO rezepte 
	(category,name,ingredients,preparation,experience,time_need,number_people,created,owner,rights) VALUES ("
	    . $recipe->getCategory() .",'"
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
	$this->dbConnection->query("UPDATE rezepte SET category="
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
			

}

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

?>
<h1>Rezeptdatenbank</h1>
<?php

$dbConnection = new DatabaseConnection();
if(db == NULL)
{
  print("Fatal Error: could not create database connection");
  exit;
}

if(!$dbConnection->connect())
{
  print("Error: Could not connect to database<br>\n");
  exit;
} else {
  //print("Successfully connected to database<br>\n");
}

if(isset($_GET["viewRecipe"]))
{
  $recipe = $dbConnection->getRecipe($_GET["viewRecipe"]);

	?>
	<table border="0" bgcolor="#0000A0" cellspacing="3">
		<tr><td>
		<table width="600" border="0" bgcolor="#DCDCFF" cellspacing="10">
			<tr>
				<td>
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
		 print("<a href=\"rezepte2.php?modifyRecipe=". $recipe->getId() ."\">Rezept ändern</a><br>\n");
		 print("<a href=\"rezepte2.php?addRecipe=1\">Rezept hinzufügen</a><br>\n");
	  }
  print("<a href=\"rezepte2.php\">Rezeptliste</a>\n");

} else if(isset($_GET["modifyRecipe"]) && ($userRole > 4)) {
	if(isset($_POST["Name"]))
	{
	  $recipe = new Recipe();
	  $recipe->setId($_GET["modifyRecipe"]);
	  $recipe->setName($_POST["Name"]);
	  $recipe->setIngredients($_POST["Ingredients"]);
	  $recipe->setPreparation($_POST["Preparation"]);
	  $recipe->setNumberPeople($_POST["NumberPeople"]);
	  $dbConnection->modifyRecipe($recipe);
	  print("Rezept wurde geändert.<br><br>\n");
	  ?>
		<br><br>
		<a href="rezepte2.php?addRecipe=1">Rezept hinzufügen</a><br>
		<a href="rezepte2.php">Rezeptliste</a>
	  <?php
		
	} else {
	  $recipe = $dbConnection->getRecipe($_GET["modifyRecipe"]);

		?>
		<table border="0" bgcolor="#0000A0" cellspacing="3">
		<tr><td>
		<table width="200" border="0" bgcolor="#DCDCFF" cellspacing="10">
			<tr><td>
				<?php print("<form action=\"rezepte2.php?modifyRecipe=". $_GET["modifyRecipe"] ."\" method=\"post\">"); ?>
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
		<a href="rezepte2.php">Rezeptliste</a>
		<?php
	}

 } else if(isset($_GET["addRecipe"]) && ($userRole > 4)) {
	if(isset($_POST["Name"]))
	{
	  $recipe = new Recipe();
	  $recipe->setName($_POST["Name"]);
	  $recipe->setIngredients($_POST["Ingredients"]);
	  $recipe->setPreparation($_POST["Preparation"]);
	  $recipe->setNumberPeople($_POST["NumberPeople"]);
	  $dbConnection->addRecipe($recipe);
	  print("Rezept wurde hinzugefügt.<br><br>\n");
	  ?>
		<br><br>
		<a href="rezepte2.php?addRecipe=1">Rezept hinzufügen</a><br>
		<a href="rezepte2.php">Rezeptliste</a>
	  <?php

	} else {

		?>
		<table border="0" bgcolor="#0000A0" cellspacing="3">
		<tr><td>
		<table width="200" border="0" bgcolor="#DCDCFF" cellspacing="10">
			<tr><td>
				<form action="rezepte2.php?addRecipe=1" method="post">
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
			</td></tr>
		</table>
		</td></tr>
		</table><br><br>
		<a href="rezepte2.php">Rezeptliste</a>
		<?php
	}

} else {

  $recipes = $dbConnection->getAllRecipes();

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
    print("<a href=rezepte2.php?viewRecipe=". $recipes[$i]->getId() .">". $recipes[$i]->getName() ."</a>\n");
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
		 print("<a href=\"rezepte2.php?addRecipe=1\">Rezept hinzufügen</a><br>\n");
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