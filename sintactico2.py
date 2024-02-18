import ply.yacc as yacc
from lexico import tokens  # Make sure this matches the name of your lexer file

# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LT', 'LTE', 'GT', 'GTE', 'NE'),  # Non-associative operators
    ('right', 'UMINUS'),  # Unary minus operator
)


# Dictionary of names (for storing variables)
names = {}
scope_stack = [{}]



def p_program(p):
    '''program : program statement
               | statement'''
    # A program is a sequence of statements

def p_statement_expr(p):
    'statement : expression SEMICOLON'
    print(p[1])

def p_statement_assign(p):
    '''statement : VAR ID ASSIGN expression SEMICOLON 
                 | ID ASSIGN expression SEMICOLON'''
    scope_stack[-1][p[2]] = p[4]


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
    # Handle return statement


def p_statement_function(p):
    '''statement : FUNCTION ID LPARENT RPARENT block
                 | FUNCTION ID LPARENT VAR ID RPARENT block'''
    # Create a new scope for the function body
    scope_stack.append({})
    
    # If the function has parameters, add them to the function's scope
    if len(p) > 6:
        # Assuming the parameter name is in p[5]
        scope_stack[-1][p[5]] = 0  # Initialize parameter with a default value or handle appropriately
    
    # Execute the function body (you might want to store the function body for later execution instead)
    # p[0] = p[len(p) - 1]  # This assigns the block's execution result to the function statement
    
    # Leaving the function's scope
    scope_stack.pop()





def p_block(p):
    '''block : LBRACE statements RBRACE
             | LBRACE RBRACE'''
    if len(p) == 4:
        # Entering a new block
        scope_stack.append({})
        p[0] = p[2]
        # Exiting the block
        scope_stack.pop()
    else:
        scope_stack.append({})
        p[0] = {}
        scope_stack.pop()


def p_statements(p):
    '''statements : statements statement
                  | statement'''
    # A block can contain multiple statements

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
    for scope in reversed(scope_stack):
        if p[1] in scope:
            p[0] = scope[p[1]]
            break
    else:
        print(f"Undefined name '{p[1]}'")
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



def p_error(p):
    if p:
        print(f"Error de Sintaxix en '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de Sintaxis al final del código")


# Build the parser
parser = yacc.yacc(debug=False)


def parse(data):
    parser.parse(data, debug=False)

# Test it out
data = '''
ITEM health = 100;
ITEM enemyHealth = 150;

CODEC attack(ITEM damage) {
    enemyHealth = enemyHealth - damage;
}


'''

if __name__ == '__main__':
    parse(data)

