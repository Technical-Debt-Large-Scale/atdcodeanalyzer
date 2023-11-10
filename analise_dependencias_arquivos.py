import utilidades
import datetime
import pandas as pd

# promocity/src/main/java/ufc/cmu/promocity
def gera_arquivos_java(path_projeto, nome_arquivo='arquivosjava.txt'):
  try:
    # Gera um arquivo contendo todos os arquivos .java do projeto
    query = f'find {path_projeto} -name "*.java" > {nome_arquivo}'
    utilidades.executa_comando(comando=query)
    print(f'Arquivo {nome_arquivo} gerado com sucesso!')
  except Exception as ex:
    print(f'Erro ao gerar o arquivosjava.txt: {str(ex)}')

# Dado 'org.apache.cassandra.index.Index.java'
# Retorne 'pilot/analises/designite/v-3-11-11/src/java/org/apache/cassandra/index/Index.java'

def get_path_file(my_file, src_java_path):
  path_file = None
  my_file = my_file.replace('.java', '') # org.apache.cassandra.index.Index
  my_file = my_file.replace('.', '/') # org/apache/cassandra/index/Index
  my_file = my_file + '.java' # org/apache/cassandra/index/Index.java
  path_file =  src_java_path  + my_file
  return path_file

def teste_find_word_in_file(my_file, my_word):
    with open(my_file) as f:
        datafile = f.readlines()
        found = False  # This isn't really necessary
        for line in datafile:
          if my_word in line:
            # found = True # Not necessary
            return True
    return False  # Because you finished the search without finding

def lista_arquivos_que_dependem_de(my_file, dicionario):
  lista_temp = []
  my_file = my_file.replace('/','.')
  if my_file in dicionario:
    for each in dicionario[my_file]:
      if each[2] == 1:
        lista_temp.append(each)
  return lista_temp

# Cria duas listas contendo o conjunto de arquivos da versão analisada
def cria_duas_listas_arquivos_analisados(nome_arquivo='arquivosjava.txt', diretorio_src_main='promocity/src/main/java'):
  lista_linhas_arquivos_cassandra = []
  lista_colunas_arquivos_cassandra = []
  with open(nome_arquivo, mode='r+', encoding='utf-8') as file:
    for line in file:
      line = line.rstrip()
      line = line.replace(diretorio_src_main, '')
      line = line.replace('/', '.')
      lista_linhas_arquivos_cassandra.append(line)
      lista_colunas_arquivos_cassandra.append(line)
  return lista_linhas_arquivos_cassandra, lista_colunas_arquivos_cassandra

def cria_dicionario_dsm(lista_linhas_arquivos_cassandra, lista_colunas_arquivos_cassandra, path_main):
  t1 = datetime.datetime.now()
  dicionario_dsm = {}
  lista_aux = []
  for each_file in lista_linhas_arquivos_cassandra:
    for each_elemento_coluna in lista_colunas_arquivos_cassandra:
      my_search = each_elemento_coluna
      my_search = my_search.replace('.java', ';')
      my_path = get_path_file(my_file=each_file, src_java_path=path_main)
      if teste_find_word_in_file(my_file=my_path,my_word=my_search):
        item = (each_file, each_elemento_coluna, 1)
      else:
        item = (each_file, each_elemento_coluna, 0)
      lista_aux.append(item)
    dicionario_dsm[each_file] = lista_aux
    lista_aux = []
  t2 = datetime.datetime.now()
  delta = t2 - t1
  print(f'Tempo para criar o dicionarário dsm: {delta}, itens percorridos: {len(dicionario_dsm)}')
  return dicionario_dsm

# path_arquivo_a='ufc.cmu.promocity.backend.context.UserLocationMonitoring.java'
def get_arquivos_A_usa_B(path_arquivo_a, dicionario_dsm):
  # Exemplo: Relação de Arquivos que UserLocationMonitoring.java depende de
  # sao os arquivos Bs que A precisa para sua implementacao
  lista_arquivos = []
  i = 1
  for tupla in dicionario_dsm[path_arquivo_a]:
    if tupla[2] == 1:
      print(f'{i}, {tupla}')
      i = i + 1
      lista_arquivos.append(tupla[1])
  return lista_arquivos

