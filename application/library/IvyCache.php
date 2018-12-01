<?php
/**
 * 
 * 封装Cache的操作
 *
 * Use PHP 5.3.0 or newer
 *
 * @package		Library
 * @author		Smart Lee <ismtlee@gmail.com>
 * @copyright	Copyright (c) 2008 - 2016, Linkerboom, Inc.
 * @since		Version 2.0
 * @filesource
 */
// ------------------------------------------------------------------------
/**
 * 
 * IvyCache
 *
 * 封装Cache的操作
 * 
 * @package Library
 * @author Smart Lee <ismtlee@gmail.com>
 * @version $Revision 2.0 2012-11-19 上午9:10:16
 * @see https://github.com/nicolasff/phpredis
 */
class IvyCache {
	// lifetime definition.
	const FOREVER = 0;
	const DAY = 86400;
	const HALF_DAY = 43200;
	const SHORT = 180;
	const NORMAL = 480;
	const LONG = 600;

    // result code definition.
    const RES_NOTFOUND = 13;
    const RES_SUCCESS = 0;

	private static $instance;
	private static $persist = false;
	private $cache;

	/**
	 * @see https://github.com/nicolasff/phpredis
	 * @return Redis
	 */
	public static function getInstance($persist = false) {
		if (self::$instance === null||self::$persist != $persist) {
			self::$instance = new IvyCache($persist);
		} 
		return self::$instance;
	}
	
