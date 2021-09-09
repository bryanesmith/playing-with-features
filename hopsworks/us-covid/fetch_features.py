import mylib
from hdfs import Feature

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
fg.read().show()

# Prob won't work, given had to disable time travel due to errors
DATE="2021-09-09 23:59:59"
print("Reading offline store data from %s: "%DATE)
fg.read(DATE).show()

print("Reading up-to-date data from online store:")
fg.read().show(online=True)

fg.select_all().filter(Feature("state") == "DC").show()

# fin
connection.close()
