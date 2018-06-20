import cvxpy as cp
from numpy import ones, maximum, minimum, sign, floor, ceil

"""
Abstract loss class and canonical loss functions.
"""

# Abstract Loss class


class Loss(object):
    def __init__(self, A): return

    def loss(self, A, U): raise NotImplementedError("Override me!")

    def encode(self, A): return A  # default

    def decode(self, A): return A  # default

    def __str__(self): return "GLRM Loss: override me!"

    def __call__(self, A, U): return self.loss(A, U)

# Canonical loss functions


class QuadraticLoss(Loss):
    def loss(self, A, U): return cp.norm(cp.Constant(A) - U, "fro")/2.0

    def __str__(self): return "quadratic loss"


class HuberLoss(Loss):
    a = 1.0  # XXX does the value of 'a' propagate if we update it?

    def loss(self, A, U): return cp.sum_entries(
        cp.huber(cp.Constant(A) - U, self.a))

    def __str__(self): return "huber loss"

# class FractionalLoss(Loss):
#     PRECISION = 1e-10
#     def loss(self, A, U):
#         B = cp.Constant(A)
#         U = cp.max_elemwise(U, self.PRECISION) # to avoid dividing by zero
#         return cp.max_elemwise(cp.mul_elemwise(cp.inv_pos(cp.pos(U)), B-U), \
#         return maximum((A - U)/U, (U - A)/A)
#


class HingeLoss(Loss):
    def loss(self, A, U): return cp.sum_entries(
        cp.pos(ones(A.shape)-cp.mul_elemwise(cp.Constant(A), U)))

    def decode(self, A): return sign(A)  # return back to Boolean

    def __str__(self): return "hinge loss"


class OrdinalLoss(Loss):
    def __init__(self, A):
        self.Amax, self.Amin = A.max(), A.min()

    def loss(self, A, U):
        return cp.sum_entries(sum(cp.mul_elemwise(1*(b >= A),
                                                  cp.pos(U-b*ones(A.shape))) + cp.mul_elemwise(1*(b < A),
                                                                                               cp.pos(-U + (b+1)*ones(A.shape))) for b in range(int(self.Amin), int(self.Amax))))

    def decode(self, A): return maximum(
        minimum(A.round(), self.Amax), self.Amin)

    def __str__(self): return "ordinal loss"
