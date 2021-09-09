import hsfs
import os

def connect_using_envvars():

    # Get environment variables
    for var in ['HSFS_HOST', 'HSFS_PORT', 'HSFS_API_KEY', 'HSFS_PROJECT']:
        if var not in os.environ:
            raise EnvironmentError("Must set environment variable: %s"%var)

    host = os.environ['HSFS_HOST']
    port = os.environ['HSFS_PORT']
    api_key = os.environ['HSFS_API_KEY']
    project = os.environ['HSFS_PROJECT']

    return hsfs.connection(
        host=host,
        port=port,
        project=project,
        api_key_value=api_key,
        hostname_verification=True
    )
