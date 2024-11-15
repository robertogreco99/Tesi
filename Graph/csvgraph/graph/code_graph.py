#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import collections

from csvgraph.process import *
from csvgraph.graph.graph_object import GPLOT

def LOAD_WITH_EXTERNAL_FIELDS(fn_csv, fn_fields, sep=','):
	"""
	Load a csv file (separated by sep) into the _DT object format, attributing the types according to the content of fn_fields.
	Removes the initial # only if present in the first position of the first line. This allows file compatibility with gnuplot.
	
	The fn_fields is designed to simplify making graphs for gnuplot of subset of data
	
	Parameters:

	* fn_csv: file name of the csv file to load
	* fn_fields: file name whose content describes the types of the data etc.
	* sep: separator ('' = python whitespaces of split, others are passed as parameter to python split)
	
	Return:

	* _DT object

        The field file is shown to make the example complete

        ``input_fields.txt``

        .. include:: input_fields2.txt
           :literal:
	
	"""

	ff=open(fn_fields,"r")
	cols={}
	formatversion=0
	line=ff.readline()
	while line:
		if line[0]!='#':
			v=line.split()
			if line[0]==':':
				if v[1]=='format':
					formatversion=v[3]
			else:
				colnum=int(v[0])
				col_role=v[1]  # default role: IN or OUT
				if not (col_role=="IN" or col_role=="OUT"):
					print("ERROR: invalid role (%s) while reading field file" % (col_role), file=sys.stderr)
					sys.exit()
				col_name=v[2]
				col_plotname=v[3]
				col_type=v[4]
				if col_name=='.': # Copy one name on the other
					col_name=col_plotname
				elif col_plotname=='.': # Copy one name on the other
					col_plotname=col_name
				cols[colnum]={'role':col_role,'name':col_name,'plotname':col_plotname,'type':col_type}
				if len(v)>=6:
					cols[colnum]['size']=v[5]
		line=ff.readline()
	ff.close()
	if formatversion!='1':
		print("ERROR: input file format (v. %s) not supported" % (formatversion), file=sys.stderr)
		sys.exit()

	ty=[]

	for i in range(len(cols)):	
		idx=i+1 # start from 1 
		if idx not in cols:
			# Assume default values
			ty.append('str')
		else:
			ty.append(cols[idx]['type'])

	dt=internal_LOAD(fn_csv, ty, sep)

	for i in range(len(cols)):	
		idx=i+1 # start from 1 
		if 'size' in cols[idx]:
			dt.s[i]=int(cols[idx]['size']) # TODO To fix for floats
		dt.i[i]['plotname']=cols[idx]['plotname']
		dt.i[i]['role']=cols[idx]['role']
	#print ty

	return dt  # class _DT


#######################################################################################################

