<?php
class IndexController extends Yaf_Controller_Abstract {

	/**
     * 获取首页数据(货币列表数据)
     * type：1为行情数据 2为交易所数据 
     * page为页码
     * lang: cn中文 us英文
     */
	public function indexAction() {
		header("Content-type:text/html;charset=utf8");
		if(!isset($_REQUEST['type']) || !$type = $_REQUEST['type']){
			$type = 1;
		}
		if(!isset($_REQUEST['lang']) || !$lang = $_REQUEST['lang']){
			$lang = 'us';
		}
		if(!isset($_REQUEST['page']) || !$page = $_REQUEST['page']){
			$page = 1;
		}
	  	if(!isset($_REQUEST['pageSize']) || !$pageSize = $_REQUEST['pageSize']){
			$pageSize = 100;
		}
		$start = ((int)$page - 1) * $pageSize;
		$date = date("Y-m-d");
		if($type == 1){
			$total = IvyDb::query("select count(*) as num from `rank` ");
<<<<<<< HEAD
			$rs = IvyDb::query("select pic,name,code,marketCap,volumeGlobal,circulatingSupply,kline,dayChange from `rank` order by `marketCap` desc limit $start,$pageSize ");
=======
			$rs = IvyDb::query("select pic,name,code,price,dayChange,marketCap,volumeGlobal,circulatingSupply,kline from `rank` order by `marketCap` desc limit $start,$pageSize ");
>>>>>>> c46ccf809b1c21ee713fdeb79b6127ae8d2abfdb
		} else {
			$rs = [];
		}
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs, 'total'=>$total[0]['num']]));
	}

	/**
     * 获取货币详细信息
     */
	public function currencyInfAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(['status'=>0, 'msg'=>'not find code']));
		}
		$rs = IvyDb::query("select * from `rank` where `code`='$code'");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs]));
	}


	/**
     * 获取饼状图数据
     */
	public function get_pie_chart_dataAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(['status'=>0, 'msg'=>'not find code']));
		}
		$rs = IvyDb::query("select * from `pie_chart` where `code`='$code'");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs]));
	}


	/**
     * 获取折线图数据 http://116.62.118.136/Index/get_line_data?name=BTC&type=DAY&start=1515737886&end=1518416286
     */
	public function get_line_dataAction() {
		if(!isset($_REQUEST['name']) || !$name = $_REQUEST['name']){
			exit(json_encode(['status'=>0, 'msg'=>'not find name']));
		}
		if(!isset($_REQUEST['type']) || !$type = $_REQUEST['type']){
			exit(json_encode(['status'=>0, 'msg'=>'not find type']));
		}
		if(!isset($_REQUEST['start']) || !$start = $_REQUEST['start']){
			$start = time() - 3600*12;
		}
		if(!isset($_REQUEST['end']) || !$end = $_REQUEST['end']){
			$end = time();
		}
		$rs = IvyDb::query("select * from `line_data` where `type`='$type' and `from`='$name' and `epochSecond`>='$start' and `epochSecond`<='$end' order by epochSecond asc");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs]));
	}

	/**
     * 搜索货币
     */
	public function searchAction() {
		if(!isset($_REQUEST['search']) || !$search = $_REQUEST['search']){
			exit(json_encode(['status'=>0, 'msg'=>'not find search']));
		}
		$rs = IvyDb::query("select pic,name,code,marketCap,volumeGlobal,circulatingSupply,kline from `rank` where name like '%".$search."%' or code like '%".$search."%' order by `marketCap` desc");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs]));
	}










	/**
     * 获取成交额排行榜数据
     */
	public function get_volume_dataAction() {
		if(!isset($_REQUEST['type']) || !$type = $_REQUEST['type']){
			exit(json_encode(['status'=>0, 'msg'=>'not find type']));
		}
		$date = date("Y-m-d");
		$date1 = date("Y-m-d", strtotime("-1 day"));
		$rs = IvyDb::query("select * from `volume` where `rank`>0 and rp_date='$date' and data_type='$type' order by `rank` asc limit 8");
		if(!$rs || !count($rs)){
			$rs = IvyDb::query("select * from `volume` where `rank`>0 and rp_date='$date1' and data_type='$type' order by `rank` asc limit 8");
		}
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs]));
	}









}

