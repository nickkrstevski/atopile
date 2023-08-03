# Generated from AtopileParser.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .AtopileParser import AtopileParser
else:
    from AtopileParser import AtopileParser

# This class defines a complete generic visitor for a parse tree produced by AtopileParser.

class AtopileParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by AtopileParser#file_input.
    def visitFile_input(self, ctx:AtopileParser.File_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#stmt.
    def visitStmt(self, ctx:AtopileParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#simple_stmts.
    def visitSimple_stmts(self, ctx:AtopileParser.Simple_stmtsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#simple_stmt.
    def visitSimple_stmt(self, ctx:AtopileParser.Simple_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#compound_stmt.
    def visitCompound_stmt(self, ctx:AtopileParser.Compound_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#block.
    def visitBlock(self, ctx:AtopileParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#class_def.
    def visitClass_def(self, ctx:AtopileParser.Class_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#class_type.
    def visitClass_type(self, ctx:AtopileParser.Class_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#import_stmt.
    def visitImport_stmt(self, ctx:AtopileParser.Import_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#assign_stmt.
    def visitAssign_stmt(self, ctx:AtopileParser.Assign_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#setas_stmt.
    def visitSetas_stmt(self, ctx:AtopileParser.Setas_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#connect_stmt.
    def visitConnect_stmt(self, ctx:AtopileParser.Connect_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#refs.
    def visitRefs(self, ctx:AtopileParser.RefsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#single_ref.
    def visitSingle_ref(self, ctx:AtopileParser.Single_refContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#instantiation.
    def visitInstantiation(self, ctx:AtopileParser.InstantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#class_ref.
    def visitClass_ref(self, ctx:AtopileParser.Class_refContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#attr.
    def visitAttr(self, ctx:AtopileParser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#value.
    def visitValue(self, ctx:AtopileParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#name.
    def visitName(self, ctx:AtopileParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#string.
    def visitString(self, ctx:AtopileParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#physical.
    def visitPhysical(self, ctx:AtopileParser.PhysicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#number.
    def visitNumber(self, ctx:AtopileParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#totally_an_integer.
    def visitTotally_an_integer(self, ctx:AtopileParser.Totally_an_integerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AtopileParser#boolean_.
    def visitBoolean_(self, ctx:AtopileParser.Boolean_Context):
        return self.visitChildren(ctx)



del AtopileParser