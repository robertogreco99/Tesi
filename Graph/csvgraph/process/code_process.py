#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import copy

# Import the operators to process rows
from csvgraph.process.op import *
import collections

debug=False

######################################################################################################
# Data element
class _DE:
	"""
	Basic class to contain one entry of the data (one csv row). The class (better, the object) contains a list of attributes
	whose name corresponds to that of the column in the csv file. This system makes the data easily accessible from the
	object with the . syntax, e.g., if el is a _DE object, colname can be accessed as el.colname (easier to describe operations on the data).
	"""
	def __init__(self, fieldnames=[], vals=[]):
		if len(vals)>0: # init with values
			for i in range(len(fieldnames)):
				setattr(self, fieldnames[i], vals[i])
		else:  # no initial values
			for i in range(len(fieldnames)):
				setattr(self, fieldnames[i], '')

	def p(self, fieldlist=[]):  # Order of fields to be printed
		if len(fieldlist)==0:
			for k in self.__dict__: # Print in not-predefined order
				print("%s: |%s| " % (k,self.__dict__[k]), end=' ')
			print()
		else:
			for k in range(len(fieldlist)):
				print("%s: |%s| " % (fieldlist[k],self.__dict__[fieldlist[k]]), end=' ')
			print()

	def p_formatted(self, fieldlist, fieldtype, fieldsize):  # Order of fields to be printed
		for k in range(len(fieldlist)):
			if fieldtype[k]=='int':
				formatstr="%%%dd" % (fieldsize[k])
			elif fieldtype[k]=='float':
				formatstr="%%%d.6f" % (fieldsize[k])
			else:
				formatstr="%%-%ds" % (fieldsize[k])
			#print "formatstr=%s" % (formatstr)
			print((formatstr) % (self.__dict__[fieldlist[k]]), end=' ')
		print()


######################################################################################################
def _DE_list_print(li, fieldlist):
	for i in range(len(li)):
		li[i].p(fieldlist)
	

######################################################################################################
# Recursive print since _DT can be nested
def _DT_print(obj, level, formatted=False, header=True):
	if header==True:
		print(' '*3*level, end=' ')
		print("_DT Header fields: %s" % (obj.h))
		print(' '*3*level, end=' ')
		print("_DT Type of fields: %s" % (obj.t))
		print(' '*3*level, end=' ')
		print("_DT Size of fields: %s" % (obj.s))
		print(' '*3*level, end=' ')
		print("_DT Info of fields: %s" % (obj.i))
		print(' '*3*level, end=' ')
		print("_DT Data:")
	le=len(obj.d)
	formatlen="%%%dd" % (len("%d" % le))
	for i in range(len(obj.d)):
		if obj.d[i].__class__.__name__=='_DT':
			print(' '*3*level, end=' ')
			print((formatlen+' _DT:') % (i), end=' ')
			print()
			_DT_print(obj.d[i], level+1, formatted, header)
		else:
			print(' '*3*level, end=' ')
			print((formatlen+' _DE:') % (i), end=' ')
			if formatted:
				obj.d[i].p_formatted(obj.h, obj.t, obj.s)  # Print as _DE
			else:
				obj.d[i].p(obj.h)  # Print as _DE

######################################################################################################
# Recursive duplicate since _DT can be nested
def _DT_dup_ref(obj, level=0):
	new_dt=[]
	for i in range(len(obj.d)):
		if obj.d[i].__class__.__name__ == '_DT':
			new_dt.append( _DT_dup_ref(obj.d[i], level+1) )
		else:
			new_dt.append( obj.d[i] )
	return _DT(obj.h[:], obj.t[:], obj.s[:], copy.deepcopy(obj.i), new_dt)

