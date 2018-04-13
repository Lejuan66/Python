#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3: Party seating problem

Team Number:
Student Names:
'''
from collections import deque
import unittest

def Is_possible(lists, table0=[], table1=[]):
   
    
    n = len(lists)
    undecided = []
        
    if(n == 0):
        return False
     
    for node in range(len(lists)):
        
        # if person node does not know anyone, he can sit on table0 or table1, we let him sit on table0
        for n in undecided :
            undecided.remove(n)
        for n in lists[node]:
            if(node in table0):  
                if(n in table0): 
                    #table0.remove(n)
                    table0 = []
                    table1 =[]
                    return False, table0,table1
                elif(n not in table1):
                    table1.append(n)
            
            if(node in table1): 
                 if(n in table1):
                     table0 = []
                     table1 =[]
                     return False, table0,table1
                 elif(n not in table0):
                    table0.append(n)
                    
            if (node not in table0 and node not in table1 and n in table0):
                table1.append(node)
                if(len(undecided)):
                    for i in undecided :
                        table0.append(i)
            if (node not in table0 and node not in table1 and n in table1):
                table0.append(node)
                if(len(undecided)):
                    for i in undecided :
                        table1.append(i)
                        
            if(node not in table0 and node not in table1 and n not in table0 and n not in table1):
                undecided.append(n) 
                
        if(node not in table0 and node not in table1):
            table0.append(node)
            for n in lists[node]:
                table1.append(n)
    #print table0, table1
    return True, table0, table1
        
def party(known):
    """
    Sig:    (int list[1..m])[1..n]
                        $\longrightarrow$ boolean, int [1..j], int [1..k]
    Pre:
    Post:
    Ex:     [[1,2],[0],[0]] $\longrightarrow$ True, [0], [1,2]
    """
    
    table0 =[]
    table1 =[]
    return Is_possible(known,table0,table1)
    


class PartySeatingTest(unittest.TestCase):
    """Test suite for party seating problem
    """
    
    def test_sanity(self):
        """Sanity test
    
        A minimal test case.
        """
        K = [[1,2],[0],[0],[]]
        #print party(K)
        (found, A, B) = party(K)
        self.assertEqual(
            len(A) + len(B), 
            len(K), 
            "wrong number of guests: {!s} guests, tables hold {!s} and {!s}".format(
                len(K),
                len(A),
                len(B)
                )
            )
        for g in range(len(K)):
            self.assertTrue(
                g in A or g in B, 
                "Guest {!s} not seated anywhere".format(g))
        for a1 in A:
            for a2 in A:
                self.assertFalse(
                    a2 in K[a1], 
                    "Guests {!s} and {!s} seated together, and know each other".format(
                        a1,
                        a2
                        )
                    )
        for b1 in B:
            for b2 in B:
                self.assertFalse(
                    b2 in K[b1], 
                    "Guests {!s} and {!s} seated together, and know each other".format(
                        b1,
                        b2
                        )
                    )
#    def test_sanity2(self):
#        """Sanity test
#    
#        A minimal test case.
#        """
#        K =[[26, 15], [65], [37], [], [], [41, 76, 73], [66, 13], [50], [], [70], [], [62, 46], [73, 76, 47], [6], [24, 58, 27, 62], [0, 50, 61], [], [78], [65, 20], [25, 22], [18], [], [73, 19, 45], [49], [33, 62, 14], [59, 19], [0, 56], [14], [70], [72, 76], [57, 42], [32], [31], [24, 34, 77], [33], [65, 55], [], [2, 78], [], [], [68, 45, 71], [75, 5], [67, 59, 30], [], [], [40, 22], [11], [12], [], [55, 23], [15, 7], [], [59], [77, 78], [], [49, 35], [57, 26], [56, 30], [78, 14], [25, 42, 52], [], [15], [24, 67, 11, 14], [], [], [1, 18, 35], [6], [72, 42, 62], [40], [], [9, 28], [40], [67, 29], [12, 5, 22], [], [41], [12, 5, 29], [33, 53, 78], [17, 58, 37, 77, 53]]
#
##print party(K)
#        (found, A, B) = party(K)
#        self.assertEqual(
#            len(A) + len(B), 
#            len(K), 
#            "wrong number of guests: {!s} guests, tables hold {!s} and {!s}".format(
#                len(K),
#                len(A),
#                len(B)
#                )
#            )
#        for g in range(len(K)):
#            self.assertTrue(
#                g in A or g in B, 
#                "Guest {!s} not seated anywhere".format(g))
#        for a1 in A:
#            for a2 in A:
#                self.assertFalse(
#                    a2 in K[a1], 
#                    "Guests {!s} and {!s} seated together, and know each other".format(
#                        a1,
#                        a2
#                        )
#                    )
#        for b1 in B:
#            for b2 in B:
#                self.assertFalse(
#                    b2 in K[b1], 
#                    "Guests {!s} and {!s} seated together, and know each other".format(
#                        b1,
#                        b2
#                        )
#                    )
#
if __name__ == '__main__':
    unittest.main()