import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import User as UserModel
from ..sqlalchemy import SQLAlchemyInputObjectType


class UserAttribute:
    firstname = graphene.String(description="first Name of the User.")
    lastname = graphene.String(description="Last Name of the User.")
    username = graphene.String(description="Username of the User.")
    email = graphene.String(description="E-Mail of the User.")
    password = graphene.String(description="Password of the User.")




class CreateUserType(graphene.ObjectType):
    username = graphene.String(description="Username of the User.")
    email = graphene.String(description="E-Mail of the User.")
    password = graphene.String(description="Password of the User.")



class RegisterUserType(graphene.ObjectType):
    username = graphene.String(description="Username of the User.")
    email = graphene.String(description="E-Mail of the User.")
    password = graphene.String(description="Password of the User.")




class UserType(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        #exclude_fields = ['id']
        #interfaces = (graphene.relay.Node,)


class RegisterUserInputType(graphene.InputObjectType):
    username = graphene.String(name='username', required=True)
    password = graphene.String(name='password',required=True)
    email = graphene.String(name='email', required=True)


class CreateUserInputType(SQLAlchemyInputObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ['id']

class UpdateUserInputType(graphene.InputObjectType, UserAttribute):
    id = graphene.ID(description="global User id.")
