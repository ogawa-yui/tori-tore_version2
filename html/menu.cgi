#!/usr/bin/perl --
#!c:/perl64/bin/perl.exe

#
#   Quiz Instructions Screen
#
#   2020-08-05 by OGAWA, Y.

use lib qw(pm .);

use strict;
use warnings;
use utf8;

use CGI;
use HTML::Template;
use CGI::Carp( 'fatalsToBrowser' );
use Time::Piece;

use Info;
use Util;
use Quiz;
use Par;

my $q = CGI->new;
$q->charset( 'UTF-8' );
my $Data_Charset = 'utf-8';

# If you came to this page without logging in
unless ($q->param( 'user' )){  # No user name → Not logged in
	# Display message and exit
	my $tmpl = &Util::load_html_tmpl('not_logged_in_message.tmpl' );
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; # Terminate all programs
}

my $user = &Util::form_str_utf8($q, 'user' );

if ($user eq "null"){ # First visit
	
	# Assign a number and direct the user to agreement.tmpl
	my $tmpl = &Util::load_html_tmpl('sitepolicy.tmpl' );
	
	my $file = &Info::get_all_user_file_path;
	my $user = &get_ssn_for_user($file);
	
	$tmpl->param( user => "$user" ); 
	
	my ($day, $date, $time) = &Util::get_day_date_time;
	
	open (FILE, ">>", $file) || die ("Failed to open user info file");# Write

	
	print FILE &Encode::encode('utf-8', "$user\t3\t$user\thoge\t$date\t$time\t$ENV{REMOTE_ADDR}\t$ENV{HTTP_USER_AGENT}\n"); 
	
	close (FILE);
	
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; # Terminate all programs
}

my $tmpl = &Util::load_html_tmpl('menu.tmpl' );

if ($q->param( 'password' )){ 
	my $pw = &Util::form_str_utf8($q, 'password');

	if (&Info::verify_password($user, $pw)){
		# ログイン成功
		&Util::write_login_log($user, "login"); # Write login information
	}
	else{
    	$tmpl = &Util::load_html_tmpl('warning_message.tmpl' );
    	my $message = "<font color='red'>ログイン失敗</font><br><br>
					＞<a href='login.html'>ログイン画面に戻る</a><br><br>
					ユーザー名、パスワードを忘れてしまった場合、もう一度登録し直してください。<br></p>";
		$tmpl->param( message => "$message" );
		print $q->header;
		print &Encode::encode('utf-8', $tmpl->output);
		exit; # Terminate all programs
	}

	# Number of quiz training questions
	my $quiz_responses = &Info::get_all_quiz_responses_file_path;
	my $quiz_count = &Quiz::get_n_solved($q, $user, $quiz_responses);
              
	$tmpl->param( login => 1 );
	
	# Set information such as login history in the template
	&set_login_info_to_template($q, $tmpl, $user, $quiz_count);
}
else{  # guest
	$tmpl->param( login => 0 );
}

$tmpl->param( user => "$user" ); 
 
#$q->charset( 'UTF-8' );
print "Set-Cookie: NAME = cookie; Secure; HttpOnly\n";
print $q->header;
print &Encode::encode('utf-8', $tmpl->output);


#####################################

sub set_login_info_to_template
{
	my $q = shift @_;
	my $tmpl = shift @_;
	my $user = shift @_;
	my $count = shift @_;
	my $login_log_file = &Info::get_login_log_path; 
	
	open (FILE, "<", $login_log_file) or die "Failed to open $login_log_file\n"; 
	my (@login_dates, %counts, @login_histories);
		
	my $line = <FILE>;       
	
	while ($line = <FILE>) {
    	
    	$line = &Encode::decode($Data_Charset, $line);
    	$line = $q->escapeHTML($line);
    	chomp $line;
    	my @data = split /\t+/, $line; 
    	my $d = $data[0];
    	my $u = $data[6];
    	
    	if ($u eq $user){ 
    		push @login_histories, $d;
    		$d = (split /\s+/, $d)[0]; # Extract only the date
    		$counts{$d}++;
    	}
    	
	}
	
	close (FILE);
	
	foreach (keys %counts){
    	push @login_dates, $_;
    }
	
	my $login_date = @login_dates; # How many days since a user logged in?
	$tmpl->param( login_date => "$login_date" ); 
	
	# Output the last 10 login records
	my @login_histories10 = @login_histories;
    if (@login_histories >= 10){
    	@login_histories10 = splice @login_histories, @login_histories - 10;
    }
	
	# Insert a new line
	my $login_history = join "<br>", @login_histories10;
	
	$tmpl->param( login_history => "$login_history" ); 
	
	# Record number of quiz training questions
	$tmpl->param( count => "$count" ); 
	
}