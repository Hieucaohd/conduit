class Endpoint:
    HELLO_WORLD = "/"
    ARTICLE = "/api/articles"
    ARTICLE1 ="/api/articles/<string:slug>"
    ARTICLE_COMMENTS ="/api/articles/<string:slug>/comments"
    ARTICLE_FAVORITE ="/api/articles/<string:slug>/favorite"
    TAG ="/api/tags"
