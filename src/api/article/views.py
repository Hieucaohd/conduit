from flask import Blueprint, request, jsonify
from datetime import datetime
from src.api.urls import Endpoint
from src.api import HttpMethod
from src.common.utils.alchemy import execute_sql, execute_sql2
from src.common.utils.condui_jwt import encode, decode
blueprint = Blueprint("article", __name__)


@blueprint.route(Endpoint.ARTICLE, methods=[HttpMethod.GET])
def get_article():
    where = response_para()
    state = f"""SELECT
            article.slug,
            article.title,
            article.description,
            article.body,
            article.created_at,
            article.updated_at,
            author.username,
            author.bio,
            author.image,
            COUNT(favorited.article_slug) AS favorites_count 
        FROM
            conduit.article AS article
            LEFT JOIN conduit.author ON article.author_name = conduit.author.username
            LEFT JOIN conduit.favorited ON article.slug = favorited.article_slug
            LEFT JOIN conduit.tag ON tag.article_slug = article.slug
        {where}
        GROUP BY
            article.slug,
            article.title,
            article.description,
            article.body,
            article.created_at,
            article.updated_at,
            author.username,
            author.bio,
            author.image
        """
    state = state.format(where)
    result = execute_sql(state)

    author = {}
    for a in result:
        taglist = retrieve_single_tag(slug=a['slug'])
        author['username'] = a['username']
        author['bio'] = a['bio']
        author['image'] = a['image']
        author['following'] = False
        del a['username']
        del a['bio']
        del a['image']
        createdAt = a['created_at']
        updatedAt = a['created_at']
        favorites_count = a['favorites_count']
        a['favoritesCount'] = favorites_count
        a['createdAt'] = createdAt
        a['updatedAt'] = updatedAt
        a['tagList'] = taglist
        del a['created_at']
        del a['updated_at']
        del a['favorites_count']
        a['author'] = author
        a['favorited'] = False
    dict_return = {"articles": result,
                   "articlesCount": len(result),
                   }

    return dict_return


def response_para():

    get_by_tag = request.args.get('tag')
    get_by_author = request.args.get('author')
    get_by_favorited = request.args.get('favorited')
    if get_by_tag:
        return f"WHERE TRIM(tag.tag_name) = '{get_by_tag}'"
    elif get_by_author:
        return f"WHERE article.author_name = '{get_by_author}'"
    elif get_by_favorited:
        return f"WHERE favorited.username ='{get_by_favorited}'"
    elif get_by_tag and get_by_author:
        return f"WHERE TRIM(tag.tag_name) ='{get_by_tag}' AND article.author_name = '{get_by_author}'"
    elif get_by_tag and get_by_favorited:
        return f"WHERE TRIM(tag.tag_name) ='{get_by_tag}' AND favorited.username ='{get_by_favorited}'"
    elif get_by_favorited and get_by_author:
        return f"WHERE favorited.username = '{get_by_favorited}' AND article.author_name ='{get_by_author}"
    elif get_by_author and get_by_favorited and get_by_tag:
        return f"WHERE favorited.username = '{get_by_favorited}' AND article.author_name='{get_by_author}' AND TRIM(tag.tag_name) ='{get_by_tag}'"
    else:
        return " "


