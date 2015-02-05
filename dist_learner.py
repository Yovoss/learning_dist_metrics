"""
Learning Distance Metrics Algorithm
"""
import time
import numpy as np 
import pandas as pd 
import scipy as sp 
from scipy.optimize import minimize

from dist_metrics import weighted_euclidean
from dist_metrics import pairwise_dist_wrapper
from dist_metrics import all_pairwise_dist
from dist_metrics import sum_grouped_dist
from dist_metrics import squared_sum_grouped_dist

class LDM(object):
    """Learning Distance Metrics (LDM)

    An aglorithm learning distance metrics in a supervsied
    context to tighten spreads of points known similar and
    amplify separation of points considered different in
    a transformed space. 

    Parameters:
    -----------

    Attributes:
    -----------
    _trans_vec: array, [n_features, ]
        The A matrix transforming the original datasets

    _ratio: float
        The ratio of sum distances of transformed points known similar
        over its couterpart of tarnsformed points known different
	"""

    def __init__(self, dist_func = None, report_excution_time= True):
    	self._dist_func = dist_func
    	self._transform_matrix = np.array([])
    	self._ratio = 1
    	self.report_excution_time = report_excution_time
        pass 

    def fit(self, X, S, D):
        """Fit the model with X and given S and D

        Parameters:
        -----------

        Retruns:
        --------
        """
        self._fit(X, S, D)
        return self 

    def fit_transform(self, X):
    	"""Fit the model with X, S, D and conduct transformation on X

    	Parameters:
    	-----------
    	X: {matrix-like, np.array}, shape (n_sample, n_features)
    		Training data, where n_samples is the number of n_samples
    		and n_features is the number of features 

    	Returns:
    	--------
    	X_new: {marix-like, np.array}, shape (n_sample, n_features)
    		The return of X transformed by fitted matrix A
    	"""
    	pass 

    def _fit(self, X, S, D):
        """Fit the model with given information: X, S, D

        Parameters:
        ----------
        X: {matrix-like, np.array}, shape (n_sample, n_features)
    	    Training data, where n_samples is the number of n_samples
    	    and n_features is the number of features 
        S: {vector-like, list} a list of tuples which define a pair of
                  data points known as similiar 
        D: {vector-like, list} a list of tuples which define a pair of
                  data points known as different

        Returns:
        --------
        _trans_vec: {matrix-like, np.array}, shape(n_features, n_features)
    	       A transformation matrix (A) 
    	_ratio: float
        """
        n_sample, n_features = X.shape

        bnds = [(0, None)] * n_features # boundaries
        init = [1] * n_features # initial weights

        def objective_func(w):
            a = squared_sum_grouped_dist(S, X, w) * 1.0
            b = squared_sum_grouped_dist(D, X, w) * 1.0
            return a / b

        start_time = time.time()

        fitted = minimize(objective_func, init, method="L-BFGS-B", bounds = bnds)

        duration = time.time() - start_time
        if self.report_excution_time:
            print("--- %s seconds ---" % duration)

        self._transform_matrix = fitted.x
        self._ratio = fitted.fun / objective_func(init)

        return (self._transform_matrix, self._ratio)

    def transform(self, X):
    	"""Tranform X by the learned tranformation matrix (A)

    	Parameters:
    	-----------
    	X: {matrix-like, np.array}, shape (n_sample, n_features)
    		Training data, where n_samples is the number of n_samples
    		and n_features is the number of features 

    	Returns:
    	--------
    	X_new: {marix-like, np.array}, shape (n_sample, n_features)
    		The return of X transformed by fitted matrix A
    	"""
    	pass

    def get_transform_matrix(self):
    	"""Returned the fitted transformation matrix (A)

    	Returns:
    	-------
    	_trans_vec: {matrix-like, np.array}, shape(n_features, n_features)
    	       A transformation matrix (A) 
    	"""
    	return self._transform_matrix

    def get_dist_func(self):
        """Returned the distance functions used in fitting model 

        Returns:
        --------
        func: {function} a function accept (x1, x2, *arg)
        """
        return self._dist_func

    def get_ratio(self):
        """The ratio of aggregate metrics of similiar points 
           over the couterparts of different points
        """
        return self._ratio



