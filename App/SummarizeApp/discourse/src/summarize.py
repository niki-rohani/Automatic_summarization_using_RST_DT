# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:37:48 2015

@author: dantidot
"""


import tkp
import sys
import argparse
import os
from parse import DiscourseParser


class Summarize(object):

    def __init__(self, l, output_file, input_file, flag=True):
        self.l = l
        if output_file == '':
            self.output_file = input_file + ".summary"
        else:
            self.output_file = output_file
        self.input_file = input_file
        self.flag = flag

    def parsing2rst(self):
        if self.flag:
            print "###########################"
            print "STEP 1: Parsing file to RST"
        rst_parser = DiscourseParser (False, False, self.output_file, False, False)
        dists = rst_parser.parse(self.input_file)
        # WTF ...?
        os.system('killall svm-scale')
        os.system('killall svm-predict-stdin')

    def convert2summary(self):
        if self.flag:
            print "###########################"
            print "STEP 2: Converting RST to TKP problem (using rst2dep.py)"
        solver = tkp.TKP() # on crée le tkp
        outfname = self.input_file + ".tree"
        solver.load(outfname) # on load le rst et fait la transformation en dep
        if self.flag:
            print "###########################"
            print "STEP 3: Solving TKP problem using ILP"
        solver.solve(self.l)
        if self.flag:
            print "###########################"
            print "STEP 4: Saving the summary"
        summary = solver.summary()
        f = open(self.output_file, 'w')
        EDUs = []
        for su in summary:
            EDUs.append('*   ' + su[0].replace('<s>', ''))
        final_summary = '\n'.join(EDUs)
        f.write(final_summary)
        f.close()
        print final_summary



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--length', type=int, required=True,
                        help="max number of words",
                        default=14)
    parser.add_argument('-o', '--output_directory', type=str,
                        help="output file",
                        default='')
    parser.add_argument('-i', '--input_file', type=str, required=True,
                        help="input file",
                        default='../TAL/fight')
    args = parser.parse_args()

    summarize = Summarize(args.length, args.output_file, args.input_file)
    summarize.parsing2rst()
    summarize.convert2summary()
    #output = "../out"
    #file = "../TAL/fight"
    #L = 100







