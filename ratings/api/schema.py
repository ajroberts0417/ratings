import graphene

from ratings.api.ratings_schema import RatingsMutation, RatingsQuery


class Query(RatingsQuery):
    pass


class Mutation(RatingsMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
