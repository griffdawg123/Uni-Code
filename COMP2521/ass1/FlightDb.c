
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "List.h"
#include "FlightDb.h"
#include "AVLTree.h"

struct flightDb {
	Tree byAirport;
	Tree byFlightNumber;
	Tree byFlightTime;
};

/////////////////////////////////////////
// Comparison Functions
int comparebyFlightTime(Record r1, Record r2);
int doCompareByFlightTime(Record r1, Record r2);

int compareByAirport(Record r1, Record r2);
int doCompareByAirport(Record r1, Record r2);

int compareByFlightNumber(Record r1, Record r2);
int doCompareByFlightNumber(Record r1, Record r2);
//
//  FlightTime > FlightNumber > Airport
int comparebyFlightTime(Record r1, Record r2) {
	int cmp = doCompareByFlightTime(r1, r2);
	if (cmp != 0) {
		return cmp;
	}
	cmp = doCompareByFlightNumber(r1, r2);
	if (cmp != 0) {
		return cmp;
	}
	return doCompareByAirport(r1, r2);
}

int doCompareByFlightTime(Record r1, Record r2) {
	if (RecordGetDepartureDay(r1) - RecordGetDepartureDay(r2) != 0) {
		return RecordGetDepartureDay(r1) - RecordGetDepartureDay(r2);
	} else if (RecordGetDepartureHour(r1) - RecordGetDepartureHour(r2) != 0) {
		return RecordGetDepartureHour(r1) - RecordGetDepartureHour(r2);
	} else if (RecordGetDepartureMinute(r1) - RecordGetDepartureMinute(r2) != 0){
		return RecordGetDepartureMinute(r1) - RecordGetDepartureMinute(r2);
	} 
	return 0;
}

// Airport > FlightTime > FlightNumber
int compareByAirport(Record r1, Record r2) {
	int cmp = doCompareByAirport(r1, r2);
	if (cmp != 0) {
		return cmp;
	}
	cmp = doCompareByFlightTime(r1, r2);
	if (cmp != 0) {
		return cmp;
	}
	return doCompareByFlightNumber(r1, r2);
}

int doCompareByAirport(Record r1, Record r2) {
	return strcmp(RecordGetDepartureAirport(r1), RecordGetDepartureAirport(r2));
}

// FlightNumber > FlightTime > Airport
int compareByFlightNumber(Record r1, Record r2) {
	int cmp = doCompareByFlightNumber(r1, r2);
	if (cmp != 0) {
		return cmp;
	}
	cmp = doCompareByFlightTime(r1, r2);
	if (cmp != 0) {
		return cmp;
	}
	return doCompareByAirport(r1, r2);
}

int doCompareByFlightNumber(Record r1, Record r2) {
	return strcmp(RecordGetFlightNumber(r1), RecordGetFlightNumber(r2));
}

/////////////////////////////////////////

/**
 * Creates a new flight DB. 
 * You MUST use the AVLTree ADT (from Task 1) in your implementation.
 */
FlightDb DbNew(void) {
	FlightDb db = malloc(sizeof(*db));
    if (db == NULL) {
        fprintf(stderr, "error: out of memory\n");
        exit(EXIT_FAILURE);
    }

    db->byAirport = TreeNew(compareByAirport);
    db->byFlightNumber = TreeNew(compareByFlightNumber);
	db->byFlightTime = TreeNew(comparebyFlightTime);
    return db;
}

/**
 * Frees all memory allocated to the given flight DB
 */
void     DbFree(FlightDb db) {
	TreeFree(db->byAirport, false);
	TreeFree(db->byFlightTime, false);
    TreeFree(db->byFlightNumber, true);
    free(db);
}

/**
 * Inserts  a  flight  record  into the given DB if there is not already
 * record with the same flight number, departure airport, day, hour  and
 * minute.
 * If  inserted successfully, this function takes ownership of the given 
 * record (so the caller should not modify or free it). 
 * Returns true if the record was successfully inserted,  and  false  if
 * the  DB  already  contained  a  record  with  the same flight number,
 * departure airport, day, hour and minute.
 * The time complexity of this function must be O(log n).
 * You MUST use the AVLTree ADT (from Task 1) in your implementation.
 */
