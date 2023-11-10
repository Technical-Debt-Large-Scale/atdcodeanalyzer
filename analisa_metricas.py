import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import utilidades
import pandas as pd

# AMLOC de todos os arquivos
# retorna o df_amloc, df_boxplot_amloc e group_files_modified_lines
def get_accumulated_modified_locs(df_files_from_db):
  # Lista arquivos ordenados por nome com suas linhas modificadas
  df_files_from_db[['name','modified_lines']].sort_values(by=['name'], ascending=True)

  # Agrupa o df por nome do arquivo
  df_groupby_name_modified_lines = df_files_from_db[['name','modified_lines']].groupby('name')

  # Soma o total de linhas modificadas de cada arquivo
  group_files_modified_lines = df_groupby_name_modified_lines.sum()

  # Cria um novo df de Linhas de Código Modificadas
  df_locm = group_files_modified_lines.copy()
  df_locm = df_locm.reset_index()

  # Acrescenta uma coluna File
  df_locm['File'] = 'File'
  df_boxplot_em = df_locm[['modified_lines', 'File']]

  df_accumulated_modified_locs = df_locm.copy()
  return df_accumulated_modified_locs, df_boxplot_em, group_files_modified_lines

def gera_boxplot_accumulated_modified_locs(df_accumulated_modified_locs_boxplot, nome_repositorio):
  # Boxplot do EM (Esforço de Manutenção de Locs Modificadas). Todos os arquivos do repositório
  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='modified_lines', data=df_accumulated_modified_locs_boxplot)
  current_path = os.getcwd()
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + '_' + 'accumulated_modified_locs_boxplot.png'
  titulo = f"{nome_repositorio} - AMLOC - Todos os arquivos do repositório"
  plt.title(titulo)
  plt.savefig(nome_boxplot)

# Remove os arquivos que nao foram modificados
# retorna o df_boxplot_amloc
def get_accumulated_modified_locs_boxplot_valid(df_boxplot_em, nome_repositorio):
  # Remove os arquivos que não foram modificados ao longo do tempo (O linhas modificadas)
  df_boxplot_em = df_boxplot_em.drop(df_boxplot_em[df_boxplot_em.modified_lines == 0].index)
  plt.figure(figsize=(6,4))
  # Constroi o Boxsplot sem os outliers
  sns.boxplot(x='File', y='modified_lines', data=df_boxplot_em,  showfliers=False)
  current_path = os.getcwd()
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + '_' + 'accumulated_modified_locs_boxplot_valid.png'
  titulo = f"{nome_repositorio} - AMLOC - Apenas arquivos válidos"
  plt.title(titulo)
  plt.savefig(nome_boxplot)
  return df_boxplot_em

# Cria um df_accumulated_modified_java_files contendo apenas arquivos .java
# df_accumulated_modified_java_files
def get_df_accumulated_modified_java_files(df_accumulated_modified_locs):
  # Cria um df sem os arquivos de Teste
  df_locm_no_test = df_accumulated_modified_locs[(df_accumulated_modified_locs["name"].str.contains('Test') == False)]
  # Cria um df contendo apenas os arquivos .java de implementacao
  df_locm_java_impl = df_locm_no_test[df_locm_no_test['name'].str.contains('.java', regex=False)]
  return df_locm_java_impl

# mostra o boxplot accumulated_modified_java_files
# retorna df_boxplot_em_java_impl contendo apenas arquivos .java
def show_boxplot_accumulated_modified_java_files(df_locm_java_impl, nome_repositorio):
  df_boxplot_em_java_impl = df_locm_java_impl[['modified_lines', 'File']]
  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='modified_lines', data=df_boxplot_em_java_impl)
  current_path = os.getcwd()
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + "_" + 'accumulated_modified_locs_boxplot_java_files.png'
  titulo = f"{nome_repositorio} - AMLOC - Apenas arquivos java"
  plt.title(titulo)
  plt.savefig(nome_boxplot)
  return df_boxplot_em_java_impl

