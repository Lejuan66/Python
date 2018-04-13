#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 2: Search String Replacement
 
Team Number: 
Student Names: 
'''
import unittest
# Sample matrix provided by us:
from string import ascii_lowercase


def build_diff_array(u, r, R):
    """
    Sig:    string, string, int[0..|A|, 0..|A|] ==> int[0...|u|][0...|r|]
    Pre:    u, r, are strings for which the difference matrix will be built
            R is a not necessarily symetric matrix of letter difference costs
    Post:    u and v have a dash character appended to the beginning
    """
    # Dash is added for the dynamic programming matrix purposes
    u = '-' + u
    r = '-' + r

    # Type: int[0..len(u)][0..len(r)]
    # Matrix, whose elements are minimal difference scores for corresponding
    # sub-strings (description of those sub-strings below)
    diff_array = [[None for m in range(len(r))] for n in range(len(u))]

    # First word constitutes a column vector in the difference matrix
    # Invariant: rows diff_array[0..i-1] contain min difference scores for substring
    #            u[0:i-1] in compare to all sub-strings r[0] to r[len(r)-1] respectively
    # Variant: i
    for i in range(len(u)):
        # Second word constitutes a row vector in the difference matrix
        # Invariant: columns diff_array[i][0...j-1] contain min difference scores between
        #            substring u[0:i] and sub-strings r[0] to r[j-1]
        # Variant: j
        for j in range(len(r)):

            # First cell of the matrix, for which the rules below don't apply
            if i == 0 and j == 0:
                diff_array[i][j] = R[u[i]][r[j]]
                continue

            # Finding two most similar sub-strings with the smallest difference cost
            # Cost of infinity indicates going out of array.
            subsolution = diff_array[i - 1][j - 1] if j > 0 and i > 0 else float("inf")
            subsolution1 = diff_array[i][j - 1] if j > 0 else float("inf")
            subsolution2 = diff_array[i - 1][j] if i > 0 else float("inf")

            # Case, when the current two letters are the same
            if u[i] == r[j]:
                diff_array[i][j] = subsolution
                continue

            # Case, when the current two letters differ
            # Evaluating the current strings constellation with use of their sub-strings
            # with minimal difference. Options are:

            # 1) Optimal sub-solution is achieved by removing a letter from both examined strings
            # Add the difference between the two letters to the optimal sub-solution
            cur_solution = subsolution + R[u[i]][r[j]]
            # 2) Optimal sub-solution is achieved by removing a letter from the 'r' string
            # Add the difference between the letter and the dash
            cur_solution1 = subsolution1 + R['-'][r[j]]
            # 3) Optimal sub-solution is achieved by removing a letter from the 'u' string
            # Add the difference between the letter and the dash
            cur_solution2 = subsolution2 + R[u[i]]['-']

            min_solution = min(cur_solution, cur_solution1, cur_solution2)
            diff_array[i][j] = min_solution

    return diff_array


# Solution to part b:
def difference(u, r, R):
    """
    Sig:    string, string, int[0..|A|, 0..|A|] ==> int
    Pre:    
    Post:    
    Example: difference("dynamic","dinamck",R) ==> 3
    """
    diff_array = build_diff_array(u, r, R)
    return diff_array[len(u)][len(r)]


# Solution to part c:
def difference_align(u, r, R):
    """
    Sig:    string, string, int[0..|A|, 0..|A|] ==> int, string, string
    Pre:    
    Post:    
    Example: difference_align("dynamic","dinamck",R) ==> 
                                    3, "dynamic-", "dinam-ck"
    """
    diff_array = build_diff_array(u, r, R)

    string1 = ''
    string2 = ''

    j = len(r)
    i = len(u)

    # Invariant:    diff_array[i][j] holds the smallest value among diff_array[i+1][j+1],
    #               diff_array[i][j+1] and diff_array[i+1][j]
    # Variant:      i, j both being the lengths of the corresponding strings at the start
    #               and decreasing to 0. The decrease reflect the backtrack route
    #               through the difference matrix
    while j > 0 or i > 0:
        subsolution = diff_array[i - 1][j - 1] if j > 0 and i > 0 else float("inf")
        subsolution1 = diff_array[i][j - 1] if j > 0 else float("inf")
        subsolution2 = diff_array[i - 1][j] if i > 0 else float("inf")

        min_subsol = min(subsolution, subsolution1, subsolution2)
        if subsolution == min_subsol:
            string1 += u[i - 1]
            string2 += r[j - 1]
            i -= 1
            j -= 1
        elif subsolution1 == min_subsol:
            string1 += '-'
            string2 += r[j - 1]
            j -= 1
        elif subsolution2 == min_subsol:
            string1 += u[i - 1]
            string2 += '-'
            i -= 1

    return [diff_array[len(u)][len(r)], revert_string(string1), revert_string(string2)]


def revert_string(s):
    """
    Sig:    string ==> string
    Pre:    s is string, for which the order of letter will be reverted
    Post:   return a string with the same letters as s, but reverse order
    """
    reverted = [''] * len(s)
    # Invariant:    reverted[len(s)-i-1: len(s)] contains letters s[0:i]
    #               in reverse order
    # Variant:      i
    for i in range(len(s)):
        reverted[len(s) - i - 1] = s[i]
    return ''.join(reverted)


def qwerty_distance():
    """Generates a QWERTY Manhattan distance resemblance matrix
     
    Costs for letter pairs are based on the Manhattan distance of the
    corresponding keys on a standard QWERTY keyboard.
    Costs for skipping a character depends on its placement on the keyboard:
    adding a character has a higher cost for keys on the outer edges,
    deleting a character has a higher cost for keys near the middle.
     
    Usage:
        R = qwerty_distance()
        R['a']['b]  # result: 5
    """
    from collections import defaultdict
    import math

    R = defaultdict(dict)
    R['-']['-'] = 0
    zones = ["dfghjk", "ertyuislcvbnm", "qwazxpo"]
    keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for num, content in enumerate(zones):
        for char in content:
            R['-'][char] = num + 1
            R[char]['-'] = 3 - num
    for a in ascii_lowercase:
        rowA = None
        posA = None
        for num, content in enumerate(keyboard):
            if a in content:
                rowA = num
                posA = content.index(a)
        for b in ascii_lowercase:
            for rowB, contentB in enumerate(keyboard):
                if b in contentB:
                    R[a][b] = math.fabs(rowB - rowA) + math.fabs(posA - contentB.index(b))
    return R


class DifferenceTest(unittest.TestCase):
    """Test Suite for search string replacement problem
     
    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own test
    cases if you wish. 
    (You may delete this class from your submitted solution.)
    """

    def test_diff_sanity(self):
        """Difference sanity test
         
        Given a simple resemblance matrix, test that the reported 
        difference is the expected minimum. Do NOT assume we will always
        use this resemblance matrix when testing!
        """
        A = qwerty_distance()
        alphabet = ascii_lowercase + '-'
        R = {
        '-': {'-': 0, 'a': 3, 'c': 2, 'b': 2, 'e': 2, 'd': 1, 'g': 1, 'f': 1, 'i': 2, 'h': 1, 'k': 1, 'j': 1, 'm': 2,
              'l': 2, 'o': 3, 'n': 2, 'q': 3, 'p': 3, 's': 2, 'r': 2, 'u': 2, 't': 2, 'w': 3, 'v': 2, 'y': 2, 'x': 3,
              'z': 3},
        'a': {'-': 1, 'a': 0.0, 'c': 3.0, 'b': 5.0, 'e': 3.0, 'd': 2.0, 'g': 4.0, 'f': 3.0, 'i': 8.0, 'h': 5.0,
              'k': 7.0, 'j': 6.0, 'm': 7.0, 'l': 8.0, 'o': 9.0, 'n': 6.0, 'q': 1.0, 'p': 10.0, 's': 1.0, 'r': 4.0,
              'u': 7.0, 't': 5.0, 'w': 2.0, 'v': 4.0, 'y': 6.0, 'x': 2.0, 'z': 1.0},
        'c': {'-': 2, 'a': 3.0, 'c': 0.0, 'b': 2.0, 'e': 2.0, 'd': 1.0, 'g': 3.0, 'f': 2.0, 'i': 7.0, 'h': 4.0,
              'k': 6.0, 'j': 5.0, 'm': 4.0, 'l': 7.0, 'o': 8.0, 'n': 3.0, 'q': 4.0, 'p': 9.0, 's': 2.0, 'r': 3.0,
              'u': 6.0, 't': 4.0, 'w': 3.0, 'v': 1.0, 'y': 5.0, 'x': 1.0, 'z': 2.0},
        'b': {'-': 2, 'a': 5.0, 'c': 2.0, 'b': 0.0, 'e': 4.0, 'd': 3.0, 'g': 1.0, 'f': 2.0, 'i': 5.0, 'h': 2.0,
              'k': 4.0, 'j': 3.0, 'm': 2.0, 'l': 5.0, 'o': 6.0, 'n': 1.0, 'q': 6.0, 'p': 7.0, 's': 4.0, 'r': 3.0,
              'u': 4.0, 't': 2.0, 'w': 5.0, 'v': 1.0, 'y': 3.0, 'x': 3.0, 'z': 4.0},
        'e': {'-': 2, 'a': 3.0, 'c': 2.0, 'b': 4.0, 'e': 0.0, 'd': 1.0, 'g': 3.0, 'f': 2.0, 'i': 5.0, 'h': 4.0,
              'k': 6.0, 'j': 5.0, 'm': 6.0, 'l': 7.0, 'o': 6.0, 'n': 5.0, 'q': 2.0, 'p': 7.0, 's': 2.0, 'r': 1.0,
              'u': 4.0, 't': 2.0, 'w': 1.0, 'v': 3.0, 'y': 3.0, 'x': 3.0, 'z': 4.0},
        'd': {'-': 3, 'a': 2.0, 'c': 1.0, 'b': 3.0, 'e': 1.0, 'd': 0.0, 'g': 2.0, 'f': 1.0, 'i': 6.0, 'h': 3.0,
              'k': 5.0, 'j': 4.0, 'm': 5.0, 'l': 6.0, 'o': 7.0, 'n': 4.0, 'q': 3.0, 'p': 8.0, 's': 1.0, 'r': 2.0,
              'u': 5.0, 't': 3.0, 'w': 2.0, 'v': 2.0, 'y': 4.0, 'x': 2.0, 'z': 3.0},
        'g': {'-': 3, 'a': 4.0, 'c': 3.0, 'b': 1.0, 'e': 3.0, 'd': 2.0, 'g': 0.0, 'f': 1.0, 'i': 4.0, 'h': 1.0,
              'k': 3.0, 'j': 2.0, 'm': 3.0, 'l': 4.0, 'o': 5.0, 'n': 2.0, 'q': 5.0, 'p': 6.0, 's': 3.0, 'r': 2.0,
              'u': 3.0, 't': 1.0, 'w': 4.0, 'v': 2.0, 'y': 2.0, 'x': 4.0, 'z': 5.0},
        'f': {'-': 3, 'a': 3.0, 'c': 2.0, 'b': 2.0, 'e': 2.0, 'd': 1.0, 'g': 1.0, 'f': 0.0, 'i': 5.0, 'h': 2.0,
              'k': 4.0, 'j': 3.0, 'm': 4.0, 'l': 5.0, 'o': 6.0, 'n': 3.0, 'q': 4.0, 'p': 7.0, 's': 2.0, 'r': 1.0,
              'u': 4.0, 't': 2.0, 'w': 3.0, 'v': 1.0, 'y': 3.0, 'x': 3.0, 'z': 4.0},
        'i': {'-': 2, 'a': 8.0, 'c': 7.0, 'b': 5.0, 'e': 5.0, 'd': 6.0, 'g': 4.0, 'f': 5.0, 'i': 0.0, 'h': 3.0,
              'k': 1.0, 'j': 2.0, 'm': 3.0, 'l': 2.0, 'o': 1.0, 'n': 4.0, 'q': 7.0, 'p': 2.0, 's': 7.0, 'r': 4.0,
              'u': 1.0, 't': 3.0, 'w': 6.0, 'v': 6.0, 'y': 2.0, 'x': 8.0, 'z': 9.0},
        'h': {'-': 3, 'a': 5.0, 'c': 4.0, 'b': 2.0, 'e': 4.0, 'd': 3.0, 'g': 1.0, 'f': 2.0, 'i': 3.0, 'h': 0.0,
              'k': 2.0, 'j': 1.0, 'm': 2.0, 'l': 3.0, 'o': 4.0, 'n': 1.0, 'q': 6.0, 'p': 5.0, 's': 4.0, 'r': 3.0,
              'u': 2.0, 't': 2.0, 'w': 5.0, 'v': 3.0, 'y': 1.0, 'x': 5.0, 'z': 6.0},
        'k': {'-': 3, 'a': 7.0, 'c': 6.0, 'b': 4.0, 'e': 6.0, 'd': 5.0, 'g': 3.0, 'f': 4.0, 'i': 1.0, 'h': 2.0,
              'k': 0.0, 'j': 1.0, 'm': 2.0, 'l': 1.0, 'o': 2.0, 'n': 3.0, 'q': 8.0, 'p': 3.0, 's': 6.0, 'r': 5.0,
              'u': 2.0, 't': 4.0, 'w': 7.0, 'v': 5.0, 'y': 3.0, 'x': 7.0, 'z': 8.0},
        'j': {'-': 3, 'a': 6.0, 'c': 5.0, 'b': 3.0, 'e': 5.0, 'd': 4.0, 'g': 2.0, 'f': 3.0, 'i': 2.0, 'h': 1.0,
              'k': 1.0, 'j': 0.0, 'm': 1.0, 'l': 2.0, 'o': 3.0, 'n': 2.0, 'q': 7.0, 'p': 4.0, 's': 5.0, 'r': 4.0,
              'u': 1.0, 't': 3.0, 'w': 6.0, 'v': 4.0, 'y': 2.0, 'x': 6.0, 'z': 7.0},
        'm': {'-': 2, 'a': 7.0, 'c': 4.0, 'b': 2.0, 'e': 6.0, 'd': 5.0, 'g': 3.0, 'f': 4.0, 'i': 3.0, 'h': 2.0,
              'k': 2.0, 'j': 1.0, 'm': 0.0, 'l': 3.0, 'o': 4.0, 'n': 1.0, 'q': 8.0, 'p': 5.0, 's': 6.0, 'r': 5.0,
              'u': 2.0, 't': 4.0, 'w': 7.0, 'v': 3.0, 'y': 3.0, 'x': 5.0, 'z': 6.0},
        'l': {'-': 2, 'a': 8.0, 'c': 7.0, 'b': 5.0, 'e': 7.0, 'd': 6.0, 'g': 4.0, 'f': 5.0, 'i': 2.0, 'h': 3.0,
              'k': 1.0, 'j': 2.0, 'm': 3.0, 'l': 0.0, 'o': 1.0, 'n': 4.0, 'q': 9.0, 'p': 2.0, 's': 7.0, 'r': 6.0,
              'u': 3.0, 't': 5.0, 'w': 8.0, 'v': 6.0, 'y': 4.0, 'x': 8.0, 'z': 9.0},
        'o': {'-': 1, 'a': 9.0, 'c': 8.0, 'b': 6.0, 'e': 6.0, 'd': 7.0, 'g': 5.0, 'f': 6.0, 'i': 1.0, 'h': 4.0,
              'k': 2.0, 'j': 3.0, 'm': 4.0, 'l': 1.0, 'o': 0.0, 'n': 5.0, 'q': 8.0, 'p': 1.0, 's': 8.0, 'r': 5.0,
              'u': 2.0, 't': 4.0, 'w': 7.0, 'v': 7.0, 'y': 3.0, 'x': 9.0, 'z': 10.0},
        'n': {'-': 2, 'a': 6.0, 'c': 3.0, 'b': 1.0, 'e': 5.0, 'd': 4.0, 'g': 2.0, 'f': 3.0, 'i': 4.0, 'h': 1.0,
              'k': 3.0, 'j': 2.0, 'm': 1.0, 'l': 4.0, 'o': 5.0, 'n': 0.0, 'q': 7.0, 'p': 6.0, 's': 5.0, 'r': 4.0,
              'u': 3.0, 't': 3.0, 'w': 6.0, 'v': 2.0, 'y': 2.0, 'x': 4.0, 'z': 5.0},
        'q': {'-': 1, 'a': 1.0, 'c': 4.0, 'b': 6.0, 'e': 2.0, 'd': 3.0, 'g': 5.0, 'f': 4.0, 'i': 7.0, 'h': 6.0,
              'k': 8.0, 'j': 7.0, 'm': 8.0, 'l': 9.0, 'o': 8.0, 'n': 7.0, 'q': 0.0, 'p': 9.0, 's': 2.0, 'r': 3.0,
              'u': 6.0, 't': 4.0, 'w': 1.0, 'v': 5.0, 'y': 5.0, 'x': 3.0, 'z': 2.0},
        'p': {'-': 1, 'a': 10.0, 'c': 9.0, 'b': 7.0, 'e': 7.0, 'd': 8.0, 'g': 6.0, 'f': 7.0, 'i': 2.0, 'h': 5.0,
              'k': 3.0, 'j': 4.0, 'm': 5.0, 'l': 2.0, 'o': 1.0, 'n': 6.0, 'q': 9.0, 'p': 0.0, 's': 9.0, 'r': 6.0,
              'u': 3.0, 't': 5.0, 'w': 8.0, 'v': 8.0, 'y': 4.0, 'x': 10.0, 'z': 11.0},
        's': {'-': 2, 'a': 1.0, 'c': 2.0, 'b': 4.0, 'e': 2.0, 'd': 1.0, 'g': 3.0, 'f': 2.0, 'i': 7.0, 'h': 4.0,
              'k': 6.0, 'j': 5.0, 'm': 6.0, 'l': 7.0, 'o': 8.0, 'n': 5.0, 'q': 2.0, 'p': 9.0, 's': 0.0, 'r': 3.0,
              'u': 6.0, 't': 4.0, 'w': 1.0, 'v': 3.0, 'y': 5.0, 'x': 1.0, 'z': 2.0},
        'r': {'-': 2, 'a': 4.0, 'c': 3.0, 'b': 3.0, 'e': 1.0, 'd': 2.0, 'g': 2.0, 'f': 1.0, 'i': 4.0, 'h': 3.0,
              'k': 5.0, 'j': 4.0, 'm': 5.0, 'l': 6.0, 'o': 5.0, 'n': 4.0, 'q': 3.0, 'p': 6.0, 's': 3.0, 'r': 0.0,
              'u': 3.0, 't': 1.0, 'w': 2.0, 'v': 2.0, 'y': 2.0, 'x': 4.0, 'z': 5.0},
        'u': {'-': 2, 'a': 7.0, 'c': 6.0, 'b': 4.0, 'e': 4.0, 'd': 5.0, 'g': 3.0, 'f': 4.0, 'i': 1.0, 'h': 2.0,
              'k': 2.0, 'j': 1.0, 'm': 2.0, 'l': 3.0, 'o': 2.0, 'n': 3.0, 'q': 6.0, 'p': 3.0, 's': 6.0, 'r': 3.0,
              'u': 0.0, 't': 2.0, 'w': 5.0, 'v': 5.0, 'y': 1.0, 'x': 7.0, 'z': 8.0},
        't': {'-': 2, 'a': 5.0, 'c': 4.0, 'b': 2.0, 'e': 2.0, 'd': 3.0, 'g': 1.0, 'f': 2.0, 'i': 3.0, 'h': 2.0,
              'k': 4.0, 'j': 3.0, 'm': 4.0, 'l': 5.0, 'o': 4.0, 'n': 3.0, 'q': 4.0, 'p': 5.0, 's': 4.0, 'r': 1.0,
              'u': 2.0, 't': 0.0, 'w': 3.0, 'v': 3.0, 'y': 1.0, 'x': 5.0, 'z': 6.0},
        'w': {'-': 1, 'a': 2.0, 'c': 3.0, 'b': 5.0, 'e': 1.0, 'd': 2.0, 'g': 4.0, 'f': 3.0, 'i': 6.0, 'h': 5.0,
              'k': 7.0, 'j': 6.0, 'm': 7.0, 'l': 8.0, 'o': 7.0, 'n': 6.0, 'q': 1.0, 'p': 8.0, 's': 1.0, 'r': 2.0,
              'u': 5.0, 't': 3.0, 'w': 0.0, 'v': 4.0, 'y': 4.0, 'x': 2.0, 'z': 3.0},
        'v': {'-': 2, 'a': 4.0, 'c': 1.0, 'b': 1.0, 'e': 3.0, 'd': 2.0, 'g': 2.0, 'f': 1.0, 'i': 6.0, 'h': 3.0,
              'k': 5.0, 'j': 4.0, 'm': 3.0, 'l': 6.0, 'o': 7.0, 'n': 2.0, 'q': 5.0, 'p': 8.0, 's': 3.0, 'r': 2.0,
              'u': 5.0, 't': 3.0, 'w': 4.0, 'v': 0.0, 'y': 4.0, 'x': 2.0, 'z': 3.0},
        'y': {'-': 2, 'a': 6.0, 'c': 5.0, 'b': 3.0, 'e': 3.0, 'd': 4.0, 'g': 2.0, 'f': 3.0, 'i': 2.0, 'h': 1.0,
              'k': 3.0, 'j': 2.0, 'm': 3.0, 'l': 4.0, 'o': 3.0, 'n': 2.0, 'q': 5.0, 'p': 4.0, 's': 5.0, 'r': 2.0,
              'u': 1.0, 't': 1.0, 'w': 4.0, 'v': 4.0, 'y': 0.0, 'x': 6.0, 'z': 7.0},
        'x': {'-': 1, 'a': 2.0, 'c': 1.0, 'b': 3.0, 'e': 3.0, 'd': 2.0, 'g': 4.0, 'f': 3.0, 'i': 8.0, 'h': 5.0,
              'k': 7.0, 'j': 6.0, 'm': 5.0, 'l': 8.0, 'o': 9.0, 'n': 4.0, 'q': 3.0, 'p': 10.0, 's': 1.0, 'r': 4.0,
              'u': 7.0, 't': 5.0, 'w': 2.0, 'v': 2.0, 'y': 6.0, 'x': 0.0, 'z': 1.0},
        'z': {'-': 1, 'a': 1.0, 'c': 2.0, 'b': 4.0, 'e': 4.0, 'd': 3.0, 'g': 5.0, 'f': 4.0, 'i': 9.0, 'h': 6.0,
              'k': 8.0, 'j': 7.0, 'm': 6.0, 'l': 9.0, 'o': 10.0, 'n': 5.0, 'q': 2.0, 'p': 11.0, 's': 2.0, 'r': 5.0,
              'u': 8.0, 't': 6.0, 'w': 3.0, 'v': 3.0, 'y': 7.0, 'x': 1.0, 'z': 0.0}}
        self.assertEqual(difference("hkamvzeq", "bjapirx", R), 15)

        R = {
            '-': {'-': 0, 'a': 50, 'c': 50, 'b': 50, 'e': 50, 'd': 50, 'g': 50, 'f': 50, 'i': 50, 'h': 50, 'k': 50,
                  'j': 50,
                  'm': 50, 'l': 50, 'o': 50, 'n': 50, 'q': 50, 'p': 50, 's': 50, 'r': 50, 'u': 50, 't': 50, 'w': 50,
                  'v': 50, 'y': 50, 'x': 50, 'z': 50},
            'a': {'-': 50, 'a': 0, 'c': 2, 'b': 1, 'e': 4, 'd': 3, 'g': 6, 'f': 5, 'i': 8, 'h': 7, 'k': 10, 'j': 9,
                  'm': 12,
                  'l': 11, 'o': 14, 'n': 13, 'q': 16, 'p': 15, 's': 18, 'r': 17, 'u': 20, 't': 19, 'w': 22, 'v': 21,
                  'y': 24, 'x': 23, 'z': 25},
            'c': {'-': 50, 'a': 2, 'c': 0, 'b': 1, 'e': 2, 'd': 1, 'g': 4, 'f': 3, 'i': 6, 'h': 5, 'k': 8, 'j': 7,
                  'm': 10,
                  'l': 9, 'o': 12, 'n': 11, 'q': 14, 'p': 13, 's': 16, 'r': 15, 'u': 18, 't': 17, 'w': 20, 'v': 19,
                  'y': 22,
                  'x': 21, 'z': 23},
            'b': {'-': 50, 'a': 1, 'c': 1, 'b': 0, 'e': 3, 'd': 2, 'g': 5, 'f': 4, 'i': 7, 'h': 6, 'k': 9, 'j': 8,
                  'm': 11,
                  'l': 10, 'o': 13, 'n': 12, 'q': 15, 'p': 14, 's': 17, 'r': 16, 'u': 19, 't': 18, 'w': 21, 'v': 20,
                  'y': 23, 'x': 22, 'z': 24},
            'e': {'-': 50, 'a': 4, 'c': 2, 'b': 3, 'e': 0, 'd': 1, 'g': 2, 'f': 1, 'i': 4, 'h': 3, 'k': 6, 'j': 5,
                  'm': 8,
                  'l': 7, 'o': 10, 'n': 9, 'q': 12, 'p': 11, 's': 14, 'r': 13, 'u': 16, 't': 15, 'w': 18, 'v': 17,
                  'y': 20,
                  'x': 19, 'z': 21},
            'd': {'-': 50, 'a': 3, 'c': 1, 'b': 2, 'e': 1, 'd': 0, 'g': 3, 'f': 2, 'i': 5, 'h': 4, 'k': 7, 'j': 6,
                  'm': 9,
                  'l': 8, 'o': 11, 'n': 10, 'q': 13, 'p': 12, 's': 15, 'r': 14, 'u': 17, 't': 16, 'w': 19, 'v': 18,
                  'y': 21,
                  'x': 20, 'z': 22},
            'g': {'-': 50, 'a': 6, 'c': 4, 'b': 5, 'e': 2, 'd': 3, 'g': 0, 'f': 1, 'i': 2, 'h': 1, 'k': 4, 'j': 3,
                  'm': 6,
                  'l': 5, 'o': 8, 'n': 7, 'q': 10, 'p': 9, 's': 12, 'r': 11, 'u': 14, 't': 13, 'w': 16, 'v': 15,
                  'y': 18,
                  'x': 17, 'z': 19},
            'f': {'-': 50, 'a': 5, 'c': 3, 'b': 4, 'e': 1, 'd': 2, 'g': 1, 'f': 0, 'i': 3, 'h': 2, 'k': 5, 'j': 4,
                  'm': 7,
                  'l': 6, 'o': 9, 'n': 8, 'q': 11, 'p': 10, 's': 13, 'r': 12, 'u': 15, 't': 14, 'w': 17, 'v': 16,
                  'y': 19,
                  'x': 18, 'z': 20},
            'i': {'-': 50, 'a': 8, 'c': 6, 'b': 7, 'e': 4, 'd': 5, 'g': 2, 'f': 3, 'i': 0, 'h': 1, 'k': 2, 'j': 1,
                  'm': 4,
                  'l': 3, 'o': 6, 'n': 5, 'q': 8, 'p': 7, 's': 10, 'r': 9, 'u': 12, 't': 11, 'w': 14, 'v': 13, 'y': 16,
                  'x': 15, 'z': 17},
            'h': {'-': 50, 'a': 7, 'c': 5, 'b': 6, 'e': 3, 'd': 4, 'g': 1, 'f': 2, 'i': 1, 'h': 0, 'k': 3, 'j': 2,
                  'm': 5,
                  'l': 4, 'o': 7, 'n': 6, 'q': 9, 'p': 8, 's': 11, 'r': 10, 'u': 13, 't': 12, 'w': 15, 'v': 14, 'y': 17,
                  'x': 16, 'z': 18},
            'k': {'-': 50, 'a': 10, 'c': 8, 'b': 9, 'e': 6, 'd': 7, 'g': 4, 'f': 5, 'i': 2, 'h': 3, 'k': 0, 'j': 1,
                  'm': 2,
                  'l': 1, 'o': 4, 'n': 3, 'q': 6, 'p': 5, 's': 8, 'r': 7, 'u': 10, 't': 9, 'w': 12, 'v': 11, 'y': 14,
                  'x': 13, 'z': 15},
            'j': {'-': 50, 'a': 9, 'c': 7, 'b': 8, 'e': 5, 'd': 6, 'g': 3, 'f': 4, 'i': 1, 'h': 2, 'k': 1, 'j': 0,
                  'm': 3,
                  'l': 2, 'o': 5, 'n': 4, 'q': 7, 'p': 6, 's': 9, 'r': 8, 'u': 11, 't': 10, 'w': 13, 'v': 12, 'y': 15,
                  'x': 14, 'z': 16},
            'm': {'-': 50, 'a': 12, 'c': 10, 'b': 11, 'e': 8, 'd': 9, 'g': 6, 'f': 7, 'i': 4, 'h': 5, 'k': 2, 'j': 3,
                  'm': 0, 'l': 1, 'o': 2, 'n': 1, 'q': 4, 'p': 3, 's': 6, 'r': 5, 'u': 8, 't': 7, 'w': 10, 'v': 9,
                  'y': 12,
                  'x': 11, 'z': 13},
            'l': {'-': 50, 'a': 11, 'c': 9, 'b': 10, 'e': 7, 'd': 8, 'g': 5, 'f': 6, 'i': 3, 'h': 4, 'k': 1, 'j': 2,
                  'm': 1,
                  'l': 0, 'o': 3, 'n': 2, 'q': 5, 'p': 4, 's': 7, 'r': 6, 'u': 9, 't': 8, 'w': 11, 'v': 10, 'y': 13,
                  'x': 12, 'z': 14},
            'o': {'-': 50, 'a': 14, 'c': 12, 'b': 13, 'e': 10, 'd': 11, 'g': 8, 'f': 9, 'i': 6, 'h': 7, 'k': 4, 'j': 5,
                  'm': 2, 'l': 3, 'o': 0, 'n': 1, 'q': 2, 'p': 1, 's': 4, 'r': 3, 'u': 6, 't': 5, 'w': 8, 'v': 7,
                  'y': 10,
                  'x': 9, 'z': 11},
            'n': {'-': 50, 'a': 13, 'c': 11, 'b': 12, 'e': 9, 'd': 10, 'g': 7, 'f': 8, 'i': 5, 'h': 6, 'k': 3, 'j': 4,
                  'm': 1, 'l': 2, 'o': 1, 'n': 0, 'q': 3, 'p': 2, 's': 5, 'r': 4, 'u': 7, 't': 6, 'w': 9, 'v': 8,
                  'y': 11,
                  'x': 10, 'z': 12},
            'q': {'-': 50, 'a': 16, 'c': 14, 'b': 15, 'e': 12, 'd': 13, 'g': 10, 'f': 11, 'i': 8, 'h': 9, 'k': 6,
                  'j': 7,
                  'm': 4, 'l': 5, 'o': 2, 'n': 3, 'q': 0, 'p': 1, 's': 2, 'r': 1, 'u': 4, 't': 3, 'w': 6, 'v': 5,
                  'y': 8,
                  'x': 7, 'z': 9},
            'p': {'-': 50, 'a': 15, 'c': 13, 'b': 14, 'e': 11, 'd': 12, 'g': 9, 'f': 10, 'i': 7, 'h': 8, 'k': 5, 'j': 6,
                  'm': 3, 'l': 4, 'o': 1, 'n': 2, 'q': 1, 'p': 0, 's': 3, 'r': 2, 'u': 5, 't': 4, 'w': 7, 'v': 6,
                  'y': 9,
                  'x': 8, 'z': 10},
            's': {'-': 50, 'a': 18, 'c': 16, 'b': 17, 'e': 14, 'd': 15, 'g': 12, 'f': 13, 'i': 10, 'h': 11, 'k': 8,
                  'j': 9,
                  'm': 6, 'l': 7, 'o': 4, 'n': 5, 'q': 2, 'p': 3, 's': 0, 'r': 1, 'u': 2, 't': 1, 'w': 4, 'v': 3,
                  'y': 6,
                  'x': 5, 'z': 7},
            'r': {'-': 50, 'a': 17, 'c': 15, 'b': 16, 'e': 13, 'd': 14, 'g': 11, 'f': 12, 'i': 9, 'h': 10, 'k': 7,
                  'j': 8,
                  'm': 5, 'l': 6, 'o': 3, 'n': 4, 'q': 1, 'p': 2, 's': 1, 'r': 0, 'u': 3, 't': 2, 'w': 5, 'v': 4,
                  'y': 7,
                  'x': 6, 'z': 8},
            'u': {'-': 50, 'a': 20, 'c': 18, 'b': 19, 'e': 16, 'd': 17, 'g': 14, 'f': 15, 'i': 12, 'h': 13, 'k': 10,
                  'j': 11, 'm': 8, 'l': 9, 'o': 6, 'n': 7, 'q': 4, 'p': 5, 's': 2, 'r': 3, 'u': 0, 't': 1, 'w': 2,
                  'v': 1,
                  'y': 4, 'x': 3, 'z': 5},
            't': {'-': 50, 'a': 19, 'c': 17, 'b': 18, 'e': 15, 'd': 16, 'g': 13, 'f': 14, 'i': 11, 'h': 12, 'k': 9,
                  'j': 10,
                  'm': 7, 'l': 8, 'o': 5, 'n': 6, 'q': 3, 'p': 4, 's': 1, 'r': 2, 'u': 1, 't': 0, 'w': 3, 'v': 2,
                  'y': 5,
                  'x': 4, 'z': 6},
            'w': {'-': 50, 'a': 22, 'c': 20, 'b': 21, 'e': 18, 'd': 19, 'g': 16, 'f': 17, 'i': 14, 'h': 15, 'k': 12,
                  'j': 13, 'm': 10, 'l': 11, 'o': 8, 'n': 9, 'q': 6, 'p': 7, 's': 4, 'r': 5, 'u': 2, 't': 3, 'w': 0,
                  'v': 1,
                  'y': 2, 'x': 1, 'z': 3},
            'v': {'-': 50, 'a': 21, 'c': 19, 'b': 20, 'e': 17, 'd': 18, 'g': 15, 'f': 16, 'i': 13, 'h': 14, 'k': 11,
                  'j': 12, 'm': 9, 'l': 10, 'o': 7, 'n': 8, 'q': 5, 'p': 6, 's': 3, 'r': 4, 'u': 1, 't': 2, 'w': 1,
                  'v': 0,
                  'y': 3, 'x': 2, 'z': 4},
            'y': {'-': 50, 'a': 24, 'c': 22, 'b': 23, 'e': 20, 'd': 21, 'g': 18, 'f': 19, 'i': 16, 'h': 17, 'k': 14,
                  'j': 15, 'm': 12, 'l': 13, 'o': 10, 'n': 11, 'q': 8, 'p': 9, 's': 6, 'r': 7, 'u': 4, 't': 5, 'w': 2,
                  'v': 3, 'y': 0, 'x': 1, 'z': 1},
            'x': {'-': 50, 'a': 23, 'c': 21, 'b': 22, 'e': 19, 'd': 20, 'g': 17, 'f': 18, 'i': 15, 'h': 16, 'k': 13,
                  'j': 14, 'm': 11, 'l': 12, 'o': 9, 'n': 10, 'q': 7, 'p': 8, 's': 5, 'r': 6, 'u': 3, 't': 4, 'w': 1,
                  'v': 2, 'y': 1, 'x': 0, 'z': 2},
            'z': {'-': 50, 'a': 25, 'c': 23, 'b': 24, 'e': 21, 'd': 22, 'g': 19, 'f': 20, 'i': 17, 'h': 18, 'k': 15,
                  'j': 16, 'm': 13, 'l': 14, 'o': 11, 'n': 12, 'q': 9, 'p': 10, 's': 7, 'r': 8, 'u': 5, 't': 6, 'w': 3,
                  'v': 4, 'y': 1, 'x': 2, 'z': 0}}
        self.assertEqual(difference("rzcuaex", "wjhlc", R), 136)

    def test_align_sanity(self):
        """Simple alignment
         
        Passes if the returned alignment matches the expected one.
        """
        alphabet = ascii_lowercase + '-'
        R = dict([(
                      a,
                      dict([(b, (0 if a == b else 1)) for b in alphabet])
                  ) for a in alphabet])
        diff, u, r = difference_align("polynomial", "exponential", R)
        self.assertEqual(diff, 6)
        # # Warning: there may be other optimal matchings!
        self.assertEqual(u, '--polynomial')
        self.assertEqual(r, 'exponen-tial')

    def test_align_sanity2(self):
        R = {'-': {'-': 0, 'a': 50, 'c': 50, 'b': 50, 'e': 50, 'd': 50, 'g': 50, 'f': 50, 'i': 50, 'h': 50, 'k': 50, 'j': 50, 'm': 50, 'l': 50, 'o': 50, 'n': 50, 'q': 50, 'p': 50, 's': 50, 'r': 50, 'u': 50, 't': 50, 'w': 50, 'v': 50, 'y': 50, 'x': 50, 'z': 50}, 'a': {'-': 50, 'a': 0, 'c': 2, 'b': 1, 'e': 4, 'd': 3, 'g': 6, 'f': 5, 'i': 8, 'h': 7, 'k': 10, 'j': 9, 'm': 12, 'l': 11, 'o': 14, 'n': 13, 'q': 16, 'p': 15, 's': 18, 'r': 17, 'u': 20, 't': 19, 'w': 22, 'v': 21, 'y': 24, 'x': 23, 'z': 25}, 'c': {'-': 50, 'a': 2, 'c': 0, 'b': 1, 'e': 2, 'd': 1, 'g': 4, 'f': 3, 'i': 6, 'h': 5, 'k': 8, 'j': 7, 'm': 10, 'l': 9, 'o': 12, 'n': 11, 'q': 14, 'p': 13, 's': 16, 'r': 15, 'u': 18, 't': 17, 'w': 20, 'v': 19, 'y': 22, 'x': 21, 'z': 23}, 'b': {'-': 50, 'a': 1, 'c': 1, 'b': 0, 'e': 3, 'd': 2, 'g': 5, 'f': 4, 'i': 7, 'h': 6, 'k': 9, 'j': 8, 'm': 11, 'l': 10, 'o': 13, 'n': 12, 'q': 15, 'p': 14, 's': 17, 'r': 16, 'u': 19, 't': 18, 'w': 21, 'v': 20, 'y': 23, 'x': 22, 'z': 24}, 'e': {'-': 50, 'a': 4, 'c': 2, 'b': 3, 'e': 0, 'd': 1, 'g': 2, 'f': 1, 'i': 4, 'h': 3, 'k': 6, 'j': 5, 'm': 8, 'l': 7, 'o': 10, 'n': 9, 'q': 12, 'p': 11, 's': 14, 'r': 13, 'u': 16, 't': 15, 'w': 18, 'v': 17, 'y': 20, 'x': 19, 'z': 21}, 'd': {'-': 50, 'a': 3, 'c': 1, 'b': 2, 'e': 1, 'd': 0, 'g': 3, 'f': 2, 'i': 5, 'h': 4, 'k': 7, 'j': 6, 'm': 9, 'l': 8, 'o': 11, 'n': 10, 'q': 13, 'p': 12, 's': 15, 'r': 14, 'u': 17, 't': 16, 'w': 19, 'v': 18, 'y': 21, 'x': 20, 'z': 22}, 'g': {'-': 50, 'a': 6, 'c': 4, 'b': 5, 'e': 2, 'd': 3, 'g': 0, 'f': 1, 'i': 2, 'h': 1, 'k': 4, 'j': 3, 'm': 6, 'l': 5, 'o': 8, 'n': 7, 'q': 10, 'p': 9, 's': 12, 'r': 11, 'u': 14, 't': 13, 'w': 16, 'v': 15, 'y': 18, 'x': 17, 'z': 19}, 'f': {'-': 50, 'a': 5, 'c': 3, 'b': 4, 'e': 1, 'd': 2, 'g': 1, 'f': 0, 'i': 3, 'h': 2, 'k': 5, 'j': 4, 'm': 7, 'l': 6, 'o': 9, 'n': 8, 'q': 11, 'p': 10, 's': 13, 'r': 12, 'u': 15, 't': 14, 'w': 17, 'v': 16, 'y': 19, 'x': 18, 'z': 20}, 'i': {'-': 50, 'a': 8, 'c': 6, 'b': 7, 'e': 4, 'd': 5, 'g': 2, 'f': 3, 'i': 0, 'h': 1, 'k': 2, 'j': 1, 'm': 4, 'l': 3, 'o': 6, 'n': 5, 'q': 8, 'p': 7, 's': 10, 'r': 9, 'u': 12, 't': 11, 'w': 14, 'v': 13, 'y': 16, 'x': 15, 'z': 17}, 'h': {'-': 50, 'a': 7, 'c': 5, 'b': 6, 'e': 3, 'd': 4, 'g': 1, 'f': 2, 'i': 1, 'h': 0, 'k': 3, 'j': 2, 'm': 5, 'l': 4, 'o': 7, 'n': 6, 'q': 9, 'p': 8, 's': 11, 'r': 10, 'u': 13, 't': 12, 'w': 15, 'v': 14, 'y': 17, 'x': 16, 'z': 18}, 'k': {'-': 50, 'a': 10, 'c': 8, 'b': 9, 'e': 6, 'd': 7, 'g': 4, 'f': 5, 'i': 2, 'h': 3, 'k': 0, 'j': 1, 'm': 2, 'l': 1, 'o': 4, 'n': 3, 'q': 6, 'p': 5, 's': 8, 'r': 7, 'u': 10, 't': 9, 'w': 12, 'v': 11, 'y': 14, 'x': 13, 'z': 15}, 'j': {'-': 50, 'a': 9, 'c': 7, 'b': 8, 'e': 5, 'd': 6, 'g': 3, 'f': 4, 'i': 1, 'h': 2, 'k': 1, 'j': 0, 'm': 3, 'l': 2, 'o': 5, 'n': 4, 'q': 7, 'p': 6, 's': 9, 'r': 8, 'u': 11, 't': 10, 'w': 13, 'v': 12, 'y': 15, 'x': 14, 'z': 16}, 'm': {'-': 50, 'a': 12, 'c': 10, 'b': 11, 'e': 8, 'd': 9, 'g': 6, 'f': 7, 'i': 4, 'h': 5, 'k': 2, 'j': 3, 'm': 0, 'l': 1, 'o': 2, 'n': 1, 'q': 4, 'p': 3, 's': 6, 'r': 5, 'u': 8, 't': 7, 'w': 10, 'v': 9, 'y': 12, 'x': 11, 'z': 13}, 'l': {'-': 50, 'a': 11, 'c': 9, 'b': 10, 'e': 7, 'd': 8, 'g': 5, 'f': 6, 'i': 3, 'h': 4, 'k': 1, 'j': 2, 'm': 1, 'l': 0, 'o': 3, 'n': 2, 'q': 5, 'p': 4, 's': 7, 'r': 6, 'u': 9, 't': 8, 'w': 11, 'v': 10, 'y': 13, 'x': 12, 'z': 14}, 'o': {'-': 50, 'a': 14, 'c': 12, 'b': 13, 'e': 10, 'd': 11, 'g': 8, 'f': 9, 'i': 6, 'h': 7, 'k': 4, 'j': 5, 'm': 2, 'l': 3, 'o': 0, 'n': 1, 'q': 2, 'p': 1, 's': 4, 'r': 3, 'u': 6, 't': 5, 'w': 8, 'v': 7, 'y': 10, 'x': 9, 'z': 11}, 'n': {'-': 50, 'a': 13, 'c': 11, 'b': 12, 'e': 9, 'd': 10, 'g': 7, 'f': 8, 'i': 5, 'h': 6, 'k': 3, 'j': 4, 'm': 1, 'l': 2, 'o': 1, 'n': 0, 'q': 3, 'p': 2, 's': 5, 'r': 4, 'u': 7, 't': 6, 'w': 9, 'v': 8, 'y': 11, 'x': 10, 'z': 12}, 'q': {'-': 50, 'a': 16, 'c': 14, 'b': 15, 'e': 12, 'd': 13, 'g': 10, 'f': 11, 'i': 8, 'h': 9, 'k': 6, 'j': 7, 'm': 4, 'l': 5, 'o': 2, 'n': 3, 'q': 0, 'p': 1, 's': 2, 'r': 1, 'u': 4, 't': 3, 'w': 6, 'v': 5, 'y': 8, 'x': 7, 'z': 9}, 'p': {'-': 50, 'a': 15, 'c': 13, 'b': 14, 'e': 11, 'd': 12, 'g': 9, 'f': 10, 'i': 7, 'h': 8, 'k': 5, 'j': 6, 'm': 3, 'l': 4, 'o': 1, 'n': 2, 'q': 1, 'p': 0, 's': 3, 'r': 2, 'u': 5, 't': 4, 'w': 7, 'v': 6, 'y': 9, 'x': 8, 'z': 10}, 's': {'-': 50, 'a': 18, 'c': 16, 'b': 17, 'e': 14, 'd': 15, 'g': 12, 'f': 13, 'i': 10, 'h': 11, 'k': 8, 'j': 9, 'm': 6, 'l': 7, 'o': 4, 'n': 5, 'q': 2, 'p': 3, 's': 0, 'r': 1, 'u': 2, 't': 1, 'w': 4, 'v': 3, 'y': 6, 'x': 5, 'z': 7}, 'r': {'-': 50, 'a': 17, 'c': 15, 'b': 16, 'e': 13, 'd': 14, 'g': 11, 'f': 12, 'i': 9, 'h': 10, 'k': 7, 'j': 8, 'm': 5, 'l': 6, 'o': 3, 'n': 4, 'q': 1, 'p': 2, 's': 1, 'r': 0, 'u': 3, 't': 2, 'w': 5, 'v': 4, 'y': 7, 'x': 6, 'z': 8}, 'u': {'-': 50, 'a': 20, 'c': 18, 'b': 19, 'e': 16, 'd': 17, 'g': 14, 'f': 15, 'i': 12, 'h': 13, 'k': 10, 'j': 11, 'm': 8, 'l': 9, 'o': 6, 'n': 7, 'q': 4, 'p': 5, 's': 2, 'r': 3, 'u': 0, 't': 1, 'w': 2, 'v': 1, 'y': 4, 'x': 3, 'z': 5}, 't': {'-': 50, 'a': 19, 'c': 17, 'b': 18, 'e': 15, 'd': 16, 'g': 13, 'f': 14, 'i': 11, 'h': 12, 'k': 9, 'j': 10, 'm': 7, 'l': 8, 'o': 5, 'n': 6, 'q': 3, 'p': 4, 's': 1, 'r': 2, 'u': 1, 't': 0, 'w': 3, 'v': 2, 'y': 5, 'x': 4, 'z': 6}, 'w': {'-': 50, 'a': 22, 'c': 20, 'b': 21, 'e': 18, 'd': 19, 'g': 16, 'f': 17, 'i': 14, 'h': 15, 'k': 12, 'j': 13, 'm': 10, 'l': 11, 'o': 8, 'n': 9, 'q': 6, 'p': 7, 's': 4, 'r': 5, 'u': 2, 't': 3, 'w': 0, 'v': 1, 'y': 2, 'x': 1, 'z': 3}, 'v': {'-': 50, 'a': 21, 'c': 19, 'b': 20, 'e': 17, 'd': 18, 'g': 15, 'f': 16, 'i': 13, 'h': 14, 'k': 11, 'j': 12, 'm': 9, 'l': 10, 'o': 7, 'n': 8, 'q': 5, 'p': 6, 's': 3, 'r': 4, 'u': 1, 't': 2, 'w': 1, 'v': 0, 'y': 3, 'x': 2, 'z': 4}, 'y': {'-': 50, 'a': 24, 'c': 22, 'b': 23, 'e': 20, 'd': 21, 'g': 18, 'f': 19, 'i': 16, 'h': 17, 'k': 14, 'j': 15, 'm': 12, 'l': 13, 'o': 10, 'n': 11, 'q': 8, 'p': 9, 's': 6, 'r': 7, 'u': 4, 't': 5, 'w': 2, 'v': 3, 'y': 0, 'x': 1, 'z': 1}, 'x': {'-': 50, 'a': 23, 'c': 21, 'b': 22, 'e': 19, 'd': 20, 'g': 17, 'f': 18, 'i': 15, 'h': 16, 'k': 13, 'j': 14, 'm': 11, 'l': 12, 'o': 9, 'n': 10, 'q': 7, 'p': 8, 's': 5, 'r': 6, 'u': 3, 't': 4, 'w': 1, 'v': 2, 'y': 1, 'x': 0, 'z': 2}, 'z': {'-': 50, 'a': 25, 'c': 23, 'b': 24, 'e': 21, 'd': 22, 'g': 19, 'f': 20, 'i': 17, 'h': 18, 'k': 15, 'j': 16, 'm': 13, 'l': 14, 'o': 11, 'n': 12, 'q': 9, 'p': 10, 's': 7, 'r': 8, 'u': 5, 't': 6, 'w': 3, 'v': 4, 'y': 1, 'x': 2, 'z': 0}}

        diff, u, r = difference_align("dugxmyq", "hqbwugcrnsd", R)
        self.assertEqual(diff, 228)
        self.assertEqual(u, 'dugxmyq----')
        self.assertEqual(r, 'hqbwugcrnsd')


if __name__ == '__main__':
    unittest.main()
