DROP TABLE IF EXISTS conduit.favorited ;
DROP TABLE IF EXISTS conduit.followed ;
DROP TABLE IF EXISTS conduit.tag ;
DROP TABLE IF EXISTS conduit.comments ;
DROP TABLE IF EXISTS conduit.article ; 
DROP TABLE IF EXISTS conduit.author ;

CREATE TABLE conduit.author (
    id SERIAL PRIMARY KEY , 
    username TEXT UNIQUE  , 
    email TEXT ,
    password  TEXT NOT NULL , 
    image TEXT ,  
    bio TEXT  
);
CREATE TABLE conduit.article (
    slug TEXT PRIMARY KEY ,
    title TEXT NOT NULL ,
    description TEXT NOT NULL , 
    body TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE ,
    updated_at TIMESTAMP WITH TIME ZONE ,
    id_author INT ,
    CONSTRAINT fk_author
    FOREIGN KEY(id_author) 
    REFERENCES conduit.author(id)
);


CREATE TABLE conduit.tag (
    tag_name TEXT ,
    article_slug TEXT ,
    PRIMARY KEY(tag_name,article_slug),
    CONSTRAINT fk_article 
    FOREIGN KEY(article_slug)
    REFERENCES conduit.article(slug)
);
CREATE TABLE conduit.favorited (
    article_slug TEXT ,
    id_author INT , 
    PRIMARY KEY (article_slug,id_author),
    CONSTRAINT fk_user 
    FOREIGN KEY (id_author)
    REFERENCES conduit.author(id),
    CONSTRAINT fk_article
    FOREIGN KEY (article_slug) 
    REFERENCES conduit.article(slug)
);
CREATE TABLE conduit.followed (
    id_author INT ,
    id_user INT ,
    PRIMARY KEY (id_author,id_user) ,
    CONSTRAINT fk_author 
    FOREIGN KEY (id_author)
    REFERENCES conduit.author(id),
    CONSTRAINT fk_user_follow
    FOREIGN KEY (id_user) 
    REFERENCES conduit.author(id)
);

CREATE TABLE conduit.comments (
    id SERIAL PRIMARY KEY ,
    created_at TIMESTAMP WITH TIME ZONE ,
    updated_at TIMESTAMP WITH TIME ZONE ,
    body TEXT , 
    article_slug TEXT , 
    id_author INT ,
    CONSTRAINT fk_article 
    FOREIGN KEY (article_slug) 
    REFERENCES conduit.article(slug),
	CONSTRAINT fk_author
    FOREIGN KEY (id_author) 
    REFERENCES conduit.author(id)
);


