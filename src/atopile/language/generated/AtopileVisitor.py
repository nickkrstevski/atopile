# Generated from Atopile.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .AtopileParser import AtopileParser
else:
    from AtopileParser import AtopileParser

# This class defines a complete generic visitor for a parse tree produced by AtopileParser.

class AtopileVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by AtopileParser#file_input.
    def visitFile_input(self, ctx:AtopileParser.File_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#statement.
    def visitStatement(self, ctx:AtopileParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#import_statement.
    def visitImport_statement(self, ctx:AtopileParser.Import_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#import_from_statement.
    def visitImport_from_statement(self, ctx:AtopileParser.Import_from_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#def_statement.
    def visitDef_statement(self, ctx:AtopileParser.Def_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#instantiate_statement.
    def visitInstantiate_statement(self, ctx:AtopileParser.Instantiate_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#pin_statement.
    def visitPin_statement(self, ctx:AtopileParser.Pin_statementContext):
        return self.visitChildren(ctx)



del AtopileParser