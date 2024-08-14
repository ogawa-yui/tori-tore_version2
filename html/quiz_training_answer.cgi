#!/usr/bin/perl --
#!c:/perl64/bin/perl.exe

#  Quiz training answer screen
#  
#  2020-07-07  by OGAWA, Yui
#  

use lib qw(pm .);

use CGI;

use CGI::Carp( 'fatalsToBrowser' );
use HTML::Template;

use strict;
use warnings;
use utf8; 

use Util;
use Info;
use Quiz;
use Par;
use Time::Piece;

use Encode; 
my $Data_Charset = 'utf-8';


my $q = CGI->new;
$q->charset( 'UTF-8' );


# If you came to this page without logging in
unless ($q->param( 'user' )){  # No user name → Not logged in
	# Display message and exit
	my $tmpl = &Util::load_html_tmpl('not_logged_in_message.tmpl' );
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; # Terminate all programs
}

my $tmpl = &Util::load_html_tmpl('quiz_training_answer.tmpl' );

my $user = &Util::form_str_utf8($q, 'user');

$tmpl->param( user => "$user" );


# If you did not respond to the question (in SAFARI) 
unless ($q->param( 'users_answer' )){ 
	my $tmpl = &Util::load_html_tmpl('warning_message.tmpl' );
	#my $message = "<form method='post' action='quiz_training.cgi' > クイズに回答してください。
	#				<br><br><input type='submit' value='クイズに戻る' class='btn'>
	#				<input type='hidden' name='user' value='$user' >";
	my $message = "<form method='post' action='quiz_training.cgi' > いずれかの種を選択してから「回答！」をクリックすると、
					答えが表示されます。
					<br><br><input type='submit' value='クイズに戻る' class='btn'>
					<input type='hidden' name='user' value="."$user"." >";
	$tmpl->param( message => "$message" );
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; # Terminate all programs
}

my $login = 1;
if ($user =~ /^[0-9]+$/){ # If only numbers are used, guest
	$login = 0;
}
$tmpl->param( login => "$login" );

my $sp_roman = &Util::form_str_utf8($q, 'sp_roman' );
$tmpl->param( sp_roman => "$sp_roman" ); 

my $mp3_file_path_name = &Util::form_str_utf8($q, 'mp3_file_path_name' );


if ($mp3_file_path_name =~ /\Amp3\/.+mp3\z/){ #(「\A」:lead、「\/」：slush、.+：One or more consecutive arbitrary characters、「\z」：last）
	# Nothing.
}
else{ # Not matched
	my $tmpl = &Util::load_html_tmpl('warning_message.tmpl' );
	my $message = "不正な操作です";
	$tmpl->param( message => "$message" );
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; #Terminate all programs
}
$tmpl->param( mp3_file_path_name => "$mp3_file_path_name" );


my $mp3_file_base_name = &Quiz::get_mp3_file_base_name($mp3_file_path_name);
$tmpl->param( mp3_file_base_name => "$mp3_file_base_name" );

my $mp3_file_sona_base_name = $mp3_file_base_name . "_sona";
$tmpl->param( mp3_file_sona_base_name => "$mp3_file_sona_base_name" );



my $spectrogram = &Util::form_str_utf8($q, 'spectrogram' );
$tmpl->param( spectrogram => "$spectrogram" );

my $correct_answer = &Util::form_str_utf8($q, 'correct_answer'); # Same as sp_jp (Japanese name of species）
$tmpl->param( correct_answer => "$correct_answer" ); 

my $users_answer = &Util::form_str_utf8($q, 'users_answer' );
$tmpl->param( users_answer => "$users_answer" ); 


my $choices = &Util::form_str_utf8($q, 'choices' ); 
my @choices = split (/\s+/, $choices); #Romanization of quiz choices (including correct answers)

my $choices_jp = &Util::form_str_utf8($q, 'choices_jp' ); 
my @choices_jp = split (/\s+/, $choices_jp); #Quiz choices of Japanese (including correct answers)

my $answer_license = &Util::form_str_utf8($q, 'answer_license' );
$tmpl->param( answer_license => "$answer_license" );




# Write question and response data
my $quiz_responses_file = &Info::get_all_quiz_responses_file_path;
&Quiz::write_data($quiz_responses_file, $user, $mp3_file_base_name, $correct_answer,
                     $users_answer, $choices_jp); 