######################################################################################################
# Data set (bag)
class _DT:
	"""
	Basic class to contain the data set (bag)
	The class contains:

	* h: header info (a python list of column names, in the order in which the data appears in the original csv file)
	* t: type info (a python list of strings that express the type of the data: str, int, float)
	* s: size info (a python list of integers that express the size of the data when must be print "aligned". This information is typically filled out with the correct value while loading the data)
	* i: additional info (a python list of dictionaries, in each dict the keys are the properties and the values are their values).  This information is typically used for making graphs, e.g., to specify input and output variables and their name on the graph.
	"""
	def __init__(self, h=[], t=[], s=[], i=[], d=[]):
		"""
		This is the constructor method. All parameters are optional, and can be assigned later.
		"""
		self.h=h  # header
		self.t=t  # type
		self.s=s  # size
		self.i=i  # additional info (e.g., role IN/OUT, plotname)
		self.d=d  # data (can be list of _DE or DT)

	def limit_header(self,new_h):  # Just show some headers, discard the others (but do not discard element values)
		"""
		This method changes the header fields contained in the :class:`_DT` object, so that only some of them are shown
		(all the original values are kept in the object).

		Parameters:

		* new_h: a python list with the names of the header fields to keep. Currently no check is performed on the validity of the names

		Return value
		
		* none
		"""
		new_t=['']*len(new_h)
		new_s=[0]*len(new_h)
		new_i=[{} for l in range(len(new_h))]
		for i in range(len(new_h)):
			idxold=self.h.index(new_h[i])
			new_t[i]=self.t[idxold]
			new_s[i]=self.s[idxold]
			new_i[i]=self.i[idxold]
		self.t=new_t
		self.s=new_s
		self.i=new_i
		self.h=new_h
		return self

	#def duplicate_all_headers_only(self):
	def dup_all_h_only(self):
		"""
		This method creates a new :class:`_DT` object that contains a copy of all the header information (field names, types, etc.)
		of the :class:`_DT` object on which it is called,
		but only a reference to the data is included (i.e., data is not duplicated).
		NB: it does NOT perform recursion.
		This is useful to keep the original information before calling limit_header

		Parameters:

		* none

		Return value
		
		* A new :class:`_DT` object with a copy of all the header info (only at the top level, no recursion)
		"""
		return _DT(self.h[:], self.t[:], self.s[:], copy.deepcopy(self.i), self.d)

	def dup_data_ref(self):
		"""
		This method creates a new :class:`_DT` object that contains a copy of all the header information (field names, types, etc.) and all references to the data
		of the :class:`_DT` object on which it is called.
		This is useful to keep the original data before applying FILTER operations.

		Parameters:

		* none

		Return value
		
		* A new :class:`_DT` object with a copy of all the header info and a reference to the data (not the data objects themselves)
		"""
		return _DT_dup_ref(self, level=0)

	def dup_all(self):
		"""
		This method creates a new :class:`_DT` object that contains a full copy of all the data
		of the :class:`_DT` object on which it is called.
		This is useful to keep the original data before applying ADD, ADDEVERY etc. operations which alters the number of columns in the data

		Parameters:

		* none

		Return value
		
		* A new :class:`_DT` object with a full copy
		"""
		return copy.deepcopy(self)

	def p(self):
		"""
		This method prints the information contained in the :class:`_DT` object on which it is called.
		"""
		_DT_print(self, 0)

	def pf(self):
		"""
		This method prints the information contained in the :class:`_DT` object on which it is called, but it aligns the data columns
		"""
		_DT_print(self, 0, formatted=True)  # print formatted

	def pf_short(self):
		"""
		This method prints the information contained in the :class:`_DT` object on which it is called, but it aligns the data columns
		and it does not print the header info, only the data is shown
		"""
		_DT_print(self, 0, formatted=True, header=False)

######################################################################################################
# Utility functions

def create_str__variables_with_val(dt_grouped, var_list):
	"""
	Create a string with varVal_varVal... using the variables in var_list and their values taken from the first _DE element in dt_grouped

	Parameters:

	* dt_grouped: the :class:`_DT` object from which the values :class:`_DE` have to be taken. NB: dt_grouped.d[0] must be a _DE element
	* var_list: a python list of variable names to insert in the string

	Return:

	* the created string, and a dictionary with key=variable name, value=variable value (values as formatted for the string)
	"""

	var_values=[]
	data_list_values={}
	for vl in range(len(var_list)):
		var=var_list[vl]
		k=dt_grouped.h.index(var)
		if dt_grouped.t[k]=='int':
			formatstr="%%0%dd" % (dt_grouped.s[k])
		elif dt_grouped.t[k]=='float':
			formatstr="%%0%df" % (dt_grouped.s[k])
		else:
			formatstr="%%-%ds" % (dt_grouped.s[k])
		#print "formatstr=%s" % (formatstr)
		#print "dt_grouped.d[i] %s" % (dt_grouped.d[i])
		#print dt_grouped.h[k]
		#print var
		#print dt_grouped.d[0]
		valu= (formatstr) % (dt_grouped.d[0].__dict__[var])
		var_values.append( valu )
		var_values[-1]=var_values[-1].replace(' ','-')   # Replaces all spaces in case the last added item is a strings
		data_list_values[var]=var_values[-1]  # Use the fixed value (spaces replaced by -)
		#print "var_values[-1]= '%s'" % (var_values[-1])

	val_string=""
	for vl in range(len(var_list)):
		val_string+=var_list[vl]
		val_string+=var_values[vl]
		if vl<len(var_list)-1:
			val_string+="_"

	return val_string, data_list_values

######################################################################################################

