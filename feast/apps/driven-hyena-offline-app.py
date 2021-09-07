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
            datetime.now() - timedelta(minutes=11),
            datetime.now() - timedelta(minutes=36),
            datetime.now() - timedelta(minutes=73),
        ],
        "driver_id": [1001] * 4
    }
)

fs = FeatureStore(repo_path="../driven_hyena")

announce('listing feature views:')
print(fs.list_feature_views())

fv = fs.get_feature_view("driver_hourly_stats")
print(fv)

training_df = fs.get_historical_features(
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate"
    ],
    entity_df=entity_df
).to_df()

announce('sampling few features:')
print(training_df.tail(5))
