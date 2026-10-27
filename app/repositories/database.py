from sqlalchemy import Column, Date, Float, Integer, MetaData, String, Table, create_engine
from sqlalchemy.orm import registry, scoped_session, sessionmaker

from app.domain.event import Event

metadata = MetaData()

events_table = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("event_type", String(32), nullable=False),
    Column("event_date", Date, nullable=False),
    Column("guest_count", Integer, nullable=False),
    Column("budget", Float, nullable=False),
)

_mapper_registry = registry()


def map_event():
    """Tell SQLAlchemy how Event is stored, without Event having to know about SQLAlchemy."""
    if not _mapper_registry.mappers:
        _mapper_registry.map_imperatively(Event, events_table)


def make_session(database_url):
    """Connect to the database, create the tables if they are missing, and return a session."""
    map_event()
    engine = create_engine(database_url)
    metadata.create_all(engine)
    # scoped_session gives each thread (each request) its own session.
    return scoped_session(sessionmaker(bind=engine))