# Calcula os quartiles de todos os arquivos referente a AMLOC
def get_quartiles_offiles_modified_lines(group_files_modified_lines, df_boxplot_em, nome_repositorio):
  list_of_files_modified_lines = group_files_modified_lines.to_dict()
  print(f'Qtd list_of_files_modified_lines: { len(list_of_files_modified_lines) }')
  # Mostra os quatis
  em_q1 = np.percentile(df_boxplot_em.modified_lines, [25])
  em_q2 = np.percentile(df_boxplot_em.modified_lines, [50])
  em_q3 = np.percentile(df_boxplot_em.modified_lines, [75])
  em_q4 = np.percentile(df_boxplot_em.modified_lines, [100])
  print(f'Quartis do Total de Linhas Modificadas: Q1: {em_q1}, Q2: {em_q2}, Q3: {em_q3}, Q4: {em_q4}')
  dict_temp = {
    'em_q1': em_q1, 'em_q2': em_q2, 'em_q3': em_q3, 'em_q4': em_q4
  }
  current_path = os.getcwd()
  path_arquivo = current_path + '/' + 'quartis' + '/'+ nome_repositorio + '/' + nome_repositorio + "_" + 'quartiles_offiles_modified_lines.csv'
  utilidades.export_csv_from_dict(dict_temp, path_arquivo)
  return em_q1, em_q2, em_q3, em_q4

# Seleciona apenas os AMLOC validos (arquivos que foram modificados pelo menos uma vez)
# retorna o df_boxplot_em_java_impl
def get_accumulated_modified_java_files_valid(df_boxplot_em_java_impl, nome_repositorio):
  # Remove os arquivos que não foram modificados ao longo do tempo (O linhas modificadas)
  df_boxplot_em_java_impl = df_boxplot_em_java_impl.drop(df_boxplot_em_java_impl[df_boxplot_em_java_impl.modified_lines == 0].index)

  plt.figure(figsize=(6,4))
  # Constroi o Boxsplot sem os outliers
  sns.boxplot(x='File', y='modified_lines', data=df_boxplot_em_java_impl,  showfliers=False)
  current_path = os.getcwd()
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + "_" + 'accumulated_modified_locs_boxplot_java_files_valid.png'
  titulo = f"{nome_repositorio} - AMLOC - Apenas arquivos java válidos"
  plt.title(titulo)
  plt.savefig(nome_boxplot)
  return df_boxplot_em_java_impl

# Calcula os quartiles dos AMLOC .java validos
def get_quartiles_offiles_modified_lines_java_files_valid(df_boxplot_em_java_impl, nome_repositorio):
  # Mostra os quatis
  em_q1_java_impl = np.percentile(df_boxplot_em_java_impl.modified_lines, [25])
  em_q2_java_impl = np.percentile(df_boxplot_em_java_impl.modified_lines, [50])
  em_q3_java_impl = np.percentile(df_boxplot_em_java_impl.modified_lines, [75])
  em_q4_java_impl = np.percentile(df_boxplot_em_java_impl.modified_lines, [100])
  print(f'Quartis do Total de Linhas Modificadas: Q1: {em_q1_java_impl}, Q2: {em_q2_java_impl}, Q3: {em_q3_java_impl}, Q4: {em_q4_java_impl}')

  dict_temp = {
    'em_q1': em_q1_java_impl, 'em_q2': em_q2_java_impl, 'em_q3': em_q3_java_impl, 'em_q4': em_q4_java_impl
  }
  current_path = os.getcwd()
  path_arquivo = current_path + '/' + 'quartis' + '/'+ nome_repositorio + '/' + nome_repositorio + "_" + 'quartiles_offiles_modified_lines_java_files_valid.csv'
  utilidades.export_csv_from_dict(dict_temp, path_arquivo)

  return em_q1_java_impl, em_q2_java_impl, em_q3_java_impl, em_q4_java_impl

# Cria um df de complexidade ciclomatica de todos os arquivos
# retorna df_cc_temp
def get_complexidade_ciclomatica(df_files_commits_from_db):
  # Mostra as Complexidades Ciclomáticas dos arquivos ordenada crescent pelo tempo
  df_cc = df_files_commits_from_db[['file_filename', 'file_complexity', 'author_date']].sort_values(by=['file_filename', 'author_date'], ascending=True)
  # Remove files that has not cc
  # cc all files
  df_cc_temp = df_cc.copy()
  df_cc_temp = df_cc_temp[df_cc_temp.file_complexity.notnull()]
  return df_cc_temp

##### Todos os arquivos #####
# gera um boxplot da complexidade ciclomatica de todos os arquivos
def get_boxplot_complexidade_ciclomatica(df_cc_temp, nome_repositorio):
  df_cc_temp['File'] = 'File'
  df_boxplot_cc_temp = df_cc_temp[['file_complexity', 'File']]
  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='file_complexity', data=df_boxplot_cc_temp)
  current_path = os.getcwd()
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + "_" + 'boxplot_complexidade_ciclomatica.png'
  titulo = f"{nome_repositorio} - Complexidade Ciclomatica - Todos os arquivos"
  plt.title(titulo)
  plt.savefig(nome_boxplot)
  return df_cc_temp, df_boxplot_cc_temp