def SAVE(dt, fname, align=False, sep=',', comment=False, log_level=0, sortvar=''):
	"""
	Save the content of the :class:`_DT` object. If nested :class:`_DT` objects are encountered, recursion is NOT performed
	
	Parameters:

	* dt: structure to save
	* fname: the filename to save to
	* align: True: attempt to align the fields so that they look good in a plain text file (default: False)
	* sep: separator character in the file. Please note that if align==True, spaces may be inserted after the separator
	* comment: True: put # at the beginning of first row with the column names
	* log_level: print log information
	* sortvar: a tuple containing pairs of variable name and sort direction, e.g. (('OutH','asc'),('OutRate','desc'))
	
	Return:

	* none
	"""

	f=open(fname,"w")
	if comment==True:
		f.write("#")  # This is to be immediately used in gnuplot
	print(sep.join(dt.h), file=f)
	cnt_DE=0
	cnt_DT=0

	sort_idx = []
	if len(sortvar)>0:
		if not isinstance(sortvar,list):
			print("ERROR: the list of variables for sorting %s must be a list of tuples, i.e., [(var,'asc')] or [(var,'asc'),(var,'asc')...] " % (str(sortvar)), file=sys.stderr)
			sys.exit(1)
		# print dt.d[0].__dict__['OutBitRate']
		# pos=dt.h.find('OutBitRate')
		# print dt.h
		# print 'OutBitRate' in dt.h
		for i in range(len(dt.d)):
			if dt.d[i].__class__.__name__ != '_DT':
				el=[]
				el.append(i)
				for m in range(len(sortvar)):
					el.append(dt.d[i].__dict__[sortvar[m][0]])
				sort_idx.append(el)
		# print sort_idx
		# sort starting from the last column to the first one
		for m in range(len(sortvar)-1,-1,-1):
			rev = False if sortvar[m][1]=='asc' else True
			sort_idx.sort(key=lambda x: x[m+1], reverse=rev)  # +1 because first column is the index
		# print sort_idx
	else:
		for i in range(len(dt.d)):
			if dt.d[i].__class__.__name__ != '_DT':
				sort_idx.append((i, ''))

	# for i in range(len(dt.d)):
	for j in range(len(sort_idx)):
		i = sort_idx[j][0]  # First element of the tuple
		#
		#for i in range(len(dt.d)):
		# Skip DT objects (to save them it is necessary to flatten them)
		if dt.d[i].__class__.__name__!='_DT':
			for k in range(len(dt.h)):
				if align==False:
					if dt.t[k]=='int':
						formatstr="%d"
					elif dt.t[k]=='float':
						formatstr="%f"
					else:
						formatstr="%s"
					#print "formatstr=%s" % (formatstr)
					f.write( (formatstr) % (dt.d[i].__dict__[dt.h[k]]) )
				else:
					if dt.t[k]=='int':
						formatstr="%%%dd" % (dt.s[k])
					elif dt.t[k]=='float':
						formatstr="%%%df" % (dt.s[k])
					else:
						formatstr="%%-%ds" % (dt.s[k])
					#print "formatstr=%s" % (formatstr)
					f.write( (formatstr) % (dt.d[i].__dict__[dt.h[k]]) )
				if k<len(dt.h)-1:
					f.write(sep)
				else:
					f.write("\n")
			cnt_DE+=1
		else:
			cnt_DT+=1
	if log_level>1:
		print("Wrote %d data lines, skipped %d DT elements, file: %s" % (cnt_DE, cnt_DT, fname))
	f.close()

######################################################################################################

def SAVEGROUPS(dt, fnamebase, variables, align=False, sep=',', comment=False, log_level=0, sortvar=''):
	"""
	Save the content of each nested :class:`_DT` object in the passed :class:`_DT` object. Sub-nested :class:`_DT` objects are NOT saved, i.e., it calls SAVE on each nested :class:`_DT` object.
	Each nested :class:`_DT` object has its own name, composed of the variables passed as parameter and their value, taken from the first in the list of the nested :class:`_DT` object.
	
	Parameters:

	* dt: structure to save

	* fnamebase: string to prepend to the filename used for saving (.txt extension is automatically added)
	* variables: list of variables to include in the filename with their value ( string as "$a,$b..." or python list with [a,b,...])
	* align: True: attempt to align the fields so that they look good in a plain text file (default: False)
	* sep: separator character in the file. Please note that if align==True, spaces may be inserted after the separator
	* comment: True: put # at the beginning of first row with the column names
	* log_level: print log information

	Return:

	* list of saved files, list of corresponding variables and values. The latter is useful to sort the results
	"""

	#print "DEBUG variables: ", variables
	fname_list=[]
	data_list=[]
	for i in range(len(dt.d)):
		# Skip DT objects (to save them it is necessary to flatten them)
		if dt.d[i].__class__.__name__=='_DT':
			if type(variables) is list:
				var_list=variables
			else:
				var_list=[x.strip().replace('$','') for x in variables.split(',')]

			var_string,data_list_values = create_str__variables_with_val(dt.d[i], var_list)	
			# Moved into the function
			#var_values=[]
			#data_list_values={}
			#for vl in range(len(var_list)):
			#	var=var_list[vl]
			#	k=dt.h.index(var)	
			#	if dt.t[k]=='int':
			#		formatstr="%%0%dd" % (dt.s[k])
			#	elif dt.t[k]=='float':
			#		formatstr="%%0%df" % (dt.s[k])
			#	else:
			#		formatstr="%%-%ds" % (dt.s[k])
			#	#print "formatstr=%s" % (formatstr)
			#	#print "dt.d[i] %s" % (dt.d[i])
			#	valu= (formatstr) % (dt.d[i].d[0].__dict__[dt.h[k]]) 
			#	var_values.append( valu )
			#	var_values[-1].replace(' ','-')   # Replaces all spaces in case the last added item is a strings
			#	data_list_values[var]=valu
			#var_string=""
			#for vl in range(len(var_list)):
			#	var_string+=var_list[vl]
			#	var_string+=var_values[vl]
			#	if vl<len(var_list)-1:
			#		var_string+='_'

			data_list.append(data_list_values)
	
			#print var_string

			fname_final="%s%s.txt" % (fnamebase, var_string)

			SAVE(dt.d[i], fname_final, align, sep, comment, log_level, sortvar)
			fname_list.append(fname_final)

	#print "DEBUG fname_list: ", fname_list
	return fname_list, data_list

