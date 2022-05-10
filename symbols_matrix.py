                                    # --- Project creators --- #
# 1. Name: Serafeim-Ilias Antoniou | A.M.: 2640 | username: cse42640 #
# 2. Name: Sophia Pasoi            | A.M.: 2798 | username: cse42798 #
# Execution Guidelines: #
# In the phase_1 folder you will find the code, plus some testing modules to verify the correct function of the program.
# The programs named "green_X.stl" are meant for the demonstration of our correct output messages.
# The programs named "red_X.stl" are meant for the demonstration of our correct error-messages output. #
# In order to execute the .py file from the command line you will need to syntax your command this way:
# python3 verbal_syntax_analysts.py green_X.stl or red_X.stl #

import string
import sys      #cmd line argument
import copy     #helps deep-copying our lists

#  ---------------------------------------------------------------------------------------------------------------- #
#                                           ---  VERBAL ANALYST: ---                                                #
# ----------------------------------------------------------------------------------------------------------------- #  
fp_position = 0             #Current file pointer position
line = 1                    #Current line
in_line_position = 1        #Position inside the line

def lex():
    # Time saving: Open file as argument in terminal: #
    try:
        file_pointer = open(sys.argv[1], 'r')
    except IndexError:
        file_pointer = open('test.stl', 'r') #Automatic compilation without terminal command

    # Marks: (strictly based on the Professor's outline) #
    state_0 = 0     #Return of symbols
    state_1 = 1     #Identifiers --> consist of one letter and a letter or digit
    state_2 = 2     #Integer numbers
    state_3 = 3     #Symbol: '<'
    state_4 = 4     #Symbol: '>'
    state_5 = 5     #Symbol: ':'
    # --- Comment marks: --- #
    state_6 = 6     #Comment symbol '//'
    state_7 = 7     #OPENING comment symbol '/*'
    state_8 = 8     #CLOSING comment symbol '*/'
    ERROR_state = -1
    OK_state = -2
    EOF_state = -3
    neg_mark = 0    #In case of negative integer numbers

    verbal_unit = []        #Empty list (filled with characters later...)
    rtrn_verbal_unit = []   #My return list

    # --- A list of reserved Starlet words: --- #
    res_words = [['program', 30], ['endprogram', 31], ['declare', 32], ['if', 33], ['then', 34], ['else', 35], ['endif', 36], ['dowhile', 37], ['enddowhile', 38, ], ['while', 39], ['endwhile', 40], ['loop', 41], ['endloop', 42], ['exit', 43], ['forcase', 44], ['endforcase', 45], ['incase', 46],
    ['endincase', 47], ['when', 48], ['default', 49], ['enddefault', 50], ['function', 51], ['endfunction', 52], ['return', 53], ['in', 54], ['inout', 55], ['inandout', 56], ['and', 57], ['or', 58], ['not', 59], ['input', 60], ['print', 61]]

    global fp_position
    global line
    global in_line_position

    # --- Counters: --- #
    letter_count = 0    #Num of letter for state_1 purposes
    mark_count = 0      #Sum of marks
    identifier = ''     #Empty string (at first)

    file_pointer.seek(fp_position)      #Go to the last checkpoint and retrieve the next word

    state = state_0     #Current state
    
    while (state != EOF_state and state != ERROR_state and state != OK_state):
        input = file_pointer.read(1)        #Read new char from file
        in_line_position += 1

        if (not input and state != state_7):
            if (state == state_1):
                state = OK_state
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [1]
            elif (state == state_2):
                state = OK_state
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [2]
            else:
                state = EOF_state

        # --- EOF state: --- #
        if (state == EOF_state):
            rtrn_verbal_unit = ['EOF'] + [62]

        # --- State_0: Initial state: --- #
        if (state == state_0):
            if (input == ' ' or input == '\n' or input == '\t'):     #covering all white character cases!
                if (input == '\n'):
                    line += 1
                    in_line_position = 0
                if (input == '\t'):
                    in_line_position += 4       #1 Tab = 4 spaces
                state = state_0
            elif (input in string.ascii_letters):   #input --> letter check
                state = state_1
            elif (input in string.digits):      #input --> integer nummber check
                state = state_2
            elif (input == '<'):
                state = state_3
            elif (input == '>'):
                state = state_4
            elif (input == ':'):
                state = state_5
            elif (input == '/'):
                state = state_6
            elif (input == '\r'):       #Hitting the enter button
                state = state_0
            elif (input == ''):
                state = EOF_state
            else:
                state = OK_state
                verbal_unit = input
                identifier = "".join(verbal_unit)

                if (input == '+'):
                    rtrn_verbal_unit += [identifier] + [3]
                elif (input == '-'):
                    # WARNING: negative integer number check
                    input = file_pointer.read(1)
                    in_line_position += 1
                    if (input in string.digits):
                        neg_mark = 1
                        state = state_2
                    else:
                        file_pointer.seek(file_pointer.tell()-2)  #Go back!
                        in_line_position -= 2
                        input = file_pointer.read(1)
                        in_line_position += 1
                        rtrn_verbal_unit += [identifier] + [4]
                elif (input == '*'):
                    rtrn_verbal_unit += [identifier] + [5]
                elif (input == '/'):
                    rtrn_verbal_unit += [identifier] + [6]
                elif (input == ';'):
                    rtrn_verbal_unit += [identifier] + [7]
                elif (input == ','):
                    rtrn_verbal_unit += [identifier] + [8]
                elif (input == '{'):
                    rtrn_verbal_unit += [identifier] + [9]
                elif (input == '}'):
                    rtrn_verbal_unit += [identifier] + [10]
                elif (input == '('):
                    rtrn_verbal_unit += [identifier] + [11]
                elif (input == ')'):
                    rtrn_verbal_unit += [identifier] + [12]
                elif (input == '['):
                    rtrn_verbal_unit += [identifier] + [13]
                elif (input == ']'):
                    rtrn_verbal_unit += [identifier] + [14]
                elif (input == '='):
                    rtrn_verbal_unit += [identifier] + [15]
                else:
                    state = ERROR_state
                    print('ERROR MSG: Unknown character detected: %s' % input)
                    print('Line -> %d:%d' % (line, in_line_position))

        # --- State_1: State_0 -> Letter --- #
        if (state == state_1):
            if (input in string.ascii_letters or input in string.digits):       #Checking if it's a letter or integer number
                letter_count += 1
                if (letter_count > 30):             #Compiler reads only the first 30 letters
                    mark_count = letter_count - 30
                if (mark_count >= 1):
                    identifier = "".join(verbal_unit)
                    rtrn_verbal_unit += [identifier] + [1]
                else:
                    verbal_unit += input
                    state = state_1
            else:
                state = OK_state
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit = [identifier] + [1]

                if (mark_count >= 1):
                    print('WARNING: Word exceeded the 30 character limit!')
                    print('Line -> %d:%d' % (line, in_line_position))

                file_pointer.seek(file_pointer.tell()-1)      #Go back 1 position
                in_line_position -= 1

        # --- State_2: State_0 -> Digit ---- #
        if (state == state_2):
            if (input in string.digits):
                state = state_2
                verbal_unit += input
            else:
                state = OK_state
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [2]
                file_pointer.seek(file_pointer.tell()-1)
                in_line_position -= 1
                # --- Digit check if it's between the limits: --- #
                if (int(identifier) > 32767 or int(identifier) < (-32767)):
                    state = ERROR_state
                    if (int(identifier) > 32767):
                        print('ERROR: Number %d exceeded the 32767 limit!' % int(identifier))
                        print('Line -> %d:%d' % (line, in_line_position))
                    else:
                        print('ERROR: Number %d is under the -32767 limit!' % int(identifier))
                        print('Line -> %d:%d' % (line, in_line_position))

        # --- State_3: State_0 -> '<' symbol ---- #
        if (state == state_3):
            state = OK_state
            input = file_pointer.read(1)
            in_line_position += 1
            if (input == '='):
                verbal_unit = '<='
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [16]
            elif (input == '>'):
                verbal_unit = '<>'
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [17]
            else:
                verbal_unit = '<'
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [18]
                file_pointer.seek(file_pointer.tell()-1)      #Go back!
                in_line_position -= 1

        # --- State_4: State_0 -> '>' symbol ---- #
        if (state == state_4):
            state = OK_state
            input = file_pointer.read(1)
            in_line_position -= 1
            if (input == '='):
                verbal_unit = '>='
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [19]
                #file_pointer.seek(file_pointer.tell() - 1)
                #in_line_position -= 1
            else:
                verbal_unit = '>'
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [20]
                file_pointer.seek(file_pointer.tell()-1)
                in_line_position -= 1

        # --- State_5: State_0 -> ':' symbol ---- #
        if (state == state_5):
            input = file_pointer.read(1)
            in_line_position += 1
            if (input == '='):
                state = OK_state
                verbal_unit = ':='
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [21]
            else:
                state = OK_state
                verbal_unit = ':'
                file_pointer.seek(file_pointer.tell()-1)
                in_line_position -= 1
                identifier = "".join(verbal_unit)
                rtrn_verbal_unit += [identifier] + [22]

        # --- State_6: State_0 -> '/*' symbol ---- #
        if (state == state_6):
            input = file_pointer.read(1)
            in_line_position += 1
            if (input == '*'):
                state = state_7
                input = file_pointer.read(1)
                in_line_position += 1
            # One-line comments '//' #
            elif (input == '/'):
                state = state_7
                input = file_pointer.read(1)
                in_line_position += 1
            else:
                state = ERROR_state
                file_pointer.seek(file_pointer.tell()-1)
                in_line_position -= 1
                print('Syntax Error: Missing "*" in comments.')
                print('Line -> %d:%d' % (line, in_line_position))
            
        # --- State_7: State_0 -> '/*' symbol --- #
        if (state == state_7):
            if (input == '*'):
                state = state_8
            elif (input == ''):
                state = ERROR_state
                print('Syntax Error: Please make sure to close your comments!')
                print('Line -> %d:%d' % (line, in_line_position))
                in_line_position += 1
            elif (input == '\t'):
                in_line_position += 4
            elif (input == '\n'):
                state = state_0
                line += 1
                in_line_position = 0
            else:
                input = file_pointer.read(1)    #EOF checkpoint
                in_line_position += 1
                if (input == ''):
                    state = ERROR_state
                    print('Syntax Error: Please make sure to close your comments!')
                    print('Line -> %d:%d' % (line, in_line_position))
                else:
                    file_pointer.seek(file_pointer.tell()-1)
                    in_line_position -= 1

        # --- State_8: State_0 -> '*/' symbol --- #
        if (state == state_8):
            input = file_pointer.read(1)
            in_line_position += 1
            if (input == '/'):
                state = state_0
            elif (input == '\n'):
                state = state_0
            elif (input == ''):
                state = ERROR_state
                print('Syntax Error: Please make sure to close your comments!')
                print('Line -> %d:%d' % (line, in_line_position))
            elif (input == '*'):
                state = state_8
                file_pointer.seek(file_pointer.tell()-1)
                in_line_position -= 1
            else:
                state = state_7
                file_pointer.seek(file_pointer.tell()-1)
                in_line_position -= 1
        if (state == ERROR_state):
            verbal_unit = '-1'
            rtrn_verbal_unit = ['ERROR'] + [-1]

    fp_position = file_pointer.tell()       #Mark current position
    identifier = "".join(verbal_unit)

    # Checking to see if the ID matches one of the Starlet reserved keywords #
    for i in range (len(res_words)):
        if (identifier == res_words[i][0]):
            rtrn_verbal_unit.pop()
            rtrn_verbal_unit += [res_words[i][1]]
            break

    file_pointer.close()
    return rtrn_verbal_unit[0], rtrn_verbal_unit[1]

