# Generated from AtopileParser.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

if "." in __name__:
    from .AtopileParserBase import AtopileParserBase
else:
    from AtopileParserBase import AtopileParserBase

def serializedATN():
    return [
        4,1,73,199,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,1,0,1,0,5,0,51,8,0,10,0,12,0,
        54,9,0,1,0,1,0,1,1,1,1,3,1,60,8,1,1,2,1,2,1,2,5,2,65,8,2,10,2,12,
        2,68,9,2,1,2,3,2,71,8,2,1,2,1,2,1,3,1,3,1,3,1,3,3,3,79,8,3,1,4,1,
        4,1,5,1,5,1,5,1,5,4,5,87,8,5,11,5,12,5,88,1,5,1,5,3,5,93,8,5,1,6,
        1,6,1,6,1,6,1,6,1,6,5,6,101,8,6,10,6,12,6,104,9,6,3,6,106,8,6,1,
        6,1,6,1,6,1,7,1,7,1,8,1,8,1,8,1,8,5,8,117,8,8,10,8,12,8,120,9,8,
        1,8,1,8,1,8,1,9,1,9,1,9,3,9,128,8,9,1,9,1,9,1,9,1,9,1,9,3,9,135,
        8,9,1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,12,1,12,1,12,5,12,
        148,8,12,10,12,12,12,151,9,12,1,13,1,13,1,13,1,13,3,13,157,8,13,
        1,13,1,13,3,13,161,8,13,1,13,1,13,3,13,165,8,13,1,14,1,14,1,14,1,
        15,1,15,3,15,172,8,15,1,16,1,16,1,16,4,16,177,8,16,11,16,12,16,178,
        1,17,1,17,1,17,1,17,3,17,185,8,17,1,18,1,18,1,19,1,19,1,20,1,20,
        1,21,1,21,1,22,1,22,1,23,1,23,1,23,0,0,24,0,2,4,6,8,10,12,14,16,
        18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,0,2,1,0,7,8,1,0,13,
        14,199,0,52,1,0,0,0,2,59,1,0,0,0,4,61,1,0,0,0,6,78,1,0,0,0,8,80,
        1,0,0,0,10,92,1,0,0,0,12,94,1,0,0,0,14,110,1,0,0,0,16,112,1,0,0,
        0,18,134,1,0,0,0,20,136,1,0,0,0,22,140,1,0,0,0,24,144,1,0,0,0,26,
        152,1,0,0,0,28,166,1,0,0,0,30,171,1,0,0,0,32,173,1,0,0,0,34,184,
        1,0,0,0,36,186,1,0,0,0,38,188,1,0,0,0,40,190,1,0,0,0,42,192,1,0,
        0,0,44,194,1,0,0,0,46,196,1,0,0,0,48,51,5,15,0,0,49,51,3,2,1,0,50,
        48,1,0,0,0,50,49,1,0,0,0,51,54,1,0,0,0,52,50,1,0,0,0,52,53,1,0,0,
        0,53,55,1,0,0,0,54,52,1,0,0,0,55,56,5,0,0,1,56,1,1,0,0,0,57,60,3,
        4,2,0,58,60,3,8,4,0,59,57,1,0,0,0,59,58,1,0,0,0,60,3,1,0,0,0,61,
        66,3,6,3,0,62,63,5,32,0,0,63,65,3,6,3,0,64,62,1,0,0,0,65,68,1,0,
        0,0,66,64,1,0,0,0,66,67,1,0,0,0,67,70,1,0,0,0,68,66,1,0,0,0,69,71,
        5,32,0,0,70,69,1,0,0,0,70,71,1,0,0,0,71,72,1,0,0,0,72,73,5,15,0,
        0,73,5,1,0,0,0,74,79,3,16,8,0,75,79,3,18,9,0,76,79,3,20,10,0,77,
        79,3,22,11,0,78,74,1,0,0,0,78,75,1,0,0,0,78,76,1,0,0,0,78,77,1,0,
        0,0,79,7,1,0,0,0,80,81,3,12,6,0,81,9,1,0,0,0,82,93,3,4,2,0,83,84,
        5,15,0,0,84,86,5,1,0,0,85,87,3,2,1,0,86,85,1,0,0,0,87,88,1,0,0,0,
        88,86,1,0,0,0,88,89,1,0,0,0,89,90,1,0,0,0,90,91,5,2,0,0,91,93,1,
        0,0,0,92,82,1,0,0,0,92,83,1,0,0,0,93,11,1,0,0,0,94,95,3,14,7,0,95,
        105,3,36,18,0,96,97,5,11,0,0,97,102,3,30,15,0,98,99,5,30,0,0,99,
        101,3,30,15,0,100,98,1,0,0,0,101,104,1,0,0,0,102,100,1,0,0,0,102,
        103,1,0,0,0,103,106,1,0,0,0,104,102,1,0,0,0,105,96,1,0,0,0,105,106,
        1,0,0,0,106,107,1,0,0,0,107,108,5,31,0,0,108,109,3,10,5,0,109,13,
        1,0,0,0,110,111,7,0,0,0,111,15,1,0,0,0,112,113,5,12,0,0,113,118,
        3,30,15,0,114,115,5,30,0,0,115,117,3,30,15,0,116,114,1,0,0,0,117,
        120,1,0,0,0,118,116,1,0,0,0,118,119,1,0,0,0,119,121,1,0,0,0,120,
        118,1,0,0,0,121,122,5,11,0,0,122,123,3,38,19,0,123,17,1,0,0,0,124,
        127,3,24,12,0,125,126,5,31,0,0,126,128,3,30,15,0,127,125,1,0,0,0,
        127,128,1,0,0,0,128,129,1,0,0,0,129,130,5,34,0,0,130,131,3,28,14,
        0,131,135,1,0,0,0,132,135,3,24,12,0,133,135,3,34,17,0,134,124,1,
        0,0,0,134,132,1,0,0,0,134,133,1,0,0,0,135,19,1,0,0,0,136,137,3,24,
        12,0,137,138,5,58,0,0,138,139,3,30,15,0,139,21,1,0,0,0,140,141,3,
        24,12,0,141,142,5,47,0,0,142,143,3,24,12,0,143,23,1,0,0,0,144,149,
        3,26,13,0,145,146,5,30,0,0,146,148,3,26,13,0,147,145,1,0,0,0,148,
        151,1,0,0,0,149,147,1,0,0,0,149,150,1,0,0,0,150,25,1,0,0,0,151,149,
        1,0,0,0,152,160,3,36,18,0,153,156,5,35,0,0,154,157,3,38,19,0,155,
        157,3,44,22,0,156,154,1,0,0,0,156,155,1,0,0,0,157,158,1,0,0,0,158,
        159,5,36,0,0,159,161,1,0,0,0,160,153,1,0,0,0,160,161,1,0,0,0,161,
        164,1,0,0,0,162,163,5,25,0,0,163,165,3,26,13,0,164,162,1,0,0,0,164,
        165,1,0,0,0,165,27,1,0,0,0,166,167,5,10,0,0,167,168,3,30,15,0,168,
        29,1,0,0,0,169,172,3,32,16,0,170,172,3,36,18,0,171,169,1,0,0,0,171,
        170,1,0,0,0,172,31,1,0,0,0,173,176,3,36,18,0,174,175,5,25,0,0,175,
        177,3,36,18,0,176,174,1,0,0,0,177,178,1,0,0,0,178,176,1,0,0,0,178,
        179,1,0,0,0,179,33,1,0,0,0,180,185,3,38,19,0,181,185,3,42,21,0,182,
        185,3,40,20,0,183,185,3,46,23,0,184,180,1,0,0,0,184,181,1,0,0,0,
        184,182,1,0,0,0,184,183,1,0,0,0,185,35,1,0,0,0,186,187,5,16,0,0,
        187,37,1,0,0,0,188,189,5,3,0,0,189,39,1,0,0,0,190,191,5,3,0,0,191,
        41,1,0,0,0,192,193,5,3,0,0,193,43,1,0,0,0,194,195,5,5,0,0,195,45,
        1,0,0,0,196,197,7,1,0,0,197,47,1,0,0,0,20,50,52,59,66,70,78,88,92,
        102,105,118,127,134,149,156,160,164,171,178,184
    ]

