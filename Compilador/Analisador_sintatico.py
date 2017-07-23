import os


class AnalisadorSintatico:
    def __init__(self):
        self.arq_entrada = "saida_lexico.txt"
        self.arq_saida = "saida_sintatico.txt"
        self.arq_saida = open("saida_sintatico.txt", 'w')

        if not os.path.exists(self.arq_entrada):
            self.arq_saida.write("Arquivo de entrada inexistente")
            return

        # Abre o arquivo de entrada do programa
        self.arquivo = open("saida_lexico.txt", 'r')
        self.tokens = self.arquivo.readlines()  # Lê do arquivo todos os tokens presentes
        self.arquivo.close()
        # Contador da linha
        self.i = 0
        # Contador para as linhas do código intermediário
        self.j = 1
        self.linha_atual = ""
        # Salva o tipo atual para verificar se os tipos são compatíveis, utilizando em <R> e <S>
        self.tipoatual = ""
        # Tabela de simbolos
        self.tabelasimbolo = {}
        # Dicionario para a tabela de quadruplas
        self.quad = {}
        # Gerador das variaveis temporarias
        self.temp = 1

    # retorna o proximo token
    # e atualiza a linha atual
    def prox_token(self):
        self.i += 1
        self.linha_atual = self.tokens[self.i][self.tokens[self.i].find('=>') + 2: -1]

    # Retornar o token e o id, como por exemplo : tok401_integer
    def qual_token(self):
        return self.tokens[self.i][:self.tokens[self.i].find('=>')]

    # Procura retornar a parte do token, como por exemplo : tok401_integer=>2 retorna integer
    def que_tipo(self):
        return self.tokens[self.i][self.tokens[self.i].find('_') + 1:self.tokens[self.i].find('=>')]

    # Cada uma das funções abaixo representa um não terminal da gramática
    # e as ações semânticas q ela realiza

    # <programa> ::= program ident <corpo>.
    def programa(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok400_program" in self.tokens[self.i]:
            self.prox_token()
            if "tok500" in self.tokens[self.i]:
                self.prox_token()
                self.corpo()
                if "tok113_." not in self.tokens[self.i]:
                    print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado '.' - linha: " + self.linha_atual + "\n")
                    self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado '.' - linha: " + self.linha_atual + "\n")
                else:
                    self.prox_token()
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado identificador - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado identificador - linha: " + self.linha_atual + "\n")

        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado 'program' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado 'program' - linha: " + self.linha_atual + "\n")

    # <corpo> ::= <dc> begin <comandos> end
    def corpo(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        self.dc()
        if "tok410_begin" in self.tokens[self.i]:
            self.prox_token()
            self.comandos()
            if "tok411_end" in self.tokens[self.i]:
                self.prox_token()
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'end' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'end' - linha: " + self.linha_atual + "\n")
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" - esperado 'begin' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" - esperado 'begin' - linha: " + self.linha_atual + "\n")

    # <dc> ::= <dc_v> <mais_dc> | <dc_p> <mais_dc> | λ
    def dc(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok401_var" in self.tokens[self.i]:
            self.dc_v()
            self.mais_dc()

        if "tok402_procedure" in self.tokens[self.i]:
            self.dc_p()
            self.mais_dc()

    # <mais_dc> ::= ; <dc> | λ
    def mais_dc(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok110_;" in self.tokens[self.i]:
            self.prox_token()
            self.dc()
        # else:
        #     print("Erro sintatico - esperado ';' - linha: " + self.linha_atual + "\n")
        #     self.arq_saida.write("Erro sintatico - esperado ';' - linha: " + self.linha_atual + "\n")

    # <dc_v> ::= var <variaveis> : <tipo_var>
    def dc_v(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok401_var" in self.tokens[self.i]:
            self.prox_token()
            self.variaveis()
            if "tok111_:" in self.tokens[self.i]:
                self.prox_token()
                self.tipo_var()
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ':' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ':' - linha: " + self.linha_atual + "\n")

        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'var' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'var' - linha: " + self.linha_atual + "\n")

    # <tipo_var> ::= real | integer
    def tipo_var(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok413_real" in self.tokens[self.i]:
            self.prox_token()
        elif "tok412_integer" in self.tokens[self.i]:
            self.prox_token()
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado declaracao de tipo: real ou integer - linha: " + self.linha_atual + "\n")
            self.arq_saida.write(
                "Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado declaracao de tipo: real ou integer - linha: " + self.linha_atual + "\n")

    # <variaveis> ::= ident <mais_var>
    def variaveis(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok500" in self.tokens[self.i]:
            self.prox_token()
            self.mais_var()
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" Esperado identificador - linha: " + self.linha_atual + "\n")
            self.arq_saida.write(
                "Erro sintatico - Erro encontrado em: "+self.que_tipo()+" Esperado identificador - linha: " + self.linha_atual + "\n")

    # <mais_var> ::= , <variaveis> | λ
    def mais_var(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok112_," in self.tokens[self.i]:
            self.prox_token()
            self.variaveis()
        elif "tok500" in self.tokens[self.i]:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ',' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ',' - linha: " + self.linha_atual + "\n")

    # <dc_p> ::= procedure ident <parametros> <corpo_p>
    def dc_p(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok402_procedure" in self.tokens[self.i]:
            self.prox_token()

            if "tok500" in self.tokens[self.i]:
                self.prox_token()
                self.parametros()
                self.corpo_p()
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado identificador - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado identificador - linha: " + self.linha_atual + "\n")

        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'procedure' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'procedure' - linha: " + self.linha_atual + "\n")

    # <parametros> ::= ( <lista_par> ) | λ
    def parametros(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok100_(" in self.tokens[self.i]:
            self.prox_token()
            self.lista_par()
            if "tok101_)" in self.tokens[self.i]:
                self.prox_token()
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ')' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ')' - linha: " + self.linha_atual + "\n")

        # else:
        #     print("Erro sintatico - esperado '(' - linha: " + self.linha_atual + "\n")
        #     self.arq_saida.write("Erro sintatico - esperado '(' - linha: " + self.linha_atual + "\n")

    # <lista_par> ::= <variaveis> : <tipo_var> <mais_par>
    def lista_par(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        self.variaveis()
        if "tok111_:" in self.tokens[self.i]:
            self.prox_token()
            self.tipo_var()
            self.mais_par()
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ':' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ':' - linha: " + self.linha_atual + "\n")

    # <mais_par> ::= ; <lista_par> | λ
    def mais_par(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok110_;" in self.tokens[self.i]:
            self.prox_token()
            self.lista_par()
        # else:
        #     print("Erro sintatico - esperado ';' - linha: " + self.linha_atual + "\n")
        #     self.arq_saida.write("Erro sintatico - esperado ';' - linha: " + self.linha_atual + "\n")

    # <corpo_p> ::= <dc_loc> begin <comandos> end
    def corpo_p(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        self.dc_loc()
        if "tok410_begin" in self.tokens[self.i]:
            self.prox_token()
            self.comandos()
            if "tok411_end" in self.tokens[self.i]:
                self.prox_token()
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'end' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'end' - linha: " + self.linha_atual + "\n")
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'begin' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado 'begin' - linha: " + self.linha_atual + "\n")

    # <dc_loc> ::= <dc_v> <mais_dcloc> | λ
    def dc_loc(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok401_var" in self.tokens[self.i]:
            self.dc_v()
            self.mais_dcloc()

    # <mais_dcloc> ::= ; <dc_loc> | λ
    def mais_dcloc(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok110_;" in self.tokens[self.i]:
            self.prox_token()
            self.dc_loc()
        # else:
        #     print("Erro sintatico - esperado ';' - linha: " + self.linha_atual + "\n")
        #     self.arq_saida.write("Erro sintatico - esperado ';' - linha: " + self.linha_atual + "\n")

    # <lista_arg> ::= (<argumentos>) | λ
    def lista_arg(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok100_(" in self.tokens[self.i]:
            self.prox_token()
            self.argumentos()
            if "tok101_)" in self.tokens[self.i]:
                self.prox_token()
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ')' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ')' - linha: " + self.linha_atual + "\n")

        # else:
        #     print("Erro sintatico - esperado '(' - linha: " + self.linha_atual + "\n")
        #     self.arq_saida.write("Erro sintatico - esperado '(' - linha: " + self.linha_atual + "\n")

    # <argumentos> ::= ident <mais_ident>
    def argumentos(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok500" in self.tokens[self.i]:
            self.prox_token()
            self.mais_ident()
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" Esperado identificador - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" Esperado identificador - linha: " + self.linha_atual + "\n")

    # <mais_ident> ::= ; <argumentos> | λ
    def mais_ident(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok110_;" in self.tokens[self.i]:
            self.prox_token()
            self.argumentos()
        # else:
        #     print("Erro sintatico - Esperado ';' - linha: " + self.linha_atual + "\n")
        #     self.arq_saida.write("Erro sintatico - Esperado ';' - linha: " + self.linha_atual + "\n")

    # <pfalsa> ::= else <comandos> | λ
    def pfalsa(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok409_else" in self.tokens[self.i]:
            self.prox_token()
            self.comandos()
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado 'else' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado 'else' - linha: " + self.linha_atual + "\n")

    # <comandos> ::= <comando> <mais_comandos>
    def comandos(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        self.comando()
        self.mais_comandos()

    # <mais_comandos> ::= ; <comandos> | λ
    def mais_comandos(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok110_;" in self.tokens[self.i]:
            self.prox_token()
            self.comandos()
        # else:
        #     print("Erro sintatico - Esperado ';' - linha: " + self.linha_atual + "\n")
        #     self.arq_saida.write("Erro sintatico - Esperado ';' - linha: " + self.linha_atual + "\n")

    # <comando> ::= read (<variaveis>) | write (<variaveis>) | while <condicao> do <comandos> $ | if <condicao> then <comandos> <pfalsa> $ | ident <restoIdent>
    def comando(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok408_read" in self.tokens[self.i]:
            self.prox_token()
            if "tok100_(" in self.tokens[self.i]:
                self.prox_token()
                self.variaveis()
                if "tok101_)" in self.tokens[self.i]:
                    self.prox_token()
                else:
                    print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado ')' - linha: " + self.linha_atual + "\n")
                    self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado ')' - linha: " + self.linha_atual + "\n")

            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado '(' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado '(' - linha: " + self.linha_atual + "\n")
        elif "tok407_write" in self.tokens[self.i]:
            self.prox_token()
            if "tok100_(" in self.tokens[self.i]:
                self.prox_token()
                self.variaveis()
                if "tok101_)" in self.tokens[self.i]:
                    self.prox_token()
                else:
                    print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ')' - linha: " + self.linha_atual + "\n")
                    self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+" esperado ')' - linha: " + self.linha_atual + "\n")

            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado '(' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado '(' - linha: " + self.linha_atual + "\n")
        elif "tok405_while" in self.tokens[self.i]:
            self.prox_token()
            self.condicao()
            if "tok406_do" in self.tokens[self.i]:
                self.prox_token()
                self.comandos()
                if "tok109_$" in self.tokens[self.i]:
                    self.prox_token()
                else:
                    print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado '$' - linha: " + self.linha_atual + "\n")
                    self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado '$' - linha: " + self.linha_atual + "\n")
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado 'do' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado 'do' - linha: " + self.linha_atual + "\n")

        elif "tok403_if" in self.tokens[self.i]:
            self.prox_token()
            self.condicao()
            if "tok404_then" in self.tokens[self.i]:
                self.prox_token()
                self.comandos()
                self.pfalsa()
                if "tok109_$" in self.tokens[self.i]:
                    self.prox_token()
                else:
                    print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado '$' - linha: " + self.linha_atual + "\n")
                    self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado '$' - linha: " + self.linha_atual + "\n")
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado 'then' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado 'then' - linha: " + self.linha_atual + "\n")
        elif "tok500" in self.tokens[self.i]:
            self.prox_token()
            self.restoIdent()
        else:
            print(
                "Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado 'read' ou 'write' ou 'while' ou 'if' ou 'identificador' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write(
                "Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado 'read' ou 'write' ou 'while' ou 'if' ou 'identificador' - linha: " + self.linha_atual + "\n")

    # <restoIdent> ::= := <expressao> | <lista_arg>
    def restoIdent(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok203_:=" in self.tokens[self.i]:
            self.prox_token()
            self.expressao()
        elif "tok100" not in self.tokens[self.i]:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado ':=' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado ':=' - linha: " + self.linha_atual + "\n")
        else:
            self.lista_arg()
            # <condicao> ::= <expressao> <relacao> <expressao>

    # < condicao >::= < expressao > < relacao > <expressao >
    def condicao(self):

        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        self.expressao()
        self.relacao()
        self.expressao()

    # <relacao> ::= = | <> | >= | <= | > | <
    def relacao(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok108_=" in self.tokens[self.i]:
            self.prox_token()
        elif "tok200_<>" in self.tokens[self.i]:
            self.prox_token()
        elif "tok201_>=" in self.tokens[self.i]:
            self.prox_token()
        elif "tok202_<=" in self.tokens[self.i]:
            self.prox_token()
        elif "tok106_>" in self.tokens[self.i]:
            self.prox_token()
        elif "tok107_<" in self.tokens[self.i]:
            self.prox_token()
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado ' = | <> | >= | <= | > | < ' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write(
                "Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado ' = | <> | >= | <= | > | < ' - linha: " + self.linha_atual + "\n")

    # <expressao> ::= <termo> <outros_termos>
    def expressao(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        self.termo()
        self.outros_termos()

    # <op_un> ::= + | - | λ
    def op_un(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok104_+" in self.tokens[self.i]:
            self.prox_token()
        elif "tok105_-" in self.tokens[self.i]:
            self.prox_token()

    # <outros_termos> ::= <op_ad> <termo> <outros_termos> | λ
    def outros_termos(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if ("tok104" or "tok105") in self.tokens[self.i]:
            self.op_ad()
            self.termo()
            self.outros_termos()

    # <op_ad> ::= + | -
    def op_ad(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok104_+" in self.tokens[self.i]:
            self.prox_token()
        elif "tok105_-" in self.tokens[self.i]:
            self.prox_token()
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado operador '+' ou '-' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write(
                "Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado operador '+' ou '-' - linha: " + self.linha_atual + "\n")

    # <termo> ::= <op_un> <fator> <mais_fatores>
    def termo(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        self.op_un()
        self.fator()
        self.mais_fatores()

    # <mais_fatores> ::= <op_mul> <fator> <mais_fatores> | λ
    def mais_fatores(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if ("tok102" or "tok103") in self.tokens[self.i]:
            self.op_mul()
            self.fator()
            self.mais_fatores()

    # <op_mul> ::= * | /
    def op_mul(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok102_*" in self.tokens[self.i]:
            self.prox_token()
        elif "tok103_/" in self.tokens[self.i]:
            self.prox_token()
        else:
            print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado operador  '*' ou '/' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write(
                "Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado operador '*' ou '/' - linha: " + self.linha_atual + "\n")

    # <fator> ::= ident | numero_int | numero_real | (<expressao>)
    def fator(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok500" in self.tokens[self.i]:
            self.prox_token()
        elif "tok300" in self.tokens[self.i]:
            self.prox_token()
        elif "tok301" in self.tokens[self.i]:
            self.prox_token()
        elif "tok100_(" in self.tokens[self.i]:
            self.prox_token()
            self.expressao()
            if "tok101_)" in self.tokens[self.i]:
                self.prox_token()
            else:
                print("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado ')' - linha: " + self.linha_atual + "\n")
                self.arq_saida.write("Erro sintatico - Erro encontrado em: "+self.que_tipo()+"esperado ')' - linha: " + self.linha_atual + "\n")
        else:
            print(
                "Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado 'identificador' | 'numero inteiro' | 'numero real' | '(' - linha: " + self.linha_atual + "\n")
            self.arq_saida.write(
                "Erro sintatico - Erro encontrado em: "+self.que_tipo()+"Esperado 'identificador' | 'numero inteiro' | 'numero real' | '(' - linha: " + self.linha_atual + "\n")
