import os
import utilidades
import extracao
import carrega_dataframes
import analisa_metricas
import scatter_plots
import analise_dependencias_arquivos as ada

DATA_BASE = "my_promocity.db"
URL_REPOSITORIO_GIT = 'https://github.com/armandossrecife/promocity.git'
NOME_REPOSITORIO = 'promocity'

# --- 1. Carrega dependencias ---
utilidades.carrega_dependencias()

# clona o repositorio para permitir a analise
utilidades.clona_repositorio(my_repositorio=URL_REPOSITORIO_GIT)

# Detalhes da faixa de commits que sera analisada
COMMIT_INICIAL = utilidades.get_primeiro_commit(repositorio=NOME_REPOSITORIO)
COMMIT_FINAL = utilidades.get_ultimo_commit(repositorio=NOME_REPOSITORIO)
print(f'commit_inicial: {COMMIT_INICIAL}, commit_final: {COMMIT_FINAL}')

# --- 2. Extrai informacoes de commits (inicial, final) e arquivos modificados em cada commmit ---
extracao.extrai_informacoes_repositorio_by_commits(my_repositorio=URL_REPOSITORIO_GIT, nome_repositorio=NOME_REPOSITORIO, commit_inicial=COMMIT_INICIAL, commit_final=COMMIT_FINAL)

# --- 3. Carrega os dados das tabelas em dataframes ---
print('Carrega os dados nos dataframes')
df_commits_from_db, df_files_from_db, df_files_commits_from_db = carrega_dataframes.load_dataframes(database_name=DATA_BASE)
# 3.1 Faz alguns ajustes nos dataframes para o calculo de AMLOC
df_files_from_db['modified_lines'] = df_files_from_db.added_lines + df_files_from_db.deleted_lines
df_files_commits_from_db['modified_lines'] = df_files_commits_from_db.file_added_lines + df_files_commits_from_db.file_deleted_lines
print('Dataframes carregados com sucesso!')
print(df_files_commits_from_db.head(3))
print(df_files_commits_from_db.tail(3))

# Cria as pastas de graficos, quartis e criticos para o repositorio analisado
current_path = os.getcwd()
pasta_grafico_repositorio_boxplot = current_path + '/' + 'graficos' + '/'+ NOME_REPOSITORIO + '/' + 'boxplot'
pasta_grafico_repositorio_scatter = current_path + '/' + 'graficos' + '/'+ NOME_REPOSITORIO + '/' + 'scatter'
pasta_quartis_repositorio = current_path + '/' + 'quartis' + '/'+ NOME_REPOSITORIO
pasta_criticos_repositorio = current_path + '/' + 'criticos' + '/'+ NOME_REPOSITORIO
utilidades.create_folder(pasta_grafico_repositorio_boxplot)
utilidades.create_folder(pasta_grafico_repositorio_scatter)
utilidades.create_folder(pasta_quartis_repositorio)
utilidades.create_folder(pasta_criticos_repositorio)

# --- 4. Faz a analise das metricas de AMLOC ---
print('Calcula o AMLOC')
df_accumulated_modified_locs, df_accumulated_modified_locs_boxplot, group_files_modified_lines = analisa_metricas.get_accumulated_modified_locs(df_files_from_db)
print('Gera o boxplot de AMLOC de todos os arquivos do repositório')
analisa_metricas.gera_boxplot_accumulated_modified_locs(df_accumulated_modified_locs_boxplot, NOME_REPOSITORIO)
print('Gera o boxplot de AMLOC')
df_accumulated_modified_locs_boxplot_validos = analisa_metricas.get_accumulated_modified_locs_boxplot_valid(df_accumulated_modified_locs_boxplot, NOME_REPOSITORIO)
print('Calcula os quartiles de AMLOC')
em_q1, em_q2, em_q3, em_q4 = analisa_metricas.get_quartiles_offiles_modified_lines(group_files_modified_lines,df_accumulated_modified_locs_boxplot_validos, NOME_REPOSITORIO)
print('Calcula o AMLOC dos arquivos .java')
df_locm_java_impl = analisa_metricas.get_df_accumulated_modified_java_files(df_accumulated_modified_locs)
print('Gera o boxplot de AMLOC dos arquivos .java')
df_boxplot_em_java_impl = analisa_metricas.show_boxplot_accumulated_modified_java_files(df_locm_java_impl, NOME_REPOSITORIO)
print('Calcula o AMLOC dos arquivos .java (Válidos - arquivos que modificaram pelo menos uma vez)')
df_boxplot_em_java_impl_valid = analisa_metricas.get_accumulated_modified_java_files_valid(df_boxplot_em_java_impl, NOME_REPOSITORIO)
print('Calcula os quartiles referente ao AMLOC dos arquivos .java')
em_q1_java_impl, em_q2_java_impl, em_q3_java_impl, em_q4_java_impl = analisa_metricas.get_quartiles_offiles_modified_lines_java_files_valid(df_boxplot_em_java_impl_valid, NOME_REPOSITORIO)

