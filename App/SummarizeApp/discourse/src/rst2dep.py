# coding: utf-8

from treelib import Node, Tree
import re
import math
import copy
import numpy as np
import pickle
import argparse
import os

#######################################################################

__author__ = "Remi Cadene"

#######################################################################

class RST_DT():
    
    def load(self, path2file):
        self.id_EDUs = []
        self.EDU = {}
        self.treeNS = Tree()
        self.tree = Tree()
        # nombre max d'espace pour init id_parents
        with open(path2file, 'r') as f:
            max_space = 0
            nb_line = 0
            for i, line in enumerate(f):
                nb_space = 0
                for c in line:
                    if c == ' ':
                        nb_space += 1
                    else:
                        break
                if nb_space > max_space:
                    max_space = nb_space
                nb_line +=1
        with open(path2file, 'r') as f:
            id_parents = [0] * max_space
            NS_parents = [0] * max_space
            for i, line in enumerate(f):
                # nombre d'espace détermine le parent
                nb_space = 0
                for c in line:
                    if c == ' ':
                        nb_space += 1
                    else:
                        break
                space = nb_space / 2
                id_parents[space] = i
                parent = id_parents[space-1]
                reg = '\(([\w\-\[\]]+)|(_!.+!_)'  # récupération du contenu
                match = re.findall(reg, line)[0]
                if match[0] == '':
                    content = match[1] # feuille EDU
                    self.id_EDUs.append(i)
                    #print content
                    self.EDU[i] = re.findall('_!(.*)!_',content)
                else:
                        content = match[0] 
                        reg2 = '\[(N|S)\]' # récupération NS
                        match2 = re.findall(reg2, content)
                        NS_parents[space] = match2 #['N','S']
                # création du noeud
                if i == 0:
                    self.tree.create_node(content, 0)
                    self.treeNS.create_node('Root', 0)
                else:
                    id_NS = len(self.tree.is_branch(parent)) #0 ou 1 car arbre binaire
                    self.tree.create_node(content, i, parent=parent)
                    self.treeNS.create_node(NS_parents[space-1][id_NS], i, parent=parent)


    def toDEP(self):

        ###############################
        # Etape 1 : construction du head_tree

        # parcours en largeur de tree afin de récupérer chaque id_node
        # pour chaque profondeur (init à 0) _! sans compter !_ les feuilles (EDUs)

        nodes_depth = [-1] * self.tree.size()
        for i in xrange(self.tree.size()):
            id_nodes = [0]
            depth = [999] * self.tree.size()
            while id_nodes: #False if empty
                id_node = id_nodes.pop(0)
                node = self.tree.get_node(id_node)
                if node.bpointer != None:
                    node_parent = self.tree.get_node(node.bpointer)
                    depth[node.identifier] = depth[node_parent.identifier] + 1
                else:
                    depth[node.identifier] = 0
                if id_node == i:
                    #print 'noeud ',i,' en profondeur', depth[node.identifier]
                    if node.fpointer:
                        nodes_depth[i] = depth[i]
                    break
                if node.fpointer:
                    id_nodes.append(node.fpointer[0])
                    id_nodes.append(node.fpointer[1])
        #print nodes_depth

        id_nodes_depth = []
        for d in xrange(self.tree.depth()):
            id_nodes_depth.append([])
            for i in xrange(self.tree.size()):
                if nodes_depth[i] == d:
                    id_nodes_depth[d].append(i)
        #print id_nodes_depth

        # 
        # construction du head_tree

        head_tree = [-1] * self.treeNS.size()
        # pour chaque noeud (non EDU/feuille) en partant de la plus grande profondeur dans l'arbre
        for d in range(len(id_nodes_depth)-1, -1, -1):
            for id_node in id_nodes_depth[d]:
                node = self.treeNS.get_node(id_node)
                node_left = self.treeNS.get_node(node.fpointer[0])
                node_right = self.treeNS.get_node(node.fpointer[1])
                if node_left.tag == 'N':
                    if head_tree[node_left.identifier] == -1:
                        identifier = node_left.identifier
                    else:
                        identifier = head_tree[node_left.identifier]
                else:
                    if head_tree[node_right.identifier] == -1:
                        identifier = node_right.identifier
                    else:
                        identifier = head_tree[node_right.identifier]
                head_tree[id_node] = identifier
        #print head_tree
        
        ###############################
        # Etape 2 : construction du DEP

        # 
        # construction du DEP    

        # init
        # root est le premier noeud de head
        # pour chaque EDU son père est le root dans DEP
        dep_tree = Tree()
        id_root = head_tree[0]
        root = self.tree.get_node(id_root)
        #dep_tree.create_node(root.tag, root.identifier)
        dep_tree.create_node(root.tag, root.identifier)
        for id_EDU in xrange(len(head_tree)):
            if head_tree[id_EDU] == -1 and id_EDU != id_root:
                node = self.tree.get_node(id_EDU)
                #dep_tree.create_node(node.tag, node.identifier, parent=id_root)
                #dep_tree.create_node(str(id_EDU), node.identifier, parent=id_root)
                dep_tree.create_node(node.tag, node.identifier, parent=id_root)

        #print '//////////////////////'
        #print 'EDU', id_root
        # pour chaque EDU
        for id_EDU in xrange(len(head_tree)):
            if head_tree[id_EDU] == -1 and id_EDU != id_root:

                EDU_NS = self.treeNS.get_node(id_EDU)
                #print '.......................'
                #print 'EDU', id_EDU
                #print 'TAG', EDU_NS.tag
                
                if EDU_NS.tag == 'N':
                    # parcours en largeur jusqu'à trouver un S avec un head donc qui soit pas EDU
                    id_nodes = [EDU_NS.identifier]
                    visited = [False] * self.treeNS.size()
                    while id_nodes:
                        id_node = id_nodes.pop(0)
                        EDU = self.tree.get_node(id_node)
                        #print 'visited EDU', EDU.identifier
                        visited[EDU.identifier] = True
                        # cas d'arret
                        head_EDU = head_tree[EDU.identifier] == -1
                        head_EDU = False
                        node_tag = self.treeNS.get_node(EDU.identifier).tag
                        #print '  head_EDU', head_EDU
                        #print '  node_tag', node_tag
                        if not head_EDU and node_tag == 'S':
                            break
                        if EDU.bpointer:
                            if not visited[EDU.bpointer]:
                                id_nodes.append(EDU.bpointer)
                        if EDU.fpointer: # sécurité
                            if not visited[EDU.fpointer[0]]:
                                id_nodes.append(EDU.fpointer[0])
                            if not visited[EDU.fpointer[1]]:    
                                id_nodes.append(EDU.fpointer[1])
                        
                    # puis ajouter au DEP comme enfant du head du parent du noeud S
                    id_head = head_tree[EDU.bpointer]

                # si parent S
                else :
                    # parcours en largeur des ancêtre jusqu'à trouver un ancêtre avec un head
                    parent = self.treeNS.get_node(EDU_NS.bpointer)
                    id_head = head_tree[parent.identifier]

                # puis ajouter au DEP comme enfant de ce head
                if id_EDU != id_head:
                    dep_tree.move_node(id_EDU, id_head)
                EDU = self.tree.get_node(id_EDU)
                #print '---- ajout de',EDU.identifier,' à',id_head
                #if id_EDU == id_head:
                    #dep_tree.show()

        return dep_tree
        #showDepth(dep_tree, 4)
        #dep_tree.show()

        #node = dep_tree.

    def toString(self):
        """ affiche comme la sortie de Hilda """
        showDepth(self.tree, 0)


class DEP_DT(object):

    def __init__(self, dep_tree, EDU):
        self.dep_tree = dep_tree

    def save(self, output_dir, fname):
        # save file
        self.dep_tree.save2file(fname)
        os.rename(fname, output_dir + fname)
        # save as pickle
        #pickle.dump(self.rst_dt.tree, open( ouput_dir + fname + '.pkl' ,'wb' ) )


def showDepth(tree, id_node):
    """ parcours en profondeur infixe """
    node = tree.get_node(id_node)
    #print node.identifier, node.tag
    if len(node.fpointer) == 0:
        return
    for i in xrange(len(node.fpointer)):
        showDepth(tree, node.fpointer[i])



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str,
                        help="path to the file containing rst_dt",
                        default='./output/exemple.rst')
    parser.add_argument('output_dir', type=str,
                        help="path to the directory used for the generation of the dep_dt",
                        default='./output/')
    args = parser.parse_args()

    rst_dt = RST_DT()
    rst_dt.load(args.input_file)
    dep_dt = rst_dt.toDEP()
    fname = args.input_file.split('/')[-1].split('.')[0] + '.dep'
    dep_dt.save(args.output_dir, fname)
    


