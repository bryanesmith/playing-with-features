import sys
import pathlib

LIB_DIR='{}/lib'.format(pathlib.Path(__file__).parent.resolve())
sys.path.append(LIB_DIR)

from google.cloud import aiplatform
from vfs import create_featurestore_sample, create_entity_type_sample, create_feature, import_feature_values

create_featurestore_sample(featurestore_id="us_covid")

create_entity_type_sample(
    featurestore_id="us_covid",
    entity_type_id="state",
    description="State in the United States"
)

create_feature(
    featurestore_id="us_covid",
    entity_type_id="state",
    feature_id="death",
    value_type=aiplatform.gapic.Feature.ValueType.INT64,
    description="The cumulative confirmed COVID-related death count for the state."
)

create_feature(
    featurestore_id="us_covid",
    entity_type_id="state",
    feature_id="hospitalized",
    value_type=aiplatform.gapic.Feature.ValueType.INT64,
    description="The cumulative confirmed COVID-related hospitalized count for the state."
)

import_feature_values(
    featurestore_id="us_covid",
    entity_type_id="state",
    entity_id_field="state",
    feature_time_field="date",
)
