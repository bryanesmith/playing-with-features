from feast import BigQuerySource, Entity, Feature, FeatureView, ValueType

driver_stats_source = BigQuerySource(
    table_ref="us-covid.daily_summaries.us_states",
    event_timestamp_column="date",
    created_timestamp_column=None,
)

state = Entity(name="state", value_type=ValueType.STRING, description="US state")

state_daily_stats_view = FeatureView(
    name="covid_gcp",
    entities=["state"],
    ttl=None,
    features=[
        Feature(name="death", dtype=ValueType.INT64),
        Feature(name="hospitalized", dtype=ValueType.INT64),
    ],
    online=True,
    batch_source=driver_stats_source,
    tags={},
)
