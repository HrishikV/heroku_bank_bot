from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory
from cassandra.auth import PlainTextAuthProvider


def connect_dataset():
    client_id = 'rxJUigxgmKYqfyfkZmLZvRlo'
    client_secret = '3WNuvDMYSzlP7Q1BKUWS6S0,i3YiKtMijXGoUUL6+pt1TbM9DHC0xv,FGm3CqNBG-kRfrrowXJJELG_47r1mLFlfnJc5ZZrLrNv7yhB68F5b7s-f0FdPJ2mucuGETr8,'
    cloud_config = {
        'secure_connect_bundle': './secure-connect-bankbot.zip'
    }
    auth_provider = PlainTextAuthProvider(client_id, client_secret)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    session.row_factory = named_tuple_factory
    return session
