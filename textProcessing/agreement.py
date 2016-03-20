__author__ = 'mladen'
import numpy as np


class aggreement():
    def generateMatrix(self):
        matrix = np.zeros(shape=(100, 3))
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
            matrix[(i - 1, j)] += 1
        return matrix

    def kappaCoeff(self, ratings, n):
        items = set()
        categories = set()
        nij = {}

        for i, c in ratings:
            items.add(i)
            categories.add(c)
            nij[(i, c)] = nij.get((i, c), 0) + 1

        N = len(items)

        pj = {}
        for c in categories:
            pj[c] = sum(nij.get((i, c), 0) for i in items) / (1.0 * n * N)

        P_i = {}
        for i in items:
            P_i[i] = (sum(nij.get((i, c), 0) ** 2 for c in categories) - n) / (n * (n - 1.0))

        P = sum(P_i.itervalues()) / (1.0 * N)
        Pe = sum(pj[c] ** 2 for c in categories)

        coeff = (P - Pe) / (1 - Pe)

        return coeff


if __name__ == "__main__":
    example = ([(1, 1)] * 1 + [(1, 2)] * 1 +
               [(2, 1)] * 2 +
               [(3, 1)] * 2 +
               [(4, 3)] * 2 +
               [(5, 1)] * 1 + [(5, 3)] * 1 +
               [(6, 3)] * 1 + [(6, 2)] * 1 +
               [(7, 1)] * 2 +
               [(8, 3)] * 2 +
               [(9, 1)] * 1 + [(9, 2)] * 1 +
               [(10, 3)] * 2 +
               [(11, 1)] * 1 + [(11, 3)] * 1 +
               [(12, 3)] * 2 +
               [(13, 1)] * 1 + [(13, 2)] * 1)
    kappa = aggreement()
    print kappa.kappaCoeff(example, 2)
