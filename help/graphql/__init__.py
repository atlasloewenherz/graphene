import importlib
import logging
import os
from abc import abstractmethod
from inspect import getmembers, isclass
from pathlib import Path

import graphene

logger = logging.getLogger(__name__)

class BaseQuery(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    pass

class BaseMutation(graphene.Mutation):
    class Meta:
        abstract = True
    @property
    @abstractmethod
    def mutation_name(self):
        pass

class BaseSubscription(graphene.ObjectType):
    @property
    @abstractmethod
    def subscription_name(self):
        pass

    pass

class OperationAbstract(graphene.ObjectType):
    scopes = ['unauthorized']
    pass


class SchemaBuilder:
    def __init__(self, api_path='help/graphql'):
        self.queries = [OperationAbstract]
        self.mutations = [OperationAbstract]

        self.queries_properties = {}
        self.mutations_properties = {}

        self.api_path = api_path
        # TODO: resolve from configuration
        base_dir = Path(api_path).resolve()
        self.subdirectories = [
            x
            for x in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, x)) and x not in ['__pycache__', 'main']
        ]

    def add_queries(self, queries):
        for query_class in queries:
            logger.debug("adding Query {0}".format(query_class))
            logger.debug("Adding properties {} of Query: {} to QueryProperties".format(query_class.__dict__, query_class.__name__))
            self.queries_properties.update(query_class.__dict__['_meta'].fields)
            self.queries.append(query_class)

    def add_mutations(self, mutations):
        for mutation_class in mutations:
            logger.debug("adding Mutation {0}".format(mutation_class))
            logger.debug("Adding properties {} of Query: {} to QueryProperties".format(mutation_class.__dict__, mutation_class.__name__))
            self.mutations_properties.update(mutation_class.__dict__['_meta'].fields)
            self.mutations.append(mutation_class)
    """
    import either queries module ( query.py ) or mutations module (mutations.py) for the provided directory
    """
    def import_graphql_module(self, directory, module_name):
        logging.debug("importing: {}.{}.{}".format(self.api_path, directory, module_name))
        try:
            base = ""
            if not self.api_path.rindex("/"):
                base = self.api_path
            else:
                base = self.api_path.replace("/", ".")
            module = importlib.import_module(f'{base}.{directory}.{module_name}')
            return module
        except ModuleNotFoundError as error:
            logging.error("ERROR: {}".format(error,))

    def build(self):
        try:
            for directory in self.subdirectories:
                #TODO resolve via App configuration
                query_module = self.import_graphql_module(directory, "queries")
                if query_module:
                    qclasses = [x for x in getmembers(query_module, isclass)]# get all classes within the module
                    queries_ = [x[1] for x in qclasses if (issubclass(x[1], BaseQuery) and x[1] != BaseQuery)] # get only Queries as they inherit from 'BaseQuery'
                    for query_ in queries_:
                        logger.debug(type(query_))
                        logger.debug("Class: {} in module: {}".format(query_.__name__,query_module ))    
                        for field in query_.__dict__:
                            logger.debug("\t Field: {} ".format(field,))
                    self.add_queries(queries_)

                mutation_module = self.import_graphql_module(directory, "mutations")
                if mutation_module:
                    mclasses = [x for x in getmembers(mutation_module, isclass)]
                    mutations_ = [x[1] for x in mclasses if (issubclass(x[1], BaseMutation) and x[1] != BaseMutation)]
                    for mutation_ in mutations_:
                        logger.debug("Class: {} in module: {}".format(mutation_.__name__,mutation_module ))    
                        for field in mutation_.__dict__:
                            logger.debug("\t Field: {} ".format(field,))
                    self.add_mutations(mutations_)
                else:
                    logger.debug("Neither a Query not a Mutation module")
                    pass
            _queries = self.queries[::-1]
            _mutations = self.mutations[::-1]
            if (len(_queries)<=1 or len(_mutations) <=1):
                return None
            _queries_properties = self.queries_properties
            _mutations_properties = self.mutations_properties
            queries_tuple = tuple(_queries)
            mutations_tuple = tuple(_mutations)
            Queries = type('Query', queries_tuple, _queries_properties)
            logger.debug("Queries Root class: {} Properties: {}".format(Queries.__name__, vars(Queries)))
            logger.debug("Mutation name: {} FIELD: {}".format(_mutations[0].mutation_name, _mutations[0].Field()))
            #Mutations = type('Mutations', mutations_tuple, _mutations_properties)

            _mtuple = tuple([graphene.ObjectType,])

            Mutation = type('Mutation', _mtuple, { _mutations[0].mutation_name: _mutations[0].Field(),})
            logger.debug(type(Mutation))
            return graphene.Schema(query=Queries, mutation=Mutation)
        except (RuntimeError, TypeError, NameError, Exception) as error:
            logging.error("ERROR: {}".format(error, ))


#schema_builder = SchemaBuilder()
#schema = schema_builder.build()
#logger.debug(schema)