# Calcula os quartiles das complexidades ciclomaticas
# retorna os quartiles
def get_quartiles_complexidade_ciclomatica(df_boxplot_cc_temp, nome_repositorio):
  # Mostra os quatis
  em_q1_cc_temp = np.percentile(df_boxplot_cc_temp.file_complexity, [25])
  em_q2_cc_temp = np.percentile(df_boxplot_cc_temp.file_complexity, [50])
  em_q3_cc_temp = np.percentile(df_boxplot_cc_temp.file_complexity, [75])
  em_q4_cc_temp = np.percentile(df_boxplot_cc_temp.file_complexity, [100])

  print(f'Quartis do Total de Linhas Modificadas: Q1: {em_q1_cc_temp}, Q2: {em_q2_cc_temp}, Q3: {em_q3_cc_temp}, Q4: {em_q4_cc_temp}')

  dict_temp = {
    'em_q1': em_q1_cc_temp, 'em_q2': em_q2_cc_temp, 'em_q3': em_q3_cc_temp, 'em_q4': em_q4_cc_temp
  }
  current_path = os.getcwd()
  path_arquivo = current_path + '/' + 'quartis' + '/'+ nome_repositorio + '/' + nome_repositorio + "_" + 'quartiles_complexidade_ciclomatica.csv'
  utilidades.export_csv_from_dict(dict_temp, path_arquivo)

  return em_q1_cc_temp, em_q2_cc_temp, em_q3_cc_temp, em_q4_cc_temp

### Apenas os arquivos .java ###
# gera um boxplot de complexidade ciclomatica apenas dos arquivos .java
def get_boxplot_complexidade_ciclomatica_only_java(df_cc_temp, nome_repositorio):
  # Cria um df sem os arquivos de Teste
  df_cc_temp_no_test = df_cc_temp[(df_cc_temp["file_filename"].str.contains('Test') == False)]
  # Cria um df contendo apenas os arquivos .java de implementacao
  df_cc_temp_java_impl = df_cc_temp_no_test[df_cc_temp_no_test['file_filename'].str.contains('.java', regex=False)]
  df_cc_temp_boxplot_em_java_impl = df_cc_temp_java_impl[['file_complexity', 'File']]

  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='file_complexity', data=df_cc_temp_boxplot_em_java_impl)
  current_path = os.getcwd()
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + "_" + 'boxplot_complexidade_ciclomatica_only_java.png'
  titulo = f"{nome_repositorio} - Complexidade Ciclomatica - Apenas os arquivos java"
  plt.title(titulo)
  plt.savefig(nome_boxplot)

  return df_cc_temp_java_impl, df_cc_temp_boxplot_em_java_impl

# calcula os quatiles das complexidade ciclomaticas apenas dos arquivos .java
# retorna os quartiles
def get_quartiles_complexidade_ciclomatica_java_impl(df_cc_temp_boxplot_em_java_impl, nome_repositorio):
  em_q1_cc_temp_java_impl = np.percentile(df_cc_temp_boxplot_em_java_impl.file_complexity, [25])
  em_q2_cc_temp_java_impl = np.percentile(df_cc_temp_boxplot_em_java_impl.file_complexity, [50])
  em_q3_cc_temp_java_impl = np.percentile(df_cc_temp_boxplot_em_java_impl.file_complexity, [75])
  em_q4_cc_temp_java_impl = np.percentile(df_cc_temp_boxplot_em_java_impl.file_complexity, [100])
  print(f'Quartis do Total de Linhas Modificadas: Q1: {em_q1_cc_temp_java_impl}, Q2: {em_q2_cc_temp_java_impl}, Q3: {em_q3_cc_temp_java_impl}, Q4: {em_q4_cc_temp_java_impl}')

  dict_temp = {
    'em_q1': em_q1_cc_temp_java_impl, 'em_q2': em_q2_cc_temp_java_impl, 'em_q3': em_q3_cc_temp_java_impl, 'em_q4': em_q4_cc_temp_java_impl
  }
  current_path = os.getcwd()
  path_arquivo = current_path + '/' + 'quartis' + '/'+ nome_repositorio + '/' + nome_repositorio + "_" + 'quartiles_complexidade_ciclomatica_java_impl.csv'
  utilidades.export_csv_from_dict(dict_temp, path_arquivo)

  return em_q1_cc_temp_java_impl, em_q2_cc_temp_java_impl, em_q3_cc_temp_java_impl, em_q4_cc_temp_java_impl

