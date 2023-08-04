from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")

def execute_sql2(state) :
    with engine.connect() as con :
        statement = text(f"{state}")
        con.execute(statement)
        con.commit()
        return True 
def execute_sql(state):
    with engine.connect() as con:
        statement = text(f"{state}")
        result = con.execute(statement)
        first = result.fetchall()
        list_data = [] 
        for i in first:
            list_data.append(dict(i._mapping))
        return list_data 


if __name__=="__main__" :
    state = """SELECT * FROM conduit.tag """
    article = execute_sql(state)
    list_slug_with_tag_name = []
    current_article = article[0]
    taglist = []
    for i in article :
        if i['article_slug'] == current_article['article_slug'] :
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
    # print(list_slug_with_tag_name)
    list1 = []
    for i in list_slug_with_tag_name :
        list1.append(i['tagList'])
    list2 = []
    list3 = []
    for t in list1 :
        for j in t:
            list2.append(j) 
    for i in list2 :
        if i not in list3 :
            list3.append(i)
    print(list3)
