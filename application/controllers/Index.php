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
		
		$total = IvyDb::query("select count(*) as num from `rank` ");
		$sum = IvyDb::query("select sum(marketCap) as sum_mark from `rank` ");
		$rs = IvyDb::query("select pic,name,code,price,marketCap,volumeGlobal,circulatingSupply,kline,dayChange from `rank` order by `marketCap` desc limit $start,$pageSize ");
		$rs2 = array();
		$i = ($page-1)*$pageSize;
		foreach ($rs as $key => $value) {
			$value['num'] = $i+1;
		        $kline = $value['kline'];
 	                $value['max'] = max(explode(",",$kline));
	       		$value['min'] = min(explode(",",$kline));
			$rs2[] = $value;
			$i++;
		}
		$rs  = $rs2;
		
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}

		$rs_all = IvyDb::query("select avg(`price`) as price,avg(`dayChange`) as dayChange from rank");
		$rs_top100 = IvyDb::query("select avg(`price`) as price,avg(`dayChange`) as dayChange from rank order by marketCap desc limit 0,100");
		$rs_hb10 = IvyDb::query("select close,open from market_detail where coin='HB10'");
		$rs_all = $rs_all[0];
		$rs_top100 = $rs_top100[0];
		$rs_hb10 = $rs_hb10[0];
		$rs_hb10_dayChange = strval($rs_hb10['close']/$rs_hb10['open']);
		$time = time()-24*3600;
		
		$all_kline = $this->handleRs(IvyDb::query("select `close` from `line_data` where `epochSecond` > '$time' and `type`='HOUR' and from ='ALL' order by epochSecond desc"));
		$top100_kline = $this->handleRs(IvyDb::query("select `close` from `line_data` where `epochSecond` > '$time' and `type`='HOUR' and from ='TOP100' order by epochSecond desc"));
		$hb10_kline = $this->handleRs(IvyDb::query("select `close` from `line_data` where `epochSecond` > '$time' and `type`='HOUR' and from ='HB10' order by epochSecond desc"));
		$all = array('code' => 'ALL',"price" => $rs_all['price'],'dayChange' => $rs_all['dayChange'],'kline' =>implode(",", $all_kline),'max'=> empty($all_kline)?"": max($all_kline) ,'min' => empty($all_kline)?"": min($all_kline));
		$top100 = array('code' => 'TOP100',"price" => $rs_top100['price'],'dayChange' => $rs_top100['dayChange'],'kline' => implode(",",$top100_kline),'max'=>  empty($top100_kline)?"":max($top100_kline),'min' => empty($top100_kline)?"": min($top100_kline));
		$hb10 = array('code' => 'HB10',"price" => $rs_hb10['close'],'dayChange' => $rs_hb10_dayChange,'kline' => implode(",",$hb10_kline),'max'=>  empty($hb10_kline)?"":max($hb10_kline),'min' => empty($hb10_kline)?"": min($hb10_kline));


		exit(json_encode(['status'=>1, 'data'=>$rs, 'total'=>$total[0]['num'], 'sum' => $sum[0]['sum_mark'],'top' => array($all,$top100,$hb10)]));
	}


	private function handleRs($rs) {
		if (empty($rs)) {
			return array();
		}
		$rec = array();
		foreach ($rs as $key => $r) {
			$rec[] = $r['close'];
		}
		return implode(",", $rec);
	}

	/**
     * 获取货币详细信息
     */
	public function currencyInfAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(['status'=>0, 'msg'=>'not find code']));
		}
		$rs = IvyDb::query("select pic,name,code,price,marketCap,volumeGlobal,circulatingSupply,dayChange from `rank` where `code`='$code'");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		$result = [];
		$res = IvyDb::query("select * from `currency_inf` where `code`='$code'");
		if(!$res || !count($res)){
			$result = $rs[0];
		} else {
			$result = array_merge($rs[0], $res[0]);
		}
		exit(json_encode(['status'=>1, 'data'=>$result]));
	}


		/**
     * 获取货币交易信息
     */
	public function market_tickerAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(['status'=>0, 'msg'=>'not find code']));
		}
		if(!isset($_REQUEST['page']) || !$page = $_REQUEST['page']){
			$page=1;
		}
		if(!isset($_REQUEST['pagesize']) || !$pagesize = $_REQUEST['pagesize']){
			$pagesize=100;
		}
		$start = ((int)$page - 1) * $pagesize;
		$total = IvyDb::query("select count(*) as num from `coin_market_ticker` where `coin_code`='$code' ");
		$rs = IvyDb::query("select * from `coin_market_ticker` where `coin_code`='$code' order by `volume` desc limit $start,$pagesize ");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		
		exit(json_encode(['status'=>1, 'data'=>$rs, 'total' => $total]));
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
     * 获取资金流向数据
     */
	public function coin_profile_fundAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(['status'=>0, 'msg'=>'not find code']));
		}
		$rs = IvyDb::query("select * from `coin_fund` where `code`='$code'");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}

		$data = json_decode($rs[0]['fund'],true);
		exit(json_encode(['status'=>1, 'data'=>$data]));
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
     * 交易所列表页
     */
	public function exchangeAction() {
		if(!isset($_REQUEST['page']) || !$page = $_REQUEST['page']){
			$page=1;
		}
		if(!isset($_REQUEST['pagesize']) || !$pagesize = $_REQUEST['pagesize']){
			$pagesize=100;
		}
		$start = ((int)$page - 1) * $pagesize;
		$total = IvyDb::query("select count(*) as num from `exchange` ");
		$sum = IvyDb::query("select sum(volumn) as sum_volumn from `exchange` ");
		$rs = IvyDb::query("select * from exchange order by `volumn` desc limit $start,$pagesize ");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs,'total'=>$total[0]['num'], 'sum' => $sum[0]['sum_volumn']]));
	}


	/**
     * 交易所成交额
     */
	public function exchangetradesAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(array('status' => 0, 'msg' => 'no code')));
		}
		$rs = IvyDb::query("select info from exchangetrades where code='$code'");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>json_decode($rs[0]['info'],true)]));
	}


		/**
     * 交易所信息
     */
	public function exchangeinfoAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(array('status' => 0, 'msg' => 'no code')));
		}
		$rs = IvyDb::query("select * from exchangeinfo where platform='$code'");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=> $rs]));
	}

		/**
     * 交易所交易对
     */
	public function exchangecoinpairsAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(array('status' => 0, 'msg' => 'no code')));
		}
		if(!isset($_REQUEST['page']) || !$page = $_REQUEST['page']){
			$page=1;
		}
		if(!isset($_REQUEST['pagesize']) || !$pagesize = $_REQUEST['pagesize']){
			$pagesize=100;
		}
		if(!isset($_REQUEST['type']) || !$type = $_REQUEST['type']){
			$type='';
		}
		$start = ((int)$page - 1) * $pagesize;
		if (!$type) {
			$total = IvyDb::query("select count(*) as num from `coin_pairs` where code='$code'");
			$rs = IvyDb::query("select * from coin_pairs where code='$code' order by `volume` desc limit $start,$pagesize");
		}else {
			$total = IvyDb::query("select count(*) as num from `coin_pairs` where code='$code' and pair2='$type'");
			$rs = IvyDb::query("select * from coin_pairs where code='$code' and pair2='$type' order by `volume` desc limit $start,$pagesize");
		}

	
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>$rs,'total'=>$total[0]['num']]));
	}

	public function exchangecoinscoreAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(array('status' => 0, 'msg' => 'no code')));
		}

		$rs = IvyDb::query("select info from exchangescore where code='$code'");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>json_decode($rs[0]['info'],true)]));


	｝


	public function exchangecoinbasepairdataAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(array('status' => 0, 'msg' => 'no code')));
		}

		$rs = IvyDb::query("select info from exchangebasepairdata where code='$code'");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>json_decode($rs[0]['info'],true)]));

	｝


	public function exchangecoinpairdataAction() {
		if(!isset($_REQUEST['code']) || !$code = $_REQUEST['code']){
			exit(json_encode(array('status' => 0, 'msg' => 'no code')));
		}

		$rs = IvyDb::query("select info from exchangepairdata where code='$code'");
		if(!$rs || !count($rs)){
			exit(json_encode(['status'=>0, 'msg'=>'no data']));
		}
		exit(json_encode(['status'=>1, 'data'=>json_decode($rs[0]['info'],true)]));
	｝






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

