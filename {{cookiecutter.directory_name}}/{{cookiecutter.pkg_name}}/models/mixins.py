from datetime import datetime
from sqlalchemy import Column, DateTime


class CreatedAtMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class UpdatedAtMixin(object):
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, index=True)