def printLex():
    while (1):
        lst = lex()
        vu = lst[0]
        scenario = lst[1]
        print(' (%s, %d)' % (lst[0], lst[1]))

        if (scenario == 62): #EOF
            break
    return
    
#printLex()     # For testing purpsoses #

# -------------------------------------------------------------------------------------------------------- #
#                            --- INTERMEDIATE CODE ASSISTIVE SUBROUTINES ---                               #
#----------------------------------------------------------------------------------------------------------#
global quad_list    # Empty global list of all the quads used by the program
quad_list = []
quad_ID = 1         # Quad number that identifies it

# Subroutine nextQuad(): returns the quad_ID of the next quad #
def nextquad():
    global quad_ID
    return quad_ID

# Subroutine genquad(op, x, y, z): creates the next quad (op, x, y, z) #
def genquad(op, v1, v2, v3):
    global quad_ID
    global quad_list

    list = []
    list = [nextquad()]                 # adding quad number
    list += [op] + [v1] + [v2] + [v3]   # adding arguments

    quad_ID += 1            # next_quad = current_quad + 1
    quad_list += [list]     # adding current list to the list with all the quads used by the program

    return list

# Subroutine newtemp(): creates & returns a temporary variable (T_x) #
def newtemp():
    global T_x
    global tmp_variables_list

    T_x = 1
    tmp_variables_list = []

    list = ['T_']
    list.append(str(T_x))
    tmp_var = "".join(list)
    T_x += 1

    tmp_variables_list += [tmp_var]

    return tmp_var

