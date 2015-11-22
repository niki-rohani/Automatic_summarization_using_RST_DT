'''
Created on Feb 19, 2013

@author: Vanessa Feng
'''
import os
import fnmatch
import re

from operator import itemgetter
from trees.parse_tree import ParseTree
from nltk.tree import Tree
#from nltk.draw.tree import *
from RST_Classes import *
import treebank_parser

def locate(pattern, root=os.getcwd()):
    for path, dirs, files in os.walk(root):
        for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
            yield filename

def common_ancestor(L1, L2):
    i = 0
    while i < len(L1) and i < len(L2) and L1[i] == L2[i]:
        i+=1
    return L1[0:i]    

def common_ancestor_list(LL):
    i = 0
    L1 = LL[0]
    stop = False
    
    while not stop:
        for L in LL:
            if i >= len(L) or L[i] != L1[i]:
                stop = True
        i+=1
    return L1[0:i-1]    

def concat_2_lists(A, B):
    A.extend(B)
    return A

def concat_lists(L):
    return reduce(concat_2_lists, L, [])

def get_concat_text(T, tags = None):
    if tags is not None:
        no_nps = []
        for word_tag in tags:
            word = ' '.join(word_tag.split('/')[ : -1])
            tag = word_tag.split('/')[-1]
            #print word, tag
            if tag.startswith('N'):
                no_nps.append(word)

    if isinstance(T, Tree):
        leaves = T.leaves()
        if tags is not None:
            return (concat_lists(leaves), len(leaves), T.height()-2, no_nps)
        return (concat_lists(leaves), len(leaves), T.height()-2)
    else:
        if tags is not None:
            return (T, 1, 0, no_nps)
        return (T, 1, 0)

def slice_text(mystr):
    #splitter = re.compile('(\$?\'?\d+\.\d+|\'s|\$?\'?\d[\d\/\%,:s\)]*|[a-z\-]*\'[a-z\-]+)|\s([a-z]\.[a-z\.]*)|\s|(<p>|--)|[^a-zA-Z0-9\-\%\s]')
    #return [part.lower() for part in splitter.split(mystr.lower().replace("\\)", ")")) if part]
    return mystr.lower().split()

def get_ngrams(items, n, NList = {}):
  #  NList = {}
    if n > 1:
        myitems = ["<!"] + items + ["!>"]
    else:
        myitems = items
    for i in range(len(myitems) - n + 1):
        ngram = "_".join(myitems[i:i+n]).lower()
        if ngram in NList:
            NList[ngram] += 1
        else:
            NList[ngram] = 1
    return NList

def get_one_ngram(items, n, freq_word_dict = None):
    if freq_word_dict is not None:
        items1 = []
        for item in items:
            if item not in freq_word_dict:
                items1.append(item)
        
        if n > 1 or n < -1:
            myitems = ["<!"] + items1 + ["!>"]
        else:
            myitems = items1
        if n > 0:
            return "_".join(myitems[0:n]).lower()
        else:
            return "_".join(myitems[n:]).lower()

    if n > 1 or n < -1:
        myitems = ["<!"] + items + ["!>"]
    else:
        myitems = items
    if n > 0:
        return "_".join(myitems[0:n]).lower()
    else:
        return "_".join(myitems[n:]).lower()

def filter_ngrams(ngrams, threshold = 1, max_threshold = 0):
    ngrams_sel = {}
    max_f = 0
    for (item, freq) in ngrams.items():
        max_f = max([max_f, freq])
        if freq > threshold and (max_threshold <= 0 or freq < max_threshold):
            ngrams_sel[item] = freq
        elif max_threshold > 0 and freq >= max_threshold:
            print "(x) %s %i > %2f" % (item, freq, max_threshold)
    return ngrams_sel


def extract_relations(T):
    if isinstance(T, Tree):
        ret = [T.node]
        for child in T:
            ret += extract_relations(child)
        return ret
    else:
        return []

def traverse_tree(T, fn):
    if isinstance(T, Tree):
        fn (T)
        for child in T:
            traverse_tree(child, fn)

def traverse_tree_with_offset(T, fn, offset = 0):
    if isinstance(T, Tree):
        fn (T, offset)
        for child in T:
            traverse_tree_with_offset(child, fn, offset)
            if isinstance(child, Tree):
                offset +=  len(child.leaves())
            else:
                offset += 1

def traverse_tree_path(T, fn, path_len, arg = None, cur_path = []):
    if len(cur_path) > path_len:
        return
    fn (T, cur_path, arg)
    if isinstance(T, Tree):
        traverse_tree_path(T[0], fn, path_len, arg, cur_path + [0])
        traverse_tree_path(T[1], fn, path_len, arg, cur_path + [1])
    else:
        traverse_tree_path(None, fn, path_len, arg, cur_path + [0])
        traverse_tree_path(None, fn, path_len, arg, cur_path + [1])
    
      
def convert_tree(t):
    label = None
    
    if t.node == "text":
        return slice_text(t[0])
    
    children = []
    for elem in t:
        if not isinstance(elem, Tree) or (elem.node != "span" and elem.node != "rel2par" and elem.node != "leaf"):
            children.append(elem)
            if isinstance(elem, Tree) and (label is None or label[0] == "span"):
                for sub in (s for s in elem if isinstance(s, Tree)):
                    if sub.node == "rel2par":
                        label = sub
                        break;
        
    if len(children) == 1:
        return convert_tree(children[0])

    label_rel = rel2class[label[0].lower()] + "[" + children[0].node[0:1] + "][" + children[1].node[0:1] + "]"
        
    if len(children) > 2:
        for item in children[1:]:
            item._parent = None

        return ParseTree(label_rel, [convert_tree(children[0]),
                                        ParseTree(label_rel, [convert_tree(children[1]),
                                                                 convert_tree(ParseTree("temp", children[2:]))])])
    else:
        return ParseTree(label_rel, [convert_tree(children[0]), convert_tree(children[1])])

def load_tree(filename):
    str = open(filename).read()
    return load_tree_from_string(str)

def load_tree_from_string(str):
    return convert_tree(treebank_parser.parse(str))

def load_raw_tree(filename):
    str = open(filename).read()
    return treebank_parser.parse(str)


def get_main_edus(T, pos = []):
    if not isinstance(T, Tree):
        #print 'not tree'
        return [pos];
    
    ret = [];
    if T.node[-5:-4] == 'N':
        ret += get_main_edus(T[0], pos + [0])
    if T.node[-2:-1] == 'N':
        ret += get_main_edus(T[1], pos + [1])
#    print T
#    print ret
    #print ret
    return ret

def is_left_nucleus(T):
    return isinstance(T, Tree) and T.node[-5:-4] == 'N'

def is_right_nucleus(T):
    return isinstance(T, Tree) and T.node[-2:-1] == 'N'

def filter_lexical_head(head_str):
    if not re.sub('^[0-9\\./\\\\,]*', '', head_str):
        return "#NUM#";
    return head_str.lower()

def filter_syntactic_tag(syntactic_tag):
    return syntactic_tag
    #return re.sub('[0-9\-=]*$', '', syntactic_tag.lower())
    
