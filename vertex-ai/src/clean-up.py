import sys
import pathlib

LIB_DIR='{}/lib'.format(pathlib.Path(__file__).parent.resolve())
sys.path.append(LIB_DIR)

from vfs import delete_featurestore

delete_featurestore(featurestore_id="us_covid")
