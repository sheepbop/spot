#!/usr/bin/perl

# control spotify via cgi and Applescript

use CGI qw/:standard *table/;

my $dim_amount = 30;
my $delta_volume = 10;

print header(
            -charset => 'UTF-8',
    ),
    start_html(
            -title => 'Spot',
            -head  => meta ({
                 -http_equiv => 'refresh',
                 -content    => '60;url=http://donkey.cissme.com:8080/cgi-bin/spotify.cgi',
            })
        ),
        p,
        img {src=>'/spotify-logo.png'},
        '<font size="6">Spotify Control</font>',
        hr,
        p,

        start_table,
            "<TR>",
                "<TD>", start_form, submit('action', 'play'), end_form, "</TD>",
                "<TD>", start_form, submit('action', 'pause'), end_form, "</TD>",
            "</TR>",
            "<TR>",
                "<TD>", start_form, submit('action', 'dim volume'), end_form, "</TD>",
                "<TD>", start_form, submit('action', 'undim'), end_form, "</TD>",
            "</TR>",
            "<TR>",
                "<TD>", start_form, submit('action', 'louder'), end_form, "</TD>",
                "<TD>", start_form, submit('action', 'quieter'), end_form, "</TD>",
            "</TR>",
            "<TR>",
                "<TD>", start_form, submit('action', 'next'), end_form, "</TD>",
                "<TD>", start_form, submit('action', 'previous'), end_form, "</TD>",
            "</TR>",
            "<TR>",
                "<TD>", start_form, submit('action', "what's playing"), end_form, "</TD>",
            "</TR>",
        end_table,

        hr;


if (param()) {
    if (param('action') =~ /play/) {
        play();
    } elsif (param('action') =~ /pause/ ) {
        pause();
    } elsif (param('action') =~ /previous/ ) {
        play_previous();
    } elsif (param('action') =~ /next/ ) {
        play_next();
    } elsif (param('action') =~ /^dim volume/ ) {
        dim_volume();
    } elsif (param('action') =~ /undim/ ) {
        undim_volume();
    } elsif (param('action') =~ /^louder$/ ) {
        increase_volume();
    } elsif (param('action') =~ /^quieter$/ ) {
        decrease_volume();
    };
    show_status();
} else {
    show_status();
}

sub show_status {
    print p, "Now ", get_state(), " - ", "<I>", get_track(), ,"</I>", " by ", "<I>", get_artist(), "</I>",
    p, "Volume: ", get_volume();
}

####

sub osascript {
    return unless (defined($_[0]));

    my $script = $_[0];

    $retval = (`/usr/bin/osascript -e '$script'`);
    chomp $retval;
    return $retval;
}

sub get_artist {
    my $script=<<_END_;

    tell application "Spotify"
        set output to artist of current track
    end tell
_END_

    osascript $script;
}

sub get_track {
    my $script=<<_END_;

    tell application "Spotify"
        set output to name of current track
    end tell
_END_

    osascript $script;
}

sub get_state {
    my $script=<<_END_;

    tell application "System Events"
        set MyList to (name of every process)
    end tell
    if (MyList contains "Spotify") is true then
        tell application "Spotify"
            set output to player state
        end tell
    else
        set output to "not running"
    end if
_END_

    osascript $script;
}

sub get_volume {
    my $script=<<_END_;

    tell application "Spotify"
        set output to sound volume
    end tell
_END_

    osascript $script;
}

sub set_volume {
    return unless (defined($_[0]));

    my $new_volume = $_[0];

    my $script=<<_END_;

    tell application "Spotify"
        set sound volume to $new_volume
    end tell
_END_

    osascript $script;
}

sub increase_volume {
    my $script=<<_END_;

    tell application "Spotify"
        set sound volume to (sound volume + $delta_volume)
    end tell
_END_

    osascript $script;
}

sub decrease_volume {
    my $script=<<_END_;

    tell application "Spotify"
        set sound volume to (sound volume - $delta_volume)
    end tell
_END_

    osascript $script;
}

sub dim_volume {
    my $script=<<_END_;

    tell application "Spotify"
        set sound volume to (sound volume - $dim_amount)
    end tell
_END_

    osascript $script;
}

sub undim_volume {
    my $script=<<_END_;

    tell application "Spotify"
        set sound volume to (sound volume + $dim_amount)
    end tell
_END_

    osascript $script;
}

sub play_pause {
    my $script=<<_END_;

    tell application "Spotify" to playpause
_END_

    osascript $script;
}

sub play {
    my $script=<<_END_;

    tell application "Spotify" to play
_END_

    osascript $script;
}

sub pause {
    my $script=<<_END_;

    tell application "Spotify" to pause
_END_

    osascript $script;
}


sub play_next {
    my $script=<<_END_;

    tell application "Spotify" to next track
_END_

    osascript $script;
}

sub play_previous {
    my $script=<<_END_;

    tell application "Spotify" to previous track
_END_

    osascript $script;
}


