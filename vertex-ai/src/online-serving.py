import sys
import pathlib

LIB_DIR='{}/lib'.format(pathlib.Path(__file__).parent.resolve())
sys.path.append(LIB_DIR)

from vfs import read_online_feature_values

vals = read_online_feature_values(
    featurestore_id="us_covid",
    entity_type_id="state",
    entity_id="DC",
    feature_ids=["death", "hospitalized"]
)
print(vals)
