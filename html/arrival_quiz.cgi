#!/usr/bin/perl --
#!c:/perl64/bin/perl.exe

#
#   Arrival quiz screen
#
#   2020-08-05 by OGAWA, Y.


use lib qw(pm .);

use CGI;

use CGI::Carp( 'fatalsToBrowser' );
use HTML::Template;

use strict;
use warnings;
use utf8; 

use Info;
use Util;
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


my $tmpl = &Util::load_html_tmpl('arrival_quiz.tmpl' );


my $user = &Util::form_str_utf8($q, 'user');
$tmpl->param( user => "$user" );

my $login = 1;
if ($user =~ /^[0-9]+$/){ # If it's only numbers, it's guest
	$login = 0;
}
$tmpl->param( login => "$login" );

my $data_set = {};

# Loading bird information
&Quiz::load_bird_info($data_set);


my ($day, $date, $time) = &Util::get_day_date_time;

my $test_log_file = &Info::get_all_test_responses_file_path;


# If you are solving the second or subsequent questions (the answers are sent to you by Form)
if ($q->param( 'correct_answer' )) { 
	my $prev_correct_answer = &Util::form_str_utf8($q, 'correct_answer' );
	
	# If you did not respond to the question (in SAFARI) 
	unless ($q->param( 'users_answer' )){ 
		my $tmpl = &Util::load_html_tmpl('warning_message.tmpl' );					
		my $message = "<form method='post' action='arrival_quiz.cgi' > いずれかの種を選択してから「回答！」をクリックすると、
					答えが表示されます。
					<br><br><input type='submit' value='腕試しに戻る' class='btn'>
					<input type='hidden' name='user' value="."$user"." >";
		#			<input type='hidden' name='user' value='$user' >";
		$tmpl->param( message => "$message" );
		print $q->header;
		print &Encode::encode('utf-8', $tmpl->output);
		exit; # Terminate all programs
	}
	
	my $prev_users_answer = &Util::form_str_utf8($q, 'users_answer');
	my $prev_mp3 = $q->param( 'mp3_for_test' );
	
	# Write question and response data
	&Quiz::write_data
	  ($test_log_file, $user, $prev_mp3, $prev_correct_answer, $prev_users_answer);

}


# Retrieve the number of questions for the test and answer list
# Return value is the number of questions, mp3 and answer list reference
my $choices_answer_file = &Info::get_all_choices_answer_file_path;

my ($question, $mp3_for_test, $correct_answer)
         = &Quiz::get_n_question_and_answer_lists($choices_answer_file, $test_log_file, $user);
$mp3_for_test = &Quiz::get_mp3_file_base_name($mp3_for_test); # Change to base name

$tmpl->param( question => "$question" ); # 26


# User's cumulative number of test responses
my $count = &Quiz::get_n_solved($q, $user, $test_log_file);

# If you already solved all test questions
if ($count >= $question){
	
	# Update Values
	$count = $count % $question; # The remainder when divided by the number of questions available
}



# How many questions are you solving now?
my $count_quiz = $count + 1; 
$tmpl->param( count_quiz => "$count_quiz" );


# If you have reached the number of questions provided, go to the answer screen.
my $next_url = "arrival_quiz.cgi";
my $next_content = "次の問題へ";

if ($question == $count_quiz){
	$next_url = "arrival_quiz_answer.cgi";
	$next_content = "次へ";
}

$tmpl->param( next_url => "$next_url" ); 
$tmpl->param( next_content => "$next_content" ); 



$tmpl->param( mp3_for_test => "$mp3_for_test" );
$tmpl->param( correct_answer => "$correct_answer" ); 



# Set the form of choices (number of all species) to the template
&Quiz::set_choices_form_to_template($data_set, $tmpl);

print "Set-Cookie: NAME = cookie; Secure; HttpOnly\n";
print $q->header;
print &Encode::encode('utf-8', $tmpl->output);


