# coding: utf-8
#!/usr/bin/env python

import os
import re
import argparse

#######################################################################

__author__ = "Remi Cadene"

#######################################################################

class Evaluation:

    def __init__(self, path2rslt='./rslt/',
                 path2txt='./corpus/txt/',
                 path2summaries='./corpus/summaries/',
                 path2models='./corpus/RST-DT/EXT-EDUS-30/',
                 path2summaries2rouge='./src/summaries2rouge/summaries2rouge.py',
                 path2rouge2csv='./src/rouge2csv/rouge2csv.pl',
                 path2rouge='./src/ROUGE-1.5.5/',
                 path2summarize='./../SummarizeApp/discourse/src/summarize.py'):
        self.path2rslt = path2rslt
        self.path2txt = path2txt
        self.path2summaries = path2summaries
        self.path2models = path2models
        self.path2summaries2rouge = path2summaries2rouge
        self.path2rouge2csv = path2rouge2csv
        self.path2rouge = path2rouge
        self.path2summarize = path2summarize
        self.model_fname_EDUs = {}
        self.model_fname_words = {}
        self.extensions = ['.abs.name1', '.abs.name2', '.ext.name4',
                           '.shortabs.name1', '.shortabs.name2']

    def loadModels(self):
        """ First method to call in order to recover the number of words
            for each model files """
        model_fnames = []
        model_EDUs = []
        for fname in os.listdir(self.path2models):
            nb_EDUs = 0
            nb_words = 0
            with open(self.path2models + fname, 'r') as f:
                for line in f:
                    reg = r"^\* *(.+)\n"
                    match = re.findall(reg, line)
                    if match:
                        nb_EDUs += 1
                        nb_words += len(re.findall(r"[a-zA-Z0-9']+[ \.\n,;?]+", match[0]))
            #print nb_words
            self.model_fname_EDUs[fname] = nb_EDUs
            self.model_fname_words[fname] = nb_words
            model_fnames.append(fname)
            model_EDUs.append(nb_EDUs)
        # for i, nb_EDUs in enumerate(model_EDUs):
        #     if i > 0 and i % 5 == 0:
        #         print "--"
        #     print nb_EDUs
        # return model_fnames, model_EDUs

    def generateSummaries(self):
        """ Second method to call in order to generate the summaries
            for each txt files (optionnal if you already have them)
        """
        for fname in os.listdir(self.path2txt):
            name = fname.split('.')[0]
            for ext in self.extensions:
                model_fname = name + ext
                #l = self.model_fname_EDUs[model_fname]
                l = self.model_fname_words[model_fname]
                path2file = self.path2txt
                input_fname = fname
                output_fname = model_fname
                self.__syscallSummarize(l, path2file,
                            input_fname, output_fname)

    def __syscallSummarize(self, l='10', path2file='./',
                           input_fname='file1.txt',
                           output_fname='file1.abs.name1'):
        #syscall = 'python ' + self.path2summarize
        syscall = 'python ./summarize.py'
        syscall += ' -l ' + str(l)
        syscall += ' -o ' + self.path2summaries + output_fname
        syscall += ' -i ' + path2file + input_fname
        #syscall += ' > ' + self.path2summaries + output_fname
        print syscall
        #os.system(syscall)
    
    def generateRougeScore(self):
        """ Third method to call in order to generate the
            ROUGE score
        """
        # generate score.txt for each summaries using summaries2rouge
        # for fname in os.listdir(self.path2txt):
        #     name = fname.split('.')[0]
        #     for ext in self.extensions:
        #         system_fname = name + ext
        #         model_fname = system_fname
        #         self.__syscallRouge(model_fname, system_fname)
        self.__syscallRouge('file1.abs.name1', 'file1.abs.name1')
        # generate total_score.csv using rouge2csv
        rouge1_lines = []
        rouge2_lines = []
        # for fname in os.listdir(self.path2txt):
        #     name = fname.split('.')[0]
        #     for ext in self.extensions:
        #         path2score = self.path2rslt + name + ext + '/score.txt'
        #         #print path2score
        #         with open(path2score, 'r') as f:
        #             for i, line in enumerate(f):
        #                 if i==1 or i==2 or i==3:
        #                     rouge1_lines.append(line)
        #                 if i==5 or i==6 or i==7:
        #                     rouge2_lines.append(line)
        #         rouge1_lines.append('\n')
        #         rouge2_lines.append('\n')
        path2score = self.path2rslt + 'file1.abs.name1' + '/score.txt'
        with open(path2score, 'r') as f:
            for i, line in enumerate(f):
                if i==1 or i==2 or i==3:
                    rouge1_lines.append(line)
                if i==5 or i==6 or i==7:
                    rouge2_lines.append(line)
        rouge1_lines.append('\n')
        rouge2_lines.append('\n')
        fscores = open(self.path2rslt + 'ROUGE1_scores.txt', 'wb')
        fscores.write(''.join(rouge1_lines))
        fscores.close()
        fscores = open(self.path2rslt + 'ROUGE2_scores.txt', 'wb')
        fscores.write(''.join(rouge2_lines))
        fscores.close()
        self.__syscallRouge2Csv(self.path2rslt + 'ROUGE1_scores.txt', 'ROUGE1')
        self.__syscallRouge2Csv(self.path2rslt + 'ROUGE2_scores.txt', 'ROUGE2')

    def __syscallRouge(self, model_fname='file1.abs.name1',
                       system_fname='file1.abs.name1'):
        if not os.path.exists(self.path2rslt + system_fname):
            os.mkdir(self.path2rslt + system_fname)
        syscall = 'python ' + self.path2summaries2rouge
        syscall += ' ' + self.path2rouge
        syscall += ' ' + self.path2rslt + system_fname + '/'
        syscall += ' -m'
        syscall += ' ' + self.path2models + model_fname
        syscall += ' -s'
        syscall += ' ' + self.path2summaries + system_fname
        syscall += ' > ' + self.path2rslt + system_fname + '/score.txt'
        #print syscall
        os.system(syscall)

    def __syscallRouge2Csv(self, score_fpath='', prefix='prefix'):
        syscall = 'perl ' + self.path2rouge2csv
        syscall += ' ' + score_fpath
        syscall += ' ' + prefix
        os.system(syscall)
        os.system('mv ' + prefix + '_score.csv ' + self.path2rslt)

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path2summarize', type=str,
                        help="path to the file summarize.py")
    args = parser.parse_args()

    evaluation = Evaluation(path2summarize=args.path2summarize)
    evaluation.loadModels()
    if args.path2summarize: #^None
        evaluation.generateSummaries()
    else:
        evaluation.generateRougeScore()
 
    


