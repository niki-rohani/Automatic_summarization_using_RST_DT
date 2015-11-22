# -*- coding: utf-8 -*-
"""
@author: dantidot
"""


from nltk.corpus import stopwords
import re
from gensim import corpora
import pulp as lp
import rst2dep as rst_dt

splitters = u'[^0-9a-zA-Z]'

"""
Retourn une liste des edu de l'arbre et leur profondeur dans l'arbre racine
edu = [["tag", prof], ["tag", prof]]

"""
def show_edu_tree (tree, edu, dep):
    edus = []
    for nid in tree.all_nodes():
        edus.append([edu[nid.identifier][0], dep.depth(nid.identifier)])
    #print edus
    return edus
        
class TKP():
    
    def load(self, path):
        self.rst_dt = rst_dt.RST_DT()
        self.rst_dt.load(path)
        self.dep_dt = self.rst_dt.toDEP()
        dep = path+'.p'
        rst_dt.pickle.dump(self.rst_dt.tree, open(  dep, 'wb' ) )
        self.xi = {}
        self.stop_words = []
        for w in stopwords.words('english'):
            self.stop_words.append(w.decode('utf-8'))
        self.word = {}
        for doc in self.rst_dt.EDU:
            self.xi[doc] = 0
            split = re.split(splitters, self.rst_dt.EDU[doc][0].lower())
            for sp in split:
                if sp != '':
                    if self.word.has_key(sp) == False:
                        self.word[sp] = 1
                    else:
                        self.word[sp]+=1
                        
        for sw in self.stop_words:
            if self.word.has_key(sw):
                del self.word[sw]
        self.total_w = 0
        for w in self.word:
            self.total_w += self.word[w]
        
            
    def depth (self, edu):
        return self.dep.depth(edu)
    
    
    def w (self,edu):
        w = 0
        words = re.split(splitters, edu.lower())
        for word in words:
            if self.word.has_key(word):            
                w+=self.word[word] / float(self.total_w)
        return w

    def w_id(self,edu) :
        return self.w (self.rst_dt.EDU[edu][0])
        
    def f (self, tree):
        f = 0
        for edu in tree.all_nodes():
            f += self.w_id (edu.identifier) / (float (self.dep_dt.depth(edu.identifier)) + 1)
        return f
        
    def summary(self):
        summary = []
        for xi in self.xi:
            if self.xi[xi].value() == 1:
                summary.append(self.rst_dt.EDU[xi])
        return summary
    
    def f_cur (self):
        f = 0
        for edu in self.dep_dt.all_nodes():
            f += (self.w_id (edu.identifier) / (float (self.dep_dt.depth(edu.identifier)) + 1)) * self.xi[edu.identifier]
        return f
        
    def f_x (self, xi):
        f = 0
        for edu in self.dep_dt.all_nodes():
            f += (self.w_id (edu.identifier) / (float (self.dep_dt.depth(edu.identifier)) + 1)) * xi[edu.identifier]
        return f
        
    def f_xi (self, edu):
        f = 0
        f = (self.w_id (edu) / (float (self.dep_dt.depth(edu)) + 1))
        return f
        
    def li (self, edu):
        li = 0
        words = re.split(splitters, edu.lower())
        for word in words:
            if (word != ''):
                li+=1
        return li
        
    def li_id (self, edu):
        return self.li (self.rst_dt.EDU[edu][0])
    
    def is_parent_active (self, edu, xi):
        if (self.dep_dt.depth(self.dep_dt.parent(edu).identifier)>0):
            return xi[self.dep_dt.parent(edu).identifier]
        return 1
    
    def parent (self, edu):
        if (self.dep_dt.depth(edu)>0):
            return self.dep_dt.parent(edu).identifier
        return edu
    
    def and_parent (self, active):
        return sum(active) == len(active)
        
    def solve(self, L):
        self.problem = lp.LpProblem ("tkp", lp.LpMaximize)
        self.xi = lp.LpVariable.dicts('edu', self.xi, 
                            lowBound = 0,
                            upBound = 1,
                            cat = lp.LpInteger)
        self.problem += sum ([self.f_xi(edu.identifier) * self.xi[edu.identifier] for edu in self.dep_dt.all_nodes()])
        self.problem += sum ([self.li_id(edu.identifier) * self.xi[edu.identifier] for edu in self.dep_dt.all_nodes()]) <= L
        self.problem += self.and_parent ([self.xi[self.parent(edu.identifier)] >= self.xi[edu.identifier] for edu in self.dep_dt.all_nodes()])
        self.problem.solve()
        
                
        
        
"""
tree = rst_dt.pickle.load( open( dep, 'rb' ) )
        
rst = 'fight.tree'
dep_dt = rst_dt.RST_DT()
dep_dt.load(rst)
tree = dep_dt.toDEP()
dep = rst+'.p'
rst_dt.pickle.dump( tree, open(  dep, 'wb' ) )


tree = rst_dt.pickle.load( open( dep, 'rb' ) )

subTrees = toSubTree(tree)

edus = show_edu_tree(subTrees[0], dep_dt.EDU, tree)
"""







