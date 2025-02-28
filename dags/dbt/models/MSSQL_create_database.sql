{{ 
    config(
            tags=["MS_SQL_CREATE_DATABASE"]
          , pre_hook = "CREATE DATABASE Test_DB"
          , post_hook = "DROP TABLE MSSQL_create_database"
          )
}}

select 1 as status