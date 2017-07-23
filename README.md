# LALG_CompiladorPy
Trabalho acadêmico para desenvolver um compilador da linguagem LALG em python.

## Linguagem para reconhecimento
Linguagem LALG (derivada do Pascal)

## Gramática
Glalg = {N,T,P,S}

### Simbolos não terminais
```
N = {<programa>, <corpo>, <dc>, <comando>, <comandos>, <dc_v>, <mais_dc>,
<dc_p>, <variaveis>, <tipo_var>, <mais_var>, <parametros>, <corpo_p>,
<lista_par>, <mais_par>, <dc_loc>, <mais_dcloc>, <lista_arg>, <argumentos>,
<pfalsa>, <condicao>, <expressao>, <relacao>, <termo>, <outros_termos>,
<op_ad>, <op_un>, <fator>, <mais_fatores>, <op_mul>}
```
### Simbolos terminais
```
T = {var, ident, numero_int, numero_real, program, procedure, if, then, while, do, write,
read, else, begin, end, integer, real, (, ), *, /, +, -, >, <, =, $, ;, :, ,, ., <>, >=, <=, := }

Palavras reservadas: { program, var, procedure, if, then, while, do, write, read, else, begin, end, integer, real }
Simbolos simples: { (, ), *, /, +, -, >, <, =, $, ;, :, ,, . }
Simbolos duplos: { <>, >=, <=, := }
Números inteiros: (0..9)+
Números reais: (0..9)+.(0..9)+
```

### Regras de produção
```
P = {
  <programa> ::= program ident <corpo> .
  <corpo> ::= <dc> begin <comandos> end
  <dc> ::= <dc_v> <mais_dc> | <dc_p> <mais_dc> | λ
  <mais_dc> ::= ; <dc> | λ
  <dc_v> ::= var <variaveis> : <tipo_var>
  <tipo_var> ::= real | integer
  <variaveis> ::= ident <mais_var>
  <mais_var> ::= , <variaveis> | λ
  <dc_p> ::= procedure ident <parametros> <corpo_p>
  <parametros> ::= (<lista_par>) | λ
  <lista_par> ::= <variaveis> : <tipo_var> <mais_par>
  <mais_par> ::= ; <lista_par> | λ
  <corpo_p> ::= <dc_loc> begin <comandos> end
  <dc_loc> ::= <dc_v> <mais_dcloc> | λ
  <mais_dcloc> ::= ; <dc_loc> | λ
  <lista_arg> ::= (<argumentos>) | λ
  <argumentos> ::= ident <mais_ident>
  <mais_ident> ::= ; <argumentos> | λ
  <pfalsa> ::= else <comandos> | λ
  <comandos> ::= <comando> <mais_comandos>
  <mais_comandos> ::= ; <comandos> | λ
  <comando> ::= read (<variaveis>) |
                write (<variaveis>) |
                while <condicao> do <comandos> $ |
                if <condicao> then <comandos> <pfalsa> $ |
                ident <restoIdent>
  <restoIdent> ::= := <expressao> | <lista_arg>
  <condicao> ::= <expressao> <relacao> <expressao>
  <relacao> ::= = | <> | >= | <= | > | <
  <expressao> ::= <termo> <outros_termos>
  <op_un> ::= + | - | λ
  <outros_termos> ::= <op_ad> <termo> <outros_termos> | λ
  <op_ad> ::= + | -
  <termo> ::= <op_un> <fator> <mais_fatores>
  <mais_fatores> ::= <op_mul> <fator> <mais_fatores> | λ
  <op_mul> ::= * | /
  <fator> ::= ident | numero_int | numero_real | (<expressao>)
}
```

## Observações
* Comentários na LALG: entre { } ou /* */
* Identificadores e números são itens léxicos da forma:

      Ident: sequência de letras e dígitos, começando por letra.
      Número inteiro: sequência de dígitos (0 a 9).
      Número real: sequencia de um ou mais dígitos seguido de um ponto decimal seguido de um ou mais digitos.     
      
* Palavras reservadas – são os tokens usados para fins específicos, ou seja, que são previamente definidos na linguagem.
* Símbolos simples e duplos – são aqueles também definidos na linguagem (<, $, >, etc. como exemplo de simples, e := como exemplo de duplo).
