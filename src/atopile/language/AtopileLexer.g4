lexer grammar AtopileLexer;

tokens { INDENT, DEDENT }

options {
    superClass=AtopileLexerBase;
}

// keywords
DOT : '.';
OPEN_PAREN : '(' {self.openBrace();};
CLOSE_PAREN : ')' {self.closeBrace();};
OPEN_BRACE : '{' {self.openBrace();};
CLOSE_BRACE : '}' {self.closeBrace();};
OPEN_BRACK : '[' {self.openBrace();};
CLOSE_BRACK : ']' {self.closeBrace();};
CONNECT : '~';

SKIP_
 : ( SPACES | COMMENT | LINE_JOINING ) -> skip
 ;

UNKNOWN_CHAR
 : .
 ;

fragment DIGIT
 : [0-9]
 ;

fragment SPACES
 : [ \t]+
 ;

fragment COMMENT
 : '#' ~[\r\n\f]*
 ;

fragment LINE_JOINING
 : '\\' SPACES? ( '\r'? '\n' | '\r' | '\f')
 ;
