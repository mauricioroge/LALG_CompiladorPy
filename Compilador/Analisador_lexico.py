# Bibliotecas para entrada e saida de arquivos
# Biblioteca para o tratamento de strings
import string
import os


# Cada codigo citado a seguir representa um tipo de token
# e o que ele representa. Essa codificacao sera impressa no
# arquivo de saida
# =====================================
# tok1 - Simbolo Simples
#     tok100 - (
#     tok101 - )
#     tok102 - *
#     tok103 - /
#     tok104 - +
#     tok105 - -
#     tok106 - >
#     tok107 - <
#     tok108 - =
#     tok109 - $
#     tok110 - ;
#     tok111 - :
#     tok112 - ,
#     tok113 - .
#
# tok2 - Simbolo Duplo
#     tok200 - <>
#     tok201 - >=
#     tok202 - <=
#     tok203 - :=
#
# tok3 - Numero
#
#     tok300 - Numero Inteiro
#     tok301 - Numero Real
#
# tok4 - Palavra reservada
#     tok400 - program
#     tok401 - var
#     tok402 - procedure
#     tok403 - if
#     tok404 - then
#     tok405 - while
#     tok406 - do
#     tok407 - write
#     tok408 - read
#     tok409 - else
#     tok410 - begin
#     tok411 - end
#     tok412 - integer
#     tok413 - real
#
# tok500 - Identificador
#
# Declarando a classe para o Analisador Lexico onde contera as funcoes para o tratamento
class AnalisadorLexico():
    # Metodo construtor da classe
    def __init__(self, entrada):
        self.arq_entrada = entrada
        self.arq_saida = "saida_lexico.txt"

    # Metodo que muda o arquivo para string
    def mudaArquivo(self):
        self.arq_entrada = string

    # Metodo para capturar o arquivo da entrada
    def getEntrada(self):
        return self.arq_entrada

    # Metodo para capturar o arquivo de saida
    def getSaida(self):
        return self.arq_saida

    # Metodo para verificar se eh simbolo simples
    def ehsimples(self, entrada):
        # Lista contendo os operadores da linguagem
        simples = "()*/+-><=$;:,."
        if entrada in simples:
            return True
        return False

    # Metodo que tokeniza o simbolo que ja foi verificado
    def qualtokensimples(self, entrada):
        # Lista contendo os operadores da linguagem
        simples = "()*/+-><=$;:,."
        posicao = simples.find(entrada)
        if posicao <= 9:
            return "tok10" + str(posicao)
        else:
            return "tok1" + str(posicao)

    # Metodo para verificar se o elemento eh um delimitador
    def ehduplo(self, entrada):
        # Lista de delimitadores
        duplo = "<>,>=,<=,:=".split(',')
        if entrada in duplo:
            return True
        return False

    # Metodo que tokeniza o delimitador que ja foi verificado
    # A funcao find retorna a posicao do caracter na string
    # caso exista
    def qualtokenduplo(self, entrada):
        # Lista de delimitadores da linguagem
        duplo = "<>,>=,<=,:=".split(',')
        posicao = 0
        for x in duplo:
            if x == entrada:
                break
            posicao += 1
        return "tok20" + str(posicao)

    # Metodo para verificar se a entrada em questao eh uma palavra reservada ou nao
    def ehReservada(self, entrada):
        # Lista de palavras reservadas da linguagem
        reservadas = "program,var,procedure,if,then,while,do,write,read,else,begin,end,integer,real".split(',')
        if entrada in reservadas:
            return True
        return False

    # Metodo para tokenizar a palavra reservada
    def qualTokenReservada(self, entrada):
        # Lista de palavras reservadas da linguagem
        reservadas = "program,var,procedure,if,then,while,do,write,read,else,begin,end,integer,real".split(',')
        posicao = 0
        for x in reservadas:
            if x == entrada:
                break
            posicao += 1
        if posicao <= 9:
            return "tok40" + str(posicao)
        else:
            return "tok4" + str(posicao)

    def ehLetra(self, entrada):
        # Lista de letras presentes no alfaberto
        letras = string.ascii_letters
        if entrada in letras:
            return True
        return False

    def ehDigito(self, entrada):
        # Lista de digitos
        digits = '0123456789'
        if entrada in digits:
            return True
        return False

    def analisa(self):

        # Abre o arquivo de saida como escrita
        arquivo_saida = open(self.arq_saida, 'w')

        # Verifica se o arquivo de entrada existe
        if not os.path.exists(self.arq_entrada):
            arquivo_saida.write("Arquivo de entrada inexistente")
            return

        # Abre o arquivo de entrada do programa

        arquivo = open(self.arq_entrada, 'r')

        # Le a primeira linha
        linha_programa = arquivo.readline()

        # Variavel q indica a linha atual do programa
        numero_da_linha = 1

        # Percorre o programa linha a linha
        while linha_programa:
            i = 0  # Representa a posicao do caracter
            tamanho_linha = len(linha_programa)

            while i < tamanho_linha:  # Percorre caracter a caracter da linha em questao
                char_atual = linha_programa[i]
                char_seguinte = None
                # So posso pegar o proximo caracter se o mesmo exister, entao:
                if i + 1 < tamanho_linha:
                    char_seguinte = linha_programa[i + 1]
                # -------------------------------------------------------------------
                # Verifica o que esta sendo lido
                # =================================================================
                # Verifica se o caracter eh um simbolo duplo
                if char_seguinte != None and self.ehduplo(char_atual + char_seguinte):
                    arquivo_saida.write(self.qualtokenduplo(
                        char_atual + char_seguinte) + '_' + char_atual + char_seguinte + '=>' + str(
                        numero_da_linha) + '\n')
                    i += 1  # Fazer isso pq aqui ele ja esta pegando 2 caracteres,entao ele vai pular esses 2 caracteres
                # Verifica os blocos de comentarios
                #= =================================================================
                elif (char_atual == '/' and char_seguinte == '*'):
                    coment = True  # Impede de acontecer erro inesperado

                    linha_comeco = numero_da_linha
                    while coment and not (char_atual == '*' and char_seguinte == '/'):
                        # Soh posso pegar o caractere atual e o proximo se ele existe na linha
                        if i + 2 < tamanho_linha:
                            i += 1
                            char_atual = linha_programa[i]
                            char_seguinte = linha_programa[i + 1]
                        else:
                            linha_programa = arquivo.readline()  # Le a proxima linha
                            tamanho_linha = len(linha_programa)
                            numero_da_linha += 1
                            i = -1
                            if (not linha_programa):
                                arquivo_saida.write(
                                    "Erro Lexico - Comentario de bloco nao fechado - linha: %d\n" % linha_comeco)
                                coment = False
                    i += 1  # Faco isso para que nao considere o '/' do final do bloco (na composicao */) no proximo loop
                elif char_atual == '{':
                    coment = True
                    linha_comeco = numero_da_linha
                    while coment and not char_atual == '}':
                        if i+1 < tamanho_linha:
                            i += 1
                            char_atual = linha_programa[i]

                        else:
                            linha_programa = arquivo.readline()
                            tamanho_linha = len(linha_programa)
                            numero_da_linha += 1
                            i = -1
                            if (not linha_programa):
                                arquivo_saida.write(
                                    "Erro Lexico - Comentario de bloco nao fechado - linha: %d\n" % linha_comeco)
                                coment = False
                # Verifica se eh um simbolo simples
                # ==============================================================================
                elif self.ehsimples(char_atual):
                    arquivo_saida.write(
                        self.qualtokensimples(char_atual) + '_' + char_atual + '=>' + str(numero_da_linha) + '\n')
                # =================================================================
                # Verifica se o caracter eh um numero
                elif (self.ehDigito(char_atual)):
                    string_temp = char_atual
                    i += 1
                    j = 0  # conta se tem 1 digito depois do '.'
                    char_atual = linha_programa[i]
                    while (self.ehDigito(char_atual) and (i + 1 < tamanho_linha)):
                        string_temp += char_atual
                        i += 1
                        char_atual = linha_programa[i]

                    if char_atual == '.':
                        if i + 1 < tamanho_linha:
                            string_temp += char_atual
                            i += 1
                            char_atual = linha_programa[i]
                            while self.ehDigito(char_atual) and i + 1 < tamanho_linha:
                                j += 1
                                string_temp += char_atual
                                i += 1
                                char_atual = linha_programa[i]

                            if (char_atual == '.'):
                                j = 0
                                # Tratamento de erro
                                while (i + 1 < tamanho_linha):
                                    i += 1
                                    char_atual = linha_programa[i]
                                    if self.ehsimples(char_atual) or char_atual == ' ':
                                        i -= 1  # Preciso voltar um elemento da linha para que o delimitador seja reconhecido no momento certo
                                        break
                        else:
                            arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' % numero_da_linha)

                        if j > 0:
                            arquivo_saida.write('tok301_' + string_temp + '=>' + str(numero_da_linha) + '\n')
                        else:
                            arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' % numero_da_linha)
                    else:
                        arquivo_saida.write('tok300_' + string_temp + '=>' + str(numero_da_linha) + '\n')

                    if not self.ehDigito(char_atual):
                        i -= 1
                # ==================================================================
                # Verifica se esta entrando uma palavra reservada ou um identificador
                elif (self.ehLetra(char_atual)):
                    # Se o primeiro caracter for uma letra, entao estamos prontos para verificar
                    # se os proximos elementos farao parte de um identificador ou de uma palavra
                    # reservada

                    string_temporaria = char_atual
                    i += 1
                    erro = False

                    while i < tamanho_linha:
                        char_seguinte = None
                        char_atual = linha_programa[i]
                        if i + 1 < tamanho_linha:
                            char_seguinte = linha_programa[i + 1]
                        if (self.ehLetra(char_atual) or self.ehDigito(char_atual) or char_atual == '_'):
                            string_temporaria += char_atual
                        elif (
                                                char_atual == ',' or char_atual == ';' or char_atual == ' ' or char_atual == '\t' or char_atual == '\r' or char_atual == '/'):
                            i -= 1  # Precisa voltar 1 posicao para que o delimitador seja reconhecido no momento certo
                            break
                        elif (char_seguinte != None and self.ehduplo(char_atual + char_seguinte) or self.ehsimples(
                                char_atual)):
                            i -= 1
                            break
                        elif char_atual != '\n':
                            arquivo_saida.write(
                                "Erro Lexico: Identificador com caracter invalido: " + char_atual + " - linha: %d\n" % numero_da_linha)
                            erro = True
                            break
                        i += 1  # Passando ate chegar ao final do identificador ou palavra reservada

                    if (erro):
                        while (i + 1 < tamanho_linha):
                            i += 1
                            char_atual = linha_programa[i]

                            if self.ehsimples(
                                    char_atual) or char_atual == ' ' or char_atual == '\t' or char_atual == '\r' or char_atual == '/':
                                i -= 1
                                break
                    else:
                        if (self.ehReservada(string_temporaria)):
                            arquivo_saida.write(
                                self.qualTokenReservada(string_temporaria) + '_' + string_temporaria + '=>' + str(
                                    numero_da_linha) + '\n')
                        else:
                            arquivo_saida.write("tok500_" + string_temporaria + '=>' + str(numero_da_linha) + '\n')

                # Se nenhuma das leituras anteriores forem acessadas e estas posteriores tambem nao,
                # significa que houve algum caracter zuado ai


                elif char_atual != '\n' and char_atual == ' ' and char_atual == '\t' and char_atual == '\r':
                    arquivo_saida.write(
                        "Erro Lexico: Caracter Invalido: " + char_atual + " - linha: %d\n" % numero_da_linha)
                # ===============================================================
                i += 1  # Incrementando a leitura dos caracteres da linha lida atual

            linha_programa = arquivo.readline()  # Leitura da proxima linha
            numero_da_linha += 1
        # Fim da leitura do programa
        arquivo_saida.write('$')
        # Fim do arquivo entrada
        arquivo.close()
        # Fim do arquivo de saida
        arquivo_saida.close()
        # ===================================
        # Fim do analisador Lexico
