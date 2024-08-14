#!/usr/bin/perl --
#!c:/perl64/bin/perl.exe

#
#   User Registration Completion Screen
#
#   2020-08-05 by OGAWA, Y.

use lib qw(pm .);

use strict;
use warnings;
use utf8;
use CGI;
use HTML::Template;
use CGI::Carp( 'fatalsToBrowser' );
use Util;

use Time::Piece;

my $Data_Charset = 'utf-8';

my $q = CGI->new;
$q->charset( 'UTF-8' );

my $tmpl = &Util::load_html_tmpl('user_registration_complete.tmpl' );

my $user = &Util::form_str_utf8($q, 'user');

# Receive username and password
my $user = &Util::form_str_utf8($q, "user" );
my $pw_md5 = &Util::form_str_utf8($q, "pw_md5" );

my ($day, $date, $time) = &Util::get_day_date_time;

my $file = &Info::get_all_user_file_path;
my $id = &Util::get_ssn_for_user($file);

&write_username;


print $q->header;
print &Encode::encode('utf-8', $tmpl->output);

sub write_username
{
	my $duplicate = 0;
	
	open (FILE, "<", $file) or die "Failed to open $file:$!\n";
	my $line = <FILE>;

	while ($line = <FILE>) {
    
    	$line = &Encode::decode($Data_Charset, $line);
    	chomp $line;
		my @data = split /\t+/, $line;
    	my $u = $data[2];
		
		if ($u eq $user){
			$duplicate = 1;
			last;
		}
		
	}
	
	if ($duplicate == 0){
		open (FILE, ">>", $file) || die ("Failed to open user info file");

		print FILE &Encode::encode('utf-8', 
                           "$id\t3\t$user\t$pw_md5\t$date\t$time\t$ENV{REMOTE_ADDR}\t$ENV{HTTP_USER_AGENT}\n");
		close (FILE);
	}
}