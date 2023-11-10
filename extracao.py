import os
import dao
import pydriller
import datetime
import utilidades

def extrai_informacoes_repositorio(my_repositorio, nome_repositorio):
    print('Cria a sessão de banco de dados')
    db_session = dao.create_session()
    print('Cria as tabelas do banco')
    dao.create_tables()
    print('Tabelas criadas com sucesso!')

    # Cria a colecao de CommitsComplete
    myCommitsCompleteCollection = dao.CommitsCompleteCollection(db_session)
    # Cria a colecao de FilesComplete
    myFilesCompleteCollection = dao.FilesCompleteCollection(db_session)

    qtd_commits = 0
    try: 
        tempo1 = datetime.datetime.now()
        print(f'Analisa commits e arquivos modificados do repositorio {nome_repositorio}. Aguarde...')
        for commit in pydriller.Repository(nome_repositorio).traverse_commits():
            try:
                currentCommit = dao.CommitComplete(
                name=nome_repositorio + '_' + commit.hash,
                hash=commit.hash,
                msg=commit.msg,
                author=commit.author.name,
                committer=commit.committer.email,
                author_date=commit.author_date,
                author_timezone=commit.author_timezone,
                committer_date=commit.committer_date,
                committer_timezone=commit.committer_timezone,
                branches=utilidades.convert_list_to_str(commit.branches),
                in_main_branch=commit.in_main_branch,
                merge=commit.merge,
                modified_files=utilidades.convert_modifield_list_to_str(commit.modified_files),
                parents=utilidades.convert_list_to_str(commit.parents),
                project_name=commit.project_name,
                project_path=commit.project_path,
                deletions=commit.deletions,
                insertions=commit.insertions,
                lines=commit.lines,
                files=commit.files,
                dmm_unit_size=commit.dmm_unit_size,
                dmm_unit_complexity=commit.dmm_unit_complexity,
                dmm_unit_interfacing=commit.dmm_unit_interfacing)
                # salva dados do commit na tabela de commits do banco do repositorio
                myCommitsCompleteCollection.insert_commit(currentCommit)
                qtd_commits = qtd_commits + 1
                # analisa cada um dos arquivos modificados no commit
                for file in commit.modified_files:
                    try:
                        if file is not None and file.filename is not None:
                            currentFile = dao.FileComplete(
                                            name=file.filename,
                                            hash=commit.hash,
                                            old_path=file.old_path,
                                            new_path=file.new_path,
                                            filename=file.filename,
                                            is_java=utilidades.testa_extensao_java(file.filename),
                                            change_type=file.change_type.name,
                                            diff=str(file.diff),
                                            diff_parsed=utilidades.convert_dictionary_to_str(file.diff_parsed),
                                            added_lines=file.added_lines,
                                            deleted_lines=file.deleted_lines,
                                            source_code=str(file.source_code),
                                            source_code_before=str(file.source_code_before),
                                            methods=utilidades.convert_list_to_str(file.methods),
                                            methods_before=utilidades.convert_list_to_str(file.methods_before),
                                            changed_methods=utilidades.convert_list_to_str(file.changed_methods),
                                            nloc=file.nloc,
                                            complexity=file.complexity,
                                            token_count=file.token_count,
                                            commit_id=myCommitsCompleteCollection.query_commit_hash(commit.hash))
                            myFilesCompleteCollection.insert_file(currentFile)
                    except Exception as ex:
                        print(f'Erro ao inserir arquivo {file.filename} na tabela de files do banco!: {str(ex)}')
            except Exception as ex:
                print(f'Erro ao salvar commit {commit.hash} no banco : {str(ex)}')
        db_session.close()
        tempo2 = datetime.datetime.now()
        print('Sessão de banco de dados fechada!')
        print(f'Quantidade de commits analisados: {qtd_commits}')
        print(f'Tempo de análise: {tempo2-tempo1}')
    except Exception as ex:
        print(f'Erro ao analisar os commits do repositório {my_repositorio}: {str(ex)}')

