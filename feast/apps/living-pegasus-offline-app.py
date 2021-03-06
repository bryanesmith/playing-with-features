import sys
sys.path.append('lib')

from feast import FeatureStore
import pandas as pd
from datetime import datetime, timedelta
from mylib import announce

entity_df = pd.DataFrame(
    {
        "event_timestamp": [
            datetime.now(),
            datetime.now()
        ],
        "state": ['DC', 'VA']
    }
)

fs = FeatureStore(repo_path="../feature-repos/living_pegasus")

announce('listing feature views:')
print(fs.list_feature_views())

fv = fs.get_feature_view("living_pegasus")
print(fv)

training_df = fs.get_historical_features(
    features=[
        'living_pegasus:death',
        'living_pegasus:hospitalized'
    ],
    entity_df=entity_df,
).to_df()

announce('sampling few features:')
print(training_df.tail(5))
