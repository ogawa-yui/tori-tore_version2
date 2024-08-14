#   A package of miscellaneous functions
#   
#  2013-11-16 by TAKENAKA, A.
#  rev 2020-07-07  by OGAWA, Yui
#  

package Util;

use Exporter;
# use CGI::Carp('fatalsToBrowser');

use Encode;
use HTML::Template;
use Time::Piece;

use Info;

@ISA = qw(Exporter);

@EXPORT = qw(
get_ssn_for_user
form_str_utf8
html_escape
quote_escape
inequ_escape
inequ_restore
get_day_date_time
load_html_tmpl
write_login_log
);

use strict;
use utf8;

my $t = localtime;

my $Data_Charset = 'utf-8';

###############################
# Set an ID (sequential number) for each user

sub get_ssn_for_user
{
	my $file = shift @_;
	push my @user_ids, 0; # Initial value 0
	
	open (FILE, "<", $file) || die ("Failed to open user info file");
	
	my $line = <FILE>;
	while ($line = <FILE>) {
	
		$line = &Encode::decode("utf-8", $line);
    	$line =~ s/[\r\n]+\z//; # Remove all newlines
    	my $id = (split /\t+/, $line)[0];
    	push @user_ids, $id;
    }
	close (FILE);
    
    @user_ids = sort {$b <=> $a} @user_ids; # Maximum value → Minimum value
	my $user_id = $user_ids[0] + 1; #Assign a number one greater than the maximum value
	$user_id = sprintf("%05d", $user_id); # If the number is less than 5 digits, fill it with zeros.
	
	return $user_id;
}

##########################
# Extracts and returns the value corresponding to the Key from the CGI object.
# Restores double quotes, converts < and > to &lt;, &gt;,
# and uses valid tags as tags.
#
#  The returned value can be displayed in HTML.
#
#  form_str_utf8(CGI_object, Key)

sub form_str_utf8
{
    my ($cgi, $key) = @_;

    my $limit_len = 4096; # If an input is longer than this, it will be considered abnormal and the process will terminate.

    my $str = $cgi->param($key);
    return '' if not defined $str;  # If there is no data with this name, returns an empty string.

    $str  = &Encode::decode('utf8', $str);
    $str =~ s/(\x0D\x0A|\x0D|\x0A)/\n/g;  # Absorbs differences in line feed codes

    # $str = &inequ_escape($str);
    # $str = &quote_escape($str);
    
    $str = $cgi->escapeHTML($str);

    return $str;
}


######################################
#  Disabling HTML tags

sub html_escape
{
    my $str = shift @_;

    $str =~ s/</&lt;/g;    # The inequality sign is &....
    $str =~ s/>/&gt;/g;

=comment
    $str =~ s/&lt;i&gt;/<i>/ig;  # The inequality signs around valid tags are back.
    $str =~ s/&lt;\/i&gt;/<\/i>/ig;

    $str =~ s/&lt;sub&gt;/<sub>/ig;
    $str =~ s/&lt;\/sub&gt;/<\/sub>/ig;

    $str =~ s/&lt;sup&gt;/<sup>/ig;
    $str =~ s/&lt;\/sup&gt;/<\/sup>/ig;
=cut

    return $str;
}


#######################################
# Escaping quotes

sub quote_escape
{
    my $str = shift @_;
    $str =~ s/\"/&#34;/g;
    return $str;
}

sub quote_restore
{
    my $str = shift @_;
    $str =~ s/&#34;/\"/g;
    return $str;
}

#######################################
# Escaping inequality quotes

sub inequ_escape
{
    my $str = shift @_;
    $str =~ s/</&lt;/g;
    $str =~ s/>/&gt;/g;
    return $str;
}

sub inequ_restore
{
    my $str = shift @_;
    $str =~ s/&lt;/</g;
    $str =~ s/&gt;/>/g;
    return $str;
}


#####################################
# Escape encoding when writing to a file


#####################################
#Gets the date and time (the number of seconds since January 1, 1970, Greenwich Mean Time, 0:00:00).

sub get_day_date_time 
{
	my $day = $t->strftime('%Y/%m/%d');
	my $date = $t->strftime('%Y/%m/%d %H:%M:%S');
	my $time = time;
	return ($day, $date, $time);
}

#####################################
#  Creates and returns an HTML::Template object.

sub load_html_tmpl
{
    my $tmpl_file = shift @_;

    my $code = 'utf8';

    my $template_path = &Info::get_template_path();

    open (my $fh, ('<:' . $code), ($template_path . $tmpl_file) )
                   || die ("Failed to open $template_path$tmpl_file");
                   
    my $tmpl = HTML::Template->new( filehandle => $fh );
    close $fh;

    return $tmpl;
}


######################################
# 

sub write_login_log
{
	my $user = shift @_;
	my $login = shift @_; #login or dlogin
	my ($day, $date, $time) = &get_day_date_time;
	my $login_log_file;
	
	my $file = &Info::get_all_user_file_path;
    open (my $fh, "<", $file) || die ("Failed to open user info file");
    my ($id, $group, $name, $pw_md5);

    my $record = <$fh>;
    while ($record = <$fh>) {
        $record = &Encode::decode($Data_Charset, $record);
        $record =~ s/[\r\n]+\z//;

        ($id, $group, $name, $pw_md5) = split(/\t/, $record);
        if ($name eq $user) {
            last;
        }
    }
    close ($fh);
	
	if ($login eq "login"){
		$login_log_file = &Info::get_login_log_path; 
    }
    else{ #dlogin
    	$login_log_file = &Info::get_d_login_log_path;
    }
    open (FILE, ">>", $login_log_file) or die "Failed to open $login_log_file\n";
    
    print FILE &Encode::encode('utf-8', "$date\t$time\t$ENV{REMOTE_ADDR}\t$ENV{HTTP_USER_AGENT}\t$id\t$group\t$user\n");   # Write date, IP, username to file
    close (FILE); 
}
1;
