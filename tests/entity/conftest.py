"""G0~G3 grid placeholders for Logic RED skeletons (Report/09).

Fixtures are comment-only until GREEN; use literals in test docstrings/comments.
"""

# G0 — complete 4x4 magic square (M=34):
# [[16, 2,  3, 13],
#  [ 5, 11, 10,  8],
#  [ 9,  7,  6, 12],
#  [ 4, 14, 15,  1]]
#
# G1 — partial; blanks (2,2),(3,3) 1-index; missing {7, 10}:
# [[16, 2,  3, 13],
#  [ 5,  0,  8, 12],
#  [ 9,  6,  0,  4],
#  [14, 15,  1, 11]]
#
# G2 — PRD D-02; Step A fail / Step B success → [3,3,6,4,4,1] (TBD verify in Report/09):
# [[16, 2,  3, 13],
#  [ 5, 11, 10,  8],
#  [ 9,  7,  0, 12],
#  [ 4, 14, 15,  0]]
#
# G3 — unsolvable partial (placeholder; replace when Report/02 appendix is fixed):
# [[ 0,  2,  3, 13],
#  [ 5, 11, 10,  8],
#  [ 9,  7,  6, 12],
#  [ 4, 14, 15, 16]]