def calcula_frequencia_commits(df_files_from_db):
  # calcula frequência dos arquivos na faixa de commits analisados
  list_of_files_frequency_in_commits = {}

  # Dataframe agrupados por arquivos e seus commits
  df_groupby_name = df_files_from_db[['name', 'hash']].groupby('name')

  print(f'Quantidade de grupos: {df_groupby_name.ngroups}')

  group_files = df_groupby_name.size()

  print('')
  list_of_files_frequency_in_commits = group_files.to_dict()
  print(f'list_of_files_frequency_in_commits: { len(list_of_files_frequency_in_commits) }')

  # Cria um df contendo o arquivo e sua frequencia de commits
  df_fc = pd.DataFrame({'name':group_files.index, 'frequency_commits': group_files.values})

  df_boxplot_fc = df_fc
  # Acrescenta a coluna File
  df_boxplot_fc['File'] = 'File'
  return df_fc, df_boxplot_fc

def gera_boxplot_frequencia_commits(df_boxplot_fc, nome_repositorio):
  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc)
  current_path = os.getcwd()
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + '_' + 'boxplot_frequencia_commmits.png'
  titulo = f"{nome_repositorio} - FOC - Todos os arquivos do repositório"
  plt.title(titulo)
  plt.savefig(nome_boxplot)
  # Constroi o Boxsplot sem os outliers
  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc, showfliers=False)
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + '_' + 'boxplot_frequencia_commmits_no_outliers.png'
  titulo = f"{nome_repositorio} - FOC - Todos os arquivos do repositório sem outliers"
  plt.title(titulo)
  plt.savefig(nome_boxplot)

def calcula_quartiles_frequencia_commits(df_boxplot_fc, nome_repositorio):
  fc_q1 = np.percentile(df_boxplot_fc.frequency_commits , [25])
  fc_q2 = np.percentile(df_boxplot_fc.frequency_commits , [50])
  fc_q3 = np.percentile(df_boxplot_fc.frequency_commits , [75])
  fc_q4 = np.percentile(df_boxplot_fc.frequency_commits , [100])
  print(f'Quartis da Frequencia de Commits Q1: {fc_q1}, Q2: {fc_q2}, Q3: {fc_q3}, Q4: {fc_q4}')

  dict_temp = {
    'fc_q1': fc_q1,'fc_q2': fc_q2,'fc_q3': fc_q2,'fc_q4': fc_q4
  }
  current_path = os.getcwd()
  path_arquivo = current_path + '/' + 'quartis' + '/'+ nome_repositorio + '/' + nome_repositorio + "_" + 'quartiles_frequencia_commits.csv'
  utilidades.export_csv_from_dict(dict_temp, path_arquivo)

  return fc_q1, fc_q2, fc_q3, fc_q4

def gera_boxplot_frequencia_commits_only_java(df_fc, nome_repositorio):
  # Cria um df sem os arquivos de Teste
  df_fc_no_test = df_fc[(df_fc["name"].str.contains('Test') == False)]
  # Cria um df contendo apenas os arquivos .java de implementacao
  df_fc_java_impl = df_fc_no_test[df_fc_no_test['name'].str.contains('.java', regex=False)]
  df_boxplot_fc_java_impl = df_fc_java_impl[['frequency_commits', 'File']]

  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc_java_impl)
  current_path = os.getcwd()
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + '_' + 'boxplot_frequencia_commmits_only_java.png'
  titulo = f"{nome_repositorio} - FOC - Arquivos .java"
  plt.title(titulo)
  plt.savefig(nome_boxplot)
  # Constroi o Boxsplot sem os outliers
  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc_java_impl, showfliers=False)
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + '_' + 'boxplot_frequencia_commmits_only_java_no_outliers.png'
  titulo = f"{nome_repositorio} - FOC - Arquivos .java sem outliers"
  plt.title(titulo)
  plt.savefig(nome_boxplot)

  # Remove as frequencias muito baixas (total de commits < 3)
  df_boxplot_fc_java_impl2 = df_boxplot_fc_java_impl.drop(df_boxplot_fc_java_impl[df_boxplot_fc_java_impl.frequency_commits < 3].index)
  # Constroi o Boxsplot sem os outliers
  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc_java_impl2, showfliers=False)
  nome_boxplot = current_path + '/' + 'graficos' + '/'+ nome_repositorio + '/' + 'boxplot' + '/' + nome_repositorio + '_' + 'boxplot_frequencia_commmits_only_java_no_outliers_less_3.png'
  titulo = f"{nome_repositorio} - FOC - Arquivos .java sem outliers <= 3"
  plt.title(titulo)
  plt.savefig(nome_boxplot)

  return df_fc_java_impl, df_boxplot_fc_java_impl, df_boxplot_fc_java_impl2

