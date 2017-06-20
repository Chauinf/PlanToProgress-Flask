from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
lists = Table('lists', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=32)),
    Column('detail', String(length=128)),
    Column('tag', String(length=32)),
    Column('timestamp', DateTime),
    Column('before', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['lists'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['lists'].drop()
