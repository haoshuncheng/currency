<?php
/**
 *
 *
 */
class IvyCrypt {

	static function byteStr2byteArray($s) {
		return array_slice(unpack("C*", "\0".$s), 1);
	}

	static function encrypt($str) {
		$bytes = self::byteStr2byteArray ( $str );
		$len = count ( $bytes );
		do {
			$seed = rand ( 5, 63 );
		} while ( $seed == 0 );
		$arr = array();
		$arr[] = $seed;
		for($i = 0; $i < $len; $i ++) {
			$tmp = $bytes[$i];
			$arr[] = $tmp + $seed < 256 ? $tmp + $seed : $tmp;
		}

		$result = "";
		foreach ($arr as $chr) {
			$result .= chr($chr);
		}
		return base64_encode($result);
	}

	static function decrypt($str) {
		$bytes = self::byteStr2byteArray ( base64_decode($str) );
		$len = count ( $bytes );
		$seed = $bytes[0];
		$arr = array();
		for($i = 1; $i < $len; $i ++) {
			$tmp = $bytes[$i];
			$t = $tmp + $seed;
			$arr[] = $t > 255 && $tmp >= 128 ? $tmp : $tmp - $seed;
		}
		$result = "";
		foreach ($arr as $chr) {
			$result .= chr($chr);
		}
		return $result;
	}

}