def calcula_quartiles_frequencia_commmits_java_impl(df_fc_java_impl, nome_repositorio):
  fc_q1_java_impl = np.percentile(df_fc_java_impl.frequency_commits , [25])
  fc_q2_java_impl = np.percentile(df_fc_java_impl.frequency_commits , [50])
  fc_q3_java_impl = np.percentile(df_fc_java_impl.frequency_commits , [75])
  fc_q4_java_impl = np.percentile(df_fc_java_impl.frequency_commits , [100])
  print(f'Quartis da Frequencia de Commits Q1: {fc_q1_java_impl}, Q2: {fc_q2_java_impl}, Q3: {fc_q3_java_impl}, Q4: {fc_q4_java_impl}')

  dict_temp = {
    'fc_q1_java_impl': fc_q1_java_impl,'fc_q2_java_impl': fc_q2_java_impl,'fc_q3_java_impl': fc_q3_java_impl,'fc_q4_java_impl': fc_q4_java_impl
  }
  current_path = os.getcwd()
  path_arquivo = current_path + '/' + 'quartis' + '/'+ nome_repositorio + '/' + nome_repositorio + "_" + 'quartiles_frequencia_commmits_java_impl.csv'
  utilidades.export_csv_from_dict(dict_temp, path_arquivo)

  return fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl

def calcula_quartiles_frequencia_commmits_no_outliers(df_boxplot_fc_java_impl, nome_repositorio):
  fc_q1_java_impl = np.percentile(df_boxplot_fc_java_impl.frequency_commits , [25])
  fc_q2_java_impl = np.percentile(df_boxplot_fc_java_impl.frequency_commits , [50])
  fc_q3_java_impl = np.percentile(df_boxplot_fc_java_impl.frequency_commits , [75])
  fc_q4_java_impl = np.percentile(df_boxplot_fc_java_impl.frequency_commits , [100])
  print(f'Quartis da Frequencia de Commits Q1: {fc_q1_java_impl}, Q2: {fc_q2_java_impl}, Q3: {fc_q3_java_impl}, Q4: {fc_q4_java_impl}')

  dict_temp = {
    'fc_q1_java_impl': fc_q1_java_impl,'fc_q2_java_impl': fc_q2_java_impl,'fc_q3_java_impl': fc_q3_java_impl,'fc_q4_java_impl': fc_q4_java_impl
  }
  current_path = os.getcwd()
  path_arquivo = current_path + '/' + 'quartis' + '/'+ nome_repositorio + '/' + nome_repositorio + "_" + 'quartiles_frequencia_commmits_no_outliers.csv'
  utilidades.export_csv_from_dict(dict_temp, path_arquivo)

  return fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl

def calcula_quartiles_frequencia_commmits_no_outliers_less_3(df_boxplot_fc_java_impl2, nome_repositorio):
  fc_q1_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [25])
  fc_q2_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [50])
  fc_q3_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [75])
  fc_q4_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [100])
  print(f'Quartis da Frequencia de Commits Q1: {fc_q1_java_impl}, Q2: {fc_q2_java_impl}, Q3: {fc_q3_java_impl}, Q4: {fc_q4_java_impl}')

  dict_temp = {
    'fc_q1_java_impl': fc_q1_java_impl,'fc_q2_java_impl': fc_q2_java_impl,'fc_q3_java_impl': fc_q3_java_impl,'fc_q4_java_impl': fc_q4_java_impl
  }
  current_path = os.getcwd()
  path_arquivo = current_path + '/' + 'quartis' + '/'+ nome_repositorio + '/' + nome_repositorio + "_" + 'quartiles_frequencia_commmits_no_outliers_less_3.csv'
  utilidades.export_csv_from_dict(dict_temp, path_arquivo)

  return fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl