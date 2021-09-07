import sys
sys.path.append('lib')

from feast import FeatureStore
from mylib import announce

fs = FeatureStore(repo_path="../feature-repos/living_pegasus")

announce('fetching online features')
online_features = fs.get_online_features(
    features=[
        'living_pegasus:death',
        'living_pegasus:hospitalized'
    ],
    entity_rows=[
        {"state": "DC"},
        {"state": "VA"}]
).to_dict()

print(online_features)
