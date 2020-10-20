import graphene

from help.graphql import BaseQuery
from help.graphql.user.loaders import load_all_users
from help.graphql.user.types import UserType


class ActiveUserQuery(BaseQuery):
    active_users = graphene.List(
        lambda : UserType,
        description="list only active users",
        resolver=load_all_users
    )
