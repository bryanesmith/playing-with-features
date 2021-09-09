import hsfs
import mylib
from os.path import dirname, abspath
import pandas


# Load COVID data
d = dirname(dirname(abspath(__file__)))
df = pandas.read_parquet('%s/data/us-covid.parquet'%d)

print('Loaded COVID dataframe: ', df.head(5))

# connect to Hopsworks feature store
connection = mylib.connect_using_envvars()
fs = connection.get_feature_store()

# Get feature group and upload data
try:
    fg = fs.get_feature_group('us_covid', 1)
    if fg:
        fg.delete()
except Exception:  # TODO: use RestAPIError
    print("Couldn't find exiting feature group, nothing to delete.")

# Set time_travel_format=None, or else get error:
#   HTTP code: 404, HTTP reason: Not Found, error code: 270118, error msg: No data is available for feature group with this commit date, user msg: featureGroup: us_covid version 1
# See: https://community.hopsworks.ai/t/error-when-trying-to-save-to-online-feature-group/526/19
fg = fs.create_feature_group('us_covid',
                        version=1,
                        description="US COVID features by state",
                        primary_key=['date', 'state'],
                        time_travel_format=None,
                        online_enabled=True)
fg.save(df)

# fin
connection.close()
