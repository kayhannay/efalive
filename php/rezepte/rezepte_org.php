<?php
session_start();
session_register("$recipes");
?>
<html>
<head>
<title>Rezeptdatenbank</title>
</head>
<body>

<?php

class Database
{
  var $server;
  var $port;
  var $username;
  var $password;
  var $database;

  function setServer($server)
  {
    $this->server = $server;
  }
  
  function setPort($port)
  {
    $this->port = $port;
  }

  function setUsername($name)
  {
    $this->username = $name;
  }

  function setPassword($pw)
  {
    $this->password = $pw;
  }
  
  function setDatabase($database)
  {
    $this->database = $database;
  }
  

}

class PostgreSQLdatabase extends Database
{
  var $dbConnection;
  
  function PostgreSQLdatabase()
  {
    $this->server = "localhost";
    $this->port = "5432";
    $this->username = "rezeptuser";
    $this->password = "pgSQLrezepte";
    $this->database = "rezepte";
    $this->table = "rezepte";
  }

  function connect()
  {
    $this->dbConnection = pg_connect("host=". $this->server .
				     " port=". $this->port .
				     " dbname=". $this->database .
				     " user=". $this->username .
				     " password=". $this->password);

    pg_exec($this->dbConnection, "SET CLIENT_ENCODING TO ISO_8859_15");

    if($this->dbConnection)
    {
      return 0;
    }
    return 1;
  }

  function disconnect()
  {
    if(pg_close($this->dbConnection)) 
      {
	return 0;
      } else {
	return 1;
      }
  }

}

class DatabaseConnection
{
  var $dbBackend;
  var $recipeArray;
  var $table;
  
  function DatabaseConnection($type = "pgSQL")
  {
    switch($type)
    {
    	case "pgSQL":
			$this->dbBackend = new PostgreSQLdatabase();
			break;
      default:
			print("Error: not a known database type!<br>\n");
			return NULL;
    }
	 $this->table = "rezepte";
  }

  function setTable($table)
  {
    $this->table = $table;
  }

  function connect()
  {
    $this->dbBackend->connect();
  }
  
  function disconnect()
  {
    $this->dbBackend->disconnect();
  }

  function getAllRecipes()
  {
    $queryResult = pg_exec($this->dbBackend->dbConnection, "SELECT * FROM ". $this->table);
    $numberResults = pg_numrows($queryResult);
    for($rowCounter=0; $rowCounter < $numberResults; $rowCounter++)
      {
	$recipe = pg_fetch_object($queryResult, $rowCounter);
	//print("testName: ". $recipe->name ."<br>\n");
	$this->recipeArray[$rowCounter] = new Recipe();
	$this->recipeArray[$rowCounter]->setID($recipe->id);
	$this->recipeArray[$rowCounter]->setCategory($recipe->category);
	$this->recipeArray[$rowCounter]->setName($recipe->name);
	$this->recipeArray[$rowCounter]->setIngredients($recipe->ingredients);
	$this->recipeArray[$rowCounter]->setPreparation($recipe->preparation);
	$this->recipeArray[$rowCounter]->setExperience($recipe->experience);
	$this->recipeArray[$rowCounter]->setTimeNeed($recipe->time_need);
	$this->recipeArray[$rowCounter]->setNumberPeople($recipe->number_people);
	$this->recipeArray[$rowCounter]->setCreated($recipe->created);
	$this->recipeArray[$rowCounter]->setOwner($recipe->owner);
	$this->recipeArray[$rowCounter]->setRights($recipe->rights);
      }
    return $this->recipeArray;
  }

  function getRecipe($id)
  {
    $queryResult = pg_exec($this->dbBackend->dbConnection, 
			   "SELECT * FROM "
			   . $this->table .
			   " WHERE id=". $id);
    //print("Anzahl Treffer: ". pg_numrows($queryResult) ."<br><br>\n");
    $dbRecipe = pg_fetch_object($queryResult, 0);
    $recipe = new Recipe();
    $recipe->setID($dbRecipe->id);
    $recipe->setCategory($dbRecipe->category);
    $recipe->setName($dbRecipe->name);
    $recipe->setIngredients($dbRecipe->ingredients);
    $recipe->setPreparation($dbRecipe->preparation);
    $recipe->setExperience($dbRecipe->experience);
	 $recipe->setTimeNeed($dbRecipe->time_need);
	 $recipe->setNumberPeople($dbRecipe->number_people);
    $recipe->setCreated($dbRecipe->created);
    $recipe->setOwner($dbRecipe->owner);
    $recipe->setRights($dbRecipe->rights);

    return $recipe;
  }

  function addRecipe($recipe)
  {
    pg_exec($this->dbBackend->dbConnection, "INSERT INTO "
	    . $this->table .
	    " (category,name,ingredients,preparation,experience,time_need,number_people,created,owner,rights) VALUES ("
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
		pg_exec($this->dbBackend->dbConnection, "UPDATE "
			. $this->table ." SET category="
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

$dbConnection = new DatabaseConnection("pgSQL");
if(db == NULL)
{
  print("Fatal Error: could not create database connection");
  exit;
}

if($dbConnection->connect())
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
	<?php print("<a href=\"rezepte.php?modifyRecipe=". $recipe->getId() ."\">Rezept ändern</a><br>\n"); ?>
	<a href="rezepte.php?addRecipe=1">Rezept hinzufügen</a><br>
	<a href="rezepte.php">Rezeptliste</a>
	<?php

} else if(isset($_GET["modifyRecipe"])) {
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
		<a href="rezepte.php?addRecipe=1">Rezept hinzufügen</a><br>
		<a href="rezepte.php">Rezeptliste</a>
	  <?php
		
	} else {
	  $recipe = $dbConnection->getRecipe($_GET["modifyRecipe"]);

		?>
		<table border="0" bgcolor="#0000A0" cellspacing="3">
		<tr><td>
		<table width="200" border="0" bgcolor="#DCDCFF" cellspacing="10">
			<tr><td>
				<?php print("<form action=\"rezepte.php?modifyRecipe=". $_GET["modifyRecipe"] ."\" method=\"post\">"); ?>
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

} else if(isset($_GET["addRecipe"])) {
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
		<a href="rezepte.php">Rezeptliste</a>
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
    print("<a href=rezepte.php?viewRecipe=". $recipes[$i]->getId() .">". $recipes[$i]->getName() ."</a>\n");
    print("</li>\n");
  }

	
	?>
		</ul></td></tr>
	</table>
	</td></tr>
	</table><br><br>
	<a href="rezepte.php?addRecipe=1">Rezept hinzufügen</a><br>
	<?php

}

if($dbConnection->disconnect())
{
  print("Error: Could not disconnect to database<br>\n");
} else {
  //print("Successfully disconnected from database<br>\n");
}
	
?>

</body>
</html>