my $data_set = {};


&Quiz::load_bird_info($data_set);

# Dictionary of jp(katakana) to roman species name
# Also referenced from within subroutines
my $JP_TO_ROMAN_DICT = &Quiz::make_jp_to_roman_dictionary($data_set);

# Read sound source information
my ($counts, $corrects) = &Quiz::load_mp3_info($data_set);


($counts, $corrects) = &Quiz::load_past_achievement($data_set, $user, $counts, $corrects);


# Set the number of responses information to the template
&Quiz::set_counts_to_template($tmpl, $counts);

# Get the species name_songing_number from the sound source of the correct species and output it.
my $song_type_num = &Quiz::get_song_type_num_for_mp3($data_set, $mp3_file_base_name);
$tmpl->param( song_type_num => "$song_type_num" );


# Returns the number of questions remaining against the target based on the cumulative number of quizzes
my $num_quiz_left = &Quiz::get_num_quiz_left($counts->{TOTAL});
my $num_quiz_left_today = &Quiz::get_num_quiz_left_today($counts->{TODAY});


# Display the accuracy rate on the page.
my $accuracy_today
 = "本日：$counts->{TODAY}"."問中$corrects->{TODAY}"."問正解！　正解率";
my $accuracy_allday
 = "累計：$counts->{TOTAL}"."問中$corrects->{TOTAL}"."問正解！　正解率";
my $accuracy_rate_today
 = sprintf( "%.0f%%", ( $corrects->{TODAY} / $counts->{TODAY} ) * 100);
my $accuracy_rate_allday
 = sprintf ("%.0f%%", ( $corrects->{TOTAL} / $counts->{TOTAL} ) * 100); 
 
$tmpl->param( accuracy_rate_today => "$accuracy_today$accuracy_rate_today" );
$tmpl->param( accuracy_rate_allday => "$accuracy_allday$accuracy_rate_allday" );



my @choices_mp3;
foreach my $sp (@choices){
	
    my $MP3_ref = $data_set->{$sp}->{MP3};
    my @mp3_parts;
	    
    foreach my $mp3 (keys %{$MP3_ref}){
        
        # If licensed
        if ($data_set->{$sp}->{MP3}->{$mp3}->{LICENSE} =~ m/by/){
        	my $sp_jp = &Quiz::get_sp_jp_name($data_set, $sp);
        	
        	$tmpl->param( mp3_license
        	 => "★$sp_jp"."の音源<br>$data_set->{$sp}->{MP3}->{$mp3}->{LICENSE}" );
        	    
        }
        
        my $mp3_file_path_name = &Quiz::get_mp3_file_path_name($mp3);
        
       
        push @mp3_parts, "<button class='btn-play' id="."$mp3"." type='button'><i class='fas fa-play'></i></button>";

    }
	    
    if (@mp3_parts == 1){ # When there is only one sound source per species
    	push @mp3_parts, "　";
    }
	    
    my $combi = join ("</td><td>", @mp3_parts);
    push @choices_mp3, $combi;
}


my @choices_jp_table;
for (my $i = 0; $i < $Par::N_CHOICES; $i++){ 
    #my $combi = "<tr><td>　</td><td>$choices_jp[$i]</td><td>$choices_mp3[$i]</td><td>
    #  <a class='image_link' href='$data_set->{$choices[$i]}{URL1}' 
    #  target='_blank'><img src='icon/saezuri_navi.png' width='70' height='50' 
    #  align='middle' alt='さえずりナビへ'></a></td><td><a class='image_link' 
    #  href='$data_set->{$choices[$i]}{URL2}' target='_blank'>
    #  <img src='icon/BIRD FAN.png' width='70' height='50' align='middle' 
    #  alt='BIRD FANへ'></a></td></tr>";
    my $combi = "<tr><td>　</td><td>$choices_jp[$i]</td><td>$choices_mp3[$i]</td><td>
      <a class='image_link' href="."$data_set->{$choices[$i]}{URL1}". 
      " target='_blank'><img src='icon/saezuri_navi.png' width='70' height='50' 
      align='middle' alt='さえずりナビへ'></a></td><td><a class='image_link' 
      href="."$data_set->{$choices[$i]}{URL2}"." target='_blank'>
      <img src='icon/BIRD FAN.png' width='70' height='50' align='middle' 
      alt='BIRD FANへ'></a></td></tr>";
    push @choices_jp_table, $combi;
}

