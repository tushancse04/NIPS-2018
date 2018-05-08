from DBManager import DBManager,dbconfig
from mln import MLN
from word2vec import word2vec

dsname = 'er'
mln = MLN(dsname)
db = DBManager(dsname,mln)
#db.merge()
db.compress(mln,.1)
#db.calculate_dom_sizes(mln)
#w2v = word2vec(dsname,db)