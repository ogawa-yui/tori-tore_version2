#!/usr/bin/perl --
#!c:/perl64/bin/perl.exe

use lib qw(pm .);

use strict;
use warnings;
use utf8;

use CGI;
use HTML::Template;
use CGI::Carp( 'fatalsToBrowser' );
use Time::Piece;

use Util;
use Quiz;

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

my $tmpl = &Util::load_html_tmpl('arrival_quiz_answer.tmpl' );

my $user = &Util::form_str_utf8($q, 'user' ); 
$tmpl->param( user => "$user" ); 

my $login = 1;
if ($user =~ /^[0-9]+$/){ # If it's only numbers, it's guest
	$login = 0;
}
$tmpl->param( login => "$login" );

my $question = &Util::form_str_utf8($q, 'question' ); # How many questions are there?
#my $posttest = $q->param( "posttest" );

my ($day, $date, $time) = &Util::get_day_date_time;


my $correct_answer = &Util::form_str_utf8($q, 'correct_answer');
chomp $correct_answer;


# If you did not respond to the question (in SAFARI) 
unless ($q->param( 'users_answer' )){ 
	my $tmpl = &Util::load_html_tmpl('warning_message.tmpl' );
	my $message = "<form method='post' action='arrival_quiz_answer.cgi' > 回答してください。
				<br><br><input type='submit' value='腕試しに戻る' class='btn'>
				<input type='hidden' name='user' value="."$user"." >";
#				<input type='hidden' name='user' value='$user' >";
	$tmpl->param( message => "$message" );
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; # Terminate all programs
}


my $users_answer = &Util::form_str_utf8($q, 'users_answer');
my $mp3_for_test = &Util::form_str_utf8($q,  'mp3_for_test' );



my $test_responses = &Info::get_all_test_responses_file_path; 
#my $test_responses = "../data/responses/test_responses.txt"; 
&Quiz::write_data
  ($test_responses, $user, $mp3_for_test, $correct_answer, $users_answer); 

# Set the test results in the template
&set_test_results_to_template($q, $test_responses, $user, $question);
#$q->charset( 'UTF-8' );
print "Set-Cookie: NAME = cookie; Secure; HttpOnly\n";
print $q->header;
print &Encode::encode('utf-8', $tmpl->output);


#######################################
sub set_test_results_to_template
{
	my $q = shift @_;
	my $test_responses = shift @_;
	my $user = shift @_;
	my $question = shift @_;
	
	my (@results, $n_question);
	my $num = 1;
	push @results, "<h3>".$num."回目</h3><table class='A'><tr><td></td><td>正誤</td><td>正解</td><td>選択</td><td>正解の音源</td></tr>";
	my $n_correct = 0;
	open (FILE, "<", $test_responses) or die "Failed to open $test_responses:$!\n"; 

	my $line = <FILE>;       
	
	while ($line = <FILE>) {
	    
	    $line = &Encode::decode('utf8', $line);
	    $line = $q->escapeHTML($line);
	    chomp $line;
	    
	    my @data = split /\t+/, $line; 
	    my $u = $data[6];
	    my $mp3 = $data[7];

		my $mp3_file_base_name = &Quiz::get_mp3_file_base_name($mp3);

	    my $correct_answer = $data[8];
    	my $users_answer = $data[9];
	    
	    if ($u eq $user){
	        
	        $n_question++;
	        my $result;
	        
	        if ($n_question > $question){

	        	$n_question = 1; # Reset for each test batch
	        	$n_correct = 0; # Reset for each test batch
	        	$num++;
	        	push @results, "</table><h3>".$num."回目</h3><table class='A'><tr><td></td><td>正誤</td><td>正解</td><td>選択</td><td>正解の音源</td></tr>";
	        }	
	        $result
	          = "<tr><td>$n_question".
	            "問目</td><td><font color='orange'><b>×</b></font></td><td>$correct_answer".
	            "</td><td>$users_answer".

	            "</td><td><button class='btn-play' id="."$mp3_file_base_name"." type='button'><i class='fas fa-play'></i></button></audio></td></tr>";

	        
	        if ($correct_answer eq $users_answer) {
	            $n_correct++; # Figure out the number of correct answers
	        	$result =~ s!<font color='orange'><b>×!<font color='green'><b>○!;
	        }
	        push @results, $result;
	        
	    }
	    
	}
	close (FILE);
	
	push @results, "</table><br>";
	
	$tmpl->param( "question" => $n_question ); 
	$tmpl->param( "correct" => $n_correct ); 
	$tmpl->param( "results" => "@results" ); 

}
