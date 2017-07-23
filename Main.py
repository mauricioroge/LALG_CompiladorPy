# Projeto de Compiladores II
# Autor: Mauricio Rogerio Ramos Araujo
# ---------------------------------------------
# Trabalho realizado utilizando como referencia de base: https://github.com/v-assys/CompiladorPhyton
from Analisador_lexico import AnalisadorLexico
from Analisador_sintatico import AnalisadorSintatico

print("==========================================")
entrada = "entrada.txt"
print("entrada.txt")
print("")
lexico = AnalisadorLexico(entrada)
lexico.analisa()
sintatico = AnalisadorSintatico()
sintatico.programa()
sintatico.arq_saida.close()
print("++++++++++++++++++++++++++++++++++++++++++")
# for k,v in sorted(sintatico.quad.items()):
#     print(v)
# print("==========================================")
# entrada = "entrada2.txt"
# print("entrada2.txt\n")
# lexico = AnalisadorLexico(entrada)
# lexico.analisa()
# sintatico = AnalisadorSintatico()
# sintatico.A()
# sintatico.arq_saida.close()
# print("++++++++++++++++++++++++++++++++++++++++++")
# for k, v in sorted(sintatico.quad.items()):
#     print(v)
#
