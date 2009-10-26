<?php
require("settings.inc.php");

class DbInterface_mysql
{
  var $dbConnection;
  var $queryResult;

  function connect()
  {
    $retVal = 0;

    $this->dbConnection = 0;
    $this->queryResult = 0;

    $this->dbConnection = mysql_connect($_SESSION['database']['host'],
                                        $_SESSION['database']['user'],
                                        $_SESSION['database']['passwd']);
    if($this->dbConnection)
    {
      $retVal = 1;
      
      mysql_select_db($_SESSION['database']['dbname'], $this->dbConnection);
      mysql_set_charset("latin1", $this->dbConnection);
    }

    return retVal;
  }

  function disconnect()
  {
    $retVal = 0;

    if(mysql_close($this->dbConnection))
      {
        $retVal = 1;
      }

    return retVal;
  }

  function query($in_queryString)
  {
    $this->queryResult = mysql_query($in_queryString, $this->dbConnection);

    return $this->queryResult;
  }

  function getResultNumber()
  {
	 return mysql_num_rows($this->queryResult);
  }

  function getResultItems()
  {
    $resultArray;
    
    $itemCounter = 0;
    while($row = mysql_fetch_array($this->queryResult, MYSQL_ASSOC)) {
      $resultArray[$itemCounter] = $row;
      $itemCounter++;
    }

    return $resultArray;
  }
}

?>