@blueprint.route(Endpoint.ARTICLE1, methods=[HttpMethod.GET])
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
	article.slug in ('{slug}') """
    result = execute_sql(state)
    if len(result) == 0:
        return {}
    author = {}
    taglist = retrieve_single_tag(slug)
    result = result[0]
    b = result["updated_at"]
    c = result["created_at"]
    del result["created_at"]
    del result["updated_at"]
    result['updatedAt'] = b
    result['createdAt'] = c
    result["favorited"] = False
    result["favoritesCount"] = 0
    result['tagList'] = taglist
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
    dict_return = {"article": result,
                   }
    return dict_return


def retrieve_single_tag(slug):
    state = f"""SELECT * FROM conduit.tag WHERE tag.article_slug = '{slug}'"""
    article = execute_sql(state)
    current_article = article[0]
    list_slug_with_tag_name = []
    taglist = []
    for i in article:
        taglist.append(i['tag_name'])
    del current_article['tag_name']
    current_article['tagList'] = taglist
    list_slug_with_tag_name.append(current_article)
    list1 = []
    for i in list_slug_with_tag_name:
        list1.append(i['tagList'])
    list2 = []
    list3 = []
    for t in list1:
        for j in t:
            list2.append(j)
    for i in list2:
        if i not in list3:
            list3.append(i)
    return list3


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
    article_body = data.get('article', {})
    description = article_body.get('description')
    body = article_body.get('body')
    taglist = article_body.get('tagList', [])
    current_date_time = datetime.now()
    state = f"""INSERT INTO conduit.article(slug,title,description,body,created_at,updated_at,author_name)
                VALUES('{title}','{title}','{description}','{body}','{current_date_time}','{current_date_time}','{username}')"""
    execute_sql2(state)
    for i in taglist:
        state1 = f"""INSERT INTO conduit.tag(tag_name,article_slug)
                VALUES ('{i}','{title}')"""
        execute_sql2(state1)
    result = get_single_article(title)
    return result


@blueprint.route(Endpoint.ARTICLE1, methods=[HttpMethod.PUT])
def update_article(slug):
    to = request.headers.get('Authorization')
    token = to[6:]
    if not token:
        return jsonify({'message': 'check your token'})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return "check your token again"
    data = request.get_json()
    title = data.get('article', {}).get('title')
    description = data.get('article', {}).get('description')
    body = data.get('article', {}).get('body')
    taglist = data.get('article', {}).get('tagList')
    state = f"""SELECT author_name FROM conduit.article WHERE slug='{slug}'"""
    result = execute_sql(state)
    result = result[0]['author_name']

    if result == username:
        state = f"""UPDATE conduit.article SET title = '{title}',description='{description}',body = '{body}' WHERE slug = '{slug}'"""
        for i in taglist:
            state4 = """SELECT """
            # KIỂM TRA NẾU MÀ TAG LIST ĐÃ TỒN TẠI TRONG DATABASE CÙNG VỚI SLUG THÌ KHÔNG THÊM NỮA
            state3 = f"""INSERT INTO conduit.tag(tag_name,article_slug) VALUES ('{i}','{slug}')"""
            execute_sql2(state3)
        execute_sql2(state)
        result = get_single_article(slug)
        return result
    else:
        return jsonify({'message': 'you are not own of article'})


@blueprint.route(Endpoint.ARTICLE1, methods=[HttpMethod.DELETE])
def detele_article(slug):
    to = request.headers.get('Authorization')
    token = to[6:]
    if not token:
        return jsonify({'message': 'check your token'})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state2 = f"""SELECT author_name FROM conduit.article WHERE slug ='{slug}'"""
    result = execute_sql(state2)
    result = result[0]
    result = result['author_name']
    if username == result:
        state1 = f"""DELETE FROM conduit.tag WHERE tag.article_slug ='{slug}'"""
        execute_sql2(state1)
        state = f"""DELETE FROM conduit.article WHERE article.slug='{slug}'"""
        execute_sql2(state)


@blueprint.route(Endpoint.ARTICLE_COMMENTS, methods=[HttpMethod.POST])
def add_comments(slug):
    to = request.headers.get('Authorization')
    token = to[6:]
    if not token:
        return jsonify({'message': 'check your token'})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    data = request.get_json()
    body = data.get('comment', {}).get('body')
    date = datetime.now()
    state = f"""INSERT INTO conduit.comments(created_at,updated_at,body,article_slug,author_name) VALUES('{date}','{date}'
    ,'{body}','{slug}','{username}')"""
    execute_sql2(state)
    state1 = f"""SELECT 
	comments.id ,
	comments.created_at,
	comments.updated_at,
	comments.body,
	author.username,
	author.bio,
	author.image
     FROM conduit.comments LEFT JOIN 
    conduit.author ON comments.author_name = author.username 
    WHERE comments.created_at = '{date}' AND id IN (SELECT id FROM conduit.comments WHERE article_slug = 
    '{slug}' AND author_name = '{username}') """
    result = execute_sql(state1)
    result_main = result[0]
    a = result_main['created_at']
    b = result_main['updated_at']
    author = {}
    author['username'] = result_main['username']
    author['bio'] = result_main['bio']
    author['image'] = result_main['image']
    author['following'] = False
    del result_main['created_at']
    del result_main['updated_at']
    del result_main['bio']
    del result_main['image']
    del result_main['username']
    result_main['created_At'] = a
    result_main['updated_At'] = b
    result_main['author'] = author
    return {'comment': result_main}


@blueprint.route(Endpoint.ARTICLE_COMMENTS, methods=[HttpMethod.GET])
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
    for i in result:
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
    dict_return = {'comments': result,
                   }
    return dict_return


@blueprint.route(Endpoint.ARTICLE_COMMENTS1, methods=[HttpMethod.DELETE])
def delete_comments(slug, id):
    to = request.headers.get('Authorization')
    token = to[6:]
    if not token:
        return jsonify({'message': 'check your token'})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"""SELECT author_name FROM conduit.comments WHERE id = '{id}'"""
    result = execute_sql(state)
    result = result[0]
    author_comment = result['author_name']
    state1 = f"""SELECT author_name FROM conduit.article WHERE slug = '{slug}'"""
    result1 = execute_sql(state1)
    result1 = result1[0]
    author_article = result1['author_name']
    if username == author_comment and username == author_article:
        state2 = f""" DELETE FROM conduit.comments WHERE id = '{id}' """
        execute_sql2(state2)
        return jsonify({'message': 'deleted comment successfully'})
    else:
        return jsonify({'message': 'you are not own comments or own article'})


@blueprint.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.POST])
def add_favourite(slug):
    to = request.headers.get('Authorization')
    token = to[6:]
    if not token:
        return jsonify({'message': 'check your token'})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"""SELECT * FROM conduit.favorited """
    result = execute_sql(state)
    result = result[0]
    username_main = result['username']
    if username == username_main and result['article_slug'] == slug:
        return jsonify({"message": "you favorited this article"})
    state = f"""INSERT INTO conduit.favorited(article_slug,username)
        VALUES ('{slug}','{username}')"""
    execute_sql2(state)
    result = get_single_article(slug)
    return result
# KIỂM TRA NẾU NGƯỜI DÙNG ADD 2 LẦN SEVER CÓ SẬP KHÔNG
# NẾU MÀ ADD_FAVORITE 2 LẦN THÌ SỬA THÀNH UN_FAVORITE


@blueprint.route(Endpoint.ARTICLE_FAVORITE, methods=[HttpMethod.DELETE])
def un_favourite(slug):
    to = request.headers.get('Authorization')
    token = to[6:]
    if not token:
        return jsonify({"message": 'check your token'})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({"message": 'check your token'})
    state = f"""DELETE FROM conduit.favorited WHERE favorited.username = ('{username}') AND favorited.article_slug = ('{slug}')"""
    execute_sql2(state)
    result = get_single_article(slug)
    return result


@blueprint.route(Endpoint.TAG, methods=[HttpMethod.GET])
def retrieve_tag():
    state = """SELECT * FROM conduit.tag """
    article = execute_sql(state)
    list_slug_with_tag_name = []
    current_article = article[0]
    taglist = []
    for i in article:
        if i['article_slug'] == current_article['article_slug']:
            taglist.append(i['tag_name'])
        else:
            del current_article['tag_name']
            current_article['tagList'] = taglist
            list_slug_with_tag_name.append(current_article)
            current_article = i
            taglist = [i['tag_name']]

    del current_article['tag_name']
    current_article['tagList'] = taglist
    list_slug_with_tag_name.append(current_article)
    # print(list_slug_with_tag_name)
    list1 = []
    for i in list_slug_with_tag_name:
        list1.append(i['tagList'])
    list2 = []
    list3 = []
    for t in list1:
        for j in t:
            list2.append(j)
    for i in list2:
        if i not in list3:
            list3.append(i)
    return {"tags": list3}
