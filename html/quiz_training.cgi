#!/usr/bin/perl --
#!c:/perl64/bin/perl.exe


#  TORI-TORE quiz training program
#  
#  2020-06-18  by TAKENAKA, Akio
#  rev 2020-06-20  by TAKENAKA, Akio
#  rev 2020-06-28  by TAKENAKA, Akio
#  rev 2020-07-07  by OGAWA, Yui
#  


use lib qw(pm .);

use CGI;

use strict;
use utf8;

use CGI::Carp( 'fatalsToBrowser' );
use HTML::Template;
use Time::Piece;

use Par;
use Util;
use Quiz;

my $q = CGI->new;
#$q->charset( 'UTF-8' );

# If you came to this page without logging in
unless ($q->param( 'user' )){  # No user name → Not logged in
	# Display message and exit
	my $tmpl = &Util::load_html_tmpl('not_logged_in_message.tmpl' );
	print $q->header;
	print &Encode::encode('utf-8', $tmpl->output);
	exit; # Terminate all programs
}

my $tmpl = &Util::load_html_tmpl('quiz_training.tmpl' );

my $user = &Util::form_str_utf8($q, 'user');

my $login = 1;
if ($user =~ /^[0-9]+$/){ # If it's only numbers, it's guest
	$login = 0;
}
$tmpl->param( login => "$login" );



# Previously quizzed species. If none, empty string.
my $prev_sp = &Util::form_str_utf8($q, 'sp_roman');  
my $prev_mp3_path_name = &Util::form_str_utf8($q, 'mp3_file_path_name'); 
my $prev_mp3 = &Quiz::get_mp3_file_base_name($prev_mp3_path_name);
my $prev_correct_answer = &Util::form_str_utf8($q, 'correct_answer');
my $prev_users_answer = &Util::form_str_utf8($q, 'users_answer');

if ($q->param('dialogue')){ # Write if receive a frequency response
	my $dialogue = &Util::form_str_utf8($q, "dialogue" );
	&Quiz::write_fix($user, $prev_sp, $dialogue); # Write a frequency
}



# Data for each species
# keys are romanized names of species, values are hash references
# Structure of nested hashes
#   {PRIORITY} learning priority (lower value means higher priority)
#   {SP_JP}  Japanese name (katakana)
#  {URL1} URL of Saezuri-Navi
#  {URL2} URL of BIRD FAN
#  {LICENSE} License of the image
#  {MP3} Reference of the hash that puts away the sound source data
#  Structure of the sound source data hash
#   The key is the mp3 filename
#   The value is a proficiency score
#  {SCORE} Proficiency level as a species. Minimum sound source proficiency level.

my $data_set = {};


&Quiz::load_bird_info($data_set);

# dictionary of jp(katakana) to roman species name
# Also referenced from within subroutines
my $JP_TO_ROMAN_DICT = &Quiz::make_jp_to_roman_dictionary($data_set);

# Read sound source information
# Return value is the number of times the sound source and the number of correct answers, initially 0
# $counts->{MP3}->{}, $counts->{MP3}->{}
my ($counts, $corrects) = &Quiz::load_mp3_info($data_set);

# Find the proficiency score from the response log and store it in the $data_set.
# Get the number of past responses by return value.
($counts, $corrects) = &Quiz::load_past_achievement($data_set, $user, $counts, $corrects);



#$tmpl->param( group => "$group" );
$tmpl->param( user => "$user" );



# Set the number of responses information to the template
&Quiz::set_counts_to_template($tmpl, $counts);


my $mp3_for_quiz;        
my @false_choices = ();  # Array of incorrect answer choices (species name)



while (1) {  # Repeat until the algorithm finds a species that is different from the last question.
	$mp3_for_quiz = &select_mp3_for_quiz_dialogue_frequency($data_set);
       last if ((&get_sp_for_mp3($mp3_for_quiz) ne $prev_sp) && $mp3_for_quiz ne ""); 		
}


# Incorrect answer options are randomly selected
@false_choices = &select_false_choices_random($data_set, $mp3_for_quiz); 

### Output
&set_quiz_to_template($tmpl, $data_set, $mp3_for_quiz, \@false_choices);

