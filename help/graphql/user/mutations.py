from sqlite3 import IntegrityError

import graphene
from graphql import GraphQLError
import logging

from sqlalchemy.exc import SQLAlchemyError

from . import logger
from core import db
from help.graphql import BaseMutation
from help.graphql.user.types import CreateUserType, RegisterUserInputType, UserType, UpdateUserInputType, \
    RegisterUserType, CreateUserInputType
from .models import User as UserModel

class CreateUser(BaseMutation):
    class Arguments:
        user_data = CreateUserInputType(required=True)
    user = graphene.Field(CreateUserType)
    mutation_name = "create_user"

    def mutate( root, info, user_data=None):
        user = CreateUserType(username=user_data.username, password=user_data.password, email=user_data.email)
        db_user = UserModel.query.filter_by(email=user_data.email).first()
        if db_user:
            userAlreadyRegistredError=GraphQLError("Username already registered")
            logger.error(userAlreadyRegistredError)
            raise userAlreadyRegistredError
        else:
            duser = UserModel(username=user_data.username, password=user_data.password, email=user_data.email)
            try:
                db.session.add(duser)
                db.session.commit()
            except SQLAlchemyError as e:
                logger.debug(vars(e))
                logger.error(e)
                db.session.rollback()
                raise GraphQLError(e.orig)
        return CreateUser(user=user)



class RegisterUser(BaseMutation):
    class Arguments:
        user_data = RegisterUserInputType(required=True)
    user = graphene.Field(CreateUserType)
    mutation_name = "register_user"

    def mutate( root, info, user_data=None):
        user = RegisterUserType(username=user_data.username, password=user_data.password, email=user_data.email)
        db_user = UserModel.query.filter_by(email=user_data.email).first()
        if db_user:
            userAlreadyRegistredError=GraphQLError("Username already registered")
            logger.error(userAlreadyRegistredError)
            raise userAlreadyRegistredError
        else:
            duser = UserModel(username=user_data.username, password=user_data.password, email=user_data.email)
            try:
                db.session.add(duser)
                db.session.commit()
            except SQLAlchemyError as e:
                logger.debug(vars(e))
                logger.error(e)
                db.session.rollback()
                raise GraphQLError(e.orig)
        return RegisterUser(user=user)




class UpdateUser(BaseMutation):
    class Arguments:
        user_data = UpdateUserInputType()
    user = graphene.Field(UserType)
    mutation_name = "update_user"

    def mutate( root, info, user_data=None):
        logger.debug(user_data)
        user = UserModel.query.filter_by(email=user_data.email).update(user_data)
        logger.debug(user_data)
        return UpdateUser(user=user)