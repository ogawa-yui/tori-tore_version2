#!/usr/bin/perl --
#!c:/perl64/bin/perl.exe

#
#   User Registration Validation Screen
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

my $q = CGI->new;
$q->charset( 'UTF-8' );

my $tmpl = &Util::load_html_tmpl('user_registration_verification.tmpl' );

my $user = &Util::form_str_utf8($q, 'user');

# Receive username and password
my $user = &Util::form_str_utf8($q, "user" );
my $pw1 = &Util::form_str_utf8($q, "password1" );
my $pw2 = &Util::form_str_utf8($q, "password2" );

if ($user =~ /^[0-9]+$/){ # If the user name is only a number
	$tmpl = &Util::load_html_tmpl('warning_message.tmpl' );
    my $message = "<font color='red'>ユーザー名は英数字5字以上15字以内で設定してください。</font><br>※修正するにはブラウザの戻るボタンを押してください。<br>";
	$tmpl->param( message => "$message" );
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; # Terminate all programs
}

if ($user =~ /^[A-Za-z]+$/){ # If the user name is only alphabet
	$tmpl = &Util::load_html_tmpl('warning_message.tmpl' );
    my $message = "<font color='red'>ユーザー名は英数字5字以上15字以内で設定してください。</font><br>※修正するにはブラウザの戻るボタンを押してください。<br>";
	$tmpl->param( message => "$message" );
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; # Terminate all programs
}

my $file = &Info::get_all_user_file_path;
open (FILE, "<", $file) || die ("Failed to open user info file");

my $line = <FILE>;
while ($line = <FILE>) {
	
	$line = &Encode::decode("utf-8", $line);
    $line =~ s/[\r\n]+\z//;
    my $u = (split /\t+/, $line)[2];
    
    if ($u eq $user){
		$tmpl = &Util::load_html_tmpl('warning_message.tmpl' );
    	my $message = "<font color='red'>入力されたユーザー名はすでに存在しています。</font><br>別のユーザー名を設定してください。<br><br>※修正するにはブラウザの戻るボタンを押してください。";
		$tmpl->param( message => "$message" );
		print $q->header;
		print &Encode::encode('utf-8', $tmpl->output);
		exit; # Terminate all programs
	}
}

if ($pw1 ne $pw2){
	$tmpl = &Util::load_html_tmpl('warning_message.tmpl' );
    my $message = "<font color='red'>２回入力されたパスワードが一致しません</font><br>";
	$tmpl->param( message => "$message" );
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; # Terminate all programs
}

# Encrypt passwords
my $pw_md5 = &Digest::MD5::md5_base64($pw1);

# Passing on user name and PW
$tmpl->param( user => "$user" ); 
$tmpl->param( pw_md5 => "$pw_md5" ); 



print $q->header;
print &Encode::encode('utf-8', $tmpl->output);