$q->charset( 'UTF-8' );
print "Set-Cookie: NAME = cookie; Secure; HttpOnly\n";
print $q->header;
print &Encode::encode('utf-8', $tmpl->output);

########## subroutine for submitting a question（Frequency-adjustment & interactive algorithm） ##########

#############
# Decide on the sound source for the questions

sub select_mp3_for_quiz_dialogue_frequency
{
    my $data_set = shift @_;
    my $quiz = &will_make_buildup_reduced_quiz($data_set); 
    my @spp;
    
    if ($quiz eq "buildup") { 
    	my $n_buildup = &get_n_buildup($data_set);
    	die("No buildup sp") if ($n_buildup == 0);
    	@spp = &get_buildup_spp_list($data_set);
    }
    elsif ($quiz eq "reduced"){
    	my $n_reduced = &get_n_reduced($data_set);
    	die("No reduced sp") if ($n_reduced == 0);
    	@spp = &get_reduced_spp_list($data_set);
    }
    elsif ($quiz eq "learning"){ 
        my $n_learning = &get_n_learning($data_set);
    	die("No learning sp") if ($n_learning == 0);
        @spp = &get_medium_score_spp_list($data_set);
    }
    else{ 
    	die ("No quiz mode");
    }
	
	unless (@spp){ 
    	die ("No spp");
    }
	my $mean_sum; # The sum of the average number of optimal questions
    my $i = 0;
    
    foreach my $sp (@spp){
    	$i++;
    	if ($i == 1){
    		$data_set->{$sp}->{THRESHOLD} = 0;
    	}
    	else{
    		$data_set->{$sp}->{THRESHOLD} = $mean_sum;
    		
    	}
    	$mean_sum += $data_set->{$sp}->{MEAN};
    	
    }
    
    my $r = rand $mean_sum;
    
	my $sp_for_quiz;
	
	foreach my $sp (sort {$data_set->{$b}->{THRESHOLD} 
							<=> $data_set->{$a}->{THRESHOLD}} @spp){ # Highest threshold value first
		if ($r >= $data_set->{$sp}->{THRESHOLD}){ # If it is higher than the threshold
			$sp_for_quiz = $sp;
			last; # Quiz that species
		}
	}
	unless ($sp_for_quiz){
		die ("No sp_for_quiz");
	}
	my $flag = 0;
	foreach my $sp (keys %$data_set){
		if ($sp eq $sp_for_quiz){
			$flag = 1;
		}
	}
	die ("No sp") if ($flag == 0);
	
	my $selected_mp3 = &select_mp3_random($data_set, $sp_for_quiz);
    
    return $selected_mp3;
}


########## Output-related subroutine ##########
#############
# Set the questions to HTML template

sub set_quiz_to_template
{
    my $tmpl = shift @_;
    my $data_set = shift @_;
    my $target = shift @_;
    my $false_choices_ref = shift @_;
    
    my $sp_roman = &get_sp_for_mp3($target);
    $tmpl->param( sp_roman => $sp_roman);
    
    my $sp_jp = &get_sp_jp_name($data_set, $sp_roman);
    $tmpl->param( correct_answer => $sp_jp );
    $tmpl->param( answer_license => "$data_set->{$sp_roman}{LICENSE}" );
    	
	my $mp3_file_base_name = &Quiz::get_mp3_file_base_name($target);
	my $mp3_file_path_name = &Quiz::get_mp3_file_path_name($target);
	$tmpl->param( spectrogram => "$mp3_file_base_name".".mp3" );
	$tmpl->param( mp3_file_path_name => $mp3_file_path_name );
	$tmpl->param( mp3_file_base_name => $mp3_file_base_name );

	# Send proficiency level
	$tmpl->param( mp3_score => "$data_set->{$sp_roman}{MP3}{$target}->{SCORE}" ); 
	
	#my @spp_to_be_learned = &get_high_score_spp_list($data_set,
    #                                    $Par::QUALIFIED_SCORE);
    
    #my $one_sp_until_all_learned = 0;
	#if (@spp_to_be_learned == 1){
	#	$one_sp_until_all_learned = 1;
	#}	
	#$tmpl->param( one_sp_until_all_learned => "$one_sp_until_all_learned" );
	
	my @spp = (@$false_choices_ref, $sp_roman);
	my @shuffled_spp = ();
    while (@spp) {   # Cut out randomly selected elements and add them to @shuffled_spp
        # until @spp is empty
        push @shuffled_spp, splice(@spp, rand(@spp), 1);
    }
    
    my @choices_jp_forms = &get_choices_jp_forms($data_set, \@shuffled_spp);
     
    # choices form
    $tmpl->param( choices_jp_forms => "@choices_jp_forms" );
	
	# choices (roman letter)
	$tmpl->param( choices => "@shuffled_spp" ); 
	
	# roman letter to Japanese
    foreach (@shuffled_spp){
    	$_ = &get_sp_jp_name($data_set, $_)
    }
    $tmpl->param( choices_jp => "@shuffled_spp" );    

}


