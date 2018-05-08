import os
import pickle
import os.path


pred_atoms_reduced_numbers = {}
class dbconfig:
	def __init__(self,dsname):
		self.MIN_DOM_SIZE = 20
		self.dsname = dsname
		self.dblocation = dsname + '/db/'
		self.db_init_name = 'db'
		self.merge_db_file = self.dblocation + self.db_init_name + '.txt'
		self.w2v__cluster_db_file = self.dblocation  + 'w2v_cluster_db.txt'
		self.random__cluster_db_file = self.dblocation  + 'random_cluster_db.txt'
		self.kmeans__cluster_db_file = self.dblocation  + 'kmeans_cluster_db.txt'
		self.mlnlocation = dsname + '/mln/'
		self.mln_file_name ='mln.txt'
		self.mln_file_full_name = self.mlnlocation + self.mln_file_name 
		self.pickle_location = dsname + '/pickle/'
		self.TOPN = 4
		self.MINK = 2

class DBManager(dbconfig):
	def __init__(self,dsname,mln):
		dbconfig.__init__(self,dsname)
		self.mln = mln
		self.set_atoms()

	def set_atoms(self):
		pred_atoms_file = self.pickle_location + 'pred_atoms.p'
		if os.path.exists(pred_atoms_file):
			self.pred_atoms = pickle.load(open( pred_atoms_file, "rb" ) )
			return

		pred_atoms = {}
		ifile = open(self.merge_db_file)
		for l in ifile:
			pred_name = l.split('(')[0].replace('!','').strip()
			if pred_name not in pred_atoms:
				pred_atoms[pred_name] = []
			objs = l.split('(')[1].split(')')[0].split(',')
			pred_atoms[pred_name] += [objs]
		self.pred_atoms = pred_atoms
		pickle.dump(pred_atoms,open(self.pickle_location + "pred_atoms.p","wb"))




	def merge(self):
		files = os.listdir(self.dblocation)
		ofile = open(self.merge_db_file,'w')
		atoms = []
		atom_lines = ''
		for f in files:
			if f.startswith(self.db_init_name):
				print(f)
				f = self.dblocation + f
				ifile = open(f)
				for l in ifile:
					if l not in atoms:
						atoms += [l]
						ofile.write(l)
				ifile.close()
		ofile.close()

	def calculate_dom_sizes(self,mln):
		ifile = open(self.dblocation + 'compress_0.1.txt')
		dom_objs_map = {}
		for l in ifile:
			l = l.strip()
			pred_name = l.split('(')[0]
			if pred_name not in mln.pdm:
				continue
			objs = l.split('(')[1].split(')')[0].split(',')
			for i,obj in enumerate(objs):
				dom = mln.pdm[pred_name][i]
				dom_size = mln.dom_sizes_map[dom]
				if dom not in dom_objs_map:
					dom_objs_map[dom] = []
				if obj not in dom_objs_map[dom]:
					dom_objs_map[dom] += [obj]
		for dom in dom_objs_map:
			print(dom,len(dom_objs_map[dom]))

	def compress(self,mln,cr):
		ifile = open(self.merge_db_file)
		ofile_name = self.dblocation + 'compress_' + str(cr) + '.txt'
		ofile = open(ofile_name,'w')
		dom_objs_map = {}
		for l in ifile:
			l = l.strip()
			pred_name = l.split('(')[0]
			if pred_name not in mln.pdm:
				continue
			objs = l.split('(')[1].split(')')[0].split(',')
			
			size_exceeded = False

			for i,obj in enumerate(objs):
				dom = mln.pdm[pred_name][i]
				dom_size = float(mln.dom_sizes_map[dom])
				if dom not in dom_objs_map:
					dom_objs_map[dom] = []
				cl = len(dom_objs_map[dom])
				if cl < (cr*dom_size):
					continue
				if cl < self.MIN_DOM_SIZE:
					continue
				if obj in dom_objs_map[dom]:
					continue
				size_exceeded = True

			if size_exceeded:
				continue

			for i,obj in enumerate(objs):
				dom = mln.pdm[pred_name][i]
				if obj not in dom_objs_map[dom]:
					dom_objs_map[dom] += [obj]

			ofile.write(l + '\n')
		ifile.close()
		ofile.close()


		for dom in dom_objs_map:
			print(dom,len(dom_objs_map[dom]))