# Dicionario que dado um arquivo X, monta uma matriz de dependencia de X, ou seja, uma lista de arquivos que dependem de X
def cria_dicionario_dsm_depende_de(lista_linhas_arquivos_cassandra, lista_colunas_arquivos_cassandra, path_main):
  t1 = datetime.datetime.now()
  dicionario_dsm_depende_de = {}
  lista_aux = []

  for each_file in lista_linhas_arquivos_cassandra:
    for each_elemento_coluna in lista_colunas_arquivos_cassandra:
      my_search = each_file
      my_search = my_search.replace('.java', ';')
      my_path = get_path_file(my_file=each_elemento_coluna, src_java_path=path_main)
      if teste_find_word_in_file(my_file=my_path,my_word=my_search):
        item = (each_elemento_coluna, each_file, 1)
      else:
        item = (each_elemento_coluna, each_file, 0)
      lista_aux.append(item)
    dicionario_dsm_depende_de[each_file] = lista_aux
    lista_aux = []

  t2 = datetime.datetime.now()

  delta = t2 - t1

  print(f'Tempo para criar o dicionarário dsm: {delta}, itens percorridos: {len(dicionario_dsm_depende_de)}')
  return dicionario_dsm_depende_de

def get_arquivos_dependem_de_A(path_arquivo_a, dicionario_dsm_depende_de):
  # Exemplo: Relação de Arquivos que dependem de UserController.java
  lista_arquivos = []
  i = 1
  for tupla in lista_arquivos_que_dependem_de(my_file=path_arquivo_a, dicionario=dicionario_dsm_depende_de):
    if tupla[2] == 1:
      print(f'{i}, {tupla}')
      i += 1
      lista_arquivos.append(tupla[0])
  return lista_arquivos

# Dada uma classe e o arquivo texto contendo todos os arquivos do repositorio,
# retorna o pacote da classe junto com classe
# path = 'promocity/src/main/java/'
def get_file_package(my_file, my_content, path):
  with open(my_content, mode='r+', encoding='utf-8') as file:
    for line in file:
      if my_file in line:
        line = line.replace(path, '')
        line = line.replace('/','.')
        line = line.strip()
        return line

# Dada a lista de arquivos criticos [(arquivo1, qtd linhas modificadas, frequencia de commits), (), ...]
# arquivo texto contendo todos os arquivos do repositorio
# dicionario com a DSM file_a uses file_b
# retorna o dicionario com chave file_a e valores lista de arquivos que file_a chama(importa)
## arquivosjava.txt e dicionario_dsm
def get_dict_file_a_uses_file_b(lista_arquivos_criticos, content, my_dictionary, path_main):
  dict_file_a_uses_file_b = {}
  lista_file_a_uses_file_b = []
  for each in lista_arquivos_criticos:
    item = each[0]
    key_file = get_file_package(my_file=item, my_content=content, path=path_main)
    if key_file is not None:
      for each_tupla in my_dictionary[key_file]:
        if each_tupla[2] == 1:
          lista_file_a_uses_file_b.append(each_tupla[1])
      dict_file_a_uses_file_b[key_file] = lista_file_a_uses_file_b
      lista_file_a_uses_file_b = []
  return dict_file_a_uses_file_b

# Todo: revisar, pois está substituindo config.java por GuardrailsConfig.java
# Dada a lista de arquivos criticos [(arquivo1, qtd linhas modificadas, frequencia de commits), (), ...]
# arquivo texto contendo todos os arquivos do repositorio
# dicionario com a DSM file_a depende de file_b
# retorna o dicionario com chave file_a e valores lista de arquivos que dependem de file_a
## content='arquivosjava.txt', my_dictionary=dicionario_dsm_depende_de
def get_dict_file_impact_other_files(lista_arquivos_criticos, content, my_dictionary, path_main):
  dict_file_impact_other_files = {}
  lista_file_a_depends_on_file_b = []

  for each in lista_arquivos_criticos:
    item = each[0]
    key_file = get_file_package(my_file=item, my_content=content, path=path_main)
    if key_file is not None:
      for tupla in lista_arquivos_que_dependem_de(my_file=key_file, dicionario=my_dictionary):
        if tupla[2] == 1:
          lista_file_a_depends_on_file_b.append(tupla[0])
      dict_file_impact_other_files[key_file] = lista_file_a_depends_on_file_b
      lista_file_a_depends_on_file_b = []
  return dict_file_impact_other_files