def extrai_informacoes_repositorio_by_commits(my_repositorio, nome_repositorio, commit_inicial, commit_final):
    print('Cria a sessão de banco de dados')
    db_session = dao.create_session()
    print('Cria as tabelas do banco')
    dao.create_tables()
    print('Tabelas criadas com sucesso!')

    # Cria a colecao de CommitsComplete
    myCommitsCompleteCollection = dao.CommitsCompleteCollection(db_session)
    # Cria a colecao de FilesComplete
    myFilesCompleteCollection = dao.FilesCompleteCollection(db_session)

    qtd_commits = 0
    try: 
        tempo1 = datetime.datetime.now()
        print(f'Analisa commits e arquivos modificados do repositorio {nome_repositorio}. Aguarde...')
        for commit in pydriller.Repository(nome_repositorio, from_commit=commit_inicial, to_commit=commit_final).traverse_commits():
            try:
                currentCommit = dao.CommitComplete(
                name=nome_repositorio + '_' + commit.hash,
                hash=commit.hash,
                msg=commit.msg,
                author=commit.author.name,
                committer=commit.committer.email,
                author_date=commit.author_date,
                author_timezone=commit.author_timezone,
                committer_date=commit.committer_date,
                committer_timezone=commit.committer_timezone,
                branches=utilidades.convert_list_to_str(commit.branches),
                in_main_branch=commit.in_main_branch,
                merge=commit.merge,
                modified_files=utilidades.convert_modifield_list_to_str(commit.modified_files),
                parents=utilidades.convert_list_to_str(commit.parents),
                project_name=commit.project_name,
                project_path=commit.project_path,
                deletions=commit.deletions,
                insertions=commit.insertions,
                lines=commit.lines,
                files=commit.files,
                dmm_unit_size=commit.dmm_unit_size,
                dmm_unit_complexity=commit.dmm_unit_complexity,
                dmm_unit_interfacing=commit.dmm_unit_interfacing)
                # salva dados do commit na tabela de commits do banco do repositorio
                myCommitsCompleteCollection.insert_commit(currentCommit)
                qtd_commits = qtd_commits + 1
                # analisa cada um dos arquivos modificados no commit
                for file in commit.modified_files:
                    try:
                        if file is not None and file.filename is not None:
                            currentFile = dao.FileComplete(
                                            name=file.filename,
                                            hash=commit.hash,
                                            old_path=file.old_path,
                                            new_path=file.new_path,
                                            filename=file.filename,
                                            is_java=utilidades.testa_extensao_java(file.filename),
                                            change_type=file.change_type.name,
                                            diff=str(file.diff),
                                            diff_parsed=utilidades.convert_dictionary_to_str(file.diff_parsed),
                                            added_lines=file.added_lines,
                                            deleted_lines=file.deleted_lines,
                                            source_code=str(file.source_code),
                                            source_code_before=str(file.source_code_before),
                                            methods=utilidades.convert_list_to_str(file.methods),
                                            methods_before=utilidades.convert_list_to_str(file.methods_before),
                                            changed_methods=utilidades.convert_list_to_str(file.changed_methods),
                                            nloc=file.nloc,
                                            complexity=file.complexity,
                                            token_count=file.token_count,
                                            commit_id=myCommitsCompleteCollection.query_commit_hash(commit.hash))
                            myFilesCompleteCollection.insert_file(currentFile)
                    except Exception as ex:
                        print(f'Erro ao inserir arquivo {file.filename} na tabela de files do banco!: {str(ex)}')
            except Exception as ex:
                print(f'Erro ao salvar commit {commit.hash} no banco : {str(ex)}')
        db_session.close()
        tempo2 = datetime.datetime.now()
        print('Sessão de banco de dados fechada!')
        print(f'Quantidade de commits analisados: {qtd_commits}')
        print(f'Tempo de análise: {tempo2-tempo1}')
    except Exception as ex:
        print(f'Erro ao analisar os commits do repositório {my_repositorio}: {str(ex)}')