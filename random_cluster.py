from DBManager import dbconfig
class random_cluster(dbconfig):
	def __init__(self,dsname):
		dbconfig.__init__(self,dsname)
	
	def generate_random_db(self):
		