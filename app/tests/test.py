from main import Lexer, Parser

def main():
    with open('app\\tests\\test.do', 'r') as f:
        content = f.read()
    
    tokens = Lexer(content).tokenize()
    Parser(tokens).parse()

if __name__ == '__main__':
    main()
