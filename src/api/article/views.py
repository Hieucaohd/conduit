from flask import Blueprint
from src.api.urls import Endpoint
from src.api import HttpMethod
from src.common.utils.alchemy import execute_sql
blueprint = Blueprint("article",__name__)

@blueprint.route(Endpoint.ARTICLE, methods =[HttpMethod.GET])
def get_articles():
    state = """SELECT
	slug,
	title,
	description,
	body,
	created_at,
	updated_at,
	username,
	bio,
	image 
FROM
conduit.article AS article
LEFT JOIN conduit.author ON article.author_name = conduit.author.username""" 
    
    result = execute_sql(state)
    author = {}
    for a in result :
        b = a["updated_at"]
        c = a["created_at"]
        del a["created_at"] 
        del a["updated_at"]
        a['updatedAt'] = b 
        a['createdAt'] = c 
        a['tagList'] = ["dragons", "training"]
        a["favorited"] = False
        a["favoritesCount"] = 0
        username = a["username"]
        bio = a["bio"] 
        image = a["image"]
        author["username"] = username 
        author["bio"] = bio 
        author["image"] = image
        del a["username"] 
        del a["bio"]
        del a["image"]
        author["following"] = False  
        a["author"] = author  
    dict_return = {"articles":result,
                   "articlesCount" :len(result),
                }
    
    return dict_return 



@blueprint.route(Endpoint.ARTICLE1, methods =[HttpMethod.GET])
def get_single_article(slug):
    state = f"""SELECT
	slug,
	title,
	description,
	body,
	created_at,
	updated_at,
	username,
	bio,
	image 
FROM
	conduit.article AS article
	LEFT JOIN conduit.author ON article.author_name = conduit.author.username 
WHERE
	article.slug = '{slug}' """
    result = execute_sql(state)
    if len(result) == 0 :
        return {} 
    author = {}
    result = result[0] 
    b = result["updated_at"]
    c = result["created_at"]
    d = result
    del result["created_at"] 
    del result["updated_at"]
    result['updatedAt'] = b 
    result['createdAt'] = c 
    result['tagList'] = ["dragons", "training"]
    result["favorited"] = False
    result["favoritesCount"] = 0
    username = result["username"]
    bio = result["bio"] 
    image = result["image"]
    author["username"] = username 
    author["bio"] = bio 
    author["image"] = image
    del result["username"] 
    del result["bio"]
    del result["image"]
    author["following"] = False  
    result["author"] = author  
    dict_return = {"article":result,
            }
    
    return dict_return 

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




    