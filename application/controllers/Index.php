<?php
class IndexController extends Yaf_Controller_Abstract {

	/**
     * 获取主数据 
     * type：1为行情数据 2为交易所数据 
     * page为页码
     * lang: cn中文 us英文
     */
	public function indexAction() {
		header("Content-type:text/html;charset=utf8");
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
		$date = date("Y-m-d");
		$date1 = date("Y-m-d", strtotime("-1 day"));
		if($type == 1){
			$rs = IvyDb::query("select * from `currency_data` where `number`>0 and rp_date='$date' order by `number` asc limit $start,$pageSize ");
			if(!$rs || !count($rs)){
				$rs = IvyDb::query("select * from `currency_data` where `number`>0 and rp_date='$date1' order by `number` asc limit $start,$pageSize ");
			}
		} else {}
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}

		var_dump($this->gbk_to_utf8($rs));die;

		var_dump(json_encode(['status'=>1, 'data'=>$rs], JSON_UNESCAPED_UNICODE));

		//exit(json_encode(['status'=>1, 'data'=>$rs], JSON_UNESCAPED_UNICODE));
	}


	function gbk_to_utf8($data) {
        if( is_array($data) ) {
            foreach ($data as $k => $v) {
                if ( is_array($v) ) {
                    $data[$k] = $this->gbk_to_utf8($v);
                } else {
                    $data[$k] = iconv('gbk', 'utf-8', $v);
                }
            }
            return $data;
        } else {
            $data = iconv('gbk', 'utf-8', $data);
            return $data;
        }
	}





}

