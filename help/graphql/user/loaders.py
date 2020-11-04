import logging

from help.graphql.user.types import UserType


logger = logging.getLogger(__name__)

def load_all_users(root, info):
    logger.debug(info)
    query = UserType.get_query(info)  # SQLAlchemy query
    return query.all()


def load_all_users(self, context, **kwargs):
    logger.debug(kwargs)
    query = UserType.get_query(context)  # SQLAlchemy query
    return query.all()
