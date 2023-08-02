from flask import Blueprint,request,jsonify,json
from datetime import datetime
from src.api.urls import Endpoint
from src.api import HttpMethod
from src.common.utils.alchemy import execute_sql,execute_sql2
from src.common.utils.condui_jwt import encode,decode 
blueprint = Blueprint("article",__name__)

@blueprint.route(Endpoint.ARTICLE, methods =[HttpMethod.GET])
def get_article() : 
    state = """SELECT
	article.slug,
	article.title,
	article.description,
	article.body,
	article.created_at,
	article.updated_at,
	tag.tag_name,
	author.username,
	author.bio,
	author.image,
	COUNT(favorited.article_slug) AS favorites_count 
FROM
	conduit.article AS article
	LEFT JOIN conduit.author ON article.author_name = conduit.author.username
	LEFT JOIN conduit.tag ON article.slug = conduit.tag.article_slug
	INNER JOIN conduit.favorited ON article.slug = favorited.article_slug
GROUP BY
	article.slug,
	article.title,
	article.description,
	article.body,
	article.created_at,
	article.updated_at,
	tag.tag_name,
	author.username,
	author.bio,
	author.image
""" 
    result = execute_sql(state)
    author = {} 
    for a in result : 
        author['username'] = a['username'] 
        author['bio'] = a['bio'] 
        author['image'] = a['image'] 
        author['following'] = False
        del a['username']
        del a['bio'] 
        del a['image'] 
        createdAt  = a['created_at'] 
        updatedAt  = a['created_at']
        tagList = a['tag_name'] 
        favorites_count = a['favorites_count']
        a['favoritesCount'] = favorites_count
        a['createdAt'] = createdAt 
        a['updatedAt'] = updatedAt
        a['tagList'] = tagList 
        del a['created_at']
        del a['updated_at']
        del a['tag_name']
        del a['favorites_count']
        a['author'] = author
        a['favorited'] = False
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
    d = result["tag_name"]
    del result["created_at"] 
    del result["updated_at"]
    del result["tag_name"]
    result['tagList'] = d
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
    dict_return = {"article":result,
    }
    return dict_return 


@blueprint.route(Endpoint.ARTICLE, methods=[HttpMethod.POST])
def create_article():
    to = request.headers.get("Authorization")
    token = to[6:]
    if not token: 
        return jsonify({"message": "your token is not committed or invalid"})
    
    jwt_token = decode(token) 
    username = jwt_token['username']
    if not username: 
        return jsonify({"message": "check your token again"})
    
    data = request.get_json()
    title = data.get('article', {}).get('title')
    state = f"""SELECT * FROM conduit.article WHERE slug = '{title}'"""
    result = execute_sql(state)
    if result:
        return jsonify({"message": "article was existed"})
    
    description = data.get('article', {}).get('description')
    body = data.get('article', {}).get('body') 
    tagList = list(data.get('article', {}).get('tagList'))
    
    current_date_time = datetime.now()
    state = f"""INSERT INTO conduit.article(slug,title,description,body,created_at,updated_at,author_name)
                VALUES('{title}','{title}','{description}','{body}','{current_date_time}','{current_date_time}','{username}')"""
    
    execute_sql2(state)
    
    state1 = f"""INSERT INTO conduit.tag(tag_name,article_slug)
                VALUES (ARRAY{tagList},'{title}')"""
    
    execute_sql2(state1)
    
    return jsonify({'message': 'success'})
    # state1 = f"""SELECT username,bio,image FROM conduit.author WHERE username = '{username}'"""
    # result1 = execute_sql(state1)
    # result_main = result1[0]
    # article = {}
    # article['slug'] = title 
    # article['title'] = title 
    # article['description'] = description 
    # article['body'] = body 
    # article['tagList'] = tagList 
    # article['created_At'] = current_date_time 
    # article['updated_At'] = current_date_time 
    # article["favorited"] = False 
    # article["favoritesCount"] = 0 
    # author ={} 
    # author['username'] = result_main['username']
    # author['bio'] = result_main['bio']
    # author['image'] = result_main['image'] 
    # author['following'] = False 
    # article['author'] = author 
    # return { 
    #     'article':article, 
    # }    
    



@blueprint.route(Endpoint.ARTICLE1, methods =[HttpMethod.PUT])
def update_article(slug):
    to = request.headers.get('Authorization')
    token = to[6:] 
    if not token :
        return jsonify({'message':'check your token'})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username :
        return "check your token again"
    data = request.get_json()
    title = data.get('article', {}).get('title')
    state = f"""SELECT author_name FROM conduit.article WHERE slug='{slug}'"""
    result = execute_sql(state) 
    result = result[0]['author_name']
    if result == username :
        state =f"""UPDATE conduit.article SET title = '{title}' WHERE slug = '{slug}'""" 
        execute_sql2(state)
    return jsonify({'message':'updated article'})



@blueprint.route(Endpoint.ARTICLE1, methods =[HttpMethod.DELETE])
def detele_article(slug):
    to = request.headers.get('Authorization')
    token = to[6:]
    if not token :
        return jsonify({'message':'check your token'})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username :
        return jsonify({'message':'check your token'})
    state = """DELETE """
    return f"deleted successfully article has id {slug}"


@blueprint.route(Endpoint.ARTICLE_COMMENTS, methods =[HttpMethod.GET])
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

@blueprint.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.POST])
def add_favourite(slug):
    to = request.headers.get('Authorization')
    token = to[6:]
    if not token :
        return jsonify({'message':'check your token'})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username :
        return jsonify({'message':'check your token'})
    state =f"""INSERT INTO conduit.favorited(article_slug,username)
        VALUES ('{slug}','{username}')"""
    execute_sql2(state) 
    result = get_single_article(slug)
    return result      

# @article.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.PUT])
# def delete_favourite():
#     return "delete favorite"

@blueprint.route(Endpoint.TAG, methods=[HttpMethod.GET])
def retrieve_tag():
    state = """SELECT 
	        tag_name
            FROM conduit.tag """
    result = execute_sql(state)
    tag = []
    for i in result :
        tag.append(i['tag_name'])
    tag_name = {"tags" : tag}
    return tag_name 






    