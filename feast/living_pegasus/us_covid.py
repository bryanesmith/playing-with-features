from feast import Entity, Feature, FeatureView, FileSource, ValueType

us_covid_stats = FileSource(
    path="/Users/bryan/Developer/playing-with-features/feast/living_pegasus/data/us-covid.parquet",
    event_timestamp_column="date",
    created_timestamp_column=None,
)

state = Entity(name="state", value_type=ValueType.STRING, description="US state")

state_daily_stats_view = FeatureView(
    name="state_daily_stats",
    entities=["state"],
    ttl=None,
    features=[
        Feature(name="death", dtype=ValueType.INT64),
        Feature(name="hospitalized", dtype=ValueType.INT64),
    ],
    online=True,
    batch_source=us_covid_stats,
    tags={},
)
