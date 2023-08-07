class Endpoint:
    HELLO_WORLD = "/hello"
    ARTICLE = "/api/articles"
    # get all article
    ARTICLE1 = "/api/articles/<string:slug>"
    # get single article
    ARTICLE_COMMENTS = "/api/articles/<string:slug>/comments"
    # get comment of article
    ARTICLE_COMMENTS1 = "/api/articles/<string:slug>/comments/<int:id>"
    # delete comment
    ARTICLE_FAVORITE = "/api/articles/<string:slug>/favorite"
    TAG = "/api/tags"
    # get all of tags
    USER = "/api/users"
    # registration
    USER4 = "/api/user"
    # get current user and update user
    USER1 = "/api/users/login"
    # login
    USER2 = "/api/profiles/<string:username>"
    # get profiles
    USER3 = "/api/profiles/<string:au_username>/follow"
    # follow user and unfollow user