class AtopileParser ( AtopileParserBase ):

    grammarFileName = "AtopileParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'block'", "'node'", 
                     "'with'", "'new'", "'from'", "'import'", "'True'", 
                     "'False'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'.'", "'...'", "'*'", "'('", 
                     "')'", "','", "':'", "';'", "'**'", "'='", "'['", "']'", 
                     "'|'", "'^'", "'&'", "'<<'", "'>>'", "'+'", "'-'", 
                     "'/'", "'%'", "'//'", "'~'", "'{'", "'}'", "'<'", "'>'", 
                     "'=='", "'>='", "'<='", "'<>'", "'!='", "'@'", "'->'", 
                     "'+='", "'-='", "'*='", "'@='", "'/='", "'%='", "'&='", 
                     "'|='", "'^='", "'<<='", "'>>='", "'**='", "'//='" ]

    symbolicNames = [ "<INVALID>", "INDENT", "DEDENT", "STRING", "PHYSICAL", 
                      "NUMBER", "INTEGER", "BLOCK", "NODE", "WITH", "NEW", 
                      "FROM", "IMPORT", "TRUE", "FALSE", "NEWLINE", "NAME", 
                      "STRING_LITERAL", "BYTES_LITERAL", "DECIMAL_INTEGER", 
                      "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", "FLOAT_NUMBER", 
                      "IMAG_NUMBER", "DOT", "ELLIPSIS", "STAR", "OPEN_PAREN", 
                      "CLOSE_PAREN", "COMMA", "COLON", "SEMI_COLON", "POWER", 
                      "ASSIGN", "OPEN_BRACK", "CLOSE_BRACK", "OR_OP", "XOR", 
                      "AND_OP", "LEFT_SHIFT", "RIGHT_SHIFT", "ADD", "MINUS", 
                      "DIV", "MOD", "IDIV", "NOT_OP", "OPEN_BRACE", "CLOSE_BRACE", 
                      "LESS_THAN", "GREATER_THAN", "EQUALS", "GT_EQ", "LT_EQ", 
                      "NOT_EQ_1", "NOT_EQ_2", "AT", "ARROW", "ADD_ASSIGN", 
                      "SUB_ASSIGN", "MULT_ASSIGN", "AT_ASSIGN", "DIV_ASSIGN", 
                      "MOD_ASSIGN", "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN", 
                      "LEFT_SHIFT_ASSIGN", "RIGHT_SHIFT_ASSIGN", "POWER_ASSIGN", 
                      "IDIV_ASSIGN", "SKIP_", "UNKNOWN_CHAR" ]

    RULE_file_input = 0
    RULE_stmt = 1
    RULE_simple_stmts = 2
    RULE_simple_stmt = 3
    RULE_compound_stmt = 4
    RULE_block = 5
    RULE_class_def = 6
    RULE_class_type = 7
    RULE_import_stmt = 8
    RULE_assign_stmt = 9
    RULE_setas_stmt = 10
    RULE_connect_stmt = 11
    RULE_refs = 12
    RULE_single_ref = 13
    RULE_instantiation = 14
    RULE_class_ref = 15
    RULE_attr = 16
    RULE_value = 17
    RULE_name = 18
    RULE_string = 19
    RULE_physical = 20
    RULE_number = 21
    RULE_totally_an_integer = 22
    RULE_boolean_ = 23

    ruleNames =  [ "file_input", "stmt", "simple_stmts", "simple_stmt", 
                   "compound_stmt", "block", "class_def", "class_type", 
                   "import_stmt", "assign_stmt", "setas_stmt", "connect_stmt", 
                   "refs", "single_ref", "instantiation", "class_ref", "attr", 
                   "value", "name", "string", "physical", "number", "totally_an_integer", 
                   "boolean_" ]

    EOF = Token.EOF
    INDENT=1
    DEDENT=2
    STRING=3
    PHYSICAL=4
    NUMBER=5
    INTEGER=6
    BLOCK=7
    NODE=8
    WITH=9
    NEW=10
    FROM=11
    IMPORT=12
    TRUE=13
    FALSE=14
    NEWLINE=15
    NAME=16
    STRING_LITERAL=17
    BYTES_LITERAL=18
    DECIMAL_INTEGER=19
    OCT_INTEGER=20
    HEX_INTEGER=21
    BIN_INTEGER=22
    FLOAT_NUMBER=23
    IMAG_NUMBER=24
    DOT=25
    ELLIPSIS=26
    STAR=27
    OPEN_PAREN=28
    CLOSE_PAREN=29
    COMMA=30
    COLON=31
    SEMI_COLON=32
    POWER=33
    ASSIGN=34
    OPEN_BRACK=35
    CLOSE_BRACK=36
    OR_OP=37
    XOR=38
    AND_OP=39
    LEFT_SHIFT=40
    RIGHT_SHIFT=41
    ADD=42
    MINUS=43
    DIV=44
    MOD=45
    IDIV=46
    NOT_OP=47
    OPEN_BRACE=48
    CLOSE_BRACE=49
    LESS_THAN=50
    GREATER_THAN=51
    EQUALS=52
    GT_EQ=53
    LT_EQ=54
    NOT_EQ_1=55
    NOT_EQ_2=56
    AT=57
    ARROW=58
    ADD_ASSIGN=59
    SUB_ASSIGN=60
    MULT_ASSIGN=61
    AT_ASSIGN=62
    DIV_ASSIGN=63
    MOD_ASSIGN=64
    AND_ASSIGN=65
    OR_ASSIGN=66
    XOR_ASSIGN=67
    LEFT_SHIFT_ASSIGN=68
    RIGHT_SHIFT_ASSIGN=69
    POWER_ASSIGN=70
    IDIV_ASSIGN=71
    SKIP_=72
    UNKNOWN_CHAR=73

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class File_inputContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(AtopileParser.EOF, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(AtopileParser.NEWLINE)
            else:
                return self.getToken(AtopileParser.NEWLINE, i)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.StmtContext)
            else:
                return self.getTypedRuleContext(AtopileParser.StmtContext,i)


        def getRuleIndex(self):
            return AtopileParser.RULE_file_input

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFile_input" ):
                listener.enterFile_input(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFile_input" ):
                listener.exitFile_input(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFile_input" ):
                return visitor.visitFile_input(self)
            else:
                return visitor.visitChildren(self)




    def file_input(self):

        localctx = AtopileParser.File_inputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_file_input)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 127368) != 0):
                self.state = 50
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [15]:
                    self.state = 48
                    self.match(AtopileParser.NEWLINE)
                    pass
                elif token in [3, 7, 8, 12, 13, 14, 16]:
                    self.state = 49
                    self.stmt()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 54
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 55
            self.match(AtopileParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_stmts(self):
            return self.getTypedRuleContext(AtopileParser.Simple_stmtsContext,0)


        def compound_stmt(self):
            return self.getTypedRuleContext(AtopileParser.Compound_stmtContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = AtopileParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmt)
        try:
            self.state = 59
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3, 12, 13, 14, 16]:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.simple_stmts()
                pass
            elif token in [7, 8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 58
                self.compound_stmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Simple_stmtsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.Simple_stmtContext)
            else:
                return self.getTypedRuleContext(AtopileParser.Simple_stmtContext,i)


        def NEWLINE(self):
            return self.getToken(AtopileParser.NEWLINE, 0)

        def SEMI_COLON(self, i:int=None):
            if i is None:
                return self.getTokens(AtopileParser.SEMI_COLON)
            else:
                return self.getToken(AtopileParser.SEMI_COLON, i)

        def getRuleIndex(self):
            return AtopileParser.RULE_simple_stmts

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimple_stmts" ):
                listener.enterSimple_stmts(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimple_stmts" ):
                listener.exitSimple_stmts(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimple_stmts" ):
                return visitor.visitSimple_stmts(self)
            else:
                return visitor.visitChildren(self)




    def simple_stmts(self):

        localctx = AtopileParser.Simple_stmtsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_simple_stmts)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.simple_stmt()
            self.state = 66
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 62
                    self.match(AtopileParser.SEMI_COLON)
                    self.state = 63
                    self.simple_stmt() 
                self.state = 68
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

            self.state = 70
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==32:
                self.state = 69
                self.match(AtopileParser.SEMI_COLON)


            self.state = 72
            self.match(AtopileParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Simple_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_stmt(self):
            return self.getTypedRuleContext(AtopileParser.Import_stmtContext,0)


        def assign_stmt(self):
            return self.getTypedRuleContext(AtopileParser.Assign_stmtContext,0)


        def setas_stmt(self):
            return self.getTypedRuleContext(AtopileParser.Setas_stmtContext,0)


        def connect_stmt(self):
            return self.getTypedRuleContext(AtopileParser.Connect_stmtContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_simple_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimple_stmt" ):
                listener.enterSimple_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimple_stmt" ):
                listener.exitSimple_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimple_stmt" ):
                return visitor.visitSimple_stmt(self)
            else:
                return visitor.visitChildren(self)




    def simple_stmt(self):

        localctx = AtopileParser.Simple_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_simple_stmt)
        try:
            self.state = 78
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 74
                self.import_stmt()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 75
                self.assign_stmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 76
                self.setas_stmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 77
                self.connect_stmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Compound_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def class_def(self):
            return self.getTypedRuleContext(AtopileParser.Class_defContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_compound_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompound_stmt" ):
                listener.enterCompound_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompound_stmt" ):
                listener.exitCompound_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompound_stmt" ):
                return visitor.visitCompound_stmt(self)
            else:
                return visitor.visitChildren(self)




    def compound_stmt(self):

        localctx = AtopileParser.Compound_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_compound_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.class_def()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_stmts(self):
            return self.getTypedRuleContext(AtopileParser.Simple_stmtsContext,0)


        def NEWLINE(self):
            return self.getToken(AtopileParser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(AtopileParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(AtopileParser.DEDENT, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.StmtContext)
            else:
                return self.getTypedRuleContext(AtopileParser.StmtContext,i)


        def getRuleIndex(self):
            return AtopileParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = AtopileParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.state = 92
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3, 12, 13, 14, 16]:
                self.enterOuterAlt(localctx, 1)
                self.state = 82
                self.simple_stmts()
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 2)
                self.state = 83
                self.match(AtopileParser.NEWLINE)
                self.state = 84
                self.match(AtopileParser.INDENT)
                self.state = 86 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 85
                    self.stmt()
                    self.state = 88 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 94600) != 0)):
                        break

                self.state = 90
                self.match(AtopileParser.DEDENT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Class_defContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def class_type(self):
            return self.getTypedRuleContext(AtopileParser.Class_typeContext,0)


        def name(self):
            return self.getTypedRuleContext(AtopileParser.NameContext,0)


        def COLON(self):
            return self.getToken(AtopileParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(AtopileParser.BlockContext,0)


        def FROM(self):
            return self.getToken(AtopileParser.FROM, 0)

        def class_ref(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.Class_refContext)
            else:
                return self.getTypedRuleContext(AtopileParser.Class_refContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AtopileParser.COMMA)
            else:
                return self.getToken(AtopileParser.COMMA, i)

        def getRuleIndex(self):
            return AtopileParser.RULE_class_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClass_def" ):
                listener.enterClass_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClass_def" ):
                listener.exitClass_def(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClass_def" ):
                return visitor.visitClass_def(self)
            else:
                return visitor.visitChildren(self)




    def class_def(self):

        localctx = AtopileParser.Class_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_class_def)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.class_type()
            self.state = 95
            self.name()
            self.state = 105
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 96
                self.match(AtopileParser.FROM)
                self.state = 97
                self.class_ref()
                self.state = 102
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==30:
                    self.state = 98
                    self.match(AtopileParser.COMMA)
                    self.state = 99
                    self.class_ref()
                    self.state = 104
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 107
            self.match(AtopileParser.COLON)
            self.state = 108
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Class_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BLOCK(self):
            return self.getToken(AtopileParser.BLOCK, 0)

        def NODE(self):
            return self.getToken(AtopileParser.NODE, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_class_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClass_type" ):
                listener.enterClass_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClass_type" ):
                listener.exitClass_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClass_type" ):
                return visitor.visitClass_type(self)
            else:
                return visitor.visitChildren(self)




    def class_type(self):

        localctx = AtopileParser.Class_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_class_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            _la = self._input.LA(1)
            if not(_la==7 or _la==8):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IMPORT(self):
            return self.getToken(AtopileParser.IMPORT, 0)

        def class_ref(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.Class_refContext)
            else:
                return self.getTypedRuleContext(AtopileParser.Class_refContext,i)


        def FROM(self):
            return self.getToken(AtopileParser.FROM, 0)

        def string(self):
            return self.getTypedRuleContext(AtopileParser.StringContext,0)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AtopileParser.COMMA)
            else:
                return self.getToken(AtopileParser.COMMA, i)

        def getRuleIndex(self):
            return AtopileParser.RULE_import_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_stmt" ):
                listener.enterImport_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_stmt" ):
                listener.exitImport_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImport_stmt" ):
                return visitor.visitImport_stmt(self)
            else:
                return visitor.visitChildren(self)




    def import_stmt(self):

        localctx = AtopileParser.Import_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_import_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.match(AtopileParser.IMPORT)
            self.state = 113
            self.class_ref()
            self.state = 118
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30:
                self.state = 114
                self.match(AtopileParser.COMMA)
                self.state = 115
                self.class_ref()
                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 121
            self.match(AtopileParser.FROM)
            self.state = 122
            self.string()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Assign_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def refs(self):
            return self.getTypedRuleContext(AtopileParser.RefsContext,0)


        def ASSIGN(self):
            return self.getToken(AtopileParser.ASSIGN, 0)

        def instantiation(self):
            return self.getTypedRuleContext(AtopileParser.InstantiationContext,0)


        def COLON(self):
            return self.getToken(AtopileParser.COLON, 0)

        def class_ref(self):
            return self.getTypedRuleContext(AtopileParser.Class_refContext,0)


        def value(self):
            return self.getTypedRuleContext(AtopileParser.ValueContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_assign_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssign_stmt" ):
                listener.enterAssign_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssign_stmt" ):
                listener.exitAssign_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssign_stmt" ):
                return visitor.visitAssign_stmt(self)
            else:
                return visitor.visitChildren(self)




    def assign_stmt(self):

        localctx = AtopileParser.Assign_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_assign_stmt)
        self._la = 0 # Token type
        try:
            self.state = 134
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 124
                self.refs()
                self.state = 127
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==31:
                    self.state = 125
                    self.match(AtopileParser.COLON)
                    self.state = 126
                    self.class_ref()


                self.state = 129
                self.match(AtopileParser.ASSIGN)
                self.state = 130
                self.instantiation()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 132
                self.refs()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 133
                self.value()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Setas_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def refs(self):
            return self.getTypedRuleContext(AtopileParser.RefsContext,0)


        def ARROW(self):
            return self.getToken(AtopileParser.ARROW, 0)

        def class_ref(self):
            return self.getTypedRuleContext(AtopileParser.Class_refContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_setas_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetas_stmt" ):
                listener.enterSetas_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetas_stmt" ):
                listener.exitSetas_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetas_stmt" ):
                return visitor.visitSetas_stmt(self)
            else:
                return visitor.visitChildren(self)




    def setas_stmt(self):

        localctx = AtopileParser.Setas_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_setas_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self.refs()
            self.state = 137
            self.match(AtopileParser.ARROW)
            self.state = 138
            self.class_ref()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Connect_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def refs(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.RefsContext)
            else:
                return self.getTypedRuleContext(AtopileParser.RefsContext,i)


        def NOT_OP(self):
            return self.getToken(AtopileParser.NOT_OP, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_connect_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConnect_stmt" ):
                listener.enterConnect_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConnect_stmt" ):
                listener.exitConnect_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConnect_stmt" ):
                return visitor.visitConnect_stmt(self)
            else:
                return visitor.visitChildren(self)




    def connect_stmt(self):

        localctx = AtopileParser.Connect_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_connect_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.refs()
            self.state = 141
            self.match(AtopileParser.NOT_OP)
            self.state = 142
            self.refs()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RefsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def single_ref(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.Single_refContext)
            else:
                return self.getTypedRuleContext(AtopileParser.Single_refContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AtopileParser.COMMA)
            else:
                return self.getToken(AtopileParser.COMMA, i)

        def getRuleIndex(self):
            return AtopileParser.RULE_refs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRefs" ):
                listener.enterRefs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRefs" ):
                listener.exitRefs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRefs" ):
                return visitor.visitRefs(self)
            else:
                return visitor.visitChildren(self)




    def refs(self):

        localctx = AtopileParser.RefsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_refs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144
            self.single_ref()
            self.state = 149
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30:
                self.state = 145
                self.match(AtopileParser.COMMA)
                self.state = 146
                self.single_ref()
                self.state = 151
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Single_refContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(AtopileParser.NameContext,0)


        def OPEN_BRACK(self):
            return self.getToken(AtopileParser.OPEN_BRACK, 0)

        def CLOSE_BRACK(self):
            return self.getToken(AtopileParser.CLOSE_BRACK, 0)

        def DOT(self):
            return self.getToken(AtopileParser.DOT, 0)

        def single_ref(self):
            return self.getTypedRuleContext(AtopileParser.Single_refContext,0)


        def string(self):
            return self.getTypedRuleContext(AtopileParser.StringContext,0)


        def totally_an_integer(self):
            return self.getTypedRuleContext(AtopileParser.Totally_an_integerContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_single_ref

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingle_ref" ):
                listener.enterSingle_ref(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingle_ref" ):
                listener.exitSingle_ref(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingle_ref" ):
                return visitor.visitSingle_ref(self)
            else:
                return visitor.visitChildren(self)




    def single_ref(self):

        localctx = AtopileParser.Single_refContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_single_ref)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self.name()
            self.state = 160
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==35:
                self.state = 153
                self.match(AtopileParser.OPEN_BRACK)
                self.state = 156
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [3]:
                    self.state = 154
                    self.string()
                    pass
                elif token in [5]:
                    self.state = 155
                    self.totally_an_integer()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 158
                self.match(AtopileParser.CLOSE_BRACK)


            self.state = 164
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==25:
                self.state = 162
                self.match(AtopileParser.DOT)
                self.state = 163
                self.single_ref()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstantiationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEW(self):
            return self.getToken(AtopileParser.NEW, 0)

        def class_ref(self):
            return self.getTypedRuleContext(AtopileParser.Class_refContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_instantiation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInstantiation" ):
                listener.enterInstantiation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInstantiation" ):
                listener.exitInstantiation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInstantiation" ):
                return visitor.visitInstantiation(self)
            else:
                return visitor.visitChildren(self)




    def instantiation(self):

        localctx = AtopileParser.InstantiationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_instantiation)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 166
            self.match(AtopileParser.NEW)
            self.state = 167
            self.class_ref()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Class_refContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def attr(self):
            return self.getTypedRuleContext(AtopileParser.AttrContext,0)


        def name(self):
            return self.getTypedRuleContext(AtopileParser.NameContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_class_ref

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClass_ref" ):
                listener.enterClass_ref(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClass_ref" ):
                listener.exitClass_ref(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClass_ref" ):
                return visitor.visitClass_ref(self)
            else:
                return visitor.visitChildren(self)




    def class_ref(self):

        localctx = AtopileParser.Class_refContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_class_ref)
        try:
            self.state = 171
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 169
                self.attr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 170
                self.name()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.NameContext)
            else:
                return self.getTypedRuleContext(AtopileParser.NameContext,i)


        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(AtopileParser.DOT)
            else:
                return self.getToken(AtopileParser.DOT, i)

        def getRuleIndex(self):
            return AtopileParser.RULE_attr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr" ):
                listener.enterAttr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr" ):
                listener.exitAttr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr" ):
                return visitor.visitAttr(self)
            else:
                return visitor.visitChildren(self)




    def attr(self):

        localctx = AtopileParser.AttrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_attr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 173
            self.name()
            self.state = 176 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 174
                self.match(AtopileParser.DOT)
                self.state = 175
                self.name()
                self.state = 178 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==25):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def string(self):
            return self.getTypedRuleContext(AtopileParser.StringContext,0)


        def number(self):
            return self.getTypedRuleContext(AtopileParser.NumberContext,0)


        def physical(self):
            return self.getTypedRuleContext(AtopileParser.PhysicalContext,0)


        def boolean_(self):
            return self.getTypedRuleContext(AtopileParser.Boolean_Context,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = AtopileParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_value)
        try:
            self.state = 184
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 180
                self.string()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 181
                self.number()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 182
                self.physical()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 183
                self.boolean_()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(AtopileParser.NAME, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterName" ):
                listener.enterName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitName" ):
                listener.exitName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitName" ):
                return visitor.visitName(self)
            else:
                return visitor.visitChildren(self)




    def name(self):

        localctx = AtopileParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.match(AtopileParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(AtopileParser.STRING, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)




    def string(self):

        localctx = AtopileParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.match(AtopileParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PhysicalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(AtopileParser.STRING, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_physical

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPhysical" ):
                listener.enterPhysical(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPhysical" ):
                listener.exitPhysical(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPhysical" ):
                return visitor.visitPhysical(self)
            else:
                return visitor.visitChildren(self)




    def physical(self):

        localctx = AtopileParser.PhysicalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_physical)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            self.match(AtopileParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(AtopileParser.STRING, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)




    def number(self):

        localctx = AtopileParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.match(AtopileParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Totally_an_integerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(AtopileParser.NUMBER, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_totally_an_integer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTotally_an_integer" ):
                listener.enterTotally_an_integer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTotally_an_integer" ):
                listener.exitTotally_an_integer(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTotally_an_integer" ):
                return visitor.visitTotally_an_integer(self)
            else:
                return visitor.visitChildren(self)




    def totally_an_integer(self):

        localctx = AtopileParser.Totally_an_integerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_totally_an_integer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self.match(AtopileParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Boolean_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(AtopileParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(AtopileParser.FALSE, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_boolean_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolean_" ):
                listener.enterBoolean_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolean_" ):
                listener.exitBoolean_(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolean_" ):
                return visitor.visitBoolean_(self)
            else:
                return visitor.visitChildren(self)




    def boolean_(self):

        localctx = AtopileParser.Boolean_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_boolean_)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            _la = self._input.LA(1)
            if not(_la==13 or _la==14):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





