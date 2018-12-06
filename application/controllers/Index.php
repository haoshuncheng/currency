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
			$total = IvyDb::query("select count(*) as num from `currency_data` where `number`>0 and rp_date='$date' ");
			if(!$total || !count($total) || $total[0]['num'] <= 0){
				$total = IvyDb::query("select count(*) as num from `currency_data` where `number`>0 and rp_date='$date1' ");
				$rs = IvyDb::query("select * from `currency_data` where `number`>0 and rp_date='$date1' order by `number` asc limit $start,$pageSize ");
			} else {
				$rs = IvyDb::query("select * from `currency_data` where `number`>0 and rp_date='$date' order by `number` asc limit $start,$pageSize ");
			}
		} else {
			$total = IvyDb::query("select count(*) as num from `exchange` where `rank`>0 and rp_date='$date' ");
			if(!$total || !count($total) || $total[0]['num'] <= 0){
				$total = IvyDb::query("select count(*) as num from `exchange` where `rank`>0 and rp_date='$date1' ");
				$rs = IvyDb::query("select * from `exchange` where `rank`>0 and rp_date='$date1' order by `rank` asc limit $start,$pageSize ");
			} else {
				$rs = IvyDb::query("select * from `exchange` where `rank`>0 and rp_date='$date' order by `rank` asc limit $start,$pageSize ");
			}
		}
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs, 'total'=>$total[0]['num']]));
	}

	/**
     * 展示图标数据
     */
	public function linedataAction() {
		$date = date("Y-m-d");
		$date1 = date("Y-m-d", strtotime("-1 day"));
		$rs = IvyDb::query("select * from `currency_data` where `number`>0 and rp_date='$date' order by `number` asc limit 5");
		if(!$rs || !count($rs)){
			$rs = IvyDb::query("select * from `currency_data` where `number`>0 and rp_date='$date1' order by `number` asc limit 5");
		}
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs]));
	}


	/**
     * 获取涨跌榜数据
     */
	public function get_up_down_dataAction() {
		if(!isset($_REQUEST['data_type']) || !$data_type = $_REQUEST['data_type']){
			exit(json_encode(['status'=>0, 'msg'=>'not find data_type']));
		}
		if(!isset($_REQUEST['searchtype']) || !$searchtype = $_REQUEST['searchtype']){
			exit(json_encode(['status'=>0, 'msg'=>'not find searchtype']));
		}
		if(!isset($_REQUEST['timetype']) || !$timetype = $_REQUEST['timetype']){
			exit(json_encode(['status'=>0, 'msg'=>'not find timetype']));
		}
		$date = date("Y-m-d");
		$date1 = date("Y-m-d", strtotime("-1 day"));
		$rs = IvyDb::query("select * from `upanddowns` where `rank`>0 and rp_date='$date' and data_type='$data_type' and search_type=$searchtype and time_type=$timetype order by `rank` asc limit 8");
		if(!$rs || !count($rs)){
			$rs = IvyDb::query("select * from `upanddowns` where `rank`>0 and rp_date='$date1' and data_type='$data_type' and search_type=$searchtype and time_type=$timetype order by `rank` asc limit 8");
		}
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs]));
	}

	/**
     * 搜索
     */
	public function searchAction() {
		if(!isset($_REQUEST['search']) || !$search = $_REQUEST['search']){
			exit(json_encode(['status'=>0, 'msg'=>'not find search']));
		}
		$date = date("Y-m-d");
		$date1 = date("Y-m-d", strtotime("-1 day"));
		$rs = IvyDb::query("select * from `currency_data` where `number`>0 and rp_date='$date' and name like '%".$search."%' order by `number` asc");
		if(!$rs || !count($rs)){
			$rs = IvyDb::query("select * from `currency_data` where `number`>0 and rp_date='$date1' and name like '%".$search."%' order by `number` asc");
		}
		$res = IvyDb::query("select * from `exchange` where `rank`>0 and rp_date='$date' and name like '%".$search."%' order by `rank` asc");
		if(!$res || !count($res)){
			$res = IvyDb::query("select * from `exchange` where `rank`>0 and rp_date='$date1' and name like '%".$search."%' order by `rank` asc");
		}
		if((!$rs || !count($rs)) && (!$res || !count($res))){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs, 'data1'=>$res]));
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

