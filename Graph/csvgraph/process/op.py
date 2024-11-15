#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math

#from . import *

#####################################

def AVG(li):
	"""
	Return the average of the elements in the list
	"""
	return float(sum(li))/float(len(li))

def CNT(li):
	"""
	Return the count of the elements in the list
	"""
	return len(li)

def DEV(li):
	"""
	Return the standard deviation of the elements in the list, computed using the E[x^2]-E^2[x] estimator.
	"""
	m=AVG(li)
	m2=AVG([x*x for x in li])
	var=m2-m*m	
	return math.sqrt(var)

def VAR(li):
	"""
	Return the variance of the elements in the list, computed using the E[x^2]-E^2[x] estimator.
	"""
	m=AVG(li)
	m2=AVG([x*x for x in li])
	var=m2-m*m	
	return var