def LOAD_DOGRAPHS(fn_dographs):
	"""
	Load the content of the fn_dograph file

	Examples are provided, however:

	lines beginning with ``:`` allows to remove parameters from the input set (with ``-`` as first character)(everything is put into the same graph regardless of the values of those parameters) or add parameters as input (with ``+`` as first character)

	Example:  ``: -w -h``

	These modifications are reset each time a new ``:`` at the beginning of a new line is found

	The extra parameters for each graph are: ``[minxrange:maxxrange] [minyrange:maxyrange] xformat yformat withstyle otherparamsjustpassed``

	``xformat, yformat, withstyle, otherparamsjustpassed`` is in the gnuplot format (use ``""`` for an empty format but to set a withstyle, do not use when setting a format such as ``%1.f``)

	Examples:

	``xvar yvar zvars [0:1] [-1:2] %.1f %.2f p``

	``xvar yvar zvars [0:1] [-1:2] "" "" p``

	
	Parameters:

	* fn_dographs: the filename, an example of the content follows

	Return:

	* A list of information about graphs

	``input_dographs.txt``

	.. include:: input_dographs2.txt
	   :literal:

	"""

	ff=open(fn_dographs,"r")
	formatversion=0
	graphs=[]
	var_list_to_add=[]
	var_list_to_del=[]
	line=ff.readline()
	linecnt=1
	while line:
		if line[0]!='#':
			v=line.split()
			if line[0]==':':
				if formatversion==0:
					if v[1]=='format':
						formatversion=v[3]
						if formatversion!='1':
							print("ERROR: input file format (v. %s) not supported" % (formatversion), file=sys.stderr)
							sys.exit()
					else:
						print("ERROR: first information must be the file format version", file=sys.stderr)
						sys.exit()
				else:
					var_list_to_add=[]
					var_list_to_del=[]
					for i in range(1,len(v)):
						if v[i][0]=='-':
							var_list_to_del.append(v[i][1:])
						elif v[i][0]=='+':
							var_list_to_add.append(v[i][1:])
			else:
				graph_data={'x':v[0],'y':v[1], 'var_add':var_list_to_add, 'var_del':var_list_to_del}
				if len(v)>=2:
					if v[2]=='.':
						z_v=[]
					else:
						z_v=v[2].split(',')
					graph_data['z']=z_v
				if len(v)>=4:
					graph_data['xrange']=v[3]
				if len(v)>=5:
					graph_data['yrange']=v[4]
				if len(v)>=6:
					graph_data['xformat']=v[5]
					if graph_data['xformat']!='""':
						if '"' in graph_data['xformat']:
							print("ERROR: format for x variable include \" while is should not: graph file %s, line %d: %s" % (fn_dographs,linecnt,line), file=sys.stderr)
							sys.exit()
				if len(v)>=7:
					graph_data['yformat']=v[6]
					if graph_data['yformat']!='""':
						if '"' in graph_data['yformat']:
							print("ERROR: format for y variable include \" while is should not: graph file %s, line %d: %s" % (fn_dographs,linecnt,line), file=sys.stderr)
							sys.exit()
				if len(v)>=8:
					graph_data['withstyle']=v[7]
					graph_data['rest']=v[8:]
				graphs.append(graph_data)
	
		line=ff.readline()
		linecnt+=1
	ff.close()

	return graphs


##########################################################################################
def SET_DOGRAPH_v1(modification, command):
	"""
	Create the internal structures necessary to draw a graph allowing specifications in the form of strings (not needed to load a file)

	Modifications are a single line beginning with ``:`` that allows to remove parameters from the input set (with ``-`` as first character)(everything is put into the same graph regardless of the values of those parameters) or add parameters as input (with ``+`` as first character)
	Command is the specification of the graph to draw

	Example:  ``SET_DOGRAPH_v1(": -w -h +QPperturbed","QPperturbed    psnr    gop,intraperiod  [:] [25:43] "" "" p")``

	Modifications, if not needed, must be set to "#"

	The extra parameters for each graph are: ``[minxrange:maxxrange] [minyrange:maxyrange] xformat yformat withstyle otherparamsjustpassed``

	``xformat, yformat, withstyle, otherparamsjustpassed`` is in the gnuplot format (use ``""`` for an empty format but to set a withstyle, do not use when setting a format such as ``%1.f``)

	Examples:

	``xvar yvar zvars [0:1] [-1:2] %.1f %.2f p``

	``xvar yvar zvars [0:1] [-1:2] "" "" p``


	Parameters:

	* modification: a string that allows to remove or add parameters from the input set

	* command: a string that specifies which graph to draw

	Return:

	* A list of information about the graph (in an internal unspecified format)

	"""

	graphs = []
	var_list_to_add = []
	var_list_to_del = []
	if len(modification) == 0:
		print("ERROR: 'modification' parameter cannot be an empty string. Use \"#\" if not needed.", file=sys.stderr)
		sys.exit()
	if modification[0] != '#':
		if modification[0] == ':':
			v = modification.split()
			for i in range(1, len(v)):
				if v[i][0] == '-':
					var_list_to_del.append(v[i][1:])
				elif v[i][0] == '+':
					var_list_to_add.append(v[i][1:])
		else:
			print("ERROR: first character of 'modification' parameter must be either '#' or ':'", file=sys.stderr)

	if len(command) == 0:
		print("ERROR: 'command' parameter cannot be an empty string", file=sys.stderr)
		sys.exit()
	v = command.split()
	graph_data = {'x': v[0], 'y': v[1], 'var_add': var_list_to_add, 'var_del': var_list_to_del}
	if len(v) >= 2:
		if v[2] == '.':
			z_v = []
		else:
			z_v = v[2].split(',')
		graph_data['z'] = z_v
	if len(v) >= 4:
		graph_data['xrange'] = v[3]
	if len(v) >= 5:
		graph_data['yrange'] = v[4]
	if len(v) >= 6:
		graph_data['xformat'] = v[5]
		if graph_data['xformat'] != '""':
			if '"' in graph_data['xformat']:
				print("ERROR: format for x variable include \" while is should not", file=sys.stderr)
				sys.exit()
	if len(v) >= 7:
		graph_data['yformat'] = v[6]
		if graph_data['yformat'] != '""':
			if '"' in graph_data['yformat']:
				print("ERROR: format for y variable include \" while is should not", file=sys.stderr)
				sys.exit()
	if len(v) >= 8:
		graph_data['withstyle'] = v[7]
		graph_data['rest'] = v[8:]
	graphs.append(graph_data)

	return graphs


