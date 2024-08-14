#   Packages that handle quiz training relations (including arrival quiz)
#  
#  2020-07-07  by OGAWA, Yui
#

package Quiz;

use Exporter;


use Encode;
use HTML::Template;
use Time::Piece;

use Info;
use Util;
use Par;


@ISA = qw(Exporter);

@EXPORT = qw(

judge_group
load_bird_info
load_mp3_info
load_past_achievement
set_sp_score
set_dialogue_to_template
set_counts_to_template
set_choices_form_to_template
write_fix
write_data
write_start_time
get_n_question_and_answer_lists
get_n_question_and_correct_for_test
judge_dialogue
get_sp_for_mp3
get_sp_jp_name
get_song_type_num_for_mp3
get_mp3_file_path_name
get_mp3_file_base_name
get_n_total
get_num_test
get_n_solved
get_num_quiz_left
get_num_quiz_left_today
get_goal_achieved
get_goal_achieved_today
make_jp_to_roman_dictionary

);

use strict;
use utf8;

my $Data_Charset = 'utf-8';


my $data_set = {};


&load_bird_info($data_set);

# dictionary of jp(katakana) to roman species name
# Also referenced from within subroutines
my $JP_TO_ROMAN_DICT = &make_jp_to_roman_dictionary($data_set);


########## Subroutine for reading files ##########

# Judge group from username
sub judge_group 
{
	my $user = shift @_;
	my $user_file = &Info::get_all_user_file_path;
	open (FILE, "<", $user_file) or die "Failed to open $user_file\n"; 
	
	my ($id, $group, $u, $pw);

	my $line = <FILE>;      
	
	while ($line = <FILE>) {

    	$line = &Encode::decode($Data_Charset, $line);
    	$line =~ s/(\x0D\x0A|\x0D|\x0A)/\n/g;  
    	chomp $line;
    	($id, $group, $u, $pw) = split /\t+/, $line; 
    	
    	if ($u eq $user){
    		last; # The relevant user ID is stored in $id
    	}
	}
	close (FILE);
	
	
	my $group = 0;  
	
	if ($id % 4 == 1){ # interactive
		$group = 1;
	}
	elsif ($id % 4 == 2){ # frequency-adjustment
		$group = 2;
	}
	elsif ($id % 4 == 3){ # frequency-adjustment & interactive
		$group = 3;
	}
	
	return $group;
}

#############

sub load_bird_info
{
    my $data_set = shift @_;

    my $file_name = &Info::get_all_bird_info_file_path;
    open (my $fh, "<", $file_name) || die ("Failed to open $file_name");

    my $record = <$fh>; 

    while ($record = <$fh>) {

        $record = &Encode::decode('utf8', $record);
        $record =~ s/[\r\n]+\z//;
        my @data = split(/\t/, $record);

        my $to_be_loaded = $data[6];
        unless ($to_be_loaded) { # Skip data for species that do not appear in the question.
            next;
        }

        my $sp_roman = $data[2];  # Roman name

        # Hereafter, the romanized name is used as the primary key to designate the species.

        $data_set->{$sp_roman} = {};

        # Priority of questions (the smaller the value, the more priority is given to learning)
        $data_set->{$sp_roman}->{PRIORITY} = $data[0]; 

        $data_set->{$sp_roman}->{SP_JP} = $data[1];
        $data_set->{$sp_roman}->{URL1} = $data[3];
        $data_set->{$sp_roman}->{URL2} = $data[4];
        $data_set->{$sp_roman}->{LICENSE} = $data[5];
        $data_set->{$sp_roman}->{MEAN} = $data[7]; 
        $data_set->{$sp_roman}->{POINT} = $data[8]; 
        $data_set->{$sp_roman}->{FIX} = 0; 
        
        $data_set->{$sp_roman}->{MP3} = {}; # Insert sound data later.
    }
    close ($fh);
    
    
    return;
}


#############
# The return value is the initial value of the number of questions and the number of correct answers for the sound source.

