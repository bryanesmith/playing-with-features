import sys
sys.path.append('lib')

from feast import FeatureStore
from mylib import announce

fs = FeatureStore(repo_path="../driven_hyena")

announce('fetching online features')
online_features = fs.get_online_features(
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate"
    ],
    entity_rows=[
        {"driver_id": 1001},
        {"driver_id": 1002}]
).to_dict()

print(online_features)