def SET_DOGRAPH_v2(modification, command, graph_obj=None):
	"""
	Create the internal structures necessary to draw a graph allowing specifications in the form of strings (not needed to load a file)

	Modifications are a single line beginning with ``:`` that allows to remove parameters from the input set (with ``-`` as first character)(everything is put into the same graph regardless of the values of those parameters) or add parameters as input (with ``+`` as first character)
	Command is the specification of the graph to draw

	Example:  ``SET_DOGRAPH_v1(": -w -h +QPperturbed","QPperturbed    psnr    gop,intraperiod  [:] [25:43] "" "" p")``

	Modifications, if not needed, must be set to "#"

	The extra parameters for each graph are: ``[minxrange:maxxrange] [minyrange:maxyrange] xformat yformat withstyle otherparamsjustpassed``

	``xformat, yformat, withstyle, otherparamsjustpassed`` is in the gnuplot format (use ``""`` for an empty format but to set a withstyle, do not use when setting a format such as ``%1.f``)

	Examples:

	``xvar yvar zvars [0:1] [-1:2] %.1f %.2f p``

	``xvar yvar zvars [0:1] [-1:2] "" "" p``


	Parameters:

	* modification: a string that allows to remove or add parameters from the input set

	* command: a string that specifies which graph to draw

	* graph_obj: an object with the graph properties (e.g., size in pixels, grid, etc.)

	Return:

	* A graph object with all the necessary info to plot

	"""

	graphs = []
	var_list_to_add = []
	var_list_to_del = []
	if len(modification) == 0:
		print("ERROR: 'modification' parameter cannot be an empty string. Use \"#\" if not needed.", file=sys.stderr)
		sys.exit()
	if modification[0] != '#':
		if modification[0] == ':':
			v = modification.split()
			for i in range(1, len(v)):
				if v[i][0] == '-':
					var_list_to_del.append(v[i][1:])
				elif v[i][0] == '+':
					var_list_to_add.append(v[i][1:])
		else:
			print("ERROR: first character of 'modification' parameter must be either '#' or ':'", file=sys.stderr)

	if len(command) == 0:
		print("ERROR: 'command' parameter cannot be an empty string", file=sys.stderr)
		sys.exit()
	v = command.split()
	graph_data = {'x': v[0], 'y': v[1], 'var_add': var_list_to_add, 'var_del': var_list_to_del}
	if len(v) >= 2:
		if v[2] == '.':
			z_v = []
		else:
			z_v = v[2].split(',')
		graph_data['z'] = z_v
	if len(v) >= 4:
		graph_data['xrange'] = v[3]
	if len(v) >= 5:
		graph_data['yrange'] = v[4]
	if len(v) >= 6:
		graph_data['xformat'] = v[5]
		if graph_data['xformat'] != '""':
			if '"' in graph_data['xformat']:
				print("ERROR: format for x variable include \" while is should not", file=sys.stderr)
				sys.exit()
	if len(v) >= 7:
		graph_data['yformat'] = v[6]
		if graph_data['yformat'] != '""':
			if '"' in graph_data['yformat']:
				print("ERROR: format for y variable include \" while is should not", file=sys.stderr)
				sys.exit()
	if len(v) >= 8:
		graph_data['withstyle'] = v[7]
		graph_data['rest'] = v[8:]
	graphs.append(graph_data)

	if graph_obj == None:
		graph_object = GPLOT()
	else:
		graph_object = graph_obj
	graph_object.graph_data = graphs

	return graph_object


