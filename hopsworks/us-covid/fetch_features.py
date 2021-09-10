import mylib
from hsfs.feature import Feature

#
# As of 21/9/9, this is untested, as my Hopsworks jobs are stuck in
#   "initializing" state
#

# Connect and get feature group
connection = mylib.connect_using_envvars()
fs = connection.get_feature_store()
fg = fs.get_feature_group('us_covid', 1)

# Read features
print("Reading up-to-date data from offline store:")
print(fg.read().head(5))

DATE="2021-09-09 23:59:59"
print("Reading offline store data from %s: "%DATE)
print(fg.read(DATE).head(5))

# Online not working
#print("Reading up-to-date data from online store:")
#print(fg.read(online=True).head(5))

print("Retrieving just DC data")
query = fg.select_all().filter(Feature("state") == "DC")
query.show(5)

# Generate a dataset for DC data
#td = fs.create_training_dataset("dc_covid_data",
#                                version=1,
#                                data_format="tfrecords",
#                                description="A test training dataset saved in TfRecords format",
#                                splits={'train': 0.7, 'test': 0.2, 'validate': 0.1})
#td.save(query)

# fin
connection.close()
