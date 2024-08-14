#!/usr/bin/perl --
#!c:/perl64/bin/perl.exe

use lib qw(pm .);

use CGI;

use strict;
use warnings;
use utf8;

use CGI::Carp( 'fatalsToBrowser' );
use HTML::Template;
use Time::Piece;


use Par;
use Quiz;
use Util;


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

my $tmpl = &Util::load_html_tmpl('count_accuracy.tmpl' );


my $user = &Util::form_str_utf8($q, 'user');
$tmpl->param( user => "$user" ); 

my $login = 1;
if ($user =~ /^[0-9]+$/){ # If it's only numbers, it's guest
	$login = 0;
}
$tmpl->param( login => "$login" );

# Determine group from username
my $group = &Quiz::judge_group($user);


my $data_set = {};


&Quiz::load_bird_info($data_set);

# Katakana name → Roman alphabet name. Also referenced from within a subroutine.
my $JP_TO_ROMAN_DICT = &Quiz::make_jp_to_roman_dictionary($data_set);

# Read sound source information
# Return value is the number of times the sound source and the number of correct answers, initially 0
# $counts->{MP3}->{}, $counts->{MP3}->{}
my ($counts, $corrects) = &Quiz::load_mp3_info($data_set);

# Find the proficiency score from the response log and store it in the $data_set.
# Get the number of past responses by return value.
# $counts->{TODAY}, $counts->{TOTAL}, $counts->{MP3}
($counts, $corrects) = &Quiz::load_past_achievement($data_set, $user, $counts, $corrects);

if ($q->param( 'sp_roman' )){
	my $correct_answer = &Util::form_str_utf8($q, 'correct_answer');
	my $correct_answer_roman = &Util::form_str_utf8($q, 'sp_roman');
	$tmpl->param( sp_roman => "$correct_answer_roman" ); 	
	my $mp3_file_path_name = &Util::form_str_utf8($q, 'mp3_file_path_name');
	my $mp3_file_base_name = &Quiz::get_mp3_file_base_name($mp3_file_path_name);
	my $users_answer = &Util::form_str_utf8($q, 'users_answer');
	my $song_type_num = &Quiz::get_song_type_num_for_mp3($data_set, $mp3_file_path_name); 
	my $users_answer_roman = $JP_TO_ROMAN_DICT->{$users_answer};
	
	#if ($group == 1 || $group == 3){
		my ($judge, $num, $num_incorrect) = &Quiz::judge_dialogue($data_set, $mp3_file_base_name, $correct_answer_roman, $correct_answer, $users_answer);
		if ($judge){
			&Quiz::set_dialogue_to_template($tmpl, $song_type_num, $judge, $num, $num_incorrect);
		}
	#}
}


my @accuracy_rates; # $accuracy_rate is reset for each species, so all species information is aggregated here.
my $i = 1; # Set 1 from the top of the table.

my $heading = "音源の種類</th><th scope='col'>音源</th>
               <th scope='col'>出題数</th><th scope='col'>";


	$heading = $heading."正解数</th><th scope='col'>頻度</th><th scope='col'>ステータス";

$heading = $heading."</th><th scope='col'>識別方法";

my @mp3_licenses;

# Species Name Romanization List
my @spp = keys %{$data_set}; 

# Display in a table on the screen in order of PRIORITY
foreach my $sp (sort {$data_set->{$a}{PRIORITY} <=> $data_set->{$b}{PRIORITY}} @spp) {
    my $MP3_ref = $data_set->{$sp}->{MP3};
    my @mp3s = keys %{$MP3_ref};
    	
    foreach my $mp3 (@mp3s){
    	
    	my $song_type_num = &Quiz::get_song_type_num_for_mp3($data_set, $mp3);
    	my $mp3_str = &Quiz::get_mp3_file_path_name($mp3);

	    my $accuracy_rate = "<tr><td>$i　$song_type_num</td><td><button class='btn-play' id="."$mp3"." type='button'><i class='fas fa-play'></i></button></td><td>$counts->{MP3}{$mp3}</td><td>";
	                         
	    # If licensed
        if ($data_set->{$sp}->{MP3}->{$mp3}->{LICENSE} =~ m/by/){
        	
        	my $sp_jp = &Quiz::get_sp_jp_name($data_set, $sp);
        	push @mp3_licenses, "★$song_type_num"."　$data_set->{$sp}->{MP3}->{$mp3}->{LICENSE}<br>";
        	    
        }

    	$accuracy_rate = $accuracy_rate."$corrects->{MP3}->{$mp3}</td>";
    	
    	#if ($group == 1 || $group == 3){
	
    	    $accuracy_rate = $accuracy_rate."<td>";
    	    #$accuracy_rate = $accuracy_rate."$data_set->{$sp}->{MP3}->{$mp3}->{SCORE}</td><td>";
    	    
    	    if ($data_set->{$sp}->{FIX} == 0){
    	    	$accuracy_rate = $accuracy_rate."　</td><td>";
    	    	#$accuracy_rate = $accuracy_rate."$data_set->{$sp}->{FIX}</td>";
    	    }
    	    elsif ($data_set->{$sp}->{FIX} == 1){
    	    	$accuracy_rate = $accuracy_rate."<font color='red'>高め</font></td><td>";
    	    }
    	    else{ #-1
    	    	$accuracy_rate = $accuracy_rate."<font color='blue'>低め</font></td><td>";
    	    }
    	    
	        if ($data_set->{$sp}->{FIX} == -1 && $data_set->{$sp}->{CORRECT} == 1){
    	        $accuracy_rate = $accuracy_rate."<font color='green'>マスター</font></td><td>";
    	        #push @accuracy_rates,
    	        #       $accuracy_rate."<font color='green'>マスター</font></td></tr>";
	        }
	        else{
	        	$accuracy_rate = $accuracy_rate."　</td><td>";
	        	#push @accuracy_rates, $accuracy_rate."　</td></tr>";
	        }
	    #}
	    
	    #else{ #group2,4
	    	#$accuracy_rate = $accuracy_rate."</td><td>";
	    #}
	    
	    $accuracy_rate = $accuracy_rate."$data_set->{$sp}->{POINT}"."</td></tr>";
	    
	    push @accuracy_rates, $accuracy_rate;
	    $i++;
	    
	}
}


$tmpl->param( heading => $heading );
$tmpl->param( accuracy_rates => "@accuracy_rates" );
$tmpl->param( mp3_licenses => "@mp3_licenses" );


my $content_info = "クイズトレーニングへ";
my $content_url = "quiz_training.cgi";

$tmpl->param( content_info => "$content_info" ); 
$tmpl->param( content_url => "$content_url" ); 

#$q->charset( 'UTF-8' );
print "Set-Cookie: NAME = cookie; Secure; HttpOnly\n";
print $q->header;
print &Encode::encode('utf-8', $tmpl->output);