######################################################################################################


def internal_LOAD(fn_csv, ty, sep):
	"""
	Internal function. Load a csv file separated by sep into the :class:`_DT` object format.
	Removes the initial # only if present in the first position of the first line. This allows file compatibility with gnuplot.
	
	Parameters:

	* fn_csv: file name of the csv file to load
	* ty: list with the types for each column (in same order as they appear in the csv file)
	* sep: separator ('' = python whitespaces of split, others are passed as parameter to python split)
	
	Return:

	* :class:`_DT` object
	"""

	sizes=[0]*len(ty) # temporary
	info=[{} for k in range(len(ty))]  # eventually updated by caller function

	f=open(fn_csv,"r")
	line=f.readline()
	if line[0]=='#':
		line=line[1:] # Remove the initial # only if present in the first position of the first line. This allows file compatibility with gnuplot
	dt=_DT()
	dt.t=ty
	if sep=='':
		head=line.split()
	else:
		head=line.split(sep)
	if len(head)<=1:
		print("ERROR: csv file seems to be only one column, maybe the separator is wrong? (assumed: '%s')" % (sep), file=sys.stdout)
		sys.exit()
	dt.h=[x.strip() for x in head]  # Header names
	line=f.readline()
	row=2
	while line:
		if sep=='':
			v=[x.strip() for x in line.split()]
		else:
			v=[x.strip() for x in line.split(sep)]

		if len(v)!=len(dt.h):
			sys.stderr.write("ERROR reading file %s at row %d : number of fields not correct (header=%d, row=%d)\n" % (fn_csv,row,len(dt.h),len(v)))
			sys.exit()
		list_val=[]
		for i in range(len(v)):
			val=v[i]
			#print "i=%d, ty=%s" % (i,ty)
			if ty[i]=='int':
				val=int(v[i])
				lenval=len("%s" % val)
			elif ty[i]=='float':
				val=float(v[i])
				lenval=len("%s" % int(val))+7
			else:
				lenval=len("%s" % val)

			if lenval>sizes[i]:
				sizes[i]=lenval

			#setattr(obj, dt.h[i], val)
			list_val.append(val)
		obj=_DE(dt.h, list_val)
		dt.d.append(obj)
		#dt.d.append(dict(zip(dt.h, v)))
		row+=1
		#obj.p(dt.h)
		#print sizes
		#sys.exit()

		line=f.readline()
	f.close()
	dt.s=sizes
	dt.i=info
	return dt  # class _DT
			
######################################################################################################

def LOAD(fn_csv, fn_types, sep=','):
	"""
	Load a csv file (separated by sep) into the :class:`_DT` object format.
	Removes the initial # only if present in the first position of the first line. This allows file compatibility with gnuplot.
	
	Parameters:

	* fn_csv: file name of the csv file to load
	* ty: list with the types for each column (in same order as they appear in the csv file)
	* sep: separator ('' = python whitespaces of split, others are passed as parameter to python split)
	
	Return:

	* :class:`_DT` object
	"""

	ft=open(fn_types,"r")
	line=ft.readline()
	if sep=='':
		ty=[x.strip() for x in line.split()]	
	else:
		ty=[x.strip() for x in line.split(sep)]	
	if len(ty)==1:
		print("WARNING:", file=sys.stderr)
		print("WARNING: it seems that the file '%s' contains only 1 field, is the separator (%s) correct?" % (fn_types,sep), file=sys.stderr)
		print("WARNING:", file=sys.stderr)
	#print ty
	line=ft.readline()
	if line:
		print("ERROR: file '%s' should contain only 1 line with all the types there" % (fn_types), file=sys.stderr)
		sys.exit()
	ft.close()
	sizes=[0]*len(ty) # temporary

	return internal_LOAD(fn_csv, ty, sep)