bool     DbInsertRecord(FlightDb db, Record r) {
	if (TreeInsert(db->byFlightTime, r)) { // if one insertion is okay, do the rest
        TreeInsert(db->byAirport, r);
	    TreeInsert(db->byFlightNumber, r);
        return true;
    } else {
        return false;
    }
}

/**
 * Searches  for  all  records with the given flight number, and returns
 * them all in a list in increasing order of  (day, hour, min).  Returns
 * an empty list if there are no such records. 
 * The  records  in the returned list should not be freed, but it is the
 * caller's responsibility to free the list itself.
 * The time complexity of this function must be O(log n + m), where m is
 * the length of the returned list.
 * You MUST use the AVLTree ADT (from Task 1) in your implementation.
 */
List     DbFindByFlightNumber(FlightDb db, char *flightNumber) {
	Record numberMin = RecordNew(flightNumber, "", "", 0, 0, 0, 0); // minimum flight number
	Record numberMax = RecordNew(flightNumber, "ZZZZZZZZ", "ZZZZZZZZ", 6, 23, 59, __INT_MAX__); // maximum flight number
	List l = TreeSearchBetween(db->byFlightNumber, numberMin, numberMax); // return the list of flights inbetween
	RecordFree(numberMin);
	RecordFree(numberMax);
	return l;
}

/**
 * Searches  for all records with the given departure airport and day of
 * week (0 to 6), and returns them all in a list in increasing order  of
 * (hour, min, flight number).
 * Returns an empty list if there are no such records.
 * The  records  in the returned list should not be freed, but it is the
 * caller's responsibility to free the list itself.
 * The time complexity of this function must be O(log n + m), where m is
 * the length of the returned list.
 * You MUST use the AVLTree ADT (from Task 1) in your implementation.
 */
List     DbFindByDepartureAirportDay(FlightDb db, char *departureAirport,
                                     int day) {
	Record numberMin = RecordNew("", departureAirport, "", day, 0, 0, 0); // minimum time on the day
	Record numberMax = RecordNew("ZZZZZZZZ", departureAirport, "ZZZZZZZZ", day, 23, 59, __INT_MAX__); // maximum time on the day
	List l = TreeSearchBetween(db->byAirport, numberMin, numberMax);
	RecordFree(numberMin);
	RecordFree(numberMax);
	return l;
}


/**
 * Searches  for  all  records  between  (day1, hour1, min1)  and (day2,
 * hour2, min2), and returns them all in a list in increasing  order  of
 * (day, hour, min, flight number).
 * Returns an empty list if there are no such records.
 * The  records  in the returned list should not be freed, but it is the
 * caller's responsibility to free the list itself.
 * The time complexity of this function must be O(log n + m), where m is
 * the length of the returned list.
 * You MUST use the AVLTree ADT (from Task 1) in your implementation.
 */
List     DbFindBetweenTimes(FlightDb db, 
                            int day1, int hour1, int min1, 
                            int day2, int hour2, int min2) {
	Record numberMin = RecordNew("", "", "", day1, hour1, min1, 0); // minimum flight number
	Record numberMax = RecordNew("ZZZZZZZZ", "ZZZZZZZZ", "ZZZZZZZZ", day2, hour2, min2, __INT_MAX__); // maximum flight number
	List l = TreeSearchBetween(db->byFlightTime, numberMin, numberMax); // return list
	RecordFree(numberMax);
	RecordFree(numberMin);
	return l;
}

/**
 * Searches  for  and  returns  the  earliest next flight from the given
 * departure airport, on or after the given (day, hour, min).
 * The returned record must not be freed or modified. 
 * The time complexity of this function must be O(log n).
 * You MUST use the AVLTree ADT (from Task 1) in your implementation.
 */
Record   DbFindNextFlight(FlightDb db, char *departureAirport, 
                          int day, int hour, int min) {
	Record temp = RecordNew("", departureAirport, "", day, hour, min, 0); // create record with given values
	Record next = TreeNext(db->byFlightTime, temp); // find the next record
	RecordFree(temp); // free temp record
	if (next != NULL) { // if there is a "next" record, return it
		return next;
	}
	// if not create a record which is the absolute minimum
	Record first = RecordNew("", departureAirport, "", 0, 0, 0, 0); 
	Record firstIn = TreeNext(db->byFlightTime, first);
	RecordFree(first);
	return firstIn;
}