# Subroutine emptylist(): creates an empty list of quad labels #
def emptylist():
    label_list = []

    return label_list

# Subroutine makelist(x): creates a list of quad labels including only "x" #
def makelist(x):
    current_list = [x]

    return current_list

# Subroutine mergelist(l1, l2): creates a list of quad labels merging the two lists #
def mergelist(list_1, list_2):
    list = []
    list += list_1 + list_2

    return list

# Subroutine backpatch(list, z): searches for quads with void last variable and fills them with the "z" label #
def backpatch(list, z):
    global quad_list

    for i in range(len(list)):
        for j in range(len(quad_list)):
            if (list[i] == quad_list[j][0] and quad_list[j][4] == '_'):
                quad_list[j][4] = z
                #j = len(quad_list)
    return

# -------------------------------------------------------------------------------------------------------- #
#                            --- SYMBOLS MATRIX FUNCTIONS ---                                              #
#----------------------------------------------------------------------------------------------------------#
# --- Triangle: --- #
class Argument():
    def __init__(self):
        self.name  = ''               #The name of the argument identifies it.
        self.type = 'Int'             #Always integers.
        self.parameterization = ''    #RET | REF | CV
        
# --- Rectangle: --- #
class Entity():
    def __init__(self):
        self.name = ''
        self.type = ''
        self.variable = self.Variable()
        self.subprogram = self.Subprogram()
        self.parameter = self.Parameter()
        self.tempVar = self.Temp_Var()

    class Variable:
        def __init__(self):
            self.type = 'Int'
            self.offset = 0       #Distance from the beginning of the stack.
    
    class Subprogram:
        def __init__(self):
            self.type = ''
            self.startingQuad = 0           #Calling nextquad().
            self.framelength = 0
            self.args_list = arguments    #List of arguments.

    class Parameter:
        def __init__(self):
            self.parameterization = ''
            self.offset = 0

    class Temp_Var:
        def __init__(self):
            self.type = 'Int'
            self.offset = 0
# --- Circle: --- #
class Scope():
    def __init__(self):
        self.name = ''
        self.entity_list = entities       #List of entities.
        self.nesting_depth = 0
        self.scope_enclosure = scopes     #Including ALL scopes

arguments = []
arguments = copy.deepcopy(arguments)

# Adding current object to the list: #
def new_argument(object):
    global arguments, entities

    arguments.append(object)       #Adding the object (obj) to my list.
    entities[-1].subprogram.args_list.append(object)

entities = []
entities = copy.deepcopy(entities)

def new_entity(object):
    global arguments, entities, scopes

    scopes[-1].entity_list.append(object)
    entities.append(object)

    arguments = []

scopes = []
scopes = copy.deepcopy(scopes)
first_scope = Scope()               #Initialization of the 1st scope!
scopes.append(first_scope)

first_point = 1 # ? ? ? ?

# Creation of a new scope: #
def new_scope(name):
    global first_scope, entities, scopes, first_point

    first_scope.name = name
    next_scope = Scope()

    if (not first_point):
        next_scope.scope_enclosure.append(first_scope)      #next_scope is included inside the first_scope!

    first_scope = next_scope
    first_scope.entity_list = []
    entities = []                   #Emptying the entities list in order to renew them

    # next_scope = next (downwards) nesting_depth + 1: #
    if (first_scope.scope_enclosure == []):
        first_scope.nesting_depth = 0           #We are at the beginning
    else:
        first_scope.nesting_depth = first_scope.scope_enclosure[-1].nesting_depth + 1   #One deeper
    first_point = 0     #We're back to square one.

def delete_scope():
    global scopes

    if (scopes != []):
        del scopes[-1]  #DELETE last scope

# Calculating our distance in bytes: #
def calculate_offset():
    global scopes

    counter = 0
    if (scopes[-1].entity_list is not []):
        for i in (scopes[-1].entity_list):
            if (i.type == 'VAR' or i.type == 'TEMP' or i.type == 'PARAM' or i.type == 'SUBPR'):
                counter += 1
    #(int) = 4bytes --> START: 3 * 4 = 12
    offset = 12 + (counter * 4)

    return offset

# Calculating the starting quad of the function: #
def calculate_startingQuad():
    global scopes

    for i in scopes[-1].scope_enclosure[-2].entity_list:
        if (i.type == 'SUBPR' and i.name == scopes[-1].scope_enclosure[-1].name):
            i.subprogram.startingQuad = nextquad()

# Calculating the framelength of the function: #
def calculate_frameLength():
    global scopes

    for i in scopes[-1].scope_enclosure[-2].entity_list:
        if (i.type == 'SUBPR' and i.name == scopes[-1].scope_enclosure[-1].name):
            i.subprogram.frameLength = calculate_offset()

# Creating entities of various parameters of functions [func a(in a, inout b)] #
def add_parameters():
    global arguments

    offset = calculate_offset()

    for i in arguments:
        ent = Entity()
        ent.name = i.name
        ent.type = 'PARAM'
        ent.parameter.parameterization = i.parameterization
        ent.parameter.offset = offset
        new_entity(ent)

# Printing the matrix: Scopes, Entities, Arguments #
def print_symbols_matrix():
    global scopes, entities, arguments

    print("--------------------------------------------------------------------------------------------------")
    for s in scopes:
        print("Scope: " + " Name: " + s.name + " Nesting_Depth: " + str(s.nesting_depth))
        print("\tEntities:")
        for e in s.entity_list:
            if (e.type == 'VAR'):
                print("\tEntity: " + " Name: " + e.name + "\t Type: " + e.type + "\t Variable_Type: " + e.variable.type + "\t Offset: " + str(e.variable.offset))
            elif (e.type == 'TEMP'):
                print("\tEntity: " + " Name: " + e.name + "\t Type: " + e.type + "\t Temp_Type: " + e.tempVar.type + "\t Offset: " + str(e.tempVar.offset))
            elif (e.type == 'SUBPR'):
                if (e.subprogram.type == 'Function'):
                    print("\tEntity: " + " Name: " + e.name + "\t Type: " + e.type + "\t Function_Type: " + e.subprogram.type + "\t Starting_Quad: " + str(e.subprogram.startingQuad))
                    print("\t\tArguments:")
                    for a in e.subprogram.args_list:
                        print("\t\tArgument: " + " Name: " + a.name + "\t Type: " + a.type + "\t Parameter_Mode: " + a.parameterization)
            elif (e.type == 'PARAM'):
                print("\tEntity: " + " Name: " + e.name + "\t Type: " + e.type + "\t Mode: " + e.parameter.parameterization + "\t Offset: " + str(e.parameter.offset))
    print("--------------------------------------------------------------------------------------------------")

