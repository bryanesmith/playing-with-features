import sys
sys.path.append('lib')

from feast import FeatureStore
from mylib import announce

fs = FeatureStore(repo_path="../feature-repos/covid_gcp")

announce('fetching online features')
online_features = fs.get_online_features(
    features=[
        'covid_gcp:death',
        'covid_gcp:hospitalized'
    ],
    entity_rows=[
        {"state": "DC"},
        {"state": "VA"}]
).to_dict()

print(online_features)