######################################################################################################


#def _is_list_of_DT(d):
#	#if isinstance(d, list):
#	if d[0].__class__.__name__ == '_DT':
#		return True
#	else:
#		return False
#	#if isinstance(d, _DT): 


#####################################

def _internal_FILTER(dt, cmdstr):
	evalstr=cmdstr.replace("$","el.")
	new_dt=[]
	for i in range(len(dt.d)):
		el=dt.d[i]
		#print el.__dict__.keys()
		#print el.b
		#print evalstr
		#print eval(evalstr)
		if eval(evalstr):  # Evaluate boolean condition
			new_dt.append(el)
	dt.d=new_dt
	return dt
	#return _DT(dt.h,dt.t,dt.s,dt.i,new_dt)

#def FILTER(dt, cmdstr):
#	if debug:
#		print "Command: FILTER '%s'  %s" % (cmdstr,dt) 
#	if _is_list_of_DT(dt.d):
#		li=[]
#		for k in dt:
#			li.append(FILTER(dt[k], cmdstr))  # Recursive, to manage nested structures
#		return li
#	else:
#		#print "Just run FILTER: no list of _DT"
#		return _internal_FILTER(dt, cmdstr)


####################################

def _internal_GROUP(dt, cmdstr):
	if type(cmdstr) is list:
		group_vars=cmdstr
	else:
		group_vars=[x.replace('$','') for x in cmdstr.split(',')]
	#print group_vars

	new_dict={}
	for i in range(len(dt.d)):
		el=dt.d[i]
		key=()  # emtpy tuple
		for k in range(len(group_vars)):
			#print group_vars[k]
			key = key+ ( eval("el.%s" % group_vars[k]), )
		#print key
		#print el.__dict__.keys()
		#print el.b
		#print eval(evalstr)
		if key not in new_dict:
			# XXX NB: lists dt.h, dt.t, dt.s, dt.i must be DUPLICATED, otherwise group headers are not independent
			# This might cause problems when adding variables to each subgroup (they get duplicated in the header!)
			new_dict[key]=_DT(dt.h[:], dt.t[:], dt.s[:], dt.i[:], [])
		new_dict[key].d.append(el)

	#print new_dict
	new_dt=[]
	for kv in new_dict:
		new_dt.append(new_dict[kv])  # Discard key kv
	# NB: Nou need to duplicate header here since it is the one of the original structure on which grouping is performed
	#     But NEEDED to change the dt.d reference
	dt.d = new_dt
	return dt
	#return _DT(dt.h, dt.t, dt.s, dt.i, new_dt)


#def GROUP(dt, cmdstr):
#	if debug:
#		print "Command: GROUP '%s'  %s" % (cmdstr,dt) 
#	if _is_list_of_DT(dt.d):
#		li=[]
#		for k in dt:
#			li.append(GROUP(dt[k], cmdstr))  # Recursive, to manage nested structures
#		return li
#	else:
#		return _internal_GROUP(dt, cmdstr)


#####################################

def _internal_SORT(dt, cmdstr, order=""):
	if type(cmdstr) is list:
		sort_vars=cmdstr
	else:
		sort_vars=[x.replace('$','') for x in cmdstr.split(',')]
	
	if type(order) is list:
		order_vars=order
	else:
		if order!="":
			order_vars=[x.strip() for x in order.split(',')]
		else:
			order_vars=[]
	#print sort_vars
	
	new_dt=dt.d[:] # Copy all the pointers (FIXME: maybe not needed?)
	for v in range(len(sort_vars)-1,-1,-1):
		rev=False
		#print order_vars
		if len(order_vars)>0:
			if order_vars[v].lower()=='desc':
				rev=True
		new_dt.sort(reverse=rev, key=lambda x:getattr(x,sort_vars[v])) # Stable sorting
		#_DE_list_print(new_dt,dt.h)
			
	dt.d = new_dt
	return dt
	#return _DT(dt.h, dt.t, dt.s, dt.i, new_dt)


#def SORT(dt, cmdstr):
#	if debug:
#		print "Command: SORT '%s'  %s" % (cmdstr,dt) 
#	if _is_list_of_DT(dt.d):
#		li=[]
#		for k in dt:
#			li.append(SORT(dt[k], cmdstr))  # Recursive, to manage nested structures
#		return li
#	else:
#		return _internal_SORT(dt, cmdstr)

def _internal_LIMIT(dt, cmdstr):
	if isinstance(cmdstr, str):
		limit_val=eval(cmdstr)
	else:
		limit_val=cmdstr  # It is already a number
	lim=int(limit_val)

	dt.d=dt.d[0:lim]
	return dt
	#return _DT(dt.h, dt.t, dt.s, dt.i, dt.d[0:lim])




