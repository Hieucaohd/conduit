from flask import Blueprint
from src.api.urls import Endpoint
from src.api import HttpMethod
from src.common.utils.alchemy import execute_sql
from sqlalchemy.sql import text
blueprint = Blueprint("article",__name__)

@blueprint.route(Endpoint.ARTICLE, methods =[HttpMethod.GET])
def get_articles():
    state = "SELECT * FROM conduit.article" 
    result = execute_sql(state)
    author = {
        "username": "jake",
        "bio": "I work at statefarm",
        "image": "https://i.stack.imgur.com/xHWG8.jpg",
        "following": False
    }
    author['id'] = 1
    for a in result : 
        a["author"]= author
    dict_return = {"articles":result,
                   "articlesCount" :len(result),
                }
    
    return dict_return 



# @blueprint.route(Endpoint.ARTICLE1, methods =[HttpMethod.GET])
# def get_single_article(slug):
#     return slug 

# @blueprint.route(Endpoint.ARTICLE, methods =[HttpMethod.POST])
# def create_article():
#     return "created successfully"

# @blueprint.route(Endpoint.ARTICLE1, methods =[HttpMethod.PUT])
# def update_article(slug):
#     return f"updated successfully article has id {slug}"

# @blueprint.route(Endpoint.ARTICLE1, methods =[HttpMethod.DELETE])
# def detele_article(slug):
#     return f"deleted successfully article has id {slug}"

# @blueprint.route(Endpoint.ARTICLE_COMMENTS, methods =[HttpMethod.GET])
# def get_comments(slug):
#     return "comments" 

# @blueprint.route(Endpoint.ARTICLE_COMMENTS, methods =[HttpMethod.POST])
# def create_comments(slug):
#     return "comments" 

# @blueprint.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.POST])
# def add_favourite():
#     return "add favorite" 

# @blueprint.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.PUT])
# def delete_favourite():
#     return "delete favorite"

# @blueprint.route(Endpoint.TAG, methods=[HttpMethod.GET])
# def retrieve_tag():
#     return "all of tag" 




    