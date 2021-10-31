import sys
import pathlib

LIB_DIR='{}/lib'.format(pathlib.Path(__file__).parent.resolve())
sys.path.append(LIB_DIR)

from vfs import batch_read_feature_values

batch_read_feature_values(
    featurestore_id="us_covid",
    entity_type_id="state",
    feature_ids=["death", "hospitalized"]
)