# --- 5. Faz a analise das metricas de Complexidade Ciclomatica ---
print('Calculo da Complexidade Ciclomatica')
df_complexidade_ciclomatica = analisa_metricas.get_complexidade_ciclomatica(df_files_commits_from_db)
print(df_complexidade_ciclomatica)
print('Calcula o boxplot de complexidade ciclomática')
df_cc_temp,df_boxplot_cc_temp = analisa_metricas.get_boxplot_complexidade_ciclomatica(df_complexidade_ciclomatica, NOME_REPOSITORIO)
print('Calcula os quartiles das complexidades ciclomáticas')
em_q1_cc_temp,em_q2_cc_temp, em_q3_cc_temp, em_q4_cc_temp = analisa_metricas.get_quartiles_complexidade_ciclomatica(df_boxplot_cc_temp, NOME_REPOSITORIO)
print('Calcula a complexidade ciclomática apenas dos arquivos .java')
df_cc_temp_java_impl, df_cc_temp_boxplot_em_java_impl = analisa_metricas.get_boxplot_complexidade_ciclomatica_only_java(df_cc_temp, NOME_REPOSITORIO)
print('Calcula os quartiles de complexidade ciclomática dos arquivos .java')
em_q1_cc_temp_java_impl, em_q2_cc_temp_java_impl, em_q3_cc_temp_java_impl, em_q4_cc_temp_java_impl= analisa_metricas.get_quartiles_complexidade_ciclomatica_java_impl(df_cc_temp_boxplot_em_java_impl, NOME_REPOSITORIO)

# --- 6. Faz a analise de FOCs (frequencia dos commits) ---
print('Calcula frequencia dos commits')
df_fc, df_boxplot_fc = analisa_metricas.calcula_frequencia_commits(df_files_from_db)
print('Gera o boxplot da frequencia de commits')
analisa_metricas.gera_boxplot_frequencia_commits(df_boxplot_fc, NOME_REPOSITORIO)
print('Calcula os quartiles das frequencias de commits')
fc_q1,fc_q2, fc_q3, fc_q4 = analisa_metricas.calcula_quartiles_frequencia_commits(df_boxplot_fc, NOME_REPOSITORIO)
print('Gera o boxplot da FOC apenas dos arquivos .java')
df_fc_java_impl, df_boxplot_fc_java_impl, df_boxplot_fc_java_impl2 = analisa_metricas.gera_boxplot_frequencia_commits_only_java(df_fc, NOME_REPOSITORIO)
fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl = analisa_metricas.calcula_quartiles_frequencia_commmits_no_outliers_less_3(df_boxplot_fc_java_impl2, NOME_REPOSITORIO)

# --- 7. Faz a juncao de AMOL e FOC para gerar os scatter plots ---
print('Gera o scatter plot AMLOC e FOC')
df_em_fc = scatter_plots.gera_df_foc_amloc(df_accumulated_modified_locs, df_fc)
df_fator_multiplicacao = scatter_plots.gera_df_fator_foc_amloc(df_em_fc)
df_em_fc_java_impl, df_fator_multiplicacao_em_fc_java_impl = scatter_plots.gera_scatter_plot_foc_amloc(df_em_fc, NOME_REPOSITORIO)
print('Gera o scatter plot AMLOC e FOC com quadrantes')
list_initial_critical_files_from_sp = scatter_plots.gera_scatter_plot_foc_amloc_com_quadrantes(df_em_fc_java_impl, em_q3_java_impl, fc_q3_java_impl, NOME_REPOSITORIO)
list_critical_files = scatter_plots.gera_scatter_plot_final_foc_amloc_com_quadrantes(list_initial_critical_files_from_sp, df_em_fc_java_impl, em_q3_java_impl, fc_q2_java_impl, NOME_REPOSITORIO)
print('Arquivos criticos: Alta AMLOC e Alta FOC')
print(list_critical_files)
current_path = os.getcwd()
nome_arquivo_csv = current_path + '/' + 'criticos' + '/'+ NOME_REPOSITORIO + '/' + NOME_REPOSITORIO + '_' + 'arquivos_criticos.csv'
nomes = []
amlocs = []
focs = [] 
for each_tupla in list_critical_files:
    nomes.append(each_tupla[0])
    amlocs.append(each_tupla[1])
    focs.append(each_tupla[2])
dict_temp = {
    'nome': nomes, 'amloc':amlocs, 'foc':focs
}
utilidades.export_csv_from_dict(dict_temp, nome_arquivo_csv)

# --- 8. Analise de dependencias, co-change e arquivos impactados ---
print('Faz a análise das dependências dos arquivos')
path_projeto_src_java = "promocity/src/main/java/"