def mostra_lista_arquivos_dependentes(lista_arquivos_criticos, content, my_dictionary, path_main):
  # Dado um arquivo chave, mostra a lista de arquivos que dependem do arquivo chave
  dict_arquivos_dependentes_arquivos_criticos = get_dict_file_impact_other_files(lista_arquivos_criticos, content, my_dictionary, path_main)

  lista_arquivos_impactados = []
  l_ac = []
  l_adac = []
  l_tamanho_adac = []
  for key, value in dict_arquivos_dependentes_arquivos_criticos.items():
    print(key, value)
    l_ac.append(key)
    l_tamanho_adac.append(len(value))
    l_adac.append(value)

  return dict_arquivos_dependentes_arquivos_criticos, lista_arquivos_impactados, l_ac, l_adac, l_tamanho_adac

def gera_df_arquivos_dependentes_arquivos_criticos(l_ac, l_tamanho_adac, l_adac):
  df_arquivos_dependentes_arquivos_criticos = pd.DataFrame({'arquivos_criticos':l_ac, 'qtd_arquivos_dependentes':l_tamanho_adac, 'arquivos_dependentes':l_adac})
  try:
    df_arquivos_dependentes_arquivos_criticos.to_csv('arquivos_dependentes_arquivos_criticos.csv')
  except Exception as ex:
    print(f'Erro ao salvar o arquivo arquivos_dependentes_arquivos_criticos.csv : {str(ex)}')
  return df_arquivos_dependentes_arquivos_criticos

# lista_arquivos_impactados_unicos
def gera_lista_arquivos_impactados_unicos(dict_arquivos_dependentes_arquivos_criticos, lista_arquivos_impactados):
  for key, value in dict_arquivos_dependentes_arquivos_criticos.items():
    print(f"Mudanças na classe {key} podem impactar {len(value)} classes")

  for key, value in dict_arquivos_dependentes_arquivos_criticos.items():
    lista_arquivos_impactados = lista_arquivos_impactados + value

  set_lista_arquivos_impactados = set(lista_arquivos_impactados)
  lista_arquivos_impactados_unicos = list(set_lista_arquivos_impactados)
  return lista_arquivos_impactados_unicos

def relatorio_linhas_alteradas_pelas_classes_criticas(lista_arquivos_impactados_unicos,lista_arquivos_criticos, df_em_fc_java_impl, df_files_commits_from_db):
  # Quantidade de arquivos impactados pelas classes críticas
  print(f"Existem {len(lista_arquivos_impactados_unicos)} classes que podem ser impactados pelas {len(lista_arquivos_criticos)} classes críticas.")

  print(f'Classes críticas: {len(lista_arquivos_criticos)}')
  print(f'Classes impactadas: {len(lista_arquivos_impactados_unicos)}')
  print(f'Total de classes .java do sistema: {df_em_fc_java_impl.shape[0]}')

  print(f'Existem {len(lista_arquivos_criticos)} arquivos: {[item[0] for item in lista_arquivos_criticos]} que podem impactar {len(lista_arquivos_impactados_unicos)} dos {df_em_fc_java_impl.shape[0]} arquivos .java')
  print(f'{len(lista_arquivos_impactados_unicos)} Potenciais arquivos impactados: {lista_arquivos_impactados_unicos}')

  # df.groupby(['A','C'])['B'].sum()
  df_lm = df_files_commits_from_db.copy()
  qtd_lm = df_lm[['file_is_java','file_filename', 'modified_lines']][df_lm.file_is_java==1].groupby('file_filename')['modified_lines'].sum()
  df_qtd_lm = qtd_lm.to_frame()
  #df_qtd_lm['file_filename'] = df_qtd_lm.index
  df_qtd_lm = df_qtd_lm.reset_index()
  #df_qtd_lm

  # Quantidade de linhas modificadas dos arquivos criticos
  dict_modified_lines_arquivos_criticos = {}

  for each in lista_arquivos_criticos:
    qtd_temp = df_qtd_lm[df_qtd_lm.file_filename == each[0]]['modified_lines'].to_list()
    if len(qtd_temp) == 1:
      dict_modified_lines_arquivos_criticos[each[0]] = qtd_temp[0]

  #dict_modified_lines_arquivos_criticos

  soma_modified_lines_arquivos_criticos = 0
  for key, value in dict_modified_lines_arquivos_criticos.items():
    soma_modified_lines_arquivos_criticos = soma_modified_lines_arquivos_criticos + value

  print(f'As {len(dict_modified_lines_arquivos_criticos)} classes criticas mudaram {soma_modified_lines_arquivos_criticos} linhas no sistema')

  lista_nomes_arquivos_impactados_unicos = []

  for each in lista_arquivos_impactados_unicos:
    each = each.split('.')
    temp = each[-2] + '.' + each[-1]
    lista_nomes_arquivos_impactados_unicos.append(temp)
  return lista_nomes_arquivos_impactados_unicos, df_qtd_lm, dict_modified_lines_arquivos_criticos, soma_modified_lines_arquivos_criticos

