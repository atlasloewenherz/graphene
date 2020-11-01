import graphene
from graphql import GraphQLError
import logging
from core import db
from help.graphql import BaseMutation, logger
from help.graphql.user.types import CreateUserType, UserInputType
from .models import User as UserModel

class CreateUser(BaseMutation):
    class Arguments:
        user_data = UserInputType(required=True)
    user = graphene.Field(CreateUserType)
    mutation_name = "create_user"

    def mutate( root, info, user_data=None):
        user = CreateUserType(username=user_data.username, password=user_data.password, email=user_data.email)
        db_user = UserModel.query.filter_by(username=user_data.username).first()
        if db_user:
            userAlreadyRegistredError=GraphQLError("Username already registered")
            logger.error(userAlreadyRegistredError)
            raise userAlreadyRegistredError
        else:
            duser = UserModel(username=user_data.username, password=user_data.password, email=user_data.email)
            db.session.add(duser)
            db.session.commit()
        return CreateUser(user=user)