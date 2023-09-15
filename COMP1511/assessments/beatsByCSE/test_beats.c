// Assignment 2 20T1 COMP1511: CS bEats
// test_beats.c
//
// This program was written by YOUR-NAME-HERE (z5555555)
// on INSERT-DATE-HERE
//
// Version 1.0.0: Assignment released.
#include <stdio.h>
#include <stdlib.h>

#include "test_beats.h"
#include "beats.h"


// Test function for `add_note_to_beat`
int test_add_note_to_beat(void) {
    // Test 1: Rejecting negative inputs.
    Beat test_beat = create_beat();
    if (add_note_to_beat(test_beat, -1, -1) != INVALID_OCTAVE) {
        return DOES_NOT_MEET_SPEC;
    }
    if (add_note_to_beat(test_beat, -1, 0) != INVALID_OCTAVE) {
        return DOES_NOT_MEET_SPEC;
    }
    if (add_note_to_beat(test_beat, 1, -1) != INVALID_KEY) {
        return DOES_NOT_MEET_SPEC;
    }

    // Test 2: Rejecting out of range inputs.
    if (add_note_to_beat(test_beat, 10, 0) != INVALID_OCTAVE) {
        return DOES_NOT_MEET_SPEC;
    }
    if (add_note_to_beat(test_beat, 0, 12) != INVALID_KEY) {
        return DOES_NOT_MEET_SPEC;
    }

    // Test 3: Testing that code rejects duel inputs
    add_note_to_beat(test_beat, 1, 1);
    if (add_note_to_beat(test_beat, 1, 1) != NOT_HIGHEST_NOTE) {
        return DOES_NOT_MEET_SPEC;
    }

    return MEETS_SPEC;
}

// Test function for `count_notes_in_octave`
int test_count_notes_in_octave(void){
    
    Beat test_beat = create_beat();
    // Test 1: empty beat
    if (count_notes_in_octave(test_beat, 3) != 0) {
        return DOES_NOT_MEET_SPEC;
    }
    add_note_to_beat(test_beat, 1, 1);
    // Test 2: invalid octave
    if (count_notes_in_octave(test_beat, -1) != 0) {
        return DOES_NOT_MEET_SPEC;
    }
    // Test 3: no notes in that octave
    if (count_notes_in_octave(test_beat, 11) != 0) {
        return DOES_NOT_MEET_SPEC;
    }
    return MEETS_SPEC;
}

// Test function for `add_beat_to_track`
int test_add_beat_to_track(void){

    Track test_track = create_track();
    Beat test_beat1 = create_beat();
    add_beat_to_track(test_track, test_beat1);
    // Test 1: can add beat
    if (count_beats_left_in_track(test_track) != 1) {
        return DOES_NOT_MEET_SPEC;
    }
    
    Beat test_beat2 = create_beat();
    add_beat_to_track(test_track, test_beat2);

    // Test 2: can add to start of track
    if (count_beats_left_in_track(test_track) != 2) {
        return DOES_NOT_MEET_SPEC;
    }
    select_next_beat(test_track);
    Beat test_beat3 = create_beat();
    add_beat_to_track(test_track, test_beat3);
    // Test 3:  Can add after selected beat
    if (count_beats_left_in_track(test_track) != 2) {
        return DOES_NOT_MEET_SPEC;
    }

    return MEETS_SPEC;
}

// Test function for `remove_selected_beat`
int test_remove_selected_beat(void){
    Track test_track = create_track();
    Beat test_beat1 = create_beat();
    add_beat_to_track(test_track, test_beat1);
    Beat test_beat2 = create_beat();
    add_beat_to_track(test_track, test_beat2);
    select_next_beat(test_track);
    // Test 1: remove selected still running
    if (remove_selected_beat(test_track) != TRACK_PLAYING) {
        return DOES_NOT_MEET_SPEC;
    }

    // Test 2: remove selected stopped
    if (remove_selected_beat(test_track) != TRACK_STOPPED) {
        return DOES_NOT_MEET_SPEC;
    }

    // Test 3: remove empty
    if (remove_selected_beat(test_track) != TRACK_STOPPED) {
        return DOES_NOT_MEET_SPEC;
    }
    return MEETS_SPEC;
}

// Test function for `add_musical_note_to_beat`
int test_add_musical_note_to_beat(void){
    Beat test_beat = create_beat();
    // Test 1: checks can add note
    if (add_musical_note_to_beat(test_beat, "0A") != VALID_NOTE) {
        return DOES_NOT_MEET_SPEC;
    }

    // Test 2: checks can handle hashes
    if (add_musical_note_to_beat(test_beat, "0A#") != VALID_NOTE) {
        return DOES_NOT_MEET_SPEC;
    }

    // Test 3: ???
    // TODO: Write Test 3

    return MEETS_SPEC;
}
