#!/usr/bin/python
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import argparse
import csv
from collections import defaultdict
from nj_common import *

def main():

    CONST_COUNTY_FILE = '../2017/20171107__nj__general__county.csv'
    CONST_PRECINCT_FILE = '../2017/20171107__nj__general__morris__precinct.csv'

    args = handle_arguments()
    process_precinct_file(args, CONST_PRECINCT_FILE)
    compare_county_and_precinct_totals(args, 
                                   CONST_COUNTY_FILE,
                                   CONST_PRECINCT_FILE)
    #spot_check_totals(args, CONST_COUNTY_FILE)

def handle_arguments():
    arg_parser = argparse.ArgumentParser(description='Validate New Jersey 2017 Morris county data')
    arg_parser.add_argument('--verbose', '-v', dest='verbose',  help='report information verbosely', action='store_true')
    arg_parser.add_argument('--case', '-c', dest='case',  help='case sensitive text compare', action='store_true')
    return arg_parser.parse_args()

def process_precinct_file(args, in_file):

    error_count = 0

    verifier = VerifyMuni(in_file, args.verbose, args.case)   
    error_count += verifier.verify_counties()
    error_count += verifier.verify_offices()
    error_count += verifier.verify_districts()
    error_count += verifier.verify_votes()
    #error_count += verifier.verify_candidate_party_relationship()
    #error_count += verifier.verify_candidate_office_relationship()
    #error_count += verifier.verify_candidate_district_relationship()

    print 'There were ' + str(error_count) + ' invalid values in the Precinct File.'

    return

def compare_county_and_precinct_totals(args, county_file, precinct_file):

    error_count = 0

    cv = VerifyCounty(county_file, args.verbose, args.case)
    mv = VerifyPrecinct(precinct_file, args.verbose, args.case)

    county_name = 'Morris'
    county_votes = cv.get_all_candidates_and_votes_by_county(county_name)
    for cand in county_votes:
        if cand == 'Philip Murphy - Shelia Oliver':
            muni_total = mv.get_candidates_votes_by_county(county_name, 'Philip Murphy')
        elif cand == 'Kim Guadagno - Carlos A. Rendo':
            muni_total = mv.get_candidates_votes_by_county(county_name, 'Kim Guadagno')
        elif cand == 'Gina Genovese - Lt. Governor Not Filed':
            muni_total = mv.get_candidates_votes_by_county(county_name, 'Gina Genovese')
        elif cand == 'Peter J. Rohrman - Karese J. Laguerre':
            muni_total = mv.get_candidates_votes_by_county(county_name, 'Peter J. Rohrman')
        elif cand == 'Seth Kaper-Dale - Lisa Durden':
            muni_total = mv.get_candidates_votes_by_county(county_name, 'Seth Kaper-Dale')
        elif cand == 'Matthew Riccardi - Lt. Governor Not Filed':
            muni_total = mv.get_candidates_votes_by_county(county_name, 'Matthew Riccardi')
        elif cand == 'Vincent Ross - April A. Johnson':
            muni_total = mv.get_candidates_votes_by_county(county_name, 'Vincent Ross')
        elif cand == 'Thomas H. Kean Jr.':
            muni_total = mv.get_candidates_votes_by_county(county_name, 'Thomas H. Kean, Jr.')
        else:
            muni_total = mv.get_candidates_votes_by_county(county_name, cand)
        if muni_total != county_votes[cand]:
            error_count += 1
            if args.verbose:
                print "Total votes are different in County (" + \
                      str(county_votes[cand]) + ") and Precinct (" + \
                      str(muni_total) + ") for " + cand + " in " + \
                      county_name + " County."

    print "There are " + str(error_count) + " vote totals that are not reconciled."

if __name__ == '__main__':
    main()