###############################
# From the choices, get the choice form on the screen and the mp3 list for playback on the answer screen

sub get_choices_jp_forms
{
	my $data_set = shift @_;
	my $choices_ref = shift @_;
	my (@choices_mp3, @parts, $combi, @choices_jp);

	# Display choices in form using i
	my @choices_forms;
	
	# Change $choices_ref to Japanese name
	foreach my $sp (@$choices_ref){
		push @choices_jp, &get_sp_jp_name($data_set, $sp);
	}
	
	for (my $i = 0; $i < $Par::N_CHOICES; $i++){ 
	    push @choices_forms, 
	    	'<tr><td><input type="radio" name="users_answer" value="'
	    	.$choices_jp[$i].'" id="r'.$i.'" required>'.
	    	'<label for="r'.$i.'">'.$choices_jp[$i].'</label></td><tr>';
	    	#"<tr><td><input type='radio' name='users_answer' value=".
	    	#"$choices_jp[$i]"." id="."r"."$i"." required>".
	    	#"<label for="."r"."$i".">".$choices_jp[$i]."</label></td><tr>";
	    	#'<tr><td><input type="radio" name="users_answer" value="'.$choices_jp[$i].'" id="r'.$i.'" required>'.'<label for="r'.$i.'">'.$choices_jp[$i].'</label></td><tr>';
	}

	return @choices_forms;
}


########## Subroutines related to the creation and alignment of species lists ##########

#############
# Returns a list excluding the specified mp3 file species from the all species list
# Call from get_level_X_false_choices 

sub get_spp_without_sp_for_given_mp3
{
    my $data_set = shift @_;
    my $mp3 = shift @_;

    # Species of designated sound source
    my $sp_of_mp3 = &get_sp_for_mp3($mp3);
    
    my @spp = ();
    
    foreach my $sp (keys(%$data_set)) {
        next if $sp eq $sp_of_mp3; # Exclude species of designated sound source
        push @spp, $sp;
    }

    return @spp;
}


#############
# Return a given group of species sorted from highest to lowest proficiency score.
# Order is random in case of ties.

sub sort_spp_by_score
{
    my $data_set = shift @_;
    my @spp = @_;

    # Shuffle
    my @shuffled_spp = ();
    while (@spp) {   # Cut out randomly selected elements and add them to @shuffled_spp
        # until @spp is empty
        push @shuffled_spp, splice(@spp, rand(@spp), 1);
    }
    
    # Sort in descending order
    my @sorted_spp = sort {$data_set->{$b}->{SCORE} <=> $data_set->{$a}->{SCORE} } 
                          @shuffled_spp;
    
    return @sorted_spp;
}


#############
# Return a list of species that responded that they will be reduced.

sub get_reduced_spp_list
{
    my $data_set = shift @_;

    my @reduced_score_spp;

    my @spp = keys %$data_set;

    foreach my $sp (@spp) {
        if ($data_set->{$sp}->{FIX} == -1) {
            push @reduced_score_spp, $sp;
        }
    }
    unless (@spp){
    	die ("No reduced spp");
    }
    return @reduced_score_spp;
}

#############
# Returns a list of species to buildup

sub get_buildup_spp_list 
{
    my $data_set = shift @_;
    my @buildup_spp;

    my @spp = keys %$data_set;

    foreach my $sp (@spp) {
        if ($data_set->{$sp}->{FIX} == 1) {
            push @buildup_spp, $sp;
        }
    }
    
    unless (@spp){
    	die ("No buildup spp");
    }
    
    return @buildup_spp;
}