# Place a ◎ in front of the answer choice
foreach (@choices_jp_table){
    $_ =~ s!<td>　</td><td>$correct_answer</td>!<td>◎</td><td>$correct_answer</td>!; 
}


my $content_info = "次へ";
my $content_url = "quiz_training.cgi";


#get_correct_or_incorrect_message
# Arguments for $data_set and @choices_jp_table
my $correct_or_incorrect; 

if ($users_answer eq $correct_answer){
    $correct_or_incorrect = '<font color="green">正解！</font>'; 

}
else{
    $correct_or_incorrect = '<font color="orange">不正解</font>'; 
    
    foreach (@choices_jp_table){
        $_ =~ s!<td>　</td><td>$users_answer</td>!<td>×</td><td>$users_answer</td>!; # Put × in front of the answer.
    }
}
$tmpl->param( correct_or_incorrect => "$correct_or_incorrect" ); 

#if ($group == 1 || $group == 3){
	my ($judge, $num, $num_incorrect) = &Quiz::judge_dialogue($data_set, $mp3_file_base_name, $sp_roman, $correct_answer, $users_answer);
	if ($judge){
		&Quiz::set_dialogue_to_template($tmpl, $song_type_num, $judge, $num, $num_incorrect);
	}
#}


$tmpl->param( content_info => "$content_info" );
$tmpl->param( content_url => "$content_url" );


# Color ◎ and ×
foreach (@choices_jp_table){
    $_ =~ s!◎!<b><font color="green">◎</font></b>!g;
    $_ =~ s!×!<b><font color="orange">×</font></b>!g;
}

$tmpl->param( choices_jp_table => "@choices_jp_table" );

#if ($group == 1 || $group == 3){
	my $image;
	my @images = "<p class='font150'>出題種一覧（写真：マスターした種、シルエット：マスターしていない種）</p>";
	foreach my $sp (sort {$data_set->{$a}{PRIORITY} <=> $data_set->{$b}{PRIORITY}} keys %$data_set){ 
    	if ($data_set->{$sp}->{FIX} == -1 && $data_set->{$sp}->{CORRECT} == 1){ #マスター
    		$image = "<img src='img/"."$sp".".jpg' width='75' height='75' title='"."$data_set->{$sp}{SP_JP}"."　"."$data_set->{$sp}{LICENSE}"."' alt='"."$data_set->{$sp}{SP_JP}"."'>";
    	}
    	else{ 
    		$image = "<img src="."silhouette/"."$sp".".png"." width='75' height='75' title="."$data_set->{$sp}{SP_JP}"." alt="."$data_set->{$sp}{SP_JP}".">";
    		#$image = "<img src='silhouette/"."$sp".".png' width='75' height='75' title='"."$data_set->{$sp}{SP_JP}"."' alt='"."$data_set->{$sp}{SP_JP}"."'>";
    	}
    	push @images, $image;
	}
	$tmpl->param( image => "@images" );
#}

print "Set-Cookie: NAME = cookie; Secure; HttpOnly\n";
print $q->header;
print &Encode::encode('utf-8', $tmpl->output);

###############################
sub get_choices_mp3
{
	my $data_set = shift @_;
	my @choices  = shift @_;
	
	foreach my $sp (@choices){
	
    my $MP3_ref = $data_set->{$sp}->{MP3};
    my @mp3_parts;
	    
    foreach my $mp3 (keys %{$MP3_ref}){
        
        # If licensed
        if ($data_set->{$sp}->{MP3}->{$mp3}->{LICENSE} =~ m/by/){
        	my $sp_jp = &Quiz::get_sp_jp_name($data_set, $sp);
        	
        	$tmpl->param( mp3_license
        	 => "★$sp_jp"."の音源<br>$data_set->{$sp}->{MP3}->{$mp3}->{LICENSE}" );
        	    
        }
        
        my $mp3_file_path_name = &Quiz::get_mp3_file_path_name($mp3);
        push @mp3_parts, "<audio src='$mp3_file_path_name' preload='none'></audio>";
    }
	    
    if (@mp3_parts == 1){ # When there is only one sound source per species
    	push @mp3_parts, "　";
    }
	    
    my $combi = join ("</td><td>", @mp3_parts);
    push @choices_mp3, $combi;
    
    return @choices_mp3;

}
}

