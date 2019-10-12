# Dot Programming Language Interpreter
import re
import shlex

class Lexer:

    def __init__(self, source_code):
        self.source_code = source_code

    def tokenize(self):
        tokens = []
        source_code = shlex.split(self.source_code, posix=False)
        source_index = 0

        # Loop through each word in code to generate tokens
        while source_index < len(source_code):
            word = source_code[source_index]

            # This recognizes a variable and creates a token for it
            if word == "var": 
                tokens.append(["VAR_DECLARATION", word])
                source_index += 1

                while word[len(word) - 1] != ";":
                    word = source_code[source_index]

                    # This recognizes a string and creates a string token for it
                    if word[0] == '"' and word[len(word) - 1] == '"':
                        if word[len(word) - 1] == ";":
                            tokens.append(['STRING', word[0:len(word) - 1]])
                        else:
                            tokens.append(['STRING', word])

                    # This recognizes a word and creates an identifier token for it
                    elif re.match('[a-z]', word) or re.match('[A-Z]', word):
                        if word[len(word) - 1] == ";":
                            tokens.append(['IDENTIFIER', word[0:len(word) - 1]])
                        else:
                            tokens.append(['IDENTIFIER', word])

                    # This recognizes an integer and creates an integer token for it
                    elif re.match('[0-9]', word):
                        if word[len(word) - 1] == ";":
                            tokens.append(['INTEGER', word[0:len(word) - 1]])
                        else:
                            tokens.append(['INTEGER', word])

                    # This recognizes operators and creates an operator token for it
                    elif word in "=/*=-+":
                        tokens.append(['OPERATOR', word])

                    source_index += 1

            # --- #

            # This recognizes a print statement and creates a token for it
            if word == "print":
                tokens.append(["PRINT", word])
                source_index += 1

                while word[len(word) - 1] != ";":
                    word = source_code[source_index]

                    # This recognises a variable and creates an identifier token for it
                    if re.match('[a-z]', word) or re.match('[A-Z]', word):
                        if word[len(word) - 1] == ";":
                            tokens.append(['VAR_NAME', word[0:len(word) - 1]])
                        else:
                            tokens.append(['VAR_NAME', word])

                    source_index += 1

            # --- #

            # If a STATEMENT_END (;) is found at the last character in a word,
            # Add a STATEMENT_END token
            if word[len(word) - 1] == ";":
                tokens.append(['STATEMENT_END', ';'])

        return tokens

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.transpiled_code = ""

    def parse(self):
        while self.token_index < len(self.tokens):
            
            # Holds the type of token e.g. IDENTIFIER
            token_type = self.tokens[self.token_index][0]
            # Holds the value of a token e.g. var
            token_value = self.tokens[self.token_index][1]

            # This will trigger when a variable declaration is found
            if token_type == "VAR_DECLARATION" and token_value == "var":
                self.parse_variable_declaration(self.tokens[self.token_index:len(self.tokens)])

            elif token_type == "PRINT" and token_value == "print":
                self.parse_print(self.tokens[self.token_index:len(self.tokens)])

            self.token_index += 1

        exec(self.transpiled_code)

    def parse_variable_declaration(self, token_stream):
        tokens_checked = 0

        name = ""
        operator = ""
        value = ""

        for token in range(0, len(token_stream)):
            # Holds the type of token e.g. IDENTIFIER
            token_type = token_stream[tokens_checked][0]
            # Holds the value of a token e.g. va
            token_value = token_stream[tokens_checked][1]

            # If the statement end is found, break out of the loop
            if token == 4 and token_type == "STATEMENT_END":
                break

            # This will get the variable name
            elif token == 1 and token_type == "IDENTIFIER":
               name = token_value
            # This will perform error validation for invalid names
            elif token == 1 and token_type != "IDENTIFIER":
                print("ERROR: Invalid variable name '" + token_value + "'")
                quit()

            # This will get the variable assignment operator e.g. =
            elif token == 2 and token_type == "OPERATOR":
                operator = token_value
            # This will perform error validation for invalid operators
            elif token == 2 and token_type != "OPERATOR":
                print("ERROR: Assignment Operator is missing or invalid")
                quit()

            # This will get the variable value assigned
            elif token == 3 and  token_type in ['STRING', 'INTEGER', 'IDENTIFIER']:
                value = token_value
            # This will perform error validation for invalid assignment values
            elif token == 3 and token_type not in ['STRING', 'INTEGER', 'IDENTIFIER']:
                print("Invalid variable assignment value: " + token_value)
                quit()

            tokens_checked += 1

        self.transpiled_code += Transpile().variable_object(name, operator, value)

        self.token_index += tokens_checked

    def parse_print(self, token_stream):
        tokens_checked = 0

        variable = ""

        for token in range(0, len(token_stream)):
            # Holds the type of token e.g. IDENTIFIER
            token_type = token_stream[tokens_checked][0]
            # Holds the value of a token e.g. va
            token_value = token_stream[tokens_checked][1]

            # If the statement end is found, break out of the loop
            if token == 4 and token_type == "STATEMENT_END":
                break

            # This will get the variable name
            elif token == 1 and token_type == "VAR_NAME":
                variable = token_value
            # This will perform error validation for invalid variable names
            elif token == 1 and token_type != "VAR_NAME":
                print("Invalid VAR_NAME: " + token_value)
                quit()

            tokens_checked += 1

        self.transpiled_code += Transpile().print_func(variable)

        self.token_index += 1

class Transpile:
    # Converts Dot into Python
    def __init__(self):
        self.exec_string = ""

    def variable_object(self, name, operator, value):
        self.exec_string += f'{name} {operator} {value}\n'
        return self.exec_string

    def print_func(self, var_name):
        self.exec_string += f'print({var_name})\n'
        return self.exec_string
