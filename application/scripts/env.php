<?php
define('APP_PATH', dirname(dirname(dirname(__FILE__))));
define('CONFIG_INI', APP_PATH . '/conf/application.ini');

set_include_path(APP_PATH . '/application/models' . PATH_SEPARATOR . APP_PATH . '/application/library' . PATH_SEPARATOR . get_include_path());

// Requests
require_once APP_PATH . '/application/library/Requests.php';
// Next, make sure Requests can load internal classes
Requests::register_autoloader();

spl_autoload_register(function($class){
    if (class_exists($class, false) || interface_exists($class, false)) {
	  	return;
	}
    $class = str_replace('_', DIRECTORY_SEPARATOR, $class);
    if(substr($class, -5) ==  'Model' && substr($class, -6) !=  DIRECTORY_SEPARATOR.'Model') { // oops, Google_Model!
        $class = substr($class, 0, -5);
    } 
    
    $file = $class.'.php';
#    if (file_exists($file)) {
#        require_once($file);
#    }
     require_once $file;
});

