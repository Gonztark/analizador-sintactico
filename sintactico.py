import ply.yacc as yacc
from lexico import tokens  
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LT', 'LTE', 'GT', 'GTE', 'NE'),  
    ('right', 'UMINUS'), 
)


# diccionario para almacenar las variables
names = {}

results = ""


def p_program(p):
    '''program : program statement
               | statement'''

def p_statement_expr(p):
    'statement : expression SEMICOLON'
    print(p[1])

def p_statement_assign(p):
    '''statement : VAR ID ASSIGN expression SEMICOLON 
    | ID ASSIGN expression SEMICOLON'''
    names[p[2]] = p[4]

def p_statement_if(p):
    'statement : IF LPARENT expression RPARENT block'
    if p[3]:
        p[0] = p[5]

def p_statement_while(p):
    'statement : WHILE LPARENT expression RPARENT block'
    while p[3]:
        p[0] = p[5]

def p_statement_for(p):
    'statement : FOR LPARENT statement SEMICOLON expression SEMICOLON expression RPARENT block'



def p_statement_return(p):
    'statement : RETURN expression SEMICOLON'


def p_statement_function(p):
    '''statement : FUNCTION ID LPARENT RPARENT block
                 | FUNCTION ID LPARENT VAR ID RPARENT block'''
    if len(p) == 6:
       
        print("Función sin parámetros")
    elif len(p) == 8:
        names[p[5]] = 0  
        print("Función con parámetro")

def p_block(p):
    '''block : LBRACE statements RBRACE
             | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = {}

def p_statements(p):
    '''statements : statements statement
                  | statement'''

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPARENT expression RPARENT'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : ID'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print(f"Nombre no reconocido '{p[1]}'")
        p[0] = 0


def p_expression_comparison(p):
    '''expression : expression LT expression
                  | expression LTE expression
                  | expression GT expression
                  | expression GTE expression
                  | expression NE expression'''
    if p[2] == '<': p[0] = p[1] < p[3]
    elif p[2] == '<=': p[0] = p[1] <= p[3]
    elif p[2] == '>': p[0] = p[1] > p[3]
    elif p[2] == '>=': p[0] = p[1] >= p[3]
    elif p[2] == '<>': p[0] = p[1] != p[3]



def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]

def p_statement_print(p):
    'statement : PRINT LPARENT expression RPARENT SEMICOLON'
    print(f"{p[3]}")


def p_statement_summon(p):
    'statement : CALL ID LPARENT arguments RPARENT SEMICOLON'


def p_arguments(p):
    '''arguments : arguments COMMA expression
                 | expression
                 | empty'''
    if len(p) == 2:  
        p[0] = [p[1]]
    elif len(p) > 2:  
        p[1].append(p[3])
        p[0] = p[1]
    else: 
        p[0] = []

def p_empty(p):
    'empty :'
    pass

def append_result(message):
    global results
    results += message + "\n"

def p_error(p):
    if p:
        append_result(f"Error de Sintaxix en '{p.value}' en la línea {p.lineno}")
        print(f"Error de Sintaxix en '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de Sintaxis al final del código")




parser = yacc.yacc(debug=False)


def parse(data):
    global results
    results = ""
    parser.parse(data, debug=False)
    return results


#prueba
data = '''# Inicialización de variables
ITEM health = 100;
ITEM enemyHealth = 150;
ITEM damage = 5;

# Definición de función
CODEC attack() {
    enemyHealth = enemyHealth - damage;
    PRINT("Vida del enemigo reducida a: ");
    SCAN (enemyHealth <= 0) {
        PRINT("Enemigo eliminado");
    }
}

    SUMMON attack();


'''

if __name__ == '__main__':
    parse(data)