#####################################

def _internal_FLATTEN(dt, level=0):

	li=[]
	for i in range(len(dt.d)):
		#print "DEBUG: dt.d[i] = %s" % (dt.d[i])
		if dt.d[i].__class__.__name__=='_DT':
			#print "DEBUG: recursive FLATTEN call"
			new_dt = _internal_FLATTEN(dt.d[i], level+1)
			#print "FLATTEN len(new_dt): ", len(new_dt.d)
			li += new_dt.d
			# Fix headers if needed
			# TODO XXX : if headers are different, missing fields should be initialized in the elements?
			for j in range(len(new_dt.h)):
				#print "DEBUG: new_dt.h[i] not in dt.h: %s %s " % (new_dt.h[i],dt.h)
				if new_dt.h[j] not in dt.h:
					dt.h+=[new_dt.h[j]]
					dt.t+=[new_dt.t[j]]
					dt.s+=[new_dt.s[j]]
					dt.i+=[new_dt.i[j]]
		else:
			#print "DEBUG: FLATTEN just add to list"
			li.append(dt.d[i])

	#print "DEBUG: list after FLATTEN: %s" % (li)
	dt.d=li
	return dt
	#return _DT(dt.h, dt.t, dt.s, dt.i, li)

#####################################

#def DIFF(li):
#	res=[]
#	for i in range(len(li)):
#		res.append(li[0]-li[1])	
#	return res
#
#def ABSDIFF(li):
#	res=[]
#	for i in range(len(li)):
#		d=li[0]-li[1]
#		if d<0:
#			d=-d
#		res.append(d)
#	return res

def _internal_ADD(dt, argstr, func):
	"""
	Add a new column with the same value for all the dataset.
	The new column name is automatically decided.
	The value is computed applying the function func to the column(s) specified by argstr
	"""

	arg_vars=[x.replace('$','') for x in argstr.split(',')]
	new_col="%s__%s" % (func,'_'.join(arg_vars))

	#print new_col

	li=[]
	for i in range(len(dt.d)):
		el=dt.d[i]
		#print "arg_vars[0]", arg_vars[0]
		li.append(eval("el.%s" % arg_vars[0]))

	res=eval("%s(li)" % func)
	for i in range(len(dt.d)):
		el=dt.d[i]
		setattr(el,new_col,res)
	
	newtype='float'
	if func=='CNT':
		newtype='int'
	newsize=9

	dt.h.append(new_col)
	dt.t.append(newtype)
	dt.s.append(newsize)

	k=dt.h.index(arg_vars[0])
	newinfo={}
	if 'role' in dt.i[k]:    # Something is set in the dt.i content, set something for the new variable
		newinfo['role']=dt.i[k]['role']	
		newinfo['plotname']=new_col
	dt.i.append(newinfo)
	#return _DT(dt.h+[new_col], dt.t+[newtype], dt.s+[9], dt.i+[newinfo], dt.d)
	return dt


def _internal_REPLACE(dt, argstr, func):
	"""
	Replace the values of a column with a new value computed using the function func.
	The value is computed applying the function func to the column(s) specified by argstr
	"""

	arg_vars=[x.replace('$','') for x in argstr.split(',')]

	li=[]
	for i in range(len(dt.d)):
		el=dt.d[i]
		#print "arg_vars[0]", arg_vars[0]
		li.append(eval("el.%s" % arg_vars[0]))

	res=eval("%s(li)" % func)
	for i in range(len(dt.d)):
		el=dt.d[i]
		setattr(el,arg_vars[0],res)
	
	return dt


def _internal_ADDEVERY(dt, argstr, new_col_name):
	"""
	Add a new column with the new_col_name doing the operation specified in the argstr
	"""

	if new_col_name=="":
		print("ERROR: new_col_name is empty; function: ADDEVERY", file=sys.stderr)
		sys.exit()

	operation=argstr.replace('$','el.')
	#print operation
	
	for i in range(len(dt.d)):
		el=dt.d[i]
		res=eval(operation)
		setattr(el,new_col_name,res)
	
	newtype='float'
	newsize=9
	defaultrole='OUT'
	newinfo={}	
	if 'role' in dt.i[0]:  # Something is set in the dt.i content, set something for the new variable
		newinfo={'plotname':new_col_name,'role':defaultrole}

	dt.h.append(new_col_name)
	dt.t.append(newtype)
	dt.s.append(newsize)
	dt.i.append(newinfo)
	#return _DT(dt.h+[new_col_name], dt.t+[newtype], dt.s+[9], dt.i+[newinfo], dt.d)
	return dt



