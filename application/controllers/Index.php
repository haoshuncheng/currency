<?php
class IndexController extends Yaf_Controller_Abstract {

	/**
     * 获取主数据 
     * type：1为行情数据 2为交易所数据 
     * page为页码
     * lang: cn中文 us英文
     */
	public function indexAction() {
		if(!isset($_REQUEST['type']) || !$type = $_REQUEST['type']){
			exit(json_encode(['status'=>0, 'msg'=>'not find type']));
		}
		if(!isset($_REQUEST['lang']) || !$lang = $_REQUEST['lang']){
			exit(json_encode(['status'=>0, 'msg'=>'not find lang']));
		}
		if(!isset($_REQUEST['page']) || !$page = $_REQUEST['page']){
			$page = 1;
		}
	  	if(!isset($_REQUEST['pageSize']) || !$pageSize = $_REQUEST['pageSize']){
			$pageSize = 100;
		}
		$start = ((int)$page - 1) * $pageSize;
		if($type == 1){
			$order = $lang=='us' ? 'market_cap_usd' : 'market_cap_cny';
			IvyDb::query("select * from `currency_data` order by `".$order."` desc limit $start,$pageSize ");
		}


	}


}

