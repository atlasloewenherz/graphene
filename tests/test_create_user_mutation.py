import logging
from collections import OrderedDict
import logging

from help.graphql import SchemaBuilder

schema_builder = SchemaBuilder()
test_schema = schema_builder.build()

logger = logging.getLogger()
import faker
import graphene
logging.getLogger(faker.__name__).setLevel(logging.ERROR)
logging.getLogger(graphene.__name__).setLevel(logging.ERROR)

#logger.info(test_schema)


create_user_mutation_ql ='''
mutation myCreateUser {
  user(data: {
      username: "test", 
      email: "test@test.cz", 
      password: "479332973"
      }) {
    user {
        username
        email
        password
    }
  }
}

'''


create_user_mutation_ql_01 = '''
    mutation SomeOperationName {
    user(user_data:{username:"one", password:"two",email:"three"}) {
        username,
        password
        email
    }
    }    
'''

def test_empty_mutation(client):
    """Start with a blank database."""
    logger.info(dir(test_schema))
    schema_mutation = '''mutation {}'''
    result = test_schema.execute(schema_mutation)
    logger.info("result:  {}".format(result))
    assert result is not None
    print(result)


from graphene.test import Client

def test_create_user_mutation():
    logger.debug(type(test_schema))
    client = Client(test_schema)
    executed = client.execute(create_user_mutation_ql)
    logger.debug(executed)
    assert executed is not None