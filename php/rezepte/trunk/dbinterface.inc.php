<?php
require_once("dbinterface_pgsql.inc.php");

class DbInterface
{
  var $dbConnector;

  function DbInterface()
  {
    $this->dbConnector = 0;

    switch($_SESSION['database']['type'])
    {
      case "pgsql":
      {
        $this->dbConnector = new DbInterface_pgsql();
        break;
      }
      default:
      {
        $this->dbConnector = new DbInterface_pgsql();
      }
    }
  }

  function connect()
  {
    return $this->dbConnector->connect();
  }

  function disconnect()
  {
    return $this->dbConnector->disconnect();
  }

  function query($in_queryString)
  {
    return $this->dbConnector->query($in_queryString);
  }

  function getResultNumber()
  {
	 return $this->dbConnector->getResultNumber();
  }

  function getResultItems()
  {
    return $this->dbConnector->getResultItems();
  }

}

?>