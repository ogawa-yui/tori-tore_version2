$(function(){
	//26 version
	
	$('.btn-play').on('click', function(){
		var btnClickID = $(this).attr('id');
		if($('.fa-pause').length > 0){
			var playingID = $('.fa-pause').parent().attr('id');
			if(!(btnClickID == playingID)){
				$('#' + playingID).html('<i class="fas fa-play"></i>');
				howl[playingID].pause();
			}
		}
	});
	
	const howl = []; 
	var arrHowl = [];
	
	howl['suzume_call_01'] = new Howl({
		src: ['mp3/suzume_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['suzume_call_01'].seek(0);
			$('#suzume_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('suzume_call_01');
	$('#suzume_call_01').on('click',function(){
		if(howl['suzume_call_01'].playing() ){
			$('#suzume_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['suzume_call_01'].pause();
		}else{
			$('#suzume_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['suzume_call_01'].play();
		}
	});
	howl['suzume_call_01_sona'] = new Howl({
		src: ['mp3/suzume_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['suzume_call_01_sona'].seek(0);
			$('#suzume_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#suzume_call_01_sona').on('click',function(){
		if(howl['suzume_call_01_sona'].playing() ){
			$('#suzume_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['suzume_call_01_sona'].pause();
		}else{
			$('#suzume_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['suzume_call_01_sona'].play();
		}
	});

	howl['kawarahiwa_song_01'] = new Howl({
		src: ['mp3/kawarahiwa_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kawarahiwa_song_01'].seek(0);
			$('#kawarahiwa_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('kawarahiwa_song_01');
	$('#kawarahiwa_song_01').on('click',function(){
		if(howl['kawarahiwa_song_01'].playing() ){
			$('#kawarahiwa_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kawarahiwa_song_01'].pause();
		}else{
			$('#kawarahiwa_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kawarahiwa_song_01'].play();
		}
	});
	howl['kawarahiwa_song_01_sona'] = new Howl({
		src: ['mp3/kawarahiwa_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kawarahiwa_song_01_sona'].seek(0);
			$('#kawarahiwa_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#kawarahiwa_song_01_sona').on('click',function(){
		if(howl['kawarahiwa_song_01_sona'].playing() ){
			$('#kawarahiwa_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kawarahiwa_song_01_sona'].pause();
		}else{
			$('#kawarahiwa_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kawarahiwa_song_01_sona'].play();
		}
	});
	
	howl['yamagara_song_01'] = new Howl({
		src: ['mp3/yamagara_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['yamagara_song_01'].seek(0);
			$('#yamagara_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('yamagara_song_01');
	$('#yamagara_song_01').on('click',function(){
		if(howl['yamagara_song_01'].playing() ){
			$('#yamagara_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['yamagara_song_01'].pause();
		}else{
			$('#yamagara_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['yamagara_song_01'].play();
		}
	});
	howl['yamagara_song_01_sona'] = new Howl({
		src: ['mp3/yamagara_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['yamagara_song_01_sona'].seek(0);
			$('#yamagara_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#yamagara_song_01_sona').on('click',function(){
		if(howl['yamagara_song_01_sona'].playing() ){
			$('#yamagara_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['yamagara_song_01_sona'].pause();
		}else{
			$('#yamagara_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['yamagara_song_01_sona'].play();
		}
	});
	
	howl['kiji_call_01'] = new Howl({
		src: ['mp3/kiji_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kiji_call_01'].seek(0);
			$('#kiji_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('kiji_call_01');
	$('#kiji_call_01').on('click',function(){
		if(howl['kiji_call_01'].playing() ){
			$('#kiji_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kiji_call_01'].pause();
		}else{
			$('#kiji_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kiji_call_01'].play();
		}
	});
	howl['kiji_call_01_sona'] = new Howl({
		src: ['mp3/kiji_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kiji_call_01_sona'].seek(0);
			$('#kiji_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#kiji_call_01_sona').on('click',function(){
		if(howl['kiji_call_01_sona'].playing() ){
			$('#kiji_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kiji_call_01_sona'].pause();
		}else{
			$('#kiji_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kiji_call_01_sona'].play();
		}
	});
	
	howl['ooyoshikiri_song_01'] = new Howl({
		src: ['mp3/ooyoshikiri_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['ooyoshikiri_song_01'].seek(0);
			$('#ooyoshikiri_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('ooyoshikiri_song_01');
	$('#ooyoshikiri_song_01').on('click',function(){
		if(howl['ooyoshikiri_song_01'].playing() ){
			$('#ooyoshikiri_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['ooyoshikiri_song_01'].pause();
		}else{
			$('#ooyoshikiri_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['ooyoshikiri_song_01'].play();
		}
	});
	howl['ooyoshikiri_song_01_sona'] = new Howl({
		src: ['mp3/ooyoshikiri_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['ooyoshikiri_song_01_sona'].seek(0);
			$('#ooyoshikiri_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#ooyoshikiri_song_01_sona').on('click',function(){
		if(howl['ooyoshikiri_song_01_sona'].playing() ){
			$('#ooyoshikiri_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['ooyoshikiri_song_01_sona'].pause();
		}else{
			$('#ooyoshikiri_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['ooyoshikiri_song_01_sona'].play();
		}
	});
	
	howl['shijukara_song_01'] = new Howl({
		src: ['mp3/shijukara_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['shijukara_song_01'].seek(0);
			$('#shijukara_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('shijukara_song_01');
	$('#shijukara_song_01').on('click',function(){
		if(howl['shijukara_song_01'].playing() ){
			$('#shijukara_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['shijukara_song_01'].pause();
		}else{
			$('#shijukara_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['shijukara_song_01'].play();
		}
	});
	howl['shijukara_song_01_sona'] = new Howl({
		src: ['mp3/shijukara_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['shijukara_song_01_sona'].seek(0);
			$('#shijukara_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#shijukara_song_01_sona').on('click',function(){
		if(howl['shijukara_song_01_sona'].playing() ){
			$('#shijukara_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['shijukara_song_01_sona'].pause();
		}else{
			$('#shijukara_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['shijukara_song_01_sona'].play();
		}
	});
	
	howl['gabicho_song_01'] = new Howl({
		src: ['mp3/gabicho_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['gabicho_song_01'].seek(0);
			$('#gabicho_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('gabicho_song_01');
	$('#gabicho_song_01').on('click',function(){
		if(howl['gabicho_song_01'].playing() ){
			$('#gabicho_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['gabicho_song_01'].pause();
		}else{
			$('#gabicho_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['gabicho_song_01'].play();
		}
	});
	howl['gabicho_song_01_sona'] = new Howl({
		src: ['mp3/gabicho_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['gabicho_song_01_sona'].seek(0);
			$('#gabicho_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#gabicho_song_01_sona').on('click',function(){
		if(howl['gabicho_song_01_sona'].playing() ){
			$('#gabicho_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['gabicho_song_01_sona'].pause();
		}else{
			$('#gabicho_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['gabicho_song_01_sona'].play();
		}
	});
	
	howl['hakusekirei_song_01'] = new Howl({
		src: ['mp3/hakusekirei_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hakusekirei_song_01'].seek(0);
			$('#hakusekirei_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('hakusekirei_song_01');
	$('#hakusekirei_song_01').on('click',function(){
		if(howl['hakusekirei_song_01'].playing() ){
			$('#hakusekirei_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hakusekirei_song_01'].pause();
		}else{
			$('#hakusekirei_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hakusekirei_song_01'].play();
		}
	});
	howl['hakusekirei_song_01_sona'] = new Howl({
		src: ['mp3/hakusekirei_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hakusekirei_song_01_sona'].seek(0);
			$('#hakusekirei_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#hakusekirei_song_01_sona').on('click',function(){
		if(howl['hakusekirei_song_01_sona'].playing() ){
			$('#hakusekirei_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hakusekirei_song_01_sona'].pause();
		}else{
			$('#hakusekirei_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hakusekirei_song_01_sona'].play();
		}
	});
	
	howl['kogera_call_01'] = new Howl({
		src: ['mp3/kogera_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kogera_call_01'].seek(0);
			$('#kogera_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('kogera_call_01');
	$('#kogera_call_01').on('click',function(){
		if(howl['kogera_call_01'].playing() ){
			$('#kogera_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kogera_call_01'].pause();
		}else{
			$('#kogera_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kogera_call_01'].play();
		}
	});
	howl['kogera_call_01_sona'] = new Howl({
		src: ['mp3/kogera_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kogera_call_01_sona'].seek(0);
			$('#kogera_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#kogera_call_01_sona').on('click',function(){
		if(howl['kogera_call_01_sona'].playing() ){
			$('#kogera_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kogera_call_01_sona'].pause();
		}else{
			$('#kogera_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kogera_call_01_sona'].play();
		}
	});
	
	howl['uguisu_song_01'] = new Howl({
		src: ['mp3/uguisu_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['uguisu_song_01'].seek(0);
			$('#uguisu_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('uguisu_song_01');
	$('#uguisu_song_01').on('click',function(){
		if(howl['uguisu_song_01'].playing() ){
			$('#uguisu_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['uguisu_song_01'].pause();
		}else{
			$('#uguisu_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['uguisu_song_01'].play();
		}
	});
	howl['uguisu_song_01_sona'] = new Howl({
		src: ['mp3/uguisu_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['uguisu_song_01_sona'].seek(0);
			$('#uguisu_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#uguisu_song_01_sona').on('click',function(){
		if(howl['uguisu_song_01_sona'].playing() ){
			$('#uguisu_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['uguisu_song_01_sona'].pause();
		}else{
			$('#uguisu_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['uguisu_song_01_sona'].play();
		}
	});
	
	howl['aogera_call_01'] = new Howl({
		src: ['mp3/aogera_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['aogera_call_01'].seek(0);
			$('#aogera_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('aogera_call_01');
	$('#aogera_call_01').on('click',function(){
		if(howl['aogera_call_01'].playing() ){
			$('#aogera_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['aogera_call_01'].pause();
		}else{
			$('#aogera_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['aogera_call_01'].play();
		}
	});
	howl['aogera_call_01_sona'] = new Howl({
		src: ['mp3/aogera_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['aogera_call_01_sona'].seek(0);
			$('#aogera_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#aogera_call_01_sona').on('click',function(){
		if(howl['aogera_call_01_sona'].playing() ){
			$('#aogera_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['aogera_call_01_sona'].pause();
		}else{
			$('#aogera_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['aogera_call_01_sona'].play();
		}
	});
	
	howl['yabusame_song_01'] = new Howl({
		src: ['mp3/yabusame_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['yabusame_song_01'].seek(0);
			$('#yabusame_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('yabusame_song_01');
	$('#yabusame_song_01').on('click',function(){
		if(howl['yabusame_song_01'].playing() ){
			$('#yabusame_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['yabusame_song_01'].pause();
		}else{
			$('#yabusame_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['yabusame_song_01'].play();
		}
	});
	howl['yabusame_song_01_sona'] = new Howl({
		src: ['mp3/yabusame_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['yabusame_song_01_sona'].seek(0);
			$('#yabusame_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#yabusame_song_01_sona').on('click',function(){
		if(howl['yabusame_song_01_sona'].playing() ){
			$('#yabusame_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['yabusame_song_01_sona'].pause();
		}else{
			$('#yabusame_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['yabusame_song_01_sona'].play();
		}
	});
	
	howl['hashibosogarasu_call_01'] = new Howl({
		src: ['mp3/hashibosogarasu_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hashibosogarasu_call_01'].seek(0);
			$('#hashibosogarasu_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('hashibosogarasu_call_01');
	$('#hashibosogarasu_call_01').on('click',function(){
		if(howl['hashibosogarasu_call_01'].playing() ){
			$('#hashibosogarasu_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hashibosogarasu_call_01'].pause();
		}else{
			$('#hashibosogarasu_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hashibosogarasu_call_01'].play();
		}
	});
	howl['hashibosogarasu_call_01_sona'] = new Howl({
		src: ['mp3/hashibosogarasu_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hashibosogarasu_call_01_sona'].seek(0);
			$('#hashibosogarasu_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#hashibosogarasu_call_01_sona').on('click',function(){
		if(howl['hashibosogarasu_call_01_sona'].playing() ){
			$('#hashibosogarasu_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hashibosogarasu_call_01_sona'].pause();
		}else{
			$('#hashibosogarasu_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hashibosogarasu_call_01_sona'].play();
		}
	});
	
	howl['hoojiro_song_01'] = new Howl({
		src: ['mp3/hoojiro_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hoojiro_song_01'].seek(0);
			$('#hoojiro_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('hoojiro_song_01');
	$('#hoojiro_song_01').on('click',function(){
		if(howl['hoojiro_song_01'].playing() ){
			$('#hoojiro_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hoojiro_song_01'].pause();
		}else{
			$('#hoojiro_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hoojiro_song_01'].play();
		}
	});
	howl['hoojiro_song_01_sona'] = new Howl({
		src: ['mp3/hoojiro_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hoojiro_song_01_sona'].seek(0);
			$('#hoojiro_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#hoojiro_song_01_sona').on('click',function(){
		if(howl['hoojiro_song_01_sona'].playing() ){
			$('#hoojiro_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hoojiro_song_01_sona'].pause();
		}else{
			$('#hoojiro_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hoojiro_song_01_sona'].play();
		}
	});
	
	howl['hibari_song_01'] = new Howl({
		src: ['mp3/hibari_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hibari_song_01'].seek(0);
			$('#hibari_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('hibari_song_01');
	$('#hibari_song_01').on('click',function(){
		if(howl['hibari_song_01'].playing() ){
			$('#hibari_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hibari_song_01'].pause();
		}else{
			$('#hibari_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hibari_song_01'].play();
		}
	});
	howl['hibari_song_01_sona'] = new Howl({
		src: ['mp3/hibari_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hibari_song_01_sona'].seek(0);
			$('#hibari_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#hibari_song_01_sona').on('click',function(){
		if(howl['hibari_song_01_sona'].playing() ){
			$('#hibari_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hibari_song_01_sona'].pause();
		}else{
			$('#hibari_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hibari_song_01_sona'].play();
		}
	});
	
	howl['tsubame_call_01'] = new Howl({
		src: ['mp3/tsubame_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['tsubame_call_01'].seek(0);
			$('#tsubame_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('tsubame_call_01');
	$('#tsubame_call_01').on('click',function(){
		if(howl['tsubame_call_01'].playing() ){
			$('#tsubame_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['tsubame_call_01'].pause();
		}else{
			$('#tsubame_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['tsubame_call_01'].play();
		}
	});
	howl['tsubame_call_01_sona'] = new Howl({
		src: ['mp3/tsubame_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['tsubame_call_01_sona'].seek(0);
			$('#tsubame_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#tsubame_call_01_sona').on('click',function(){
		if(howl['tsubame_call_01_sona'].playing() ){
			$('#tsubame_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['tsubame_call_01_sona'].pause();
		}else{
			$('#tsubame_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['tsubame_call_01_sona'].play();
		}
	});
	
	howl['mukudori_call_01'] = new Howl({
		src: ['mp3/mukudori_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['mukudori_call_01'].seek(0);
			$('#mukudori_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('mukudori_call_01');
	$('#mukudori_call_01').on('click',function(){
		if(howl['mukudori_call_01'].playing() ){
			$('#mukudori_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['mukudori_call_01'].pause();
		}else{
			$('#mukudori_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['mukudori_call_01'].play();
		}
	});
	howl['mukudori_call_01_sona'] = new Howl({
		src: ['mp3/mukudori_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['mukudori_call_01_sona'].seek(0);
			$('#mukudori_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#mukudori_call_01_sona').on('click',function(){
		if(howl['mukudori_call_01_sona'].playing() ){
			$('#mukudori_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['mukudori_call_01_sona'].pause();
		}else{
			$('#mukudori_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['mukudori_call_01_sona'].play();
		}
	});
	
	howl['kijibato_call_01'] = new Howl({
		src: ['mp3/kijibato_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kijibato_call_01'].seek(0);
			$('#kijibato_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('kijibato_call_01');
	$('#kijibato_call_01').on('click',function(){
		if(howl['kijibato_call_01'].playing() ){
			$('#kijibato_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kijibato_call_01'].pause();
		}else{
			$('#kijibato_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kijibato_call_01'].play();
		}
	});
	howl['kijibato_call_01_sona'] = new Howl({
		src: ['mp3/kijibato_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kijibato_call_01_sona'].seek(0);
			$('#kijibato_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#kijibato_call_01_sona').on('click',function(){
		if(howl['kijibato_call_01_sona'].playing() ){
			$('#kijibato_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kijibato_call_01_sona'].pause();
		}else{
			$('#kijibato_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kijibato_call_01_sona'].play();
		}
	});
	
	howl['kisekirei_song_01'] = new Howl({
		src: ['mp3/kisekirei_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kisekirei_song_01'].seek(0);
			$('#kisekirei_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('kisekirei_song_01');
	$('#kisekirei_song_01').on('click',function(){
		if(howl['kisekirei_song_01'].playing() ){
			$('#kisekirei_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kisekirei_song_01'].pause();
		}else{
			$('#kisekirei_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kisekirei_song_01'].play();
		}
	});
	howl['kisekirei_song_01_sona'] = new Howl({
		src: ['mp3/kisekirei_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kisekirei_song_01_sona'].seek(0);
			$('#kisekirei_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#kisekirei_song_01_sona').on('click',function(){
		if(howl['kisekirei_song_01_sona'].playing() ){
			$('#kisekirei_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kisekirei_song_01_sona'].pause();
		}else{
			$('#kisekirei_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kisekirei_song_01_sona'].play();
		}
	});
	
	howl['segurosekirei_song_01'] = new Howl({
		src: ['mp3/segurosekirei_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['segurosekirei_song_01'].seek(0);
			$('#segurosekirei_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('segurosekirei_song_01');
	$('#segurosekirei_song_01').on('click',function(){
		if(howl['segurosekirei_song_01'].playing() ){
			$('#segurosekirei_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['segurosekirei_song_01'].pause();
		}else{
			$('#segurosekirei_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['segurosekirei_song_01'].play();
		}
	});
	howl['segurosekirei_song_01_sona'] = new Howl({
		src: ['mp3/segurosekirei_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['segurosekirei_song_01_sona'].seek(0);
			$('#segurosekirei_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#segurosekirei_song_01_sona').on('click',function(){
		if(howl['segurosekirei_song_01_sona'].playing() ){
			$('#segurosekirei_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['segurosekirei_song_01_sona'].pause();
		}else{
			$('#segurosekirei_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['segurosekirei_song_01_sona'].play();
		}
	});
	
	howl['hiyodori_call_01'] = new Howl({
		src: ['mp3/hiyodori_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hiyodori_call_01'].seek(0);
			$('#hiyodori_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('hiyodori_call_01');
	$('#hiyodori_call_01').on('click',function(){
		if(howl['hiyodori_call_01'].playing() ){
			$('#hiyodori_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hiyodori_call_01'].pause();
		}else{
			$('#hiyodori_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hiyodori_call_01'].play();
		}
	});
	howl['hiyodori_call_01_sona'] = new Howl({
		src: ['mp3/hiyodori_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hiyodori_call_01_sona'].seek(0);
			$('#hiyodori_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#hiyodori_call_01_sona').on('click',function(){
		if(howl['hiyodori_call_01_sona'].playing() ){
			$('#hiyodori_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hiyodori_call_01_sona'].pause();
		}else{
			$('#hiyodori_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hiyodori_call_01_sona'].play();
		}
	});

	howl['kibitaki_song_01'] = new Howl({
		src: ['mp3/kibitaki_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kibitaki_song_01'].seek(0);
			$('#kibitaki_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('kibitaki_song_01');
	$('#kibitaki_song_01').on('click',function(){
		if(howl['kibitaki_song_01'].playing() ){
			$('#kibitaki_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kibitaki_song_01'].pause();
		}else{
			$('#kibitaki_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kibitaki_song_01'].play();
		}
	});
	howl['kibitaki_song_01_sona'] = new Howl({
		src: ['mp3/kibitaki_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kibitaki_song_01_sona'].seek(0);
			$('#kibitaki_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#kibitaki_song_01_sona').on('click',function(){
		if(howl['kibitaki_song_01_sona'].playing() ){
			$('#kibitaki_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kibitaki_song_01_sona'].pause();
		}else{
			$('#kibitaki_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kibitaki_song_01_sona'].play();
		}
	});
	
	howl['hototogisu_song_01'] = new Howl({
		src: ['mp3/hototogisu_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hototogisu_song_01'].seek(0);
			$('#hototogisu_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('hototogisu_song_01');
	$('#hototogisu_song_01').on('click',function(){
		if(howl['hototogisu_song_01'].playing() ){
			$('#hototogisu_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hototogisu_song_01'].pause();
		}else{
			$('#hototogisu_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hototogisu_song_01'].play();
		}
	});
	howl['hototogisu_song_01_sona'] = new Howl({
		src: ['mp3/hototogisu_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hototogisu_song_01_sona'].seek(0);
			$('#hototogisu_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#hototogisu_song_01_sona').on('click',function(){
		if(howl['hototogisu_song_01_sona'].playing() ){
			$('#hototogisu_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hototogisu_song_01_sona'].pause();
		}else{
			$('#hototogisu_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hototogisu_song_01_sona'].play();
		}
	});
	
	howl['mejiro_song_01'] = new Howl({
		src: ['mp3/mejiro_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['mejiro_song_01'].seek(0);
			$('#mejiro_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('mejiro_song_01');
	$('#mejiro_song_01').on('click',function(){
		if(howl['mejiro_song_01'].playing() ){
			$('#mejiro_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['mejiro_song_01'].pause();
		}else{
			$('#mejiro_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['mejiro_song_01'].play();
		}
	});
	howl['mejiro_song_01_sona'] = new Howl({
		src: ['mp3/mejiro_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['mejiro_song_01_sona'].seek(0);
			$('#mejiro_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#mejiro_song_01_sona').on('click',function(){
		if(howl['mejiro_song_01_sona'].playing() ){
			$('#mejiro_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['mejiro_song_01_sona'].pause();
		}else{
			$('#mejiro_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['mejiro_song_01_sona'].play();
		}
	});
	
	howl['kakko_song_01'] = new Howl({
		src: ['mp3/kakko_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kakko_song_01'].seek(0);
			$('#kakko_song_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('kakko_song_01');
	$('#kakko_song_01').on('click',function(){
		if(howl['kakko_song_01'].playing() ){
			$('#kakko_song_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kakko_song_01'].pause();
		}else{
			$('#kakko_song_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kakko_song_01'].play();
		}
	});
	howl['kakko_song_01'] = new Howl({
		src: ['mp3/kakko_song_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['kakko_song_01_sona'].seek(0);
			$('#kakko_song_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#kakko_song_01_sona').on('click',function(){
		if(howl['kakko_song_01_sona'].playing() ){
			$('#kakko_song_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['kakko_song_01_sona'].pause();
		}else{
			$('#kakko_song_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['kakko_song_01_sona'].play();
		}
	});
	
	howl['hashibutogarasu_call_01'] = new Howl({
		src: ['mp3/hashibutogarasu_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hashibutogarasu_call_01'].seek(0);
			$('#hashibutogarasu_call_01').html('<i class="fas fa-play"></i>');
		}
	});
	arrHowl.push('hashibutogarasu_call_01');
	$('#hashibutogarasu_call_01').on('click',function(){
		if(howl['hashibutogarasu_call_01'].playing() ){
			$('#hashibutogarasu_call_01').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hashibutogarasu_call_01'].pause();
		}else{
			$('#hashibutogarasu_call_01').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hashibutogarasu_call_01'].play();
		}
	});
	howl['hashibutogarasu_call_01_sona'] = new Howl({
		src: ['mp3/hashibutogarasu_call_01.mp3'],
		preload: true,   // Pre load
		volume: 1.0,     // Volume (specify in the range 0.0 to 1.0)
		loop: false,     // Loop playback
		autoplay: false, // Auto playback
		onend: function() {
			howl['hashibutogarasu_call_01_sona'].seek(0);
			$('#hashibutogarasu_call_01_sona').html('<i class="fas fa-play"></i>');
		}
	});
	$('#hashibutogarasu_call_01_sona').on('click',function(){
		if(howl['hashibutogarasu_call_01_sona'].playing() ){
			$('#hashibutogarasu_call_01_sona').html('<i class="fas fa-play"></i>');  // Change to "playback button"
			howl['hashibutogarasu_call_01_sona'].pause();
		}else{
			$('#hashibutogarasu_call_01_sona').html('<i class="fas fa-pause"></i>');  // Change to "stop button"
			howl['hashibutogarasu_call_01_sona'].play();
		}
	});
});