#############
# Returns a list of species with an initial frequency of occurrence.

sub get_medium_score_spp_list 
{
    my $data_set = shift @_;
    
    my @medium_score_spp;

    my @spp = keys %$data_set;

    foreach my $sp (@spp) {
        if ($data_set->{$sp}->{FIX} == 0) {
            push @medium_score_spp, $sp;
        }
    }
    
    unless (@spp){ 
    	die ("No learning spp");
    }
    
    return @medium_score_spp;
}


#############
# Return the given species groups (in Roman alphabet) sorted from the species 
# with the highest PRIORITY to the species with the lowest PRIORITY (in ascending order of PRIORITY value).

sub sort_spp_by_priority
{
    my $data_set = shift @_;
    my @spp = @_;
    
    # Ascending order of value, i.e. descending order of priority
    my @sorted = sort {$data_set->{$a}->{PRIORITY} <=> $data_set->{$b}->{PRIORITY}} @spp;

    return @sorted;
}


########## Props subroutine ##########

#############
# Returns the proficiency level of a given sound source

sub get_score_of_mp3
{
    my $data_set = shift @_;
    my $mp3_for_quiz  = shift @_;

    my $sp = &get_sp_for_mp3($mp3_for_quiz);
    my $score = $data_set->{$sp}->{MP3}->{$mp3_for_quiz}->{SCORE};

    return $score;
}


#############
#  Returns the sound source with the lowest proficiency score of the specified species.

sub get_min_score_mp3_for_sp
{
    my $data_set = shift @_;
    my $sp = shift @_;
    
    my $MP3_ref = $data_set->{$sp}->{MP3};
    my @mp3s = keys %{$MP3_ref};
    
    die("No mp3 for $sp") unless @mp3s; 
    
    # Arranged in ascending order of score. Lowest score at the top
    my @sorted = sort {$MP3_ref->{$a} <=> $MP3_ref->{$b}} @mp3s;
    
    return $sorted[0];
}


#############
# Get the species name (romanized) from the name of the mp3 file
# Subfolder name and extension may or may not be present

sub get_sp_for_mp3
{
    my $mp3 = shift @_;

    if ($mp3 =~ /([a-z]+)_.+_\d\d/) {
        return $1;
    }

    return "";  # Not matched
}



#############
# Return the katakana name corresponding to the roman name

sub get_sp_jp_name
{
    my $data_set = shift @_;
    my $sp_roman = shift @_;
    
    if ($data_set->{$sp_roman}) {
        return $data_set->{$sp_roman}->{SP_JP};
    }
    else {  # Returns an empty string if there is no corresponding species
        return "";
    }
}


#############
# Get number of learning species

sub get_n_learning
{
    my $data_set = shift @_;
    
    my $n_buildup = &get_n_buildup($data_set);
    my $n_reduced = &get_n_reduced($data_set);
    my $n_total = &Quiz::get_n_total($data_set);
    
    my $n_to_be_learned = $n_total - $n_buildup - $n_reduced;
    
    return $n_to_be_learned;

}

#############
# Get the number of reduced species

sub get_n_reduced
{
    my $data_set = shift @_;

    # Reduced species
    my @reduced_spp = &get_reduced_spp_list($data_set);
    
    return scalar(@reduced_spp);
}

#############
# Get the number of buildup species

sub get_n_buildup
{
    my $data_set = shift @_;

    my @buildup_spp = &get_buildup_spp_list($data_set);
    
    return scalar(@buildup_spp);
}


###############################
# Returns the number of questions remaining against the target based on the cumulative number of quizzes
sub get_num_quiz_left
{
	# Cumulative number of quizzes solved
	my $total = shift @_;
	
	# Remaining number of quiz trainig questions
	my $num_quiz_left = $Par::N_QUIZZES_TO_GOAL - $total; 

	return $num_quiz_left;
}



###############################
sub select_sp_random
{
	my @spp_pool = shift @_;
	return $spp_pool[rand(@spp_pool)];
}

###############################

sub select_mp3_random
{
    my $data_set = shift @_;
    my $sp = shift @_;
    
    my @mp3s;
    foreach my $mp3 (keys %{$data_set->{$sp}->{MP3}}) {
        push @mp3s, $mp3;
    }
    return $mp3s[rand(@mp3s)];
}
