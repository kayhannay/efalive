<?php
require("settings.inc.php");

class DbInterface_pgsql
{
  var $dbConnection;
  var $queryResult;

  function connect()
  {
    $retVal = 0;

    $this->dbConnection = 0;
    $this->queryResult = 0;

    $this->dbConnection = pg_connect("host=". $_SESSION['database']['host'] .
                                     " port=". $_SESSION['database']['port'] .
                                     " dbname=". $_SESSION['database']['dbname'] .
                                     " user=". $_SESSION['database']['user'] .
                                     " password=". $_SESSION['database']['passwd']);
    if($this->dbConnection)
    {
      $retVal = 1;

      pg_query($this->dbConnection, "SET CLIENT_ENCODING TO ISO_8859_15");
    }

    return retVal;
  }

  function disconnect()
  {
    $retVal = 0;

    if(pg_close($this->dbConnection))
      {
        $retVal = 1;
      }

    return retVal;
  }

  function query($in_queryString)
  {
    $this->queryResult = pg_query($this->dbConnection, $in_queryString);

    return $this->queryResult;
  }

  function getResultNumber()
  {
	 return pg_num_rows($this->queryResult);
  }

  function getResultItems()
  {
    $resultArray;
    $itemNumber = pg_num_rows($this->queryResult);

    for($itemCounter = 0; $itemCounter < $itemNumber; $itemCounter++)
    {
      $resultArray[$itemCounter] = pg_fetch_array($this->queryResult, $itemCounter, PGSQL_ASSOC);
    }

    return $resultArray;
  }
}

?>