sub load_mp3_info
{
    my $data_set = shift @_;
    my $count = {};
    my $correct = {};

    my $file_name = &Info::get_all_mp3_info_file_path;
    open (my $fh, "<", $file_name) || die ("Failed to open $file_name");

    my $record = <$fh>;

    while ($record = <$fh>) {

        $record = &Encode::decode('utf8', $record);
        $record =~ s/[\r\n]+\z//;
        my @data = split(/\t/, $record);
        
        my $to_be_loaded = $data[3];
        unless ($to_be_loaded) { #  Skip data for species that do not appear in the question.
            next;
        }
        my $mp3 = $data[1];
        my $sp = &get_sp_for_mp3($mp3);
        my $mp3_license = $data[2];

        $data_set->{$sp}->{MP3}->{$mp3}->{SCORE} = 0;  # Initial value of proficiency
        $data_set->{$sp}->{MP3}->{$mp3}->{LICENSE} = $mp3_license;  # License of mp3
        $count->{MP3}->{$mp3} = 0;  # Initial value of  number of questioned
        $correct->{MP3}->{$mp3} = 0;  # Initial value of number of corrected

    }
	
    close ($fh);
    
    return ($count, $correct);
}


#############
# Read the answer log file and get the score so far for each sound source for the user in question.
# The return value is a hash reference that records the number of responses and correct answers so far.

sub load_past_achievement
{
    my $data_set = shift @_;
    my $user = shift @_;
    my $count = shift @_;
    my $correct = shift @_;    
	
    my $t = localtime;
    my $today = $t->strftime('%Y/%m/%d');
    
    my %sp_latest_time; # The latest timing asked about the frequency of species

    my $file_name = "../data/responses/fix_responses.txt";
    open (my $fh, "<", $file_name) || die ("Failed to open $file_name");

    my $record = <$fh>;

    while ($record = <$fh>) {

        $record = &Encode::decode('utf8', $record);
        $record =~ s/[\r\n]+\z//;
        my @data = split(/\t/, $record);
        
        my $who = $data[6];
        next unless($who eq $user); # naive user
        
        my $sp = $data[7];
        
        $sp_latest_time{$sp} = $data[1]; # The date and time of the species are being overwritten.
        $data_set->{$sp}->{CORRECT} = $data[9]; # Overwrite sp and the correct or incorrect (1or-1) at that time
        
        if (($data_set->{$sp}->{FIX} != 0) &&($data_set->{$sp}->{FIX} == $data[8])){
        	$data_set->{$sp}->{FIX} = $data[8];
        }
        else{	
        	$data_set->{$sp}->{FIX} += $data[8]; #Add frequency
        }
    }
    close ($fh);
    
    
    $file_name = &Info::get_all_quiz_responses_file_path;
    open (my $fh, "<", $file_name) || die ("Failed to open $file_name");

    $count->{TODAY} = 0;
    $count->{TOTAL} = 0;
    
    $correct->{TODAY} = 0;
    $correct->{TOTAL} = 0;
    
    
    $record = <$fh>;

    while ($record = <$fh>) {

        $record = &Encode::decode('utf8', $record);
        chomp $record;
        my @data = split(/\t/, $record);

        my $who = $data[6];
        next unless($who eq $user); # naive user

        $count->{TOTAL} += 1;

        my $date = $data[0];
        if ($date =~ m!$today!) {
            $count->{TODAY} += 1;
        }
        my $unix_time = $data[1];

        my $mp3 = $data[7];
        $count->{MP3}->{$mp3} += 1;
        my $sp = &get_sp_for_mp3($mp3);

        
        my $correct_answer = $data[8];
        my $users_answer = $data[9];

        if ($correct_answer eq $users_answer) { 
            
            $correct->{TOTAL} += 1;
            $correct->{MP3}->{$mp3} += 1;	
            
            if ($date =~ m!$today!) {
            	$correct->{TODAY} += 1;
        	}
        	# There is no upper limit.
            if ($data_set->{$sp}->{MP3}->{$mp3}->{SCORE} < 0) {
            	$data_set->{$sp}->{MP3}->{$mp3}->{SCORE} = 1; 
            }
            else{
            	$data_set->{$sp}->{MP3}->{$mp3}->{SCORE} += 1; 
            }
            
        }
        else {   
            if ($unix_time > $sp_latest_time{$sp} && $data_set->{$sp}->{FIX} == -1 
                && $data_set->{$sp}->{CORRECT} == 1){ # If the latest was "aquired"
            	$data_set->{$sp}->{INCORRECT} += 1;
            }
            
            # Increase the number of consecutive incorrect answers to the sound source
            if ($data_set->{$sp}->{MP3}->{$mp3}->{SCORE} > 0) { # Score is over 0
                $data_set->{$sp}->{MP3}->{$mp3}->{SCORE} = -1; 
            }  
            else{ 
                $data_set->{$sp}->{MP3}->{$mp3}->{SCORE} -= 1; 
            }

            # Increase the number of consecutive incorrect answers for each sound source of a misselected species.
            my $wrong_answer = $JP_TO_ROMAN_DICT->{$users_answer};
            my @mp3s_wrong = keys %{$data_set->{$wrong_answer}->{MP3}};

            foreach my $mp3_wrong (@mp3s_wrong) {
                if ($data_set->{$wrong_answer}->{MP3}->{$mp3_wrong}->{SCORE} > 0) {
                    $data_set->{$wrong_answer}->{MP3}->{$mp3_wrong}->{SCORE} = -1; 
                } 
                else{
                    $data_set->{$wrong_answer}->{MP3}->{$mp3_wrong}->{SCORE} -= 1;
                } 
                
                if ($unix_time > $sp_latest_time{$wrong_answer} && $data_set->{$wrong_answer}->{FIX} == -1 
                    && $data_set->{$wrong_answer}->{CORRECT} == 1){ # If the latest was "aquired"
            		$data_set->{$wrong_answer}->{INCORRECT} += 1;
            	}
            }
        }
    }

    close ($fh);
    
    # Find the proficiency level for each species (the lowest score of proficiency for the sound source)
    &set_sp_score($data_set);     
    
    
    return ($count, $correct);
}


