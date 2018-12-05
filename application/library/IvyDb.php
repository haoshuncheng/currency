<?php
class IvyDb {
	private static $conn = null;

	private static function init() {
		$opt = array (PDO::ATTR_PERSISTENT => true);
		$config = new Yaf_Config_Ini(CONFIG_INI, 'product');
		self::$conn = new PDO ($config->database->uri, 
			$config->database->username, $config->database->password, $opt);
    }

	/**
	 * @return PDO
	 */
	public static function getInstance() {
        if (self::$conn === null) {
            self::init();
        }
        return self::$conn;
    }

    static function exception($stmt) {
    	$info_array = $stmt->errorInfo();
//     	throw new Exception("PDO ERROR: " . $info_array[2]);
    	error_log("PDO ERROR: " . $info_array[2]);
    }

    /**
     * 根据sql查询。
     */
    public static function query($sql,$type='query') {
        $conn = self::getInstance();
        $stmt = $conn->prepare($sql);
        $result = null;
 
        if($stmt->execute()) {
        	switch ($type) {
        		case 'query':
        			$result = $stmt->fetchAll(PDO::FETCH_ASSOC); //fetchAll
        			break;
        		case 'update':
        			return true;
        			break;
        		case 'insert':
        			$result = $conn->lastInsertId();
        			break;
        		case 'delete':
        			return true;
        			break;
        		default:
        			# code...
        			break;
        	}
            
        } else {
            IvyDb::exception($stmt);
        }
        return $result;
    }

 
    
    //sample,  cannot called!
	/*    
    function insert() {
    	$conn = IvyDb::getInstance();
    	$sql = "insert into tab_name (column_1, column_2) values(?, ?)";
    	$stmt = $conn->prepare($sql);
    	$params = array(1, "a");
    	if($stmt->execute($params)) {
    		echo $conn->lastInsertId();//如果想取自增长id
    	} else {
    		IvyDb::exception($stmt);
    	}
    	
    }
    
	function update() {
		$conn = IvyDb::getInstance();
		$sql = "update tab_name set col1 = ?, col2 = ? where id = ?";
		$stmt = $conn->prepare($sql);
		$params = array(2, "b", 1);
		if($stmt->execute($params)) {
			return true;
		} else {
			IvyDb::exception($stmt);
		}
	}
	
	function query() {
		$sql = "select col1, col2 from tab_name where id = ? ";
		$conn = IvyDb::getInstance();
		$stmt = $conn->prepare($sql);
		$params = array(1);
		if($stmt->execute($params)) {
			//$result = $stmt->fetch(PDO::FETCH_ASSOC); //fetchOne
			$result = $stmt->fetchAll(PDO::FETCH_ASSOC); //fetchAll
			print_r($result);
		} else {
			IvyDb::exception($stmt);
		}
			
	}
    
	public function delete() {
		$conn = IvyDb::getInstance();
		$sql = "delete from tab_name where id = ?";
		$stmt = $conn->prepare($sql);
		$params = array(1);
		if($stmt->execute($params)) {
			return true;
		} else {
			IvyDb::exception($stmt);
		}
	}
    */
}