# ----------------------------------------------------------------------------------------------------------- #
#                                 ---  SYNTAX ANALYST & INTERMEDIATE CODE ---                                 #
# ----------------------------------------------------------------------------------------------------------- #

def syntax_analyst(code):
    # Necessary checkpoint to determine whether our source program is Starlet grammar compliant #
    global token        #verbal unit entity
    global tmp
    global flag
    global doWhileFlag, exitFlag, minOneReturnFlag

    flag = 0
    doWhileFlag = 0
    exitFlag = 0
    minOneReturnFlag = 0

    # Loading 1st token/entity: #
    token = lex()

    # --- STARLET GRAMMAR: --- #
    # <program> ::= program id <block> endprogram #
    def program():      
        global token

        if (token[0] == 'program'):
            token = lex()           #Refill
            if (token[1] == 1):     #Checking to see if after the 1st letter follows another letter or digit
                prog_name = token[0]
                token = lex()
                block(prog_name, 1)
            else:
                print('ERROR: Expected the name of the program instead of "{0}".' .format(token[0]))
                print('Line -> {0}:{1}'.format(line, in_line_position))
                exit(-1)
            if (token[0] == 'endprogram'):
                token = lex()
            else:
                print('ERROR: Expected the keyword "endprogram" instead of "{0}".' .format(token[0]))
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        else:
            print('ERROR: Expected the keyword "program" instead of "{0}".' .format(token[0]))
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)
        return

    # <block> ::= <declare> <subprograms> <statements> #        
    def block(block_name, mainProgBlockFlag):        
        global token

        #token = lex()
        new_scope(block_name)

        if (mainProgBlockFlag != 1):    #Creating entities
            add_parameters()
        
        if (token[0] == 'declare'):
            declarations()
        subprograms()
        genquad('begin_block', block_name, '_', '_')

        if (mainProgBlockFlag != 1):    #Calculating the starting quad of the next quad
            calculate_startingQuad()
        statements()
        if (doWhileFlag != 1 and exitFlag == 1):
            print('ERROR: Keyword "exit" can only be applied inside "do-while" loops.')
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)

        closedBlockFlag = 1
        token = lex()
        if (mainProgBlockFlag == 1):
            genquad('halt', '_', '_', '_')
        else:
            calculate_frameLength()     #After closing the block, we are calculating the framelength
        genquad('end_block', block_name, '_', '_')

        print("Print Symbols-Matrix: ")
        print_symbols_matrix()
        delete_scope()
        print("Last scope is deleted.")

        return

    # <declare> ::= (declare <varlist>;)* #
    def declarations():
        global token

        while (token[0] == 'declare'):
            code.write("int ")
            token = lex()
            varlist()
            if (token[0] == ';'):
                code.write(";\n\t")
                token = lex()
                return
            else:
                print('ERROR: Expected ";" after after the variable "{0}".'.format(token[0]))
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        return

    # <varlist> ::= ε | id ( , id )* #
    def varlist():      
        global token

        if (token[1] == 1):     #identifier (a.k.a. tokenID)
            code.write(token[0])

            #Creating an entity:
            ent = Entity()
            ent.type = 'VAR'
            ent.name = token[0]
            ent.variable.offset = calculate_offset()
            new_entity(ent)

            token = lex()
            while (token[0] == ','):
                code.write(token[0])
                token = lex()
                if (token[1] == 1):
                    code.write(token[0])

                    #Creating an entity (again):
                    ent = Entity()
                    ent.type = 'VAR'
                    ent.name = token[0]
                    ent.variable.offset = calculate_offset()
                    new_entity(ent)       
                                 
                    token = lex()
                else:
                    print('ERROR: Variable was expected before "{0}".'.format(token[0]))
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
        return

    # <subprograms> ::= (<subprogram>)* #
    def subprograms():      
        global token

        while (token[0] == 'function'):
            subprogram()
        return

    # <subprogram> ::= function id <funcbody> endfunction #
    def subprogram():
        global token

        if (token[0] == 'function'):
            token = lex()
            if (token[1] == 1):     # tokenID
                name = token[0]     # Keep the name of the procedure

                #Creating an entity:
                ent = Entity()
                ent.type = 'SUBPR'
                ent.name = token[0]
                ent.subprogram.type = 'Function'
                new_entity(ent)

                token = lex()
                funcbody(name, 1)   # Because it is a function
                if (token[0] == 'endfunction'):
                    token = lex()
                else:
                    print('ERROR: Keyword "endfunction" was expected or you missed a semicolon ";".')
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            else:
                print('ERROR: ID number expected.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        else:
            print('ERROR: Keyword "function" was expected.')
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)
        return

    # <funcbody> ::= <formalpars> <block> #
    def funcbody(block_name, func):     
        global token, minOneReturnFlag

        formalpars()            #same syntax principles as <block>
        block(block_name, -1)   #not a main program block

        #Every function includes at least one return
        if (func == 1):
            if (minOneReturnFlag != 1):
                print('ERROR: Fuction {0} is missing the keyword "return".' .format(block_name))
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
            else:
                minOneReturnFlag = 0
                
        return

    # <formalpars> ::= ( <formalparlist> ) #
    def formalpars():       
        global token

        if (token[0] == '('):
            token = lex()
            if (token[0] == 'in' or token[0] == 'inout' or token[0] == 'inandout'):
                formalparlist()
                if (token[0] == ')'):
                    token = lex()
                    return
                else:
                    print('ERROR: Expected right parenthesis ")" instead of "{0}".'.format(token[0]))
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            elif (token[0] == ')'):
                token = lex()
                return
            else:
                print('ERROR: Expected keywords "in" or "inout" or "inandout" after the comma (",").')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        else:
            print('ERROR: Expected left parenthesis "(" instead of "{0}".'.format(token[0]))
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)
        return

    # <formalparlist> ::= <formalparitem> ( , <formalparitem> )* | ε #
    def formalparlist():        
        global token

        formalparitem()
        while (token[0] == ','):
            token = lex()
            if (token[0] == 'in' or token[0] == 'inout' or token[0] == 'inandout'):
                formalparitem()
            else:
                print('ERROR: Expected keywords "in" or "inout" or "inandout" after the comma (",").')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        return
    
    # <formalparitem> ::= in id | inout id | inandout id #
    def formalparitem():
        global token

        if (token[0] == 'in'):
            token = lex()
            if (token[1] == 1):     #identifier ID
                #Creation of an argument:
                a = Argument()
                a.name = token[0]
                a.parameterization = 'CV'
                new_argument(a)

                token = lex()
                return
            else:
                print('ERROR: Variable name expected after the keyword "in".')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        elif (token[0] == 'inout'):
            token = lex()
            if (token[1] == 1):
                #Creation of an argument (again):
                a = Argument()
                a.name = token[0]
                a.parameterization = 'PAR'
                new_argument(a)

                token = lex()
                return
            else:
                print('ERROR: Variable name expected after the keyword "inout".')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        elif (token[0] == 'inandout'):
            token = lex()
            if (token[1] == 1):
                #Creation of an argument (again):
                a = Argument()
                a.name = token[0]
                a.parameterization = 'REF'
                new_argument(a)

                token = lex()
                return
            else:
                print('ERROR: Variable name expected after the keyword "inandout".')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        return
    
    # <statements> ::= <statement> ( ; <statement> )* #
    def statements():
        global token

        statement()
        while (token[0] == ';'):
            token = lex()
            statement()
        return
    
    # <statement> ::= ε | <assignment-stat> | <if-stat> | <while-stat> | <do-while-stat>
    #                   | <loop-stat> | <exit-stat> | <forcase-stat> | <incase-stat> |
    #                   | <return-stat> | <input-stat> | <print-stat> #
    def statement():
        global token

        if (token[1] == 1):
            assignment_stat()
        elif (token[0] == 'if'):
            if_stat()
        elif (token[0] == 'while'):
            while_stat()
        elif (token[0] == 'dowhile'):
            do_while_stat()
        elif (token[0] == 'loop'):
            loop_stat()
        elif (token[0] == 'exit'):
            exit_stat()
        elif (token[0] == 'forcase'):
            for_case_stat()
        elif (token[0] == 'incase'):
            in_case_stat()
        elif (token[0] == 'return'):
            return_stat()
        elif (token[0] == 'input'):
            input_stat()
        elif (token[0] == 'print'):
            print_stat()
        return
    
    # <assignment-stat> ::= id := <expression> #
    # INTR_CODE: assignment_stat -> id := expression {P1} #
    def assignment_stat():
        global token
        global tmp
        global flag

        id = token[0]

        token = lex()
        if (token[0] == ':='):
            token = lex()
            E_place = expression()
            #{P1}:
            if (flag == 1):                     #whether it is a function
                genquad(':=', tmp, '_', id)
                flag = 0
            else:
                genquad(':=', E_place, '_', id)
        else:
            print('ERROR: Expected ":=" before "{0}".'.format(token[0]))
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)
        return

    # <if-stat> ::= if (<condition>) then <statements> <elsepart> endif #
    # INTR_CODE: if_stat -> if cond then {P1} statements {P2} else_part endif {P3} #
    def if_stat():
        global token

        # There is always an if token, otherwise it won't enter the if_stat() function #
        token = lex()
        if (token[0] == '('):
            token = lex()
            cond = condition()
            if (token[0] == ')'):
                token = lex()
                if (token[0] == 'then'):
                    token = lex()
                    #{P1}:
                    backpatch(cond[0], nextquad())      #cond[0] = TRUE
                    statements()
                    #{P2}:
                    is_list = makelist(nextquad())
                    genquad('JUMP', '_', '_', '_')
                    backpatch(cond[1], nextquad())      #cond[1] = FALSE
                    else_part()
                    if (token[0] == 'endif'):
                        token = lex()
                        #{P3}:
                        backpatch(is_list, nextquad())
                    else:
                        print('ERROR: Expected the keyword "endif" or a questionmark ";".')
                        print('Line -> {0}:{1}' .format(line, in_line_position))
                        exit(-1)
                else:
                    print('ERROR: Expected the keyword "then".')
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            else:
                print('ERROR: Expected right parenthesis ")" instead of "{0}".'.format(token[0]))
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        else:
            print('ERROR: Expected left parenthesis "(" instead of "{0}".'.format(token[0]))
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)

        ifStat_TRUE = cond[0]
        ifStat_FALSE = cond[1]

        return ifStat_TRUE, ifStat_FALSE
        
    # <elsepart> ::= ε | else <statements> #
    def else_part():
        global token

        if (token[0] == 'else'):
            token = lex()
            statements()
        return

    # <while-stat> ::= while (<condition>) <statements> endwhile #
    # INTR_CODE: while_stat -> while ({P1} cond) {P2} statements endwhile {P3}#
    def while_stat():
        global token

        #token = lex()    na to dw to proxwraw askopa
        if (token[0] == 'while'):
            token = lex()
            if (token[0] == '('):
                token = lex()
                #{P1}:
                cond_quad = nextquad()
                cond = condition()
                if (token[0] == ')'):
                    #{P2}:
                    backpatch(cond[0], nextquad())              #cond[0] = TRUE
                    token = lex()
                    statements()
                    if (token[0] == 'endwhile'):
                        token = lex()
                        #{P3}:
                        genquad('JUMP', '_', '_', cond_quad)
                        backpatch(cond[1], nextquad())          #cond[1] = FALSE
                    else:
                        print('ERROR: Expected the keyword "endwhile" instead of "{0}".' .format(token[0]))
                        print('Line -> {0}:{1}' .format(line, in_line_position))
                        exit(-1)
                else:
                    print('ERROR: Expected right parenthesis ")" instead of "{0}" in order to close the while-loop.' .format(token[0]))
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            else:
                print('ERROR: Expected left parenthesis "(" instead of "{0}" in order to open the while-loop.' .format(token[0]))
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)

        whileStat_TRUE = cond[0]
        whileStat_FALSE = cond[1]

        return whileStat_TRUE, whileStat_FALSE

    # <do-while-stat> ::= dowhile <statements> enddowhile (<condition>) #
    # INTR_CODE: do_while_stat -> dowhile {P1} statements enddowhile (cond {P2}) #
    def do_while_stat():
        global token

        if (token[0] == 'dowhile'):
            token = lex()
            #{P1}:
            jumpX = nextquad()              #jumpX variable shows where to jump
            statements()
            if (token[0] == 'enddowhile'):
                token = lex()
                if (token[0] == '('):
                    token = lex()
                    cond = condition()
                    #{P2}:
                    backpatch(cond[0], jumpX)       #cond[0] = TRUE
                    backpatch(cond[1], nextquad())  #cond[0] = FALSE
                    if (token[0] == ')'):
                        token = lex()
                        return
                    else:
                        print('ERROR: Expected right parenthesis ")" instead of "{0}" in order to close the while-loop.'.format(token[0]))
                        print('Line -> {0}:{1}' .format(line, in_line_position))
                        exit(-1)
                else:
                    print('ERROR: Expected left parenthesis "(" instead of "{0}" in order to open the while-loop.'.format(token[0]))
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            else:
                print('ERROR: Expected the keyword "while" instead of "{0}".'.format(token[0]))
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)

        doWhileStat_TRUE = cond[0]
        doWhileStat_FALSE = cond[1]

        return doWhileStat_TRUE, doWhileStat_FALSE

    # <loop-stat> ::= loop <statements> endloop #
    # (?) INTR_CODE: loop_stat -> loop {P1} statements endloop {P2} #
    def loop_stat():
        global token

        #{P1}:
        #jumpX = nextquad()
        #token = lex()
        #statements()

        if (token[0] == 'loop'):
            token = lex()
            #stat = statements()
            if (token[0] == 'endloop'):
                token = lex()
                #{P2}:
                #backpatch(stat[0], jumpX)           #stat[0] = TRUE
                #backpatch(stat[1], nextquad())      #stat[1] = FALSE
            else:
                print('ERROR: OPEN LOOP - Expected the keyword "endloop".')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
            
        #loopStat_TRUE = stat[0]
        #loopStat_FALSE = stat[1]

        return #loopStat_TRUE, loopStat_FALSE
    
    # <exit-stat> ::= exit #
    def exit_stat():
        global token

        token = lex()
        
        return
    
    # <forcase-stat> ::= forcase
    #                       ( when (<condition>) : <statements> )* 
    #                       default: <statements> enddefault
    #                    endforcase #
    # INTR_CODE: for_case_stat -> {P0} forcase 
    #                                       ( when {P1} (cond) : {P2} statements )
    #                                       default: statements enddefault
    #                                   endforcase {P3} #
    def for_case_stat():
        global token

        #{P0}:
        exit_list = emptylist()

        if (token[0] == 'forcase'):
            token = lex()
            while (token[0] == 'when'):
                token = lex()
                if (token[0] == '('):
                    token = lex()
                    #{P1}:
                    cond_quad = nextquad()
                    cond = condition()
                    if (token[0] == ')'):
                        token = lex()
                        if (token[0] == ':'):
                            token = lex()
                            #{P2}:
                            backpatch(cond[0],nextquad())
                            statements()
                            tmp_list = makelist(nextquad())
                            genquad('JUMP', '_', '_', '_')
                            exit_list = mergelist(exit_list, tmp_list)
                            backpatch(exit_list, nextquad())
                        else:
                            print('ERROR: Expected ":" symbol.')
                            print('Line -> {0}:{1}' .format(line, in_line_position))
                            exit(-1)
                    else:
                        print('ERROR: Expected right parenthesis ")".')
                        print('Line -> {0}:{1}' .format(line, in_line_position))
                        exit(-1)
                else:
                    print('ERROR: Expected left parenthesis "(".')
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            if (token[0] == 'default'):
                token = lex()
                if (token[0] == ':'):
                    token = lex()
                    statements()
                    if (token[0] == 'enddefault'):
                        token = lex()
                        #{P3}:
                        backpatch(exit_list, nextquad())
                    else:
                        print('ERROR: Keyword "enddefault" expected.')
                        print('Line -> {0}:{1}' .format(line, in_line_position))
                        exit(-1)
                else:
                    print('ERROR: Expected ":" symbol.')
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            else:
                print('ERROR: Keyword "default" expected.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        return
    
    # <incase-stat> ::= incase
    #                       ( when (<condition>) : <statements> )*
    #                   endincase #
    # INTR_CODE: incase_stat -> incase 
    #                               ( when {P1} cond : {P2} statements )
    #                           endincase {P3} #
    def in_case_stat():
        global token

        if (token[0] == 'incase'):
            token = lex()
            while (token[0] == 'when'):
                token = lex()
                if (token[0] == '('):
                    token = lex()
                    #{P1}:
                    cond_quad = nextquad()
                    cond = condition()
                    if (token[0] == ')'):
                        token = lex()
                        if (token[0] == ':'):
                            #{P2}:
                            backpatch(cond[0], nextquad())      #cond[0] = TRUE
                            token = lex()
                            statements()
                        else:
                            print('ERROR: Expected ":" symbol.')
                            print('Line -> {0}:{1}' .format(line, in_line_position))
                            exit(-1)
                    else:
                        print('ERROR: Expected right parenthesis ")".')
                        print('Line -> {0}:{1}' .format(line, in_line_position))
                        exit(-1)
                else:
                    print('ERROR: Expected left parenthesis "(".')
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            if (token[0] == 'endincase'):
                token = lex()
                #{P3}:
                genquad('JUMP', '_', '_', cond_quad)            
                backpatch(cond[1], nextquad())                  #cond[1] = FALSE
            else:
                print('ERROR: Expected the keyword "endincase".')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)

        inCaseStat_TRUE = cond[0]
        inCaseStat_FALSE = cond[1]

        return inCaseStat_TRUE, inCaseStat_FALSE
    
    # <return-stat> ::= return <expression> #
    # INTR_CODE: return_stat -> return E {P1} #
    def return_stat():
        global token, minOneReturnFlag

        minOneReturnFlag = 1

        #token = lex()
        if (token[0] == 'return'):
            token = lex()
            #{P1}: 
            E_place = expression()
            genquad('retv', E_place, '_', '_')
        return

    # <print-stat> ::= print <expression> #
    # INTR_CODE: print_stat -> print E {P1} #
    def print_stat():
        global token

        if (token[0] == 'print'):
            token = lex()
            #{P1}:
            E_place = expression()
            genquad('out', E_place, '_', '_')    #is out a good name? 
        return

    # <input-stat> ::= input id #
    def input_stat():
        global token

        if (token[0] == 'input'):
            token = lex()
            if (token[1] == 1):
                token = lex()
                id_name = token[0]
                return
            else:
                print('ERROR: Expected the name of the function.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        return

    # <actualpars> ::= ( <actualparlist> ) #
    def actual_pars(is_func, id_name):
        global token
        global tmp

        if (token[0] == '('):
            token = lex()
            if (token[0] == 'in' or token[0] == 'inout' or token[0] == 'inandout'):
                actual_par_list()
                if (token[0] == ')'):
                    token = lex()
                    #If it's a function:
                    if (is_func == 1):
                        w = newtemp()
                        genquad('par', w, 'RET', '_')
                        genquad('call', id_name, '_', '_')
                        tmp = w
                    #If it's a procedure:
                    else:
                        genquad('call', id_name, '_', '_')
                else:
                    print('ERROR: Expected right parenthesis ")".')
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
        return

    # <actualparlist> ::= <actualparitem> ( , <actualparitem> )* | ε #
    def actual_par_list():
        global token

        actual_par_item()
        while (token[0] == ','):
            token = lex()
            actual_par_item()
        return

    # <actual_par_item> ::= in <expression> | inout id | inandout id #
    def actual_par_item():
        global token

        if (token[0] == 'in'):
            token = lex()
            current_expression = expression()
            genquad('par', current_expression, 'CV', '_')
        elif (token[0] == 'inout'):
            token = lex()
            if (token[1] == 1):
                genquad('par', token[0], 'REF', '_')
                token = lex()
            else:
                print('ERROR: Token ID was expected.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        elif (token[0] == 'inandout'):
            token = lex()
            if (token[1] == 1):
                genquad('par', token[0], 'REF', '_')    
                token = lex()
            else:
                print('ERROR: Token ID was expected.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        else:
            print('ERROR: Missing one of the reserved words "in | inout | inandout".')
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)
        return
    
    # <condition> ::= <boolterm> (or <boolterm>)* #
    # INTR_CODE: Cond -> Boolterm1 {P1} (or {P2} Boolterm2 {P3}) #   #!!!na ta simpliroso pantou
    def condition():
        global token

        cond_TRUE = []
        cond_FALSE = []

        bool_term1 = bool_term()
        #{P1}:
        cond_TRUE = bool_term1[0]
        cond_FALSE = bool_term1[1]

        while (token[0] == 'or'):
            token = lex()
            #{P2}:
            backpatch(cond_FALSE, nextquad())
            bool_term2 = bool_term()
            #{P3}:
            cond_TRUE = mergelist(cond_TRUE, bool_term2[0])
            cond_FALSE = bool_term2[1]

        return cond_TRUE, cond_FALSE

    # <boolterm> ::= <boolfactor> (and <boolfactor>)* #
    # INTR_CODE: boolterm -> boolfactor1 {P1} (and {P2} boolfactor2 {P3}) #
    def bool_term():
        global token

        boolterm_TRUE = []
        boolterm_FALSE = []

        bool_factor1 = bool_factor()
        #{P1}:
        boolterm_TRUE = bool_factor1[0]
        boolterm_FALSE = bool_factor1[1]

        while (token[0] == 'and'):
            token = lex()
            #{P2}:
            backpatch(boolterm_TRUE, nextquad())
            bool_factor2 = bool_factor()
            #{P3}:
            boolterm_FALSE = mergelist(boolterm_FALSE, bool_factor2[1])
            boolterm_TRUE = bool_factor2[0]

        return boolterm_TRUE, boolterm_FALSE
    
    # <boolfactor> ::= not [<condition>] | [<condition>] | <expression> <relational-oper> <expression> #
    def bool_factor():
        global token

        boolFactor_TRUE = []
        boolFactor_FALSE = []
        E_place1 = ''
        E_place2 = ''
        relop = ''

        # opposites! #
        # INTR_CODE: boolfactor -> not [condition] {P1} #
        if (token[0] == 'not'):
            token = lex()
            if (token[0] == '['):
                token = lex()
                cond = condition()              #returns 2 lists (TRUE & FALSE)
                if (token[0] == ']'):
                    token = lex()
                    #{P1}:
                    boolFactor_TRUE = cond[1]   #cond[1] = FALSE
                    boolFactor_FALSE = cond[0]  #cond[0] = TRUE
                else:
                    print('ERROR: Expected right square bracket "]" after the condition.')
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            else:
                print('ERROR: Expected left square bracket "[" after the condition.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        # NOT opposites! #
        # INTR_CODE: boolfactor -> [condition] {P1} #
        elif (token[0] == '['):
            token = lex()
            cond = condition()
            if (token[0] == ']'):
                token = lex()
                #{P1}:
                boolFactor_TRUE = cond[0]   #cond[0] = TRUE
                boolFactor_FALSE = cond[1]  #cond[1] = FALSE
            else:
                print('ERROR: Expected right square bracket "]" after the condition.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        # INTR_CODE: boolfactor -> E1_place relop E2_place {P1} #
        else:
            E1_place = expression()
            #print(E1_place)
            relop = relational_oper()
            #print(relop)
            E2_place = expression()
            #{P1}:
            boolFactor_TRUE = makelist(nextquad())
            genquad(relop, E1_place, E2_place, '_')     #needs backpatching!
            boolFactor_FALSE = makelist(nextquad())
            genquad('JUMP', '_', '_', '_')              #needs backpatching!

        return boolFactor_TRUE, boolFactor_FALSE
    
    # <expression> ::= <optional-sign> <term> ( <add-oper> <term> )* #
    # INTR_CODE: expression -> T1 (+- T2 {P1})* {P2} #
    def expression():
        global token

        optional_sign()
        T1_place = term()
        while (token[0] == '+' or token[0] == '-'):
            plus_minus = add_oper()
            T2_place = term()
            #{P1}:
            w = newtemp()
            genquad(plus_minus, T1_place, T2_place, w)
            T1_place = w
        #{P2}:
        E_place = T1_place

        return E_place

    # <term> ::= <factor> (<mul-oper> <factor>)* #
    # INTR_CODE: factor1 (muloper factor2 {P1})* {P2} #
    def term():
        global token

        F1_place = factor()
        while (token[0] == '*' or token[0] == '/'):
            mul_div = mul_oper()
            F2_place = factor()
            #{P1}:
            w = newtemp()
            genquad(mul_div, F1_place, F2_place, w)
            F1_place = w
        #{P2}:
        T_place = F1_place

        return T_place

    # <factor> ::= constant | (<expression>) | id <idtail> #
    def factor():
        global token

        if (token[1] == 2):         #digit = integer -> constant
            factorial = token[0]    #storing the string of the verbal unit
            token = lex()
            return
        elif (token[0] == '('):
            token = lex()
            E_place = expression()
            if (token[0] == ')'):
                factorial = E_place
                token = lex()
                return
            else:
                print('ERROR: Expected right parenthesis ")" after the expression.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        elif (token[1] == 1):       #identifier (ID)
            factorial = token[0]
            token = lex()
            id_tail(factorial)
            return
        else:
            print('ERROR: Expected constant or expression or variable instead of "%s".' % token[0])
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)

        return factorial
    
    # <idtail> ::= ε | <actualpars> #
    def id_tail(id_name):
        global token
        global flag

        if (token[0] == '('):           #<actualpars> token -> "(" open parenthesis symbol
            flag = 1
            actual_pars(1, id_name)     #1 menas it's a function
            return

    # <relational-oper> ::= = | <= | >= | > | < | <> #
    def relational_oper():
        global token

        if (token[0] == '=' or token[0] == '<=' or token[0] == '>=' or token[0] == '>' or token[0] == '<' or token[0] == '<>'):
            relop = token[0]
            token = lex()
        else:
            print('ERROR: Missing: "=" | "<=" | ">=" | ">" | "<" | "<>" !')
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)
        return relop
    
    # <add-oper> ::= + | - #
    def add_oper():
        global token

        if (token[0] == '+' or token[0] == '-'):
            addition_op = token[0]                  #addition_op is for both + & - because subtraction is a negative addition
            token = lex()

        return addition_op

    # <mul-oper> ::= * | / #
    def mul_oper():
        global token

        if (token[0] == '*' or token[0] == '/'):
            multi_op = token[0]
            token = lex()

        return multi_op

    # <optional-sign> ::= ε | <add-oper> #
    def optional_sign():
        global token

        if (token[0] == '+' or token[0] == '-'):    #uses the tokens of <add_oper>
            addition_subtraction = add_oper()
            return

    program()
    print('---------------------------------------------------')
    print('--- ***STARLET PROGRAM COMPILED SUCCESSFULLY*** ---')
    print('---------------------------------------------------')

#syntax_analyst()

# Writing all quads on test.int #
def test_file(test):
    for i in range(len(quad_list)):
        quad = quad_list[i]
        test.write(str(quad[0]))
        test.write(": ")
        test.write(str(quad[1]))
        test.write(" ")
        test.write(str(quad[2]))
        test.write(" ")
        test.write(str(quad[3]))
        test.write(" ")
        test.write(str(quad[4]))
        test.write("\n")

def c_file(code):
    global tmp_variables_list

    if (len(tmp_variables_list) != 0):
        code.write("int ")
    #Temp_X variables
    for i in range(len(tmp_variables_list)):
        code.write(tmp_variables_list[i])
        if (len(tmp_variables_list) == i + 1):
            code.write(";\n\n\t")
        else:
            code.write(",")
    for j in range(len(quad_list)):
        if (quad_list[j][1] == 'begin_block'):
            code.write("L_" + str(j+1) + ":\n\t")
        elif (quad_list[j][1] == ":="):
            code.write("L_" + str(j+1) + ": " + quad_list[j][4] + "=" + quad_list[j][2] + ";\n\t")
        elif (quad_list[j][1] == "+"):
            code.write("L_" + str(j+1) + ": " + quad_list[j][4] + "=" + quad_list[j][2] + "+" + quad_list[j][3] + ";\n\t")
        elif (quad_list[j][1] == "-"):
            code.write("L_" + str(j+1) + ": " + quad_list[j][4] + "=" + quad_list[j][2] + "-" + quad_list[j][3] + ";\n\t")
        elif (quad_list[j][1] == "*"):
            code.write("L_" + str(j+1) + ": " + quad_list[j][4] + "=" + quad_list[j][2] + "*" + quad_list[j][3] + ";\n\t")
        elif (quad_list[j][1] == "/"):
            code.write("L_" + str(j+1) + ": " + quad_list[j][4] + "=" + quad_list[j][2] + "/" + quad_list[j][3] + ";\n\t")
        elif (quad_list[j][1] == "JUMP"):
            code.write("L_" + str(j+1) + ": " + "goto L_" + str(quad_list[j][4]) + ";\n\t")
        elif (quad_list[j][1] == "<"):
            code.write("L_" + str(j+1) + ": " + "if (" + quad_list[j][2] + "<" + quad_list[j][3] + ") goto L_" + str(quad_list[j][4]) + ";\n\t")
        elif (quad_list[j][1] == ">"):
            code.write("L_" + str(j+1) + ": " + "if (" + quad_list[j][2] + ">" + quad_list[j][3] + ") goto L_" + str(quad_list[j][4]) + ";\n\t")
        elif (quad_list[j][1] == ">="):
            code.write("L_" + str(j+1) + ": " + "if (" + quad_list[j][2] + ">=" + quad_list[j][3] + ") goto L_" + str(quad_list[j][4]) + ";\n\t")
        elif (quad_list[j][1] == "<="):
            code.write("L_" + str(j+1) + ": " + "if (" + quad_list[j][2] + "<=" + quad_list[j][3] + ") goto L_" + str(quad_list[j][4]) + ";\n\t")
        elif (quad_list[j][1] == "<>"):
            code.write("L_" + str(j+1) + ": " + "if (" + str(quad_list[j][2]) + "!=" + str(quad_list[j][3]) + ") goto L_" + str(quad_list[j][4]) + ";\n\t")
        elif (quad_list[j][1] == "="):
            code.write("L_" + str(j+1) + ": " + "if (" + quad_list[j][2] + "==" + quad_list[j][3] + ") goto L_" + str(quad_list[j][4]) + ";\n\t")
        #Printing the result of the expression
        elif (quad_list == "out"):
            code.write("L_" + str(j+1) + ": " + "printf(\""+ quad_list[j][2] + "= %d\", " + quad_list[j][2] + ");\n\t")
        elif (quad_list[j][1] == "halt"):
            code.write("L_" + str(j+1) + ": {}\n\t")

def my_files():
    test = open('test.int', 'w')
    c_code = open('c_code', 'w')

    c_code.write("int main () {\n\t")
    syntax_analyst(c_code)
    test_file(test)
    c_file(c_code)
    c_code.write("\n}")
    
    c_code.close()
    test.close()
my_files()

def print_quad_list():
    for i in range(len(quad_list)):
        print(str(quad_list[i][0] + " " + quad_list[i][1] + " " + quad_list[i][2] + " " + quad_list[i][3] + " " + quad_list[i][4]))