def _internal_REPLACEEVERY(dt, argstr, col_name):
	"""
	Replace the content of a column by doing, for each row, the operation specified in the argstr (that can involve other columns)
	"""

	operation=argstr.replace('$','el.')
	#print operation
	
	for i in range(len(dt.d)):
		el=dt.d[i]
		res=eval(operation)
		setattr(el,col_name,res)
	
	return dt


def _internal_ADDCONDOP(dt, argstr, row_condition, new_col_name):
        #* Example: ``CSV('ADDCONDOP', dt, 'abs($col2/float(#col2))', '$col3==2 and $col4==6', 'NewRatio')``

	"""
	Add a new column with the new_col_name doing the operation specified in the argstr
	"""

	if new_col_name=="":
		print("ERROR: new_col_name is empty; function: ADDCONDOP", file=sys.stderr)
		sys.exit()

	operation=argstr.replace('$','el.')
	#print operation
	
	# find row to which the condition applies
	row_cond_operation=row_condition.replace('$','el.')
	row=-1
	for i in range(len(dt.d)):
		el=dt.d[i]
		res=eval(row_cond_operation)
		if res==True:
			row=i
			break

	if row<0:
		print("WARNING: ADDCONDOP: cannot find any row that matches condition '%s'" % (row_condition), file=sys.stderr)
		#print >> sys.stderr, "Printing the corresponding_data"
		#dt.pf()
		print("WARNING: adding 0.000000", file=sys.stderr)
		#sys.exit()
		for i in range(len(dt.d)):
			el=dt.d[i]
			res=0.000000
			setattr(el,new_col_name,res)
	else:
		# All references to variables starting with '#' are references to the row!
		operation=operation.replace('#','dt.d[%d].' % (row))
		#print operation

		for i in range(len(dt.d)):
			el=dt.d[i]
			res=eval(operation)
			setattr(el,new_col_name,res)
	
	newtype='float'
	newsize=9
	defaultrole='OUT'
	newinfo={}	
	if 'role' in dt.i[0]:  # Something is set in the dt.i content, set something for the new variable
		newinfo={'plotname':new_col_name,'role':defaultrole}

	dt.h.append(new_col_name)
	dt.t.append(newtype)
	dt.s.append(newsize)
	dt.i.append(newinfo)
	#return _DT(dt.h+[new_col_name], dt.t+[newtype], dt.s+[9], dt.i+[newinfo], dt.d)
	#print "dt.h=%s" % (dt.h)
	return dt



