# Generated from Atopile.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .AtopileParser import AtopileParser
else:
    from AtopileParser import AtopileParser

# This class defines a complete listener for a parse tree produced by AtopileParser.
class AtopileListener(ParseTreeListener):

    # Enter a parse tree produced by AtopileParser#file_input.
    def enterFile_input(self, ctx:AtopileParser.File_inputContext):
        pass

    # Exit a parse tree produced by AtopileParser#file_input.
    def exitFile_input(self, ctx:AtopileParser.File_inputContext):
        pass


    # Enter a parse tree produced by AtopileParser#statement.
    def enterStatement(self, ctx:AtopileParser.StatementContext):
        pass

    # Exit a parse tree produced by AtopileParser#statement.
    def exitStatement(self, ctx:AtopileParser.StatementContext):
        pass


    # Enter a parse tree produced by AtopileParser#import_statement.
    def enterImport_statement(self, ctx:AtopileParser.Import_statementContext):
        pass

    # Exit a parse tree produced by AtopileParser#import_statement.
    def exitImport_statement(self, ctx:AtopileParser.Import_statementContext):
        pass


    # Enter a parse tree produced by AtopileParser#import_from_statement.
    def enterImport_from_statement(self, ctx:AtopileParser.Import_from_statementContext):
        pass

    # Exit a parse tree produced by AtopileParser#import_from_statement.
    def exitImport_from_statement(self, ctx:AtopileParser.Import_from_statementContext):
        pass


    # Enter a parse tree produced by AtopileParser#def_statement.
    def enterDef_statement(self, ctx:AtopileParser.Def_statementContext):
        pass

    # Exit a parse tree produced by AtopileParser#def_statement.
    def exitDef_statement(self, ctx:AtopileParser.Def_statementContext):
        pass


    # Enter a parse tree produced by AtopileParser#instantiate_statement.
    def enterInstantiate_statement(self, ctx:AtopileParser.Instantiate_statementContext):
        pass

    # Exit a parse tree produced by AtopileParser#instantiate_statement.
    def exitInstantiate_statement(self, ctx:AtopileParser.Instantiate_statementContext):
        pass


    # Enter a parse tree produced by AtopileParser#pin_statement.
    def enterPin_statement(self, ctx:AtopileParser.Pin_statementContext):
        pass

    # Exit a parse tree produced by AtopileParser#pin_statement.
    def exitPin_statement(self, ctx:AtopileParser.Pin_statementContext):
        pass



del AtopileParser