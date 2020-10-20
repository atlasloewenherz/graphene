import graphene
from graphql import GraphQLError

from help.graphql import BaseMutation
from help.graphql.user.types import CreateUserType
from .models import User as UserModel

class UserInput(graphene.InputObjectType):
    username = graphene.String(name='username', required=True)
    password = graphene.String(name='password',required=True)
    email = graphene.String(name='email', required=True)




class CreateUser(BaseMutation):
    #class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)
    user = graphene.Field(CreateUserType)


    def mutate( root, info, user_data=None):
        user = CreateUserType(username=user_data.username, password=user_data.password, email=user_data.email)
        db_user = UserModel.query.filter_by(username=user_data.username).first()
        if db_user:
            raise GraphQLError("Username already registered")
        else:
            duser = UserModel(username=user_data.username, password=user_data.password, email=user_data.email)
            db.add(duser)
            db.commit()
        return CreateUser(user=user)