##########################################################################################
def _sanity_check_presence(var,h,role,grnum):
	"""
	Internal function to verify the presence of a variable or a list of variables in the input data

	:param var: the var (or python list of names of the vars) to verify
	:param h: the .h field of the _DT structure containing the data
	:param role: message about the role of the variable (e.g., x, y, zlist, ...) to show in case of errors
	:param grnum: graph number in which the processing is taking place
	:return: None
	"""

	if type(var) is list:
		for zz in range(len(var)):
			if var[zz] not in h:
				print("ERROR: variable %s (role: %s) is unknown in the data, graph no. %d" % (var[zz], role, grnum), file=sys.stderr)
				sys.exit()
	else:
		if var not in h:
			print("ERROR: variable %s (role: %s) is unknown in the data, graph no. %d" % (var, role, grnum), file=sys.stderr)
			sys.exit()


##########################################################################################
# TODO: improve management of labels: is it possible to use the printed labels instead of the csv labels in the graph definition?
def EXEC_GRAPHS(dtorig, graph_data_param, dirname="plots", graph_cnt=0, log_level=0, sortvar=''):
	"""
	Perform the operations needed to generate the graphs
	
	Parameters:

	* dtorig: the data to be processed to create the graphs
	* graph_data: a list of information about the graphs to do (or an object with the info)
	* dirname: directory path into which files are put. If the dirs do not exist they are created.
	* graph_cnt: value from which the graph numbering starts (so that EXEC_GRAPHS can be invocated more times without creating a messy dir content)
	* log_level: if 0 no messages, if >0 it will log messages about which files are written etc.
	* sortvar: a tuple containing pairs of variable name and sort direction, e.g. (('OutH','asc'),('OutRate','desc'))
	
	Return:

	* The last used value of graph_cnt+1 (it can be passed as is to a new invocation of EXEC_GRAPHS)
	"""

	var_plotnames={}
	for k in range(len(dtorig.h)):
		#print "dtorig.i[k]", dtorig.i[k]
		var_plotnames[dtorig.h[k]]=dtorig.i[k]['plotname']

	cwdir=os.getcwd()
	# Create dirs if they do not exist
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	os.chdir(dirname)

	#print("DEBUG --- : %s" % (graph_data_param))
	#if isinstance(graph_data_param, collections.Iterable):
	if isinstance(graph_data_param, type):
		graph_data_object = GPLOT()
		graph_data_object.graph_data = graph_data_param
	else:
		graph_data_object = graph_data_param

	graph_data = graph_data_object.graph_data  # field of an object, taken either from the newly created object or the parameter (for compatibility with previous versions)

	for i in range(len(graph_data)):
		if log_level>0:
			print("Doing graph no. %d ..." % (graph_cnt))
		dt=dtorig.dup_all_h_only() # Needed to copy all control structures of the object, that otherwise would not be available to the next iteration

		gr=graph_data[i]
		x=gr['x']
		y=gr['y']
		zlist=gr['z'] # No need to duplicate since the list is compulsory and rewritten each time in the file
		list_var_add=gr['var_add'][:] # Duplicate, otherwise the list for other graphs may be changed (since it may not be updated in the file)
		list_var_del=gr['var_del'][:] # Duplicate, otherwise the list for other graphs may be changed (since it may not be updated in the file)
		#print x,y,zlist

		# sanity checks: variables are present in the input data?
		_sanity_check_presence(x,dtorig.h,"supposed to be the x variable",i)
		_sanity_check_presence(y,dtorig.h,"supposed to be the y variable",i)
		_sanity_check_presence(zlist,dtorig.h,"supposed to be one of the zlist variables",i)
		_sanity_check_presence(list_var_add,dtorig.h,"supposed to be one of the variables to add in the input list with +",i)
		_sanity_check_presence(list_var_del,dtorig.h,"supposed to be one of the variables to remove from the input list with -",i)
		# end of sanity checks

		list_var_in=[]
		list_var_out=[]
		for k in range(len(dt.h)):
			if dt.i[k]['role']=='IN':
				list_var_in.append(dt.h[k])
			else:
				list_var_out.append(dt.h[k])
		
		for k in range(len(list_var_add)):
			va=list_var_add[k]
			list_var_in.append(va)

		for k in range(len(list_var_del)):
			va=list_var_del[k]
			if va not in list_var_in:
				print("ERROR: cannot del variable %s from list since it is not in the list, graph no. %d" % (va, i), file=sys.stderr)
				sys.exit()
			else:
				list_var_in.remove(va)
		# ### Now list_var_in is the IN ok for the graph
		list_var_keep = list_var_in + list_var_out	
		# This is the list of variables to keep

		# Ok since headers have been copied. The original ones are not destroyed (they are kept in dtorig)
		dt.limit_header(list_var_keep)
		_A1 = dt
	
		if log_level>0:
			print("x: ", x)
			print("y: ", y)
			print("zlist: ", zlist)
			print("list_var_in: ", list_var_in)
			print("list_var_out: ", list_var_out)
	

		#list_var_group_except_x = list_var_in[:] # copy list
		#if x not in list_var_group_except_x:
		#	print >>sys.stderr, "ERROR: cannot set variable x (%s): cannot find it in input" % (x)
		#	sys.exit()
		#list_var_group_except_x.remove(x)
		
		list_var_group = list_var_in[:]
		if x not in list_var_group:
			print("WARNING: x variable %s not in the list of IN type variables, maybe there is an error in the specified graphs. To suppress warning, add +%s to the previous line starting with :" % (x, x), file=sys.stderr)
		else:
			list_var_group.remove(x)

		for k in range(len(zlist)):
			va=zlist[k]
			if va not in list_var_group:
				print("ERROR: cannot del variable %s from list_var_group since it is not in the list, graph no. %d" % (va, i), file=sys.stderr)
				sys.exit()
			else:
				list_var_group.remove(va)

		# do group on list_var_group : the variables not used in the graphs but for each of their unique combination a new graph is done
		_A2=CSV('GROUP',_A1, list_var_group)

		# do group on zlist variables : the variables used as the lines in the graph, for each of their unique combination there is a line in the graph
		_A3=CSV('GROUP',_A2, zlist)
		
		# do sort on x
		_A4=CSV('SORT',_A3, [x])

		#_A4.pf()

		for subgr in range(len(_A4.d)):
			_A4sub = _A4.d[subgr]

			#print "-------------------------------"
			#_A4sub.d[0].pf_short()
			#_A4sub.pf_short()
			#_A4.pf_short()
			#print "-------------------------------"

			# Values for all the variables to be considered but not included in the graph
			fixed_vals_str, fixed_vals_dict = create_str__variables_with_val(_A4sub.d[0], list_var_group)

			##print "sys.exit()"
			##sys.exit()

			# do save groups (variables in name: all those IN, add the + ones, minus the ones marked with -)
			[fname_list, data_list]=SAVEGROUPS(_A4sub, "data_gr%03d__%s__" % (graph_cnt, fixed_vals_str)  , zlist , align=True, sep=' ', comment=True, log_level=log_level, sortvar=sortvar)
			#print "DATA: ",fname_list, data

			join_data_list=list(zip(data_list,fname_list))
			# sort files based on variables values, from last to first (to sort all of them together)
			for v in range(len(zlist)-1,-1,-1):
				rev=False
				# f[0] is the first element of the tuple created with the zip, i.e., the data_list
				join_data_list.sort(reverse=rev, key=lambda f:f[0][zlist[v]]) # Stable sorting
			#print "DATA: ",join_data
			data_list=[d[0] for d in join_data_list]
			fname_list=[d[1] for d in join_data_list]

			subgraph_cnt=0

			gp_lt=[]
			gp_pt=[]
			#print "DATA: ",fname_list, data
			if len(zlist)==1:
				# Values of the variable cannot be repeated because they came out from a grouping operation
				# So, just assign to each one a value starting from 1
				gp_lt=list(range(1,len(data_list)+1))
				gp_pt=gp_lt
			else: # >= 2 : process all variables in zlist, but fix values of lt and pt only for the first two variables
				values_unique={}
				for k in range(len(zlist)):
					values_to_sort={}
					for m in range(len(data_list)):
						values_to_sort[ data_list[m][zlist[k]] ]=1 # Any value is ok, it is unused
					values_unique[k]={}
					cnt=1
					for key in sorted(values_to_sort):  # Sort the values present in the data_list for variable k and assign a plot code
						values_unique[k][key]=cnt	
						cnt+=1
				gp_lt=[]
				gp_pt=[]
				#print data_list
				#print values_unique[0]
				#print values_unique[1]
				#print zlist
				for p in range(len(data_list)):
					gp_lt.append(values_unique[0][data_list[p][zlist[0]]] )
					gp_pt.append(values_unique[1][data_list[p][zlist[1]]] )
				#print gp_lt
				#print gp_pt
					
			#print "gp_lt: ",gp_lt
			#print "gp_pt: ",gp_pt
                
                
                
			#  = count groups
			# create the gnuplot
			fn_base="graph_%03d__%s__%s_vs_%s" % ( graph_cnt,  fixed_vals_str,  y,x)
			fn_gp=fn_base+".gplot"
			fn_png=fn_base+".png"
			gp=open(fn_gp,"w")
			print("set terminal png %senhanced size %s,%s" % (graph_data_object.enhanced_str, graph_data_object.w, graph_data_object.h), file=gp)
			print("set out \"%s\"" % (fn_png), file=gp)
			print("set title \"%s\"" % (fixed_vals_str), file=gp)
			print("set %sgrid" % (graph_data_object.grid_str), file=gp)
			print("set xlabel \"%s\"" % (var_plotnames[x]), file=gp)
			print("set ylabel \"%s\"" % (var_plotnames[y]), file=gp)
			if 'xformat' in gr:
				if gr['xformat']!='""':
					print("set format x \"%s\"" % (gr['xformat']), file=gp)
			if 'yformat' in gr:
				if gr['yformat']!='""':
					print("set format y \"%s\"" % (gr['yformat']), file=gp)
			if len(graph_data_object.option_str)>0:
				gp.write("%s" % (graph_data_object.option_str))
			xrang=gr['xrange'] if 'xrange' in gr else ''
			yrang=gr['yrange'] if 'yrange' in gr else ''
			withstyle=gr['withstyle'] if 'withstyle' in gr else 'lp' # default style: w lp (just write  lp or p or other)
			rest=" ".join(gr['rest']) if 'rest' in gr else ' '
			print("plot %s %s \\" % (xrang,yrang), file=gp)
			for k in range(len(fname_list)):
				# Needed to display values in order as expressed by zlist, taking them from the dict data_list
				title="_".join([ke+data_list[k][ke] for ke in zlist])
				lt=1
				pt=1
				gp.write("\"%s\" u ($%d):($%d) t \"%s\" w %s lt %d pt %d %s" % (fname_list[k], dt.h.index(x)+1, dt.h.index(y)+1, title, withstyle, gp_lt[k], gp_pt[k], rest) )
				if k<len(fname_list)-1:
					gp.write(",\\\n")
				else:
					gp.write("\n")
			gp.close()
			if log_level>1:
				print("Wrote gnuplot file %s" % (fn_gp))
                
			exitval=os.system("gnuplot %s" % (fn_gp))
			if exitval!=0:
				print("######################################")
				print("WARNING: gnuplot error, file %s . Maybe some parameters such as format (%%d instead of %%f) are not correct in the input files?" % (fn_gp))
				print("######################################")

	
		if log_level>0:
			print("Done.")
			print()
		graph_cnt+=1
	os.chdir(cwdir)
	return graph_cnt

##########################################################################################

def LOAD_GRAPH_INPUT_FILES(fn_csv, fn_fields, fn_dographs, sep=''):
	"""
	Function to load the data and the two files needed to plot graphs
	
	Parameters:
	
	* fn_csv: filename of the csv file
	* fn_fields: filename of the field description file
	* fn_dographs: filename describing which graphs to plot

	Return:
	
	* (_DT object with data, list of graphs to plot). The list of graphs can be passed directly to the ``EXEC_GRAPHS()`` function
	"""
	dt=LOAD_WITH_EXTERNAL_FIELDS(fn_csv, fn_fields, sep)
	graphs=LOAD_DOGRAPHS(fn_dographs)
	return dt,graphs

