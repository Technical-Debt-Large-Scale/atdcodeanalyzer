# 4.2 Carrega as tabelas do banco em dataframes
import pandas as pd
import sqlite3

def load_dataframes(database_name):
    conexao_banco = sqlite3.connect(database_name)

    my_query_commits = "select * from commitscomplete"
    my_query_files = "select * from filescomplete"
    my_query_files_commits = "select f.id as 'file_id', f.hash as 'file_hash_commit', f.description as 'file_description', f.is_java as 'file_is_java', f.created_date as 'file_created_date', f.old_path as 'file_old_path', f.new_path as 'file_new_path', f.filename as 'file_filename', f.change_type as 'file_change_type', f.diff as 'file_diff', f.diff_parsed as 'file_diff_parsed', f.added_lines as 'file_added_lines', f.deleted_lines as 'file_deleted_lines', f.source_code as 'file_source_code', f.source_code_before as 'file_source_code_before', f.nloc as 'file_nloc', f.complexity as 'file_complexity', f.token_count as 'file_token_count', f.commit_id as 'file_commit_id', c.* from filescomplete f, commitscomplete c where f.commit_id=c.id"

    df_commits_from_db = pd.read_sql_query(my_query_commits, conexao_banco)
    df_files_from_db = pd.read_sql_query(my_query_files, conexao_banco)
    df_files_commits_from_db = pd.read_sql(my_query_files_commits, conexao_banco)

    conexao_banco.close() 

    return df_commits_from_db, df_files_from_db, df_files_commits_from_db