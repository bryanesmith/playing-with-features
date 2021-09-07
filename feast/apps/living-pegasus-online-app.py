import sys
sys.path.append('lib')

from feast import FeatureStore
from mylib import announce

fs = FeatureStore(repo_path="../living_pegasus")

announce('fetching online features')
online_features = fs.get_online_features(
    features=[
        'state_daily_stats:death',
        'state_daily_stats:hospitalized'
    ],
    entity_rows=[
        {"state": "DC"},
        {"state": "VA"}]
).to_dict()

print(online_features)
