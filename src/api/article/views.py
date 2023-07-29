from flask import Blueprint
from src.api.urls import Endpoint
from src.api import HttpMethod
from src.common.utils.alchemy import execute_sql
article = Blueprint("article",__name__)

@article.route(Endpoint.ARTICLE, methods =[HttpMethod.GET])
def get_article() : 
    state = """SELECT
	slug,
	title,
	description,
	body,
	created_at,
	updated_at,
	tag_name,
	username,
	bio,
	image 
FROM
	conduit.article AS article
	LEFT JOIN conduit.author ON article.author_name = conduit.author.username 
	LEFT JOIN conduit.tag ON article.slug = conduit.tag.article_slug 
ORDER BY
  slug ASC;
""" 
    state1 ="""SELECT
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
    
    list_slug_with_tag_name = []
    current_article = result[0]
    taglist = []
    for i in result :
        if i['slug'] == current_article['slug'] :
            taglist.append(i['tag_name'])
        else : 
            del current_article['tag_name']
            current_article['tagList']=taglist
            list_slug_with_tag_name.append(current_article)
            current_article = i 
            taglist=[i['tag_name']]

    del current_article['tag_name']
    current_article['tagList']=taglist 
    list_slug_with_tag_name.append(current_article)

    
    result1 = execute_sql(state1) 
    author = {} 
    for a in result1 : 
        author['username'] = a['username'] 
        author['bio'] = a['bio'] 
        author['image'] = a['image'] 
        author['following'] = False
        del a['username']
        del a['bio'] 
        del a['image'] 
        createdAt  = a['created_at'] 
        updatedAt  = a['created_at'] 
        a['createdAt'] = createdAt 
        a['updatedAt'] = updatedAt 
        del a['created_at']
        del a['updated_at']
        a['author'] = author
        a['favorited'] = False
        a['favoritesCount'] = 0 
        # a['tagList'] = []
    for a in result1 :     
        for i in list_slug_with_tag_name :
            if i['slug'] == a['slug'] :
                a['tagList'] = i['tagList']


    dict_return = {"articles":result1,
                    "articlesCount" :len(result1),
                    }
    
    return dict_return 



@article.route(Endpoint.ARTICLE1, methods =[HttpMethod.GET])
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
    state_with_tag = f"""SELECT
	slug,
	title,
	description,
	body,
	created_at,
	updated_at,
	tag_name,
	username,
	bio,
	image 
FROM
	conduit.article AS article
	LEFT JOIN conduit.author ON article.author_name = conduit.author.username 
	LEFT JOIN conduit.tag ON article.slug = conduit.tag.article_slug 
WHERE 
	article.slug in ('{slug}') """ 
    result = execute_sql(state)
    if len(result) == 0 :
        return {} 
    author = {}
    result = result[0]
    b = result["updated_at"]
    c = result["created_at"]
    del result["created_at"] 
    del result["updated_at"]
    result['updatedAt'] = b 
    result['createdAt'] = c 
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
    
    result1 = execute_sql(state_with_tag)
    list_slug_with_tag_name = []
    current_article = result1[0]
    taglist = []
    for i in result1 :
        taglist.append(i['tag_name'])
    del current_article['tag_name']
    current_article['tagList']=taglist
    list_slug_with_tag_name.append(current_article)
    result["tagList"] = list_slug_with_tag_name[0]['tagList']
    dict_return = {"article":result,
            }
    
    return dict_return 

# @article.route(Endpoint.ARTICLE, methods =[HttpMethod.POST])
# def create_article():
#     return "created successfully"

# @article.route(Endpoint.ARTICLE1, methods =[HttpMethod.PUT])
# def update_article(slug):
#     return f"updated successfully article has id {slug}"

# @article.route(Endpoint.ARTICLE1, methods =[HttpMethod.DELETE])
# def detele_article(slug):
#     return f"deleted successfully article has id {slug}"

@article.route(Endpoint.ARTICLE_COMMENTS, methods =[HttpMethod.GET])
def get_comments(slug):
    state = f"""
SELECT 
	id ,
	comments.created_at,
	comments.updated_at,
	comments.body,
	author.username,
	author.bio,
	author.image
FROM conduit.comments AS comments 
INNER JOIN conduit.author ON comments.author_name = author.username 
RIGHT JOIN conduit.article ON comments.article_slug = article.slug 
WHERE 
	slug in ('{slug}')
"""
    result = execute_sql(state)
    author = {}
    for i in result : 
        a = i['username']
        b = i['bio']
        c = i['image']
        i['createdAt'] = i['created_at']
        i['updatedAt'] = i['updated_at']
        del i['created_at']
        del i['updated_at'] 
        del i['username']
        del i['bio']
        del i['image']
        author['username'] = a 
        author['bio'] = b 
        author['image'] = c 
        author['following'] = False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        i['author'] = author 
    dict_return = {'comments' :result , 
    }
    return dict_return



# @article.route(Endpoint.ARTICLE_COMMENTS, methods =[HttpMethod.POST])
# def create_comments(slug):
#     return "comments" 

# @article.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.POST])
# def add_favourite():
#     return "add favorite" 

# @article.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.PUT])
# def delete_favourite():
#     return "delete favorite"

@article.route(Endpoint.TAG, methods=[HttpMethod.GET])
def retrieve_tag():
    state = """SELECT 
	        tag_name
            FROM conduit.tag """
    result = execute_sql(state)
    tag = []
    for i in result :
        tag.append(i['tag_name'])
    tag_name = {"tags" : tag
    }
    return tag_name 






    