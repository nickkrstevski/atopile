# Generated from Atopile.g4 by ANTLR 4.12.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,12,68,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,1,0,5,0,16,8,0,10,0,12,0,19,9,0,1,0,1,0,1,1,1,1,1,1,3,1,26,8,1,
        1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,5,3,36,8,3,10,3,12,3,39,9,3,1,3,
        1,3,1,4,1,4,1,4,1,4,1,4,1,4,3,4,49,8,4,1,4,1,4,5,4,53,8,4,10,4,12,
        4,56,9,4,1,4,1,4,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,0,0,7,0,2,4,
        6,8,10,12,0,0,66,0,17,1,0,0,0,2,25,1,0,0,0,4,27,1,0,0,0,6,29,1,0,
        0,0,8,42,1,0,0,0,10,59,1,0,0,0,12,63,1,0,0,0,14,16,3,2,1,0,15,14,
        1,0,0,0,16,19,1,0,0,0,17,15,1,0,0,0,17,18,1,0,0,0,18,20,1,0,0,0,
        19,17,1,0,0,0,20,21,5,0,0,1,21,1,1,0,0,0,22,26,3,4,2,0,23,26,3,12,
        6,0,24,26,3,8,4,0,25,22,1,0,0,0,25,23,1,0,0,0,25,24,1,0,0,0,26,3,
        1,0,0,0,27,28,3,6,3,0,28,5,1,0,0,0,29,30,5,1,0,0,30,31,5,11,0,0,
        31,32,5,2,0,0,32,37,5,11,0,0,33,34,5,3,0,0,34,36,5,11,0,0,35,33,
        1,0,0,0,36,39,1,0,0,0,37,35,1,0,0,0,37,38,1,0,0,0,38,40,1,0,0,0,
        39,37,1,0,0,0,40,41,5,4,0,0,41,7,1,0,0,0,42,43,5,5,0,0,43,44,5,11,
        0,0,44,45,5,6,0,0,45,48,5,7,0,0,46,47,5,1,0,0,47,49,3,10,5,0,48,
        46,1,0,0,0,48,49,1,0,0,0,49,50,1,0,0,0,50,54,5,8,0,0,51,53,3,2,1,
        0,52,51,1,0,0,0,53,56,1,0,0,0,54,52,1,0,0,0,54,55,1,0,0,0,55,57,
        1,0,0,0,56,54,1,0,0,0,57,58,5,9,0,0,58,9,1,0,0,0,59,60,5,11,0,0,
        60,61,5,6,0,0,61,62,5,7,0,0,62,11,1,0,0,0,63,64,5,10,0,0,64,65,5,
        11,0,0,65,66,5,4,0,0,66,13,1,0,0,0,5,17,25,37,48,54
    ]

class AtopileParser ( Parser ):

    grammarFileName = "Atopile.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'from'", "'import'", "','", "';'", "'def'", 
                     "'('", "')'", "'{'", "'}'", "'pin'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "ID", "WS" ]

    RULE_file_input = 0
    RULE_statement = 1
    RULE_import_statement = 2
    RULE_import_from_statement = 3
    RULE_def_statement = 4
    RULE_instantiate_statement = 5
    RULE_pin_statement = 6

    ruleNames =  [ "file_input", "statement", "import_statement", "import_from_statement", 
                   "def_statement", "instantiate_statement", "pin_statement" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    ID=11
    WS=12

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.12.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class File_inputContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(AtopileParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.StatementContext)
            else:
                return self.getTypedRuleContext(AtopileParser.StatementContext,i)


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
            self.state = 17
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1058) != 0):
                self.state = 14
                self.statement()
                self.state = 19
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 20
            self.match(AtopileParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_statement(self):
            return self.getTypedRuleContext(AtopileParser.Import_statementContext,0)


        def pin_statement(self):
            return self.getTypedRuleContext(AtopileParser.Pin_statementContext,0)


        def def_statement(self):
            return self.getTypedRuleContext(AtopileParser.Def_statementContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = AtopileParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 25
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 22
                self.import_statement()
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 2)
                self.state = 23
                self.pin_statement()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 24
                self.def_statement()
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


    class Import_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_from_statement(self):
            return self.getTypedRuleContext(AtopileParser.Import_from_statementContext,0)


        def getRuleIndex(self):
            return AtopileParser.RULE_import_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_statement" ):
                listener.enterImport_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_statement" ):
                listener.exitImport_statement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImport_statement" ):
                return visitor.visitImport_statement(self)
            else:
                return visitor.visitChildren(self)




    def import_statement(self):

        localctx = AtopileParser.Import_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_import_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.import_from_statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_from_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(AtopileParser.ID)
            else:
                return self.getToken(AtopileParser.ID, i)

        def getRuleIndex(self):
            return AtopileParser.RULE_import_from_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_from_statement" ):
                listener.enterImport_from_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_from_statement" ):
                listener.exitImport_from_statement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImport_from_statement" ):
                return visitor.visitImport_from_statement(self)
            else:
                return visitor.visitChildren(self)




    def import_from_statement(self):

        localctx = AtopileParser.Import_from_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_import_from_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.match(AtopileParser.T__0)
            self.state = 30
            self.match(AtopileParser.ID)
            self.state = 31
            self.match(AtopileParser.T__1)
            self.state = 32
            self.match(AtopileParser.ID)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3:
                self.state = 33
                self.match(AtopileParser.T__2)
                self.state = 34
                self.match(AtopileParser.ID)
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 40
            self.match(AtopileParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Def_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(AtopileParser.ID, 0)

        def instantiate_statement(self):
            return self.getTypedRuleContext(AtopileParser.Instantiate_statementContext,0)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AtopileParser.StatementContext)
            else:
                return self.getTypedRuleContext(AtopileParser.StatementContext,i)


        def getRuleIndex(self):
            return AtopileParser.RULE_def_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDef_statement" ):
                listener.enterDef_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDef_statement" ):
                listener.exitDef_statement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDef_statement" ):
                return visitor.visitDef_statement(self)
            else:
                return visitor.visitChildren(self)




    def def_statement(self):

        localctx = AtopileParser.Def_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_def_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(AtopileParser.T__4)
            self.state = 43
            self.match(AtopileParser.ID)
            self.state = 44
            self.match(AtopileParser.T__5)
            self.state = 45
            self.match(AtopileParser.T__6)
            self.state = 48
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 46
                self.match(AtopileParser.T__0)
                self.state = 47
                self.instantiate_statement()


            self.state = 50
            self.match(AtopileParser.T__7)
            self.state = 54
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1058) != 0):
                self.state = 51
                self.statement()
                self.state = 56
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 57
            self.match(AtopileParser.T__8)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Instantiate_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(AtopileParser.ID, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_instantiate_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInstantiate_statement" ):
                listener.enterInstantiate_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInstantiate_statement" ):
                listener.exitInstantiate_statement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInstantiate_statement" ):
                return visitor.visitInstantiate_statement(self)
            else:
                return visitor.visitChildren(self)




    def instantiate_statement(self):

        localctx = AtopileParser.Instantiate_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_instantiate_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(AtopileParser.ID)
            self.state = 60
            self.match(AtopileParser.T__5)
            self.state = 61
            self.match(AtopileParser.T__6)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pin_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(AtopileParser.ID, 0)

        def getRuleIndex(self):
            return AtopileParser.RULE_pin_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPin_statement" ):
                listener.enterPin_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPin_statement" ):
                listener.exitPin_statement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPin_statement" ):
                return visitor.visitPin_statement(self)
            else:
                return visitor.visitChildren(self)




    def pin_statement(self):

        localctx = AtopileParser.Pin_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_pin_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(AtopileParser.T__9)
            self.state = 64
            self.match(AtopileParser.ID)
            self.state = 65
            self.match(AtopileParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





