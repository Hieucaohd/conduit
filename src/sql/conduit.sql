DROP TABLE IF EXISTS conduit.favorited ;
DROP TABLE IF EXISTS conduit.followed ;
DROP TABLE IF EXISTS conduit.tag ;
DROP TABLE IF EXISTS conduit.comments ;
DROP TABLE IF EXISTS conduit.article ; 
DROP TABLE IF EXISTS conduit.author ;

CREATE TABLE conduit.author (
    username TEXT UNIQUE PRIMARY KEY , 
    password  TEXT NOT NULL , 
    image TEXT ,  
    bio TEXT  ,
    author_token TEXT 
);
CREATE TABLE conduit.article (
    slug TEXT PRIMARY KEY ,
    title TEXT NOT NULL ,
    description TEXT NOT NULL , 
    body TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE ,
    updated_at TIMESTAMP WITH TIME ZONE ,
    author_name TEXT,
    CONSTRAINT fk_author
    FOREIGN KEY(author_name) 
    REFERENCES conduit.author(username)
);


CREATE TABLE conduit.tag (
    tag_name TEXT[] ,
    article_slug TEXT ,
    CONSTRAINT fk_article 
    FOREIGN KEY(article_slug)
    REFERENCES conduit.article(slug)
);
CREATE TABLE conduit.favorited (
    article_slug TEXT ,
    username TEXT , 
    PRIMARY KEY (article_slug,username),
    CONSTRAINT fk_user 
    FOREIGN KEY (username)
    REFERENCES conduit.author(username),
    CONSTRAINT fk_article
    FOREIGN KEY (article_slug) 
    REFERENCES conduit.article(slug)
);
CREATE TABLE conduit.followed (
    author_username TEXT ,
    user_username TEXT ,
    PRIMARY KEY (author_username,user_username) ,
    CONSTRAINT fk_author 
    FOREIGN KEY (author_username)
    REFERENCES conduit.author(username),
    CONSTRAINT fk_user_follow
    FOREIGN KEY (user_username) 
    REFERENCES conduit.author(username)
);

CREATE TABLE conduit.comments (
		id SERIAL PRIMARY KEY ,
		created_at TIMESTAMP WITH TIME ZONE ,
		updated_at TIMESTAMP WITH TIME ZONE ,
		body TEXT , 
		article_slug TEXT , 
		author_name TEXT ,
		CONSTRAINT fk_article 
    FOREIGN KEY (article_slug) 
    REFERENCES conduit.article(slug),
	CONSTRAINT fk_author
    FOREIGN KEY (author_name) 
    REFERENCES conduit.author(username)
);


