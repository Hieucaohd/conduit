from sqlalchemy import create_engine
from sqlalchemy.sql import text
engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")


# def execute_sql(state):
#     with engine.connect() as con :
#         statement = text(f"{state}")
#         result=con.execute(statement)
#         return type(result) 

# print(execute_sql("SELECT * FROM conduit.article"))


def execute_sql(state):
    with engine.connect() as con:
        statement = text(f"{state}")
        result = con.execute(statement)
        first = result.fetchall()
        list_data = [] 
        for i in first:
            list_data.append(i._mapping._key_to_index)
        return list_data

 