# Dada uma classe critica e um dataframe contendo todos os commits analisados
# retorna a lista de arquivos que sao modificados junto com o arquivo critico
def get_lista_arquivos_modificados_with_critico(filename, df):
  lista_temp_arquivos = []
  lista_temp = []

  lista_arquivos_modificados_com_filename = df[df['modified_files'].str.contains(filename)]['modified_files'].to_list()

  for each in lista_arquivos_modificados_com_filename:
    lista_temp = each.split(',')
    lista_temp_arquivos = lista_temp_arquivos + lista_temp
    lista_temp = []

  set_lista_temp_arquivos = set(lista_temp_arquivos)
  lista_temp_arquivos_unicos = list(set_lista_temp_arquivos)
  return lista_temp_arquivos_unicos

# Data a lista de arquivos criticos e todos os commits da faixa analisada
# retorna um dicionario com chave no arquivo critico e a lista dos arquivos que sao modificados em conjunto com ele.
def get_dict_arquivos_modificados_with_critico(lista, df):
  dict_arquivos_modificados_with_critico = {}
  lista_temp = []
  for filename in lista:
    lista_temp = get_lista_arquivos_modificados_with_critico(filename[0], df)
    dict_arquivos_modificados_with_critico[filename[0]] = lista_temp
    lista_temp = []
  return dict_arquivos_modificados_with_critico

# Dado um arquivo critico,
# retorna a lista de arquivos impactados por ele
def get_arquivos_impactados_por_file(lista, filename, path_main):
  lista_arquivos_criticos = lista
  lista_temp = []
  for key, value in get_dict_file_impact_other_files(lista_arquivos_criticos, content='arquivosjava.txt', my_dictionary=dicionario_dsm_depende_de, path_main=path_main).items():
    if filename in key:
      lista_temp = []
      for file in value:
        temp = file.split('.')[-2]
        temp = temp + '' + '.java'
        lista_temp.append(temp)
  return lista_temp

# dicionário de arquivos criticos e seus arquivos que dependem dele e também sao co-change
def get_dict_arquivos_dependem_e_cochange_critico(lista, path_main):
  lista_arquivos_criticos = lista
  dict_arquivos_dependem_e_cochange_critico = {}

  for filename in lista_arquivos_criticos:
    lista_temp_dependem_filename = get_arquivos_impactados_por_file(lista_arquivos_criticos, filename[0], path_main)
    lista_temp_cochange_filename = dict_arquivo_critico_cochange[filename[0]]

    lista_arquivos_dependem_de_and_cochange_filename = []
    for each in lista_temp_dependem_filename:
      if each in lista_temp_cochange_filename:
        lista_arquivos_dependem_de_and_cochange_filename.append(each)

    dict_arquivos_dependem_e_cochange_critico[filename[0]] = lista_arquivos_dependem_de_and_cochange_filename

  return dict_arquivos_dependem_e_cochange_critico