#############
# Determine the proficiency level for each species and record it in the $data_set.
# Call from load_past_achievement

sub set_sp_score
{
    my $data_set = shift @_;

    my @spp = keys %$data_set;

    foreach my $sp (@spp) {
        my $min_mp3_score = $Par::MAX_SCORE;

        my @mp3s = keys %{$data_set->{$sp}->{MP3}};

        foreach my $mp3 (@mp3s) { # Find the minimum score for each sound source
            my $score = $data_set->{$sp}->{MP3}->{$mp3}->{SCORE};
            if ($score < $min_mp3_score) {
                $min_mp3_score = $score;
            }
        }
        $data_set->{$sp}->{SCORE} = $min_mp3_score;
    }
}


########## Output-related subroutine ##########

#############
# Set the a frequency question in the HTML template
sub set_dialogue_to_template
{
    my $tmpl = shift @_;
    my $song_type_num = shift @_;
    my $judge = shift @_;
    my $num = shift @_;
    my $num_incorrect = shift @_;
    
    if ($num < 0){
    	$num = abs($num);
    }
    
    # <1/0/-1>\t<correct 1 /incorrect -1> from current frequency
    if ($judge == 1){ # Correct & frequency is not -1
        $tmpl->param( dialogue => "<p class='font75'><font color='green'>$song_type_num　$num"."回連続正解!!</font><br>出題頻度を減らしますか？<br>
        	                           <label><input type='radio' name='dialogue' value='-1\t1' required>減らす(マスターした)</label>　
        	                           <label><input type='radio' name='dialogue' value='0\t1' required>減らさない(マスターしていない)</label>　</p>" );
    }
    elsif ($judge == 5){ # Correct & frequency -1 & 3 previous incorrect answers in a row (After reducing it by an incorrect answer, the user got it right four times in a row.)
    	$tmpl->param( dialogue => "<p class='font75'><font color='green'>$song_type_num　$num"."回連続正解!!</font><br>出題頻度を…<br>
        	                           <label><input type='radio' name='dialogue' value='0\t1' required>減らしたままにする（マスターした）</label><br>
        	                           <label><input type='radio' name='dialogue' value='1\t1' required>増やす（マスターしていない）</label>　</p>" );
    }
    elsif ($judge == 2){ #Incorrect & frequency is 0
        $tmpl->param( dialogue => "<p class='font75'><font color='orange'>$song_type_num　$num"."回連続不正解　</font><br>出題頻度を減らしますか？<br>
    	                           <label><input type='radio' name='dialogue' value='-1\t-1' required>減らす</label>　
        	                       <label><input type='radio' name='dialogue' value='0\t-1' required>減らさない</label>　
        	                       <label><input type='radio' name='dialogue' value='1\t-1' required>増やす</label>　</p>");
    }
    elsif ($judge == 3){#Incorrect & frequency is 1
    	$tmpl->param( dialogue => "<p class='font75'><font color='orange'>$song_type_num　$num"."回連続不正解　</font><br>出題頻度を減らしますか？<br>
    	                           <label><input type='radio' name='dialogue' value='-1\t-1' required>減らす</label>　
        	                       <label><input type='radio' name='dialogue' value='0\t-1' required>減らさない</label>　</p>");
    }
    elsif ($judge == 4){#Incorrect & frequency is -1
    	$tmpl->param( dialogue => "<p class='font75'><font color='orange'>$song_type_num　$num"."回連続不正解　</font><br>出題頻度を増やしますか？<br>
    	                           <label><input type='radio' name='dialogue' value='1\t-1' required>増やす</label>　
        	                       <label><input type='radio' name='dialogue' value='0\t-1' required>増やさない</label>　</p>");
    }
    elsif ($judge == 6){ # Incorrect & more than 2 incorrect after aquired
    	$tmpl->param( dialogue => "<p class='font75'>マスターした後<font color='orange'>$song_type_num　$num_incorrect"."回不正解　</font><br>出題頻度を増やしますか？<br>
    	                           <label><input type='radio' name='dialogue' value='1\t-1' required>増やす</label>　
        	                       <label><input type='radio' name='dialogue' value='0\t-1' required>増やさない</label>　</p>");
    }
    
}

#############
# Set past number of responses information into HTML template
# $counts->{TODAY}, $counts->{TOTAL}を参照して。

sub set_counts_to_template
{
    my $tmpl = shift @_;
    my $counts= shift @_;

    $tmpl->param(num_quiz_solved_today => $counts->{TODAY});
    $tmpl->param(num_quiz_solved_allday => $counts->{TOTAL});
    
	# Number of questions remaining against goal 
	my $num_quiz_left = &get_num_quiz_left($counts->{TOTAL});
	my $num_quiz_left_today = &get_num_quiz_left_today($counts->{TOTAL});
	#$tmpl->param( num_quiz_left_today => $num_quiz_left_today );

	# Goal achieved or not
	my $goal_achieved_today = &get_goal_achieved_today($num_quiz_left_today);
	#$tmpl->param( goal_achieved_today => $goal_achieved_today );
}


#############
# Set the form of the choices (all species) to the template
# Only for arrival quiz
sub set_choices_form_to_template
{
	my $data_set = shift @_;
	my $tmpl = shift @_;
	
	my @choices_jp; #choices (all species)
	
	# Store choices (Japanese) in array
	foreach my $sp (keys %{$data_set}){
		push @choices_jp, $data_set->{$sp}->{SP_JP};
	}

	# In alphabetical order
	@choices_jp = sort @choices_jp;

	### Choice Fitting ###
	# Display choices in form using i
	my @choices_jp_form;

	# number of total species
	my $n_total_spp = &get_n_total($data_set);

	for (my $i = 0; $i < "$n_total_spp"; $i++){ 
	    # Inserting form parts into elements
	    push @choices_jp_form, '<li><input type="radio" name="users_answer" value="'
	                            .$choices_jp[$i].'" id="r'.$i.'" required>'.
	                            '<label for="r'.$i.'">'.$choices_jp[$i].'</label></li>'; 
	}

	# Add "I don't know."
	push @choices_jp_form, '<li><input type="radio" name="users_answer" value="'."わからない".
	                       '" id="r'."$n_total_spp+1".'" required>'.'<label for="r'.
	                       "$n_total_spp+1".'">'."わからない".'</label></li>';

	$tmpl->param( choices_jp_form => "@choices_jp_form" );
}


########## File read/write subroutine ##########

#############
# 
sub write_fix
{
	my ($day, $date, $time) = &Util::get_day_date_time;
	my $user = shift @_;
	my $sp = shift @_;
	my $response = shift @_;
	
	
	# Last response data for that user
	my $prev_data = 0; 
	
	my $file = &Info::get_all_fix_responses_file_path;
	
	
	open (FILE, "<", $file) or die "Failed to open $file:$!\n";
	my $line = <FILE>;       

	while ($line = <FILE>) {
    
    	$line = &Encode::decode($Data_Charset, $line);
    	chomp $line;
		my @data = split /\t+/, $line;
    	my ($date, $time, $ip, $os, $id, $group, $u, $sp, $fix1, $fix2) = split /\t+/, $line;
		
		if ($u eq $user){
			
			# Discard two date data relations
			shift @data; 
			shift @data;
			
			# The last data in the file
			$prev_data = join "\t", @data;
			
		}
		
	}
	
	my $user_file = &Info::get_all_user_file_path;
	open (FILE, "<", $user_file) or die "Failed to open $user_file\n"; 
	
	my ($id, $group, $u, $pw);

	my $line = <FILE>;       
	
	while ($line = <FILE>) {

    	$line = &Encode::decode($Data_Charset, $line);
    	$line =~ s/(\x0D\x0A|\x0D|\x0A)/\n/g;  
    	chomp $line;
    	my @data = split /\t+/, $line; 
    	($id, $group, $u, $pw) = split /\t+/, $line; 
    	
    	if ($u eq $user){
    		last; # The ID of the corresponding user is stored in $id
    	}
	}
	close (FILE);
	
	# Data for this question
	my $data = "$ENV{REMOTE_ADDR}\t$ENV{HTTP_USER_AGENT}\t$id\t$group\t$user\t$sp\t$response";
	
	open (FILE, ">>", $file) or die "Failed to open $file\n";
	
	# Compare with the last data of that user and
	# not be written at the exact same time (e.g., at page refresh)
	if ($prev_data ne $data){ 
		print FILE &Encode::encode('utf-8', "$date\t$time\t$data\n");
	}
	
	close (FILE);
}


#############
# Write data to the text file specified by the argument.
# Prevent duplicate writes by pressing the update button or the back button

sub write_data
{
	my ($day, $date, $time) = &Util::get_day_date_time; 
	my $responses_file = shift @_;
	my $user = shift @_;
	my $mp3 = shift @_;
	my $correct_answer = shift @_;
	my $users_answer = shift @_;
	my $choices_jp = shift @_;
	
	# Last response data for that user
	my $prev_data = 0; 
	
	# Stores all answers for that user
	my @correct_answers;
	
	open (FILE, "<", $responses_file) or die "Failed to open $responses_file:$!\n";
	my $line = <FILE>;

	while ($line = <FILE>) {
    
    	$line = &Encode::decode($Data_Charset, $line);
    	chomp $line;
		my @data = split /\t+/, $line;
    	my $u = $data[6];
		
		if ($u eq $user){
			
			push @correct_answers, $data[8];
			
			# Discard two date data relations
			shift @data; 
			shift @data;
			
			# The last data in the file
			$prev_data = join "\t", @data;
			
		}
		
	}
	
	my $user_file = &Info::get_all_user_file_path;
	open (FILE, "<", $user_file) or die "Failed to open $user_file\n"; 
	
	my ($id, $group, $u, $pw);

	my $line = <FILE>;
	
	while ($line = <FILE>) {

    	$line = &Encode::decode($Data_Charset, $line);
    	$line =~ s/(\x0D\x0A|\x0D|\x0A)/\n/g;  
    	chomp $line;
    	($id, $group, $u, $pw) = split /\t+/, $line; 
    	
    	if ($u eq $user){
    		last; # The ID of the corresponding user is stored in $id
    	}
	}
	close (FILE);
	
	# Data for this question
	my $data = "$ENV{REMOTE_ADDR}\t$ENV{HTTP_USER_AGENT}\t$id\t$group\t$user\t$mp3\t$correct_answer\t$users_answer\t$choices_jp";
	
	if ($responses_file =~ m!test!){ # For arrival quiz data, do not fill in choices
		$data = "$ENV{REMOTE_ADDR}\t$ENV{HTTP_USER_AGENT}\t$id\t$group\t$user\t$mp3\t$correct_answer\t$users_answer";
	}
	
	
	open (FILE, ">>", $responses_file) or die "Failed to open $responses_file\n";
	
	# Compare with the last data of that user and
	# not be written at the exact same time (e.g., at page refresh)
	if ($prev_data ne $data){ 
		
		print FILE &Encode::encode('utf-8', "$date\t$time\t$data\n");
	}

	close (FILE);
}

#############
# Retrieve the number of questions for the test and answer list
# Return value is the number of questions, mp3 and answer list reference
sub get_n_question_and_answer_lists
{
	my $choices_answer_file = shift @_;
	my $test_responses = shift @_;
	my $user = shift @_;
	my $n = 0; #Count the number of arrival quiz answer
	my (%test_data, @test_mp3s, @tested_mp3s, $n_question);
	
	open (FILE, "<", $choices_answer_file) or die "Failed to open $choices_answer_file:$!\n"; 

	my $line = <FILE>;

	while ($line = <FILE>) {
    
    	$line = &Encode::decode($Data_Charset, $line);
    	$line =~ s/[\r\n]+\z//;
    	my @data = split /\t+/, $line;
    
    	my $to_be_loaded = $data[1];
    	unless ($to_be_loaded) {
        	next;
    	}
    
    	my $mp3 = $data[2];
    	my $mp3_str = &get_mp3_file_path_name($mp3);
    	$test_data{$mp3_str} = $data[3]; # key: mp3 with path, value: Japanese answer
    	push @test_mp3s, $mp3_str;
    	$n_question++; # Number of arrival quiz qurstions
    
	}
	
	close (FILE);
	
	
	open (FILE, "<", $test_responses) or die "Failed to open $test_responses:$!\n"; 
	my $line = <FILE>;  
	while ($line = <FILE>) {
	    $line = &Encode::decode('utf8', $line);
	    chomp $line;
	    my @data = split /\t+/, $line; 
	    my $u = $data[6];
	    my $mp3 = $data[7];
    	my $mp3_str = &get_mp3_file_path_name($mp3);
	    my $correct_answer = $data[8];
	    
	    
	    if ($u eq $user){
	    	$n++;
	    	push @tested_mp3s, $mp3_str;
	    }
	    if ($n % $n_question == 0){
	    	@tested_mp3s = (); # Reset
	    }
	}
	
	close (FILE);
	
	
	
	
	my $mp3_for_test; # Null
	
	while ($mp3_for_test eq ''){
		$mp3_for_test = $test_mp3s[rand(@test_mp3s)]; # Select mp3 on shuffle
		foreach my $tested_mp3 (@tested_mp3s){
			if ($mp3_for_test eq $tested_mp3){
				$mp3_for_test = '';
				last;
			}
		}
	}
	
	return ($n_question, $mp3_for_test, $test_data{$mp3_for_test});
	
}


#############
# Read the arrival quiz results record file to determine the number of questions and the number of correct answers by the user.
sub get_n_question_and_correct_for_test
{
	my $q = shift @_;
	my $user = shift @_;
	my $test_responses = shift @_;
	my $n_question = 0;
	my $n_correct = 0;
	
	open (FILE, "<", $test_responses) or die "Failed to open $test_responses:$!\n"; 

	my $line = <FILE>;       

	while ($line = <FILE>) {
    
    	$line = &Encode::decode('utf8', $line);
    	chomp $line;
    	my @data = split /\t+/, $line;    
    
    	my $u = $data[6];
    	my $correct_answer = $data[8];
    	my $users_answer = $data[9];
    
    	if ($u eq $user){
        	if ($correct_answer eq $users_answer) {
            	$n_correct++; 
        	}
        	$n_question++;
    	}
    
	}
	
	close (FILE);
	
	return ($n_question, $n_correct);
}

########## Props subroutine ##########

#############
#
sub judge_dialogue
{
	my $data_set = shift @_;
    my $mp3 = shift @_;
    my $correct_answer_roman = shift @_;
    my $correct_answer = shift @_;
    my $users_answer = shift @_;
    
    my $judge;
    
    if ($users_answer eq $correct_answer){        	
    	if ($data_set->{$correct_answer_roman}{MP3}{$mp3}->{SCORE} >= 4){
        	if ($data_set->{$correct_answer_roman}->{FIX} != -1){
        		$judge = 1;
        	}
        	elsif ($data_set->{$correct_answer_roman}->{CORRECT} == -1){
        		$judge = 5;
        	}
        }
        
    }
    else{ 
    	if ($data_set->{$correct_answer_roman}{MP3}{$mp3}->{SCORE} <= -3){
    		if ($data_set->{$correct_answer_roman}->{FIX} == 0){ # Initial value
    			$judge = 2;
    		}
    		elsif ($data_set->{$correct_answer_roman}->{FIX} == 1){
    			$judge = 3;
    		}
    		else{ #-1
    			$judge = 4;
        	}
        }
        elsif ($data_set->{$correct_answer_roman}->{INCORRECT} >= 2){ # if wrong anser at least twice after aquired it.
    		$judge = 6;
    	}
    }    
    return ($judge, $data_set->{$correct_answer_roman}{MP3}{$mp3}->{SCORE}, $data_set->{$correct_answer_roman}->{INCORRECT});
}


#############
 Get the species name (romanized) from the name of the mp3 file
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


#########
# Get call type and sound source number from the name of the mp3 file
# Subfolder name and extension may or may not be present

sub get_song_type_num_for_mp3
{
    my $data_set = shift @_;
    my $mp3 = shift @_;
    my $sp = &get_sp_for_mp3($mp3);
    my $sp_jp = &get_sp_jp_name($data_set, $sp);
    my $song_type_num_for_mp3;

    if ($mp3 =~ /_(.+)_(\d\d)/) {

        my $song_type = $1;
        my $num = $2;

        if ($song_type eq "song") {
            $song_type_num_for_mp3 = "$sp_jp"."_さえずり_$2";
        }
        elsif ($song_type eq "call") {
            $song_type_num_for_mp3 =  "$sp_jp"."_地鳴き_$2";
        }
        elsif ($song_type eq "wingbeat") {
            $song_type_num_for_mp3 =  "$sp_jp"."_幌打ち_$2";
        }
        
        return $song_type_num_for_mp3;
    }

    return "";  #  Not matched
}


#########
# Add subdirectory name and extension to the base name of the mp3 file
# If it already has these, do nothing.

sub get_mp3_file_path_name
{
    my $mp3_str = shift @_;
    
    # "^" means at the beginning, and "\" means escape sequence. Using them, check to see if there's an "mp3/" at the beginning.
    if ($mp3_str !~ /^mp3\//) { 
        $mp3_str = "mp3/" . $mp3_str;
    }
    if ($mp3_str !~ /\.mp3$/) {
        $mp3_str .= ".mp3";
    }

    return $mp3_str;
}


#########
# Return the base name of the mp3 file.
# Strip subdirectory names and extensions.
# If they are not attached, leave them as they are.

sub get_mp3_file_base_name
{
    my $mp3_str = shift @_;
    
    if ($mp3_str =~ /^mp3\/(.+)/) {
        $mp3_str = $1;
    }
    if ($mp3_str =~ /(.+)\.mp3$/) {
        $mp3_str = $1;
    }

    return $mp3_str;
}


#############
# Get the total number of species

sub get_n_total
{
    my $data_set = shift @_;

    my @spp = keys %$data_set;

    return scalar(@spp);
}


###############################
# Return the user's cumulative number of test responses
sub get_n_solved
{
	my $q = shift @_;
	my $user = shift @_;
	my $filename = shift @_;
	
	my $i = 0;
	
	open (FILE, "<", $filename) or die "Failed to open $filename:$!\n"; 
	
	my $line = <FILE>;  
	
	while ($line = <FILE>) {
		
		$line = &Encode::decode($Data_Charset, $line);
		chomp $line;
		
		my $u = (split /\t+/, $line)[6];
		if ($u eq $user){
			$i++;
		}
		
	}
	
	return $i;
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
# Returns the number of questions remaining against the target based on the cumulative number of quizzes until today
sub get_num_quiz_left_today
{
	my $today = localtime;
	$today = $today->strftime($Par::DATE_FORMAT);
	
	# Cumulative number of quizzes solved
	my $total = shift @_;
	
	# Remaining number of quiz trainig questions
	my $num_quiz_left_today;
	
	#if ($today eq "$Par::EXPERIMENT_2ND_DAY"){
		#$num_quiz_left_today = $Par::N_QUIZZES_PER_DAY - $total; 
	#}
	#elsif ($today eq "$Par::EXPERIMENT_3RD_DAY" || $today eq "$Par::EXPERIMENT_4TH_DAY"){
	#	$num_quiz_left_today = $Par::N_QUIZZES_TO_MTEST - $total;
	#}
	#elsif ($today eq "$Par::EXPERIMENT_5TH_DAY"){
	#	$num_quiz_left_today = $Par::N_QUIZZES_TO_MTEST + $Par::N_QUIZZES_PER_DAY - $total;
	#}
	#elsif ($today eq "$Par::EXPERIMENT_6TH_DAY" || $today eq "$Par::EXPERIMENT_7TH_DAY"){
		$num_quiz_left_today = $Par::N_QUIZZES_TO_GOAL - $total;
	#}	

	return $num_quiz_left_today;
}


###############################
# Returns whether the goal is achieved or not based on the number of questions remaining.
sub get_goal_achieved
{
	# Remaining number of quiz trainig questions
	my $num_quiz_left = shift @_; 
	my $goal_achieved = 0;

	if ($num_quiz_left <= 0){
		$goal_achieved = 1;
	}

	return $goal_achieved;
}


###############################
# Returns whether the goal is achieved or not based on the number of questions remaining.
sub get_goal_achieved_today
{
	# Remaining number of quiz trainig questions
	my $num_quiz_left_today = shift @_; 
	my $goal_achieved_today = 0;

	if ($num_quiz_left_today <= 0){
		$goal_achieved_today = 1;
	}

	return $goal_achieved_today;
}


#############
# Create a hash that converts Japanese names (katakana) to romanized names
# Return hash references

sub make_jp_to_roman_dictionary
{
    my $data_set = shift @_;

    my $jp_to_roman_dict = {};
    
    foreach my $sp_roman (keys %$data_set) {
        my $jp_name = $data_set->{$sp_roman}->{SP_JP};
        $jp_to_roman_dict->{$jp_name} = $sp_roman;
    }
    
    return $jp_to_roman_dict;
}
1;