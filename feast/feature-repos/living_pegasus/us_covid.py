from feast import Entity, Feature, FeatureView, FileSource, ValueType

from os.path import dirname, abspath
d = dirname(dirname(dirname(abspath(__file__))))

csv_file = "%s/data/us-covid.csv"%d

us_covid_stats = FileSource(
    path="%s/data/us-covid.parquet"%d,
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
