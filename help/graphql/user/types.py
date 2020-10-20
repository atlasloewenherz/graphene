import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import User as UserModel

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




class UserType(SQLAlchemyObjectType, UserAttribute):
    class Meta:
        model = UserModel
        #interfaces = (relay.Node,)
