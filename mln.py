import os
from DBManager import dbconfig

class MLN(dbconfig):
	def __init__(self,dsname):
		dbconfig.__init__(self,dsname)
		self.initialize()

	def initialize(self):
		ifile = open(self.mln_file_full_name)
		l = ifile.readline()
		ifile.close()
		l=l.strip()
		parts = l.split(' ')
		pdm = {}
		dom_sizes_map = {}
		dom_pred_map = {}
		size_dom_map ={}
		for p in parts:
			pred_domains = p.split(':')
			predname = pred_domains[0]
			ds = pred_domains[1:]
			if predname not in pdm:
				pdm[predname] = []
			for i,s in enumerate(ds):
				if s not in size_dom_map:
					size_dom_map[s] = len(size_dom_map)
				d = size_dom_map[s]
				if d not in dom_sizes_map:
					dom_sizes_map[d] = s					
				pdm[predname] += [d]
				if d not in dom_pred_map:
					dom_pred_map[d] = []
				dom_pred_map[d] += [[predname,i]]
		self.dom_pred_map = dom_pred_map
		self.pdm = pdm
		self.dom_sizes_map = dom_sizes_map
		self.size_dom_map = size_dom_map
		return pdm