	private function __construct($persist = false) {
		self::$persist = $persist;
		$this->cache = new Redis();
		$config = new Yaf_Config_Ini(CONFIG_INI, 'product');
		if($persist) {
			$this->cache->connect($config->cachedb->uri, $config->cachedb->port,$config->cachedb->timeout);
			// $this->cache->auth($config->cachedb->pass);
		} else {
			$this->cache->connect($config->cache->uri, $config->cache->port,$config->cache->timeout);
			// $this->cache->auth($config->cache->pass);
		}
		$this->cache->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_IGBINARY);
	}

	public function setOption($k, $v) {
		$this->cache->setOption($k, $v);
	}

	/**
	 * return cache.
	 * if u wanna revoke transactions op, 
	 * u can call directly by this instance.
	 */
	public function getCache() {
		return $this->cache;
	}

	public function flushAll() {
	return $this->cache->flushAll();
	}
	
	/**
	 * Set the string value in argument as value of the key.
	 * @param string $key
	 * @param string $value
	 * @param int $lifetime seconds.
	 * @return bool: true when success.
	 */
	public function set($key, $value, $lifetime=0) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
		if($lifetime == 0) {
			return $this->cache->set($key, $value);
		}
		return $this->cache->setex($key, $lifetime, $value);
	}
	
	/**
	 * Adds a value to the hash stored at key. If this value is already in the hash, FALSE is returned.
	 * 
	 * @param string $key
	 * @param string $subKey
	 * @param string $value
	 * @param int $lifetime
	 * @return long 1 if value didn't exist and was added successfully, 0 if the value was already present and was replaced, FALSE if there was an error.
	 */
	public function hSet($key, $subKey, $value, $lifetime = 0) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
		$rs = $this->cache->hSet($key, $subKey, $value);
		$lifetime > 0 && $this->cache->setTimeout($key, $lifetime);
		return $rs;
	}

	public function hVals($key) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
	 return $this->cache->hVals($key);
		
	}

	/**
	 * Fills in a whole hash. Non-string values are converted to string, using the standard (string) cast. NULL values are stored as empty strings.
	 * 
	 * @param string $key
	 * @param string $members
	 * @param int $lifetime
	 * @return long 1 if value didn't exist and was added successfully, 0 if the value was already present and was replaced, FALSE if there was an error.
	 */
	public function hMSet($key, array $members, $lifetime = 0) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
		$rs = $this->cache->hMSet($key, $members);
		$lifetime > 0 && $this->cache->setTimeout($key, $lifetime);
		return $rs;
	}
	
	/**
	 * Gets a value from the hash stored at key. If the hash table doesn't exist, or the key doesn't exist, FALSE is returned.
	 * @param string $key
	 * @param string $subKey
	 * @return string
	 */
	public function hGet($key, $subKey) {
		$data = $this->cache->hGet($key, $subKey);
		// $data_temp = json_decode($data,true);
		// if ($data_temp){
		// 	$data = $data_temp;
		// }
		return $data;
	}

	public function sRem($key, $subkey) {
		$data = $this->cache->sRem($key, $subkey);
	}

	/**
	 * Retrieve the values associated to the specified fields in the hash.
	 * @param string $key
	 * @param string $subKey
	 * @return string
	 */
	public function hMGet($key, array $memberKeys) {
		$data = $this->cache->hMGet($key, $memberKeys);
		// $data_temp = json_decode($data,true);
		// if ($data_temp){
		// 	$data = $data_temp;
		// }
		return $data;
	}
	
	/**
	 * Removes a value from the hash stored at key. If the hash table doesn't exist, or the key doesn't exist, FALSE is returned.
	 * @param string $key
	 * @param string $subKey
	 * @return bool
	 */
	public function hDel($key, $subKey) {
		return $this->cache->hDel($key, $subKey);
	}
	
	public function hDelAll($key) {
		return $this->cache->del($key);
	}

	/**
	 * Returns the whole hash, as an array of strings indexed by strings.
	 * @param string $key
	 * @return array
	 */
	public function hGetAll($key) {
		return $this->cache->hGetAll($key);
	}

	/**
	 * Returns the keys in a hash, as an array of strings.
	 * @param string $key
	 * @return array An array of elements, the keys of the hash. This works like PHP's array_keys().
	 */
	public function hKeys($key) {
		return $this->cache->hKeys($key);
	}

	/**
	 * Verify if the specified member exists in a key.
	 * @return BOOL: If the member exists in the hash table, return TRUE, otherwise return FALSE.
	 */
	public function hExists($key, $memberKey) {
		return $this->cache->hExists($key, $memberKey);
	}

	public function lGet($key,$index){
		return $this->cache->lGet($key,$index);
	}
	
	/**
	 * Adds the string value to the head (left) of the list. Creates the list if the key didn't exist. If the key exists and is not a list, FALSE is returned.
	 * @param string $key
	 * @param string $value
	 * @return long The new length of the list in case of success, FALSE in case of Failure.
	 */
	public function lPush($key, $value) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
		return $this->cache->lPush($key, $value);
	}


	public function lPushx($key, $value) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
		return $this->cache->lPushx($key, $value);
	}

	/**
	 * Insert value in the list before or after the pivot value.
	 * @param $key
	 * @param $pivot
	 * @param $value
	 * @param $before 1: before 0: after default 1
	 * @return The number of the elements in the list, -1 if the pivot didn't exists.
	 */
	public function lInsert($key, $pivot, $value, $before = 1) {
		if(!$before) {
			return $this->cache->lInsert($key, Redis::AFTER, $pivot, $value);
		}
		return $this->cache->lInsert($key, Redis::BEFORE, $pivot, $value);
	}

	/**
	 * Returns the size of a list identified by Key.If the list didn't exist or is empty, the command returns 0. If the data type identified by Key is not a list, the command return FALSE.
	 * @param string $key
	 * @param string $value
	 * @return long The new length of the list in case of success, FALSE in case of Failure.
	 */
	public function lSize($key) {
		return $this->cache->lSize($key);
	}

	
	/**
	 * Return and remove the first element of the list.
	 * @param string $key
	 * @return string STRING if command executed successfully BOOL FALSE in case of failure (empty list)
	 */
	public function lPop($key) {
		return $this->cache->lPop($key);
	}
	
	/**
	 * Adds the string value to the tail (right) of the list. Creates the list if the key didn't exist. If the key exists and is not a list, FALSE is returned.
	 * @param string $key
	 * @param string $value
	 * @return long The new length of the list in case of success, FALSE in case of Failure.
	 */
	public function rPush($key, $value) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
		return $this->cache->rPush($key, $value);
	}

		public function rPushx($key, $value) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
		return $this->cache->rPushx($key, $value);
	}
	
	/**
	 * Returns and removes the last element of the list.
	 * @param string $key
	 * @return string if command executed successfully BOOL FALSE in case of failure (empty list).
	 */
	public function rPop($key) {
		return $this->cache->rPop($key);
	}
	
	/**
	 * Returns the specified elements of the list stored at the specified key in the range [start, end]. start and stop are interpretated as indices: 0 the first element, 1 the second ... -1 the last element, -2 the penultimate ...
	 * @param string $start
	 * @param string $end 
	 * @return array  containing the values in specified range.
	 */
	public function lRange($key, $start, $end) {
		// lRange('key', 0, -1) get the all elements.
		return $this->cache->lRange($key, $start, $end);
	}

	public function lRem($key,$value,$len){
		//remove $len of record from $key list
		return $this->cache->lRem($key,$value,$len);
	}
	
	/**
	 * Adds a value to the set value stored at key. If this value is already in the set, FALSE is returned.
	 * @param string $key
	 * @param string $value
	 * @return long The new length of the list in case of success, FALSE in case of Failure.
	 */
	public function sAdd($key, $value) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
		return $this->cache->sAdd($key, $value);
	}

	/**
	 * Returns the cardinality of the set identified by key.
	 * @param string $key
	 * @return long The new length of the list in case of success, FALSE in case of Failure.
	 */
	public function sSize($key) {
		return $this->cache->sSize($key);
	}

	/**
	 * Returns the contents of a set.
	 * @param string $start
	 * @param string $end 
	 * @return array  containing the values in specified range.
	 */
	public function sMembers($key) {
		return $this->cache->sMembers($key);
	}

	/**
	 * Returns a random element from the set value at Key, without removing it.
	 * @param string $key
	 * @param int $count 
	 * @return array  containing the values in specified range.
	 */
	public function sRandMember($key, $count) {
		return $this->cache->sRandMember($key, $count);
	}


	/**
	 * Add one or more members to a sorted set or update its score if it already exists
	 * @param string $key
	 * @param double $score
	 * @param string $value
	 * @return Long 1 if the element is added. 0 otherwise.
	 */
	public function zAdd($key, $score, $value) {
		// if (is_array($value)){
		// 	$value = json_encode($value);
		// }
		return $this->cache->zAdd($key, $score, $value);
	}


	/**
	 * Returns the cardinality of an ordered set.
	 * @param string $key
	 * @return Long, the set's cardinality.
	 *
	 */
	public function zSize($key) {
		return $this->cache->zSize($key);
	}

	/**
	 * Returns the number of elements of the sorted set stored at the specified key which have scores in the range [start,end]. Adding a parenthesis before start or end excludes it from the range. +inf and -inf are also valid limits.
	 * @param string $key
	 * @param int $start
	 * @param int @end
	 * @return Long, the set's cardinality.
	 *
	 */
	public function zCount($key, $start, $end) {
		return $this->cache->zCount($key, $start, $end);
	}

	/**
	 * Returns the specified elements of the list stored at the specified key in the range [start, end]. start and stop are interpretated as indices: 0 the first element, 1 the second ... -1 the last element, -2 the penultimate ...
	 * @param long $start
	 * @param long $end
	 * @param bool withscores  
	 * @return array  Array containing the values in specified range.
	 */
	public function zRange($key, $start, $end, $withscores = false) {
		// lRange('key', 0, -1) get the all elements.
		return $this->cache->zRange($key, $start, $end, $withscores);
	}

	/**
	 * Returns the elements of the sorted set stored at the specified key in the range [start, end] in reverse order. 
	 */
	public function zRevRange($key, $start, $end, $withscores = false) {
		// lRange('key', 0, -1) get the all elements.
		return $this->cache->zRevRange($key, $start, $end, $withscores);
	}

	/**
	 * Returns the elements of the sorted set stored at the specified key which have scores in the range [start,end]. Adding a parenthesis before start or end excludes it from the range. +inf and -inf are also valid limits. zRevRangeByScore returns the same items in reverse order, when the start and end parameters are swapped.
	 * @param long $start
	 * @param long $end
	 * @param array options Two options are available: withscores => TRUE, and limit => array($offset, $count)
	 * Note: if members are serialized, using withscores would report an notice:Array to string conversion .
	 * @return array  Array containing the values in specified range.
	 */
	public function zRangeByScore($key, $start, $end, $options = null) {
		// lRange('key', 0, -1) get the all elements.
		if(!$options) {
			return $this->cache->zRangeByScore($key, $start, $end);
		}
		return $this->cache->zRangeByScore($key, $start, $end, $options);
	}

	/**
	 * Returns the same items in reverse order, when the start and end parameters are swapped.
	 * @param long $start
	 * @param long $end
	 * @param array options Two options are available: withscores => TRUE, and limit => array($offset, $count)
	 * @return array  Array containing the values in specified range.
	 */
	public function zRevRangeByScore($key, $start, $end, $options = null) {
		// lRange('key', 0, -1) get the all elements.
		if(!$options) {
			return $this->cache->zRevRangeByScore($key, $start, $end);
		}
		return $this->cache->zRevRangeByScore($key, $start, $end, $options);
	}

	/**
	 * Increments the score of a member from a sorted set by a given amount.
	 * @param long $amount
	 * @param string $value
	 * @return double the new value
	 */
	public function zIncrBy($key, $amount, $value) {
		return $this->cache->zIncrBy($key, $amount, $value);
	}

	/**
	 * Returns the rank of a given member in the specified sorted set, starting at 0 for the item with the smallest score. zRevRank starts at 0 for the item with the largest score.
	 *
	 *
	 */
	public function zRank($key, $member) {
		return $this->cache->zRank($key, $member);
	}

	public function zRevRank($key, $member) {
		return $this->cache->zRevRank($key, $member);
	}

	/**
	 * Deletes a specified member from the ordered set.
	 * @param string $key
	 * @param string $member
	 * @return LONG 1 on success, 0 on failure.
	 */
	public function zRem($key, $member) {
		return $this->cache->zRem($key, $member);
	}

	/**
	 * Deletes the elements of the sorted set stored at the specified key which have rank in the range [start,end].
	 *
	 * @return LONG The number of values deleted from the sorted set. 
	 */
	public function zRemRangeByRank($key, $start, $end) {
		return $this->cache->zRemRangeByRank($key, $start, $end);
	}

	/**
	 * Deletes the elements of the sorted set stored at the specified key which have scores in the range [start,end].
	 *
	 * @return LONG The number of values deleted from the sorted set.
	 */
	public function zRemRangeByScore($key, $start, $end) {
		return $this->cache->zRemRangeByScore($key, $start, $end);
	}

	/**
	 * Returns the score of a given member in the specified sorted set.
	 * @param string $key
	 * @param string $member
	 * @return Double score
	 */
	public function zScore($key, $member) {
		return $this->cache->zScore($key, $member);
	}


	/**
	 * Get the value related to the specified key.
	 * @param string $key
	 * @return string|bool: If key didn't exist, FALSE is returned. 
	 * 		Otherwise, the value related to this key is returned.
	 */
	public function get($key) {
		$data = $this->cache->get($key);
		// $data_temp = json_decode($data,true);
		// if ($data_temp){
		// 	$data = $data_temp;
		// }
		if ($data == "[]"){
			return null;
		}
		return $data;
	}
	
	/**
	 * Remove specified key.
	 * @param string $key
	 * @return int: 1 success.
	 */
	public function delete($key) {
		return $this->cache->delete($key);
	}
	
	/**
	 * Returns the keys that match a certain pattern.
	 * @param $pattern STRING: pattern, using '*' as a wildcard.
	 *
	 * @return Array of STRING: The keys that match a certain pattern.
	 */
	public function keys($pattern) {
		return $this->cache->keys($pattern);
	}

	/**
	 * Verify if the specified key exists.
	 * @param string $key
	 * @return bool: If the key exists, return TRUE, otherwise return FALSE.
	 */
	public function exists($key) {
		return $this->cache->exists($key);
	}
	
	/**
	 * Increment the number stored at key by one. If the second argument is filled, it will be used as the integer value of the increment.
	 * @param string $key
	 * @param string $value value that will be added to key, default is one.
	 * @return int: The new value.
	 */
	public function incr($key, $value = 1) {
		return $this->cache->incr($key);
	}
	
	/**
	* Decrement the number stored at key by one. If the second argument is filled, it will be used as the integer value of the decrement.
	* @param string $key
	* @param string $value value that will be substracted to key, default is one.
	* @return int: The new value.
	*/
	public function decr($key, $value = 1) {
		return $this->cache->decr($key);
	}
	
	/**
	* Remove specified keys.
	* @param array $keys
	* @return long: Number of keys deleted.
	*/
	public function delMulti(array $keys) {
		return $this->cache->delete($keys);
	}
	
	/**
	 * Get the values of all the specified keys. If one or more keys dont exist, the array will contain FALSE at the position of the key.
	 * @param array $keys
	 * @return array:Array containing the values related to keys in argument.
	 */
	public function getMulti(array $keys) {
		return $this->cache->mget($keys);
	}

	/**
	 * Increment the number stored at key by one. If the second argument is filled, it will be used as the integer value of the increment.
	 * @return int the new value. 
	 */
	public function incrBy($key, $increment = 1) {
		return $this->cache->incrBy($key, $increment);
	}
	
	public function info(){
		return $this->cache->info();
	}
	
	/**
	 * Sets an expiration date (a timeout) on an item.
	 * @param string $key
	 * @param int $expire_time 
	 * @return bool: TRUE in case of success, FALSE in case of failure.
	 */
	public function setExpireTime($key, $expire_time) {
		return $this->cache->setTimeout($key, $expire_time);
	}

    public function setTimeout($key, $expire_time) {
        return $this->cache->setTimeout($key, $expire_time);
    }

    public function expireAt($key, $expire_time) {
        return $this->cache->expireAt($key, $expire_time);
    }
	
	public function getLastTime($key){
		return $this->cache->ttl($key);
	}
}
