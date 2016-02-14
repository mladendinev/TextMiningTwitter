__author__ = 'mladen'
import numpy as np


class aggreement():
    def generateMatrix(self):
        mat = np.zeros(shape=(100, 3))
        annotatedTweets = ''
        raters = ''
        global j
        for i, tweet in enumerate(annotatedTweets):
            for rater in raters:
                if tweet[rater] == 'yes':
                    j = 0
                elif tweet[rater] == 'neutral':
                    j = 1
                else:
                    j = 2
            mat[(i - 1, j)] += 1
        return mat


def kappaCoeff(ratings, n):

    items = set()
    categories = set()
    n_ij = {}

    for i, c in ratings:
        items.add(i)
        categories.add(c)
        n_ij[(i,c)] = n_ij.get((i,c), 0) + 1

    N = len(items)

    p_j = {}
    for c in categories:
        p_j[c] = sum(n_ij.get((i,c), 0) for i in items) / (1.0*n*N)

    P_i = {}
    for i in items:
        P_i[i] = (sum(n_ij.get((i,c), 0)**2 for c in categories)-n) / (n*(n-1.0))

    P_bar = sum(P_i.itervalues()) / (1.0*N)
    P_e_bar = sum(p_j[c]**2 for c in categories)

    coeff = (P_bar - P_e_bar) / (1 - P_e_bar)

    return kappa
