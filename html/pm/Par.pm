# Parameter for TORI-TORE
#
#  2020-06-26  TAKENAKA, Akio
#  rev 2020-07-07  by OGAWA, Yui
#  update 2023-02-22 by OGAWA, Yui
#
package Par;

use utf8;
use strict;
use Info;
use Time::Piece;
use POSIX qw(strftime);

# Define package variables with "our". 
# From outside the scope (package), refer to it by its fully qualified name with "Par::".
# e.g.：   my $n = $Par::N_CHOICES;



our $SECONDS_OF_DAY = 86400; # Seconds in a day
our $SECONDS_OF_TIME_DIFFERENCE = 9*60*60; # Unix time and time in Japan are 9h * 60m * 60s apart.
our $DATE_FORMAT = '%Y-%m-%d';


our $FOCUS_SIZE = 26;  # The size of the species group to focus on

our $N_CHOICES = 5;    # Number of choices at the time of the question.
                       # $N_CHOICES minus 1 is the number of incorrect answer choices.

our $MAX_SCORE = 4;    # Max proficiency


# P: Frequency of generate questions from being mastered species
#  P = $MAX_REVIEW_PROB * ($REVIEW_WEIGHT * N) / (X + $REVIEW_WEIGHT * N)
#  X  Number of learning species
#  N  Number of aquired species

our $BUILDUP_WEIGHT = 3;  # Weight of one buildup species for one learning species
our $REDUCED_WEIGHT = 0.25;  # Weight of one reduced species for one learning species

our $MAX_BUILDUP_PROB = 1;
our $MAX_REDUCED_PROB = 1; # Maximum frequency of reduced species 
                           #  (no matter how many species are aquired, 
                           #   the total frequency of review of all of them will not exceed this value)


1;
