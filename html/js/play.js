<!-- // Start playback
function audioPlay(){
    document.getElementById("audio").play();
}
 
// Stop playback
function audioPause(){
    document.getElementById("audio").pause();
}
-->


$(function() {
    $('.playBtn').click(function() {
        if($('#video1')[0].paused){
          $('#video1')[0].play();
        }else{
          $('#video1')[0].pause();
        }
    });
});
