from flask import Blueprint
from src.api.urls import Endpoint
from src.api import HttpMethod

blueprint = Blueprint("article",__name__)

@blueprint.route(Endpoint.ARTICLE, methods =[HttpMethod.GET])
def get_articles():
    return "article"

@blueprint.route(Endpoint.ARTICLE1, methods =[HttpMethod.GET])
def get_single_article(slug):
    return slug 

@blueprint.route(Endpoint.ARTICLE, methods =[HttpMethod.POST])
def create_article():
    return "created successfully"

@blueprint.route(Endpoint.ARTICLE1, methods =[HttpMethod.PUT])
def update_article(slug):
    return f"updated successfully article has id {slug}"

@blueprint.route(Endpoint.ARTICLE1, method =[HttpMethod.DELETE])
def detele_article(slug):
    return f"deleted successfully article has id {slug}"

@blueprint.route(Endpoint.ARTICLE_COMMENTS, method =[HttpMethod.GET])
def get_comments(slug):
    return "comments" 

@blueprint.route(Endpoint.ARTICLE_COMMENTS, method =[HttpMethod.POST])
def create_comments(slug):
    return "comments" 

@blueprint.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.POST])
def add_favourite(slug):
    return "add favorite" 

@blueprint.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.PUT])
def delete_favourite(slug):
    return "delete favorite"

@blueprint.route(Endpoint.TAG, methods=[HttpMethod.GET])
def retrieve_tag(slug):
    return "all of tag" 




    