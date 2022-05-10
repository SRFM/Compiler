                                    # --- Project creators --- #
# 1. Name: Serafeim-Ilias Antoniou | A.M.: 2640 | username: cse42640 #
# 2. Name: Sophia Pasoi            | A.M.: 2798 | username: cse42798 #
# Execution Guidelines: #
# In the phase_1 folder you will find the code, plus some testing modules to verify the correct function of the program.
# The programs named "green_X.stl" are meant for the demonstration of our correct output messages.
# The programs named "red_X.stl" are meant for the demonstration of our correct error-messages output. #
# In order to execute the .py file from the command line you'll need to syntax your command this way:
# python3 verbal_syntax_analysts.py green_X.stl or red_X.stl #

import string
import sys      #cmd line argument


# ---  VERBAL ANALYST: --- #
fp_position = 0             #Current file pointer position
line = 1                    #Current line
in_line_position = 1        #Position inside the line

def lex():
    # Time saving: Open file as argument in terminal: #
    try:
        file_pointer = open(sys.argv[1], 'r')
    except IndexError:
        file_pointer = open('source_1.txt', 'r') #Automatic compilation without terminal command

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
    res_words = [['program', 30], ['endprogram', 31], ['declarations', 32], ['if', 33], ['then', 34], ['else', 35], ['endif', 36], ['dowhile', 37], ['enddowhile', 38, ], ['while', 39], ['endwhile', 40], ['loop', 41], ['endloop', 42], ['exit', 43], ['forcase', 44], ['endforcase', 45], ['incase', 46],
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
# ---  SYNTAX ANALYST: --- #
# -------------------------------------------------------------------------------------------------------- #

def syntax_analyst():
# Necessary checkpoint to determine whether our source program identifies as Starlet grammar #
    global token        #verbal unit entity

    # Loading 1st token/entity: #
    token = lex()

    # --- Starlet Grammar: --- #
    # <program> ::= program id <block> endprogram #
    def program():      
        global token

        if (token[0] == 'program'):
            token = lex()           #Refill
            if (token[1] == 1):     #Checking to see if after the 1st letter follows another letter or digit
                token = lex()
                block()
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
    def block():        
        global token

        declare()
        subprograms()
        statements()

        return

    # <declare> ::= (declare <varlist>;)* #
    def declare():
        global token

        while (token[0] == 'declare'):
            token = lex()
            varlist()
            if (token[0] == ';'):
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
            token = lex()
            while (token[0] == ','):
                token = lex()
                if (token[1] == 1):
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
            if (token[1] == 1):     #tokenID
                token = lex()
                funcbody()
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
    def funcbody():     
        global token

        formalpars()       #same syntax principles as <block>
        block()

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
                print('ERROR: Expected keywords "in" or "inout" or "inandout" after the comma (",").'.format(token[0]))
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
            if (token[1] == 1):
                token = lex()
                return
            else:
                print('ERROR: Variable name expected after the keyword "in".')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        elif (token[0] == 'inout'):
            token = lex()
            if (token[1] == 1):
                token = lex()
                return
            else:
                print('ERROR: Variable name expected after the keyword "inout".')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        elif (token[0] == 'inandout'):
            token = lex()
            if (token[1] == 1):
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
    def assignment_stat():
        global token

        token = lex()
        if (token[0] == ':='):
            token = lex()
            expression()
            return
        else:
            print('ERROR: Expected ":=" before "{0}".'.format(token[0]))
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)

    # <if-stat> ::= if (<condition>) then <statements> <elsepart> endif #
    def if_stat():
        global token

        # There is always an if token, otherwise it won't enter the function #
        token = lex()
        if (token[0] == '('):
            token = lex()
            condition()
            if (token[0] == ')'):
                token = lex()
                if (token[0] == 'then'):
                    token = lex()
                    statements()
                    else_part()
                    if (token[0] == 'endif'):
                        token = lex()
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
        return
        
    # <elsepart> ::= ε | else <statements> #
    def else_part():
        global token

        if (token[0] == 'else'):
            token = lex()
            statements()
        return

    # <while-stat> ::= while (<condition>) <statements> <endwhile> #
    def while_stat():
        global token

        #token = lex()    na to dw to proxwraw askopa
        if (token[0] == 'while'):
            token = lex()
            if (token[0] == '('):
                token = lex()
                condition()
                if (token[0] == ')'):
                    token = lex()
                    statements()
                    if (token[0] == 'endwhile'):
                        token = lex()
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
        return

    # <do-while-stat> ::= dowhile <statements> enddowhile (<condition>) #
    def do_while_stat():
        global token

        if (token[0] == 'dowhile'):
            token = lex()
            statements()
            if (token[0] == 'enddowhile'):
                token = lex()
                if (token[0] == '('):
                    token = lex()
                    condition()
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
                print('ERROR: Expected the keyword "enddowhile" instead of "{0}".'.format(token[0]))
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        return

    # <loop-stat> ::= loop <statements> endloop #
    def loop_stat():
        global token

        if (token[0] == 'loop'):
            token = lex()
            statements()
            if (token[0] == 'endloop'):
                token = lex()
            else:
                print('ERROR: OPEN LOOP - Expected the keyword "endloop".')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        return
        
    
    # <exit-stat> ::= exit #
    def exit_stat():
        global token

        if (token[0] == 'exit'):
            token = lex()
        
        return
    
    # <forcase-stat> ::= forcase
    #                       ( when (<condtion>) : <statements> )* 
    #                       default: <statements> enddefault
    #                    endforcase #
    def for_case_stat():
        global token

        if (token[0] == 'forcase'):
            token = lex()
            while (token[0] == 'when'):
                token = lex()
                if (token[0] == '('):
                    token = lex()
                    condition()
                    if (token[0] == ')'):
                        token = lex()
                        if (token[0] == ':'):
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
            if (token[0] == 'default'):
                token = lex()
                if (token[0] == ':'):
                    token = lex()
                    statements()
                    if (token[0] == 'enddefault'):
                        token = lex()
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
    #                       ( when <condition> : <statements> )*
    #                   endincase #
    def in_case_stat():
        global token

        if (token[0] == 'incase'):
            token = lex()
            while (token[0] == 'when'):
                token = lex()
                if (token[0] == '('):
                    token = lex()
                    condition()
                    if (token[0] == ')'):
                        token = lex()
                        if (token[0] == ':'):
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
                return
            else:
                print('ERROR: Expected the keyword "endincase".')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        return
    
    # <return-stat> ::= return <expression> #
    def return_stat():
        global token

        if (token[0] == 'return'):
            token = lex()
            expression()
        return

    # <print-stat> ::= print <expression> #
    def print_stat():
        global token

        if (token[0] == 'print'):
            token = lex()
            expression()     
        return

    # <input-stat> ::= input id #
    def input_stat():
        global token

        if (token[0] == 'input'):
            token = lex()
            if (token[1] == 1):
                token = lex()
                return
            else:
                print('ERROR: Expected the name of the function.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        return

    # <actualpars> ::= ( <actualparlist> ) #
    def actual_pars():
        global token

        if (token[0] == '('):
            token = lex()
            if (token[0] == 'in' or token[0] == 'inout' or token[0] == 'inandout'):
                actual_par_list()
                if (token[0] == ')'):
                    token = lex()
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
            expression()
        elif (token[0] == 'inout'):
            token = lex()
            if (token[1] == 1):
                token = lex()
            else:
                print('ERROR: Token ID was expected.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        elif (token[0] == 'inandout'):
            token = lex()
            if (token[1] == 1):
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
    def condition():
        global token

        bool_term()
        while (token[0] == 'or'):
            token = lex()
            bool_term()
        return

    # <boolterm> ::= <boolfactor> (and <boolfactor>)* #
    def bool_term():
        global token

        bool_factor()
        while (token[0] == 'and'):
            token = lex()
            bool_factor()
        return
    
    # <boolfactor> ::= not [<condition>] | [<condition>] | 
    #                      <expression> <relational-oper> <expression> #
    def bool_factor():
        global token

        if (token[0] == 'not'):
            token = lex()
            if (token[0] == '['):
                token = lex()
                condition()
                if (token[0] == ']'):
                    token = lex()
                    return
                else:
                    print('ERROR: Expected right square bracket "]" after the condition.')
                    print('Line -> {0}:{1}' .format(line, in_line_position))
                    exit(-1)
            else:
                print('ERROR: Expected left square bracket "[" after the condition.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        elif (token[0] == '['):
            token = lex()
            condition()
            if (token[0] == ']'):
                token = lex()
                return
            else:
                print('ERROR: Expected right square bracket "]" after the condition.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        else:
            expression()
            relational_oper()
            expression()
        return
    
    # <expression> ::= <optional-sign> <term> ( <add-oper> <term> )* #
    def expression():
        global token

        optional_sign()
        term()
        while (token[0] == '+' or token[0] == '-'):
            add_oper()
            term()
        return

    # <term> ::= <factor> (<mul-oper> <factor>)* #
    def term():
        global token

        factor()
        while (token[0] == '*' or token[0] == '/'):
            mul_oper()
            factor()
        return

    # <factor> ::= constant | (<expression>) | id <idtail> #
    def factor():
        global token

        if (token[1] == 2):     #digit = integer -> constant
            token = lex()
            return
        elif (token[0] == '('):
            token = lex()
            expression()
            if (token[0] == ')'):
                token = lex()
                return
            else:
                print('ERROR: Expected right parenthesis ")" after the expression.')
                print('Line -> {0}:{1}' .format(line, in_line_position))
                exit(-1)
        elif (token[1] == 1):   #identifier (ID)
            token = lex()
            id_tail()
            return
        else:
            print('ERROR: Expected constant or expression or variable instead of "%s".' % token[0])
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)
        return
    
    # <idtail> ::= ε | <actualpars> #
    def id_tail():
        global token

        if (token[0] == '('):   #<actualpars> token -> "(" open parenthesis symbol
            actual_pars()
            return

    # <relational-oper> ::= = | <= | >= | > | < | <> #
    def relational_oper():
        global token

        if (token[0] == '='):
            token = lex()
        elif (token[0] == '<='):
            token = lex()
        elif (token[0] == '>='):
            token = lex()
        elif (token[0] == '>'):
            token = lex()
        elif (token[0] == '<'):
            token = lex()
        elif (token[0] == '<>'):
            token = lex()
        else:
            print('ERROR: Missing: "=" | "<=" | ">=" | ">" | "<" | "<>" !')
            print('Line -> {0}:{1}' .format(line, in_line_position))
            exit(-1)
        return
    
    # <add-oper> ::= + | - #
    def add_oper():
        global token

        if (token[0] == '+'):
            token = lex()
        elif (token[0] == '-'):
            token = lex()
        return

    # <mul-oper> ::= * | / #
    def mul_oper():
        global token

        if (token[0] == '*'):
            token = lex()
        elif (token[0] == '/'):
            token = lex()
        return

    # <optional-sign> ::= ε | <add-oper> #
    def optional_sign():
        global token

        if (token[0] == '+' or token[0] == '-'):    #uses the tokens of <add_oper>
            add_oper()
            return


    program()
    print('---------------------------------------------')
    print('--- STARLET PROGRAM COMPILED SUCCESSFULLY ---')
    print('---------------------------------------------')

syntax_analyst()