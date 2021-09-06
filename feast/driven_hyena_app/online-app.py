from feast import FeatureStore 

def announce(s:str):
    hr="- " * 20
    print()
    print(hr)
    print(s)
    print(hr)

features = [
    "driver_hourly_stats:conv_rate",
    "driver_hourly_stats:acc_rate"
]

fs = FeatureStore(repo_path="../driven_hyena")

announce('fetching online features')
online_features = fs.get_online_features(
    features=features,
    entity_rows=[
        {"driver_id": 1001},
        {"driver_id": 1002}]
).to_dict()

print(online_features)