#####################################
#####################################
#####################################
#####################################
def CSV(func_name, dt, cmdstr1="", cmdstr2="", cmdstr3="", level=0):
	"""
	This is the main function to perform operations on the data.

	Parameters:
	
	* func_name: string corresponding to the name of the operation to do: FLATTEN, FILTER, GROUP, SORT, LIMIT, ADD, ADDEVERY etc.
	* dt: the object on which the operation must be performed.
	* cmdstr1: an optional parameter whose meaning depends on the chosen func_name
	* cmdstr2: an optional parameter whose meaning depends on the chosen func_name
	* cmdstr3: an optional parameter whose meaning depends on the chosen func_name
	* level: internal parameter, with a default value (internally used for recursion when needed).

	Return:

	* The processed :class:`_DT` object

	Specification of the functions:

	* FLATTEN: Reduces all content and subcontent of the dt to a single list in the _DT. Useful to come back from GROUP operations
		* Example: ``CSV('FLATTEN', dt)``

	* FILTER: Drop rows of data that evaluates as False for the expression. The filtering is recursively performed on sub-_DT structures if present.
		* Example: ``CSV('FILTER', dt, '$colname>1')``
		* cmdstr1: boolean expression in python syntax to be evaluated for each row in dt. If False, the row is dropped. Each column name must be preceded by $
	
	* GROUP: Groups the data into sub-_DT structures. The result is a list of _DT structures, each one containing a subset of the data that have the same value for the specified columns. The grouping is recursively performed on sub-_DT structures if present.
		* Example: ``CSV('GROUP', dt, '$col1,$col2')``
		* cmdstr1: List of column names on which grouping is performed. Each column name must be preceded by $. The list can also be a python list (names need not be preceded by $)
	
	* SORT: Sort the data according to the specified columns. The sorting is recursively performed on sub-_DT structures if present.
		* Example: ``CSV('SORT', dt, '$col1,$col2')``
		* cmdstr1: List of column names on which sorting is performed. Each column name must be preceded by $. The list can also be a python list (names need not be preceded by $)
	
	* LIMIT: Drops the rows that exceed the specified number. The limit is recursively performed on sub-_DT structures if present.
		* Example: ``CSV('LIMIT', dt, 1)``
		* cmdstr1: An interger value (the number of rows after which rows are dropped)

	* ADD: Add a column (the name is automatically chosen) that contains the result of the specified operator. The result is repeated once for each row. The operation is performed on all rows belonging to the same group (i.e., all data rows in a :class:`_DT` object). The operation is recursively performed on sub-_DT structures if present.
		* Example: ``CSV('ADD', dt, '$col2', 'AVG')``
		* cmdstr1: The column on which the operation is applied.
		* cmdstr2: A predefined operation in the op package (AVG, CNT, DEV, VAR). Variance and standard deviation are computed using the E[x^2]-E^2[x] estimator.
	
	* ADDEVERY: Add a column with the specified name that contains the result of the specified operation, performed row-by-row. The operation is recursively performed on sub-_DT structures if present.
		* Example: ``CSV('ADDEVERY', dt, 'abs($col2-$col1)', 'NewDiff')``
		* cmdstr1: The operation to perform. The syntax of the operation must be valid in python. python functions can be used. Each column name must be preceded by $.
		* cmdstr2: The name of the new added column

	* ADDCONDOP: Add a column with the specified name that contains the result of the specified operation, performed for each row eventually referring to conditions that include other rows in the same set. The operation is recursively performed on sub-_DT structures if present.
		* Example: ``CSV('ADDCONDOP', dt, 'abs($col2/float(#col2))', '$col3==2 and $col4==6', 'NewRatio')``
		* cmdstr1: The operation to perform. The syntax of the operation must be valid in python. python functions can be used. Each column name must be preceded by $. Column names preceded by # are the values where the conditions are met.
		* cmdstr2: The conditions of the row to consider when referring to expressions starting with #.
		* cmdstr3: The name of the new added column

	* REPLACE: Replace a column content with the result of the specified operator. The result is repeated once for each row. The operation is performed on all rows belonging to the same group (i.e., all data rows in a :class:`_DT` object). The operation is recursively performed on sub-_DT structures if present.
		* Example: ``CSV('REPLACE', dt, '$col2', 'AVG')``
		* cmdstr1: The column on which the operation is applied.
		* cmdstr2: A predefined operation in the op package (AVG, CNT, DEV, VAR). Variance and standard deviation are computed using the E[x^2]-E^2[x] estimator.
	
	* REPLACEEVERY: Replace the content of a column with the specified name with the result of the specified operation, performed row-by-row. The operation is recursively performed on sub-_DT structures if present.
		* Example: ``CSV('REPLACEEVERY', dt, 'abs($col2-$col1)', 'Diff')``
		* cmdstr1: The operation to perform. The syntax of the operation must be valid in python. python functions can be used. Each column name must be preceded by $.
		* cmdstr2: The name of the column on which the operation is applied.

	"""
	if debug:
		print(' '*3*level, end=' ')
		print("Command: %s '%s' '%s' '%s'  %s" % (func_name,cmdstr1,cmdstr2,cmdstr3,dt)) 

	if func_name.upper()=='FLATTEN':  # No recursion here, otherwise it cannot be flattened
		return _internal_FLATTEN(dt)
	else:
		if len(dt.d)==0:  # The set is empty, just return that at the upper level
			#sys.stderr.write("WARNING: operating '%s' on an empty set\n" % (func_name.upper() ));
			return dt
		elif dt.d[0].__class__.__name__ == '_DT':
			# We assume that if the first element is a _DT, it is a list of all _DT elements, therefore we call this function recursively on each element
			# In other words, _DT and _DE objects cannot coexist in the same list
			li=[]
			for k in range(len(dt.d)):
				li.append( CSV(func_name, dt.d[k], cmdstr1, cmdstr2, cmdstr3, level+1) )  # Recursive, to manage nested structures
			dt.d=li
			return dt
		else:
			if func_name.upper()=='FILTER':
				return _internal_FILTER(dt, cmdstr1)
			elif func_name.upper()=='GROUP':
				return _internal_GROUP(dt, cmdstr1)
			elif func_name.upper()=='SORT':
				return _internal_SORT(dt, cmdstr1, cmdstr2)
			elif func_name.upper()=='LIMIT':
				return _internal_LIMIT(dt, cmdstr1)
			elif func_name.upper()=='ADD':
				return _internal_ADD(dt, cmdstr1, cmdstr2)
			elif func_name.upper()=='ADDCONDOP':
				return _internal_ADDCONDOP(dt, cmdstr1, cmdstr2, cmdstr3)
			elif func_name.upper()=='REPLACE':
				return _internal_REPLACE(dt, cmdstr1, cmdstr2)
			elif func_name.upper()=='ADDEVERY':
				return _internal_ADDEVERY(dt, cmdstr1, cmdstr2)
			elif func_name.upper()=='REPLACEEVERY':
				return _internal_REPLACEEVERY(dt, cmdstr1, cmdstr2)
			else:
				sys.stderr.write("ERROR: function unknown: %s\n" % (func_name))
				sys.exit()


#####################################
#####################################
#####################################
#####################################