# Faz a análise das dependências dos arquivos
ada.gera_arquivos_java(path_projeto=path_projeto_src_java, nome_arquivo='arquivosjava.txt')
# Cria a matriz de relacao entre os arquivos do projeto da pasta src
lista_linhas_arquivos_cassandra, lista_colunas_arquivos_cassandra = ada.cria_duas_listas_arquivos_analisados(nome_arquivo='arquivosjava.txt', diretorio_src_main=path_projeto_src_java)
# Gera dicionarios de dependencias entre os arquivos
dicionario_dsm = ada.cria_dicionario_dsm(lista_linhas_arquivos_cassandra, lista_colunas_arquivos_cassandra, path_main=path_projeto_src_java)
dicionario_dsm_depende_de = ada.cria_dicionario_dsm_depende_de(lista_linhas_arquivos_cassandra, lista_colunas_arquivos_cassandra, path_main=path_projeto_src_java)
lista_arquivos_criticos = list_critical_files

# arquivosjava.txt e dicionario_dsm
ada.get_dict_file_a_uses_file_b(lista_arquivos_criticos, content='arquivosjava.txt', my_dictionary=dicionario_dsm, path_main=path_projeto_src_java)
ada.get_dict_file_a_uses_file_b(lista_arquivos_criticos, content='arquivosjava.txt', my_dictionary=dicionario_dsm_depende_de, path_main=path_projeto_src_java)

dict_arquivos_dependentes_arquivos_criticos, lista_arquivos_impactados, l_ac, l_adac, l_tamanho_adac = ada.mostra_lista_arquivos_dependentes(lista_arquivos_criticos, content='arquivosjava.txt', my_dictionary=dicionario_dsm_depende_de, path_main=path_projeto_src_java)
df_arquivos_dependentes_arquivos_criticos = ada.gera_df_arquivos_dependentes_arquivos_criticos(l_ac, l_tamanho_adac, l_adac)

lista_arquivos_impactados_unicos = ada.gera_lista_arquivos_impactados_unicos(dict_arquivos_dependentes_arquivos_criticos, lista_arquivos_impactados)
print(f'Arquivos impactados unicos: {lista_arquivos_impactados_unicos}')
lista_nomes_arquivos_impactados_unicos, df_qtd_lm, dict_modified_lines_arquivos_criticos, soma_modified_lines_arquivos_criticos = ada.relatorio_linhas_alteradas_pelas_classes_criticas(lista_arquivos_impactados_unicos,lista_arquivos_criticos, df_em_fc_java_impl, df_files_commits_from_db)

print('Testes de impacto de mudancas')
# Quantidade de linhas modificadas dos arquivos impactados
dict_modified_lines_arquivos_impactados = {}

for each in lista_nomes_arquivos_impactados_unicos:
  qtd_temp = df_qtd_lm[df_qtd_lm.file_filename == each]['modified_lines'].to_list()
  if len(qtd_temp) == 1:
    dict_modified_lines_arquivos_impactados[each] = qtd_temp[0]
  else:
    dict_modified_lines_arquivos_impactados[each] = 0

soma_modified_lines_arquivos_impactados = 0
for key, value in dict_modified_lines_arquivos_impactados.items():
  soma_modified_lines_arquivos_impactados = soma_modified_lines_arquivos_impactados + value

print(f'As {len(dict_modified_lines_arquivos_impactados)} classes impactadas, pelos arquivos críticos, mudaram {soma_modified_lines_arquivos_impactados} linhas no sistema')

## Soma de todas as linhas modificadas pelos arquivos .java
qtd_arquivos_java = df_qtd_lm.shape[0]
qtd_modified_lines_arquivos_java = df_qtd_lm['modified_lines'].sum()

print(f'{qtd_arquivos_java} arquivos mudaram {qtd_modified_lines_arquivos_java} LOC no sistema')

# As classes críticas e as classes impactada correspondem a X linhas modificadas
# o que dá P % de linhas modificadas no sistema

soma_modified_lines_analisadas = soma_modified_lines_arquivos_criticos + soma_modified_lines_arquivos_impactados

percentual_modified_lines_analisadas = round( (soma_modified_lines_analisadas/qtd_modified_lines_arquivos_java) * 100 , 2)

print(f'As {len(dict_modified_lines_arquivos_criticos)} classes criticas e as {len(dict_modified_lines_arquivos_impactados)} classes impactadas correspondem a {percentual_modified_lines_analisadas}% das linhas modificadas no sistema')

# Dataframe contendo todos os commits da faixa analisada
df = df_commits_from_db[['name', 'modified_files']]

# Lista arquivos críticos
print(f'{len(lista_arquivos_criticos)}, {lista_arquivos_criticos}')

# Arquivos impactados únicos
print(f' {len(lista_arquivos_impactados_unicos)}, {lista_arquivos_impactados_unicos}')

# Dicionário com o arquivo crítico e todos os seus arquivos co-change (além dos arquivos de implementação existem os arquivos .txt, de configuração, testes, entre outros)
dict_arquivo_critico_cochange = ada.get_dict_arquivos_modificados_with_critico(lista_arquivos_criticos, df)
print(f'{len(dict_arquivo_critico_cochange)}')
