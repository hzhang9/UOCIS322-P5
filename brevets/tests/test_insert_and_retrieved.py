import nose
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log=logging.getLogger(__name__)
import os
from pymongo import MongoClient

def test_db_insertion_and_retrieved():
    client = MongoClient('mongodb://'+os.environ['MONGODB_HOSTNAME'],27017)
    db=client.tododb
    db.tododb.insert_one({'insert':'testing'})
    retrieved=db.tododb.find_one({'insert':'testing'})
    assert retrieved['insert']=='testing'
    db.tododb.remove({})
    retrieved=db.tododb.find_one({'insert':'testing'})
    assert retrieved== None
