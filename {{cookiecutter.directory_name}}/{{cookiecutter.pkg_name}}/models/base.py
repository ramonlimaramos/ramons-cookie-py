from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['db_session', 'Base', 'CreatedAtMixin', 'UpdatedAtMixin']

db_session = scoped_session(sessionmaker(autoflush=True, autocommit=False))
Base = declarative_base()
Base.query = db_session.query_property()