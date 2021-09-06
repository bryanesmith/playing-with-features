from feast import FeatureStore 
import pandas as pd
from datetime import datetime, timedelta

def announce(s:str):
    hr="- " * 20
    print()
    print(hr)
    print(s)
    print(hr)

entity_df = pd.DataFrame(
    {
#        "event_timestamp": [pd.Timestamp(datetime.now(), tz="UTC")],
        "event_timestamp": [
            datetime.now(),
            datetime.now() - timedelta(minutes=11),
            datetime.now() - timedelta(minutes=36),
            datetime.now() - timedelta(minutes=73),
        ],

        "driver_id": [1001] * 4
    }
)

features = [
    "driver_trips:average_daily_rides",
    "driver_trips:maximum_daily_rides",
    "driver_trips:rating",
    "driver_trips:rating:trip_completed",
]

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

