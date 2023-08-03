# Generated from AtopileParser.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .AtopileParser import AtopileParser
else:
    from AtopileParser import AtopileParser

# This class defines a complete listener for a parse tree produced by AtopileParser.
class AtopileParserListener(ParseTreeListener):

    # Enter a parse tree produced by AtopileParser#file_input.
    def enterFile_input(self, ctx:AtopileParser.File_inputContext):
        pass

    # Exit a parse tree produced by AtopileParser#file_input.
    def exitFile_input(self, ctx:AtopileParser.File_inputContext):
        pass


    # Enter a parse tree produced by AtopileParser#stmt.
    def enterStmt(self, ctx:AtopileParser.StmtContext):
        pass

    # Exit a parse tree produced by AtopileParser#stmt.
    def exitStmt(self, ctx:AtopileParser.StmtContext):
        pass


    # Enter a parse tree produced by AtopileParser#simple_stmts.
    def enterSimple_stmts(self, ctx:AtopileParser.Simple_stmtsContext):
        pass

    # Exit a parse tree produced by AtopileParser#simple_stmts.
    def exitSimple_stmts(self, ctx:AtopileParser.Simple_stmtsContext):
        pass


    # Enter a parse tree produced by AtopileParser#simple_stmt.
    def enterSimple_stmt(self, ctx:AtopileParser.Simple_stmtContext):
        pass

    # Exit a parse tree produced by AtopileParser#simple_stmt.
    def exitSimple_stmt(self, ctx:AtopileParser.Simple_stmtContext):
        pass


    # Enter a parse tree produced by AtopileParser#compound_stmt.
    def enterCompound_stmt(self, ctx:AtopileParser.Compound_stmtContext):
        pass

    # Exit a parse tree produced by AtopileParser#compound_stmt.
    def exitCompound_stmt(self, ctx:AtopileParser.Compound_stmtContext):
        pass


    # Enter a parse tree produced by AtopileParser#block.
    def enterBlock(self, ctx:AtopileParser.BlockContext):
        pass

    # Exit a parse tree produced by AtopileParser#block.
    def exitBlock(self, ctx:AtopileParser.BlockContext):
        pass


    # Enter a parse tree produced by AtopileParser#class_def.
    def enterClass_def(self, ctx:AtopileParser.Class_defContext):
        pass

    # Exit a parse tree produced by AtopileParser#class_def.
    def exitClass_def(self, ctx:AtopileParser.Class_defContext):
        pass


    # Enter a parse tree produced by AtopileParser#class_type.
    def enterClass_type(self, ctx:AtopileParser.Class_typeContext):
        pass

    # Exit a parse tree produced by AtopileParser#class_type.
    def exitClass_type(self, ctx:AtopileParser.Class_typeContext):
        pass


    # Enter a parse tree produced by AtopileParser#import_stmt.
    def enterImport_stmt(self, ctx:AtopileParser.Import_stmtContext):
        pass

    # Exit a parse tree produced by AtopileParser#import_stmt.
    def exitImport_stmt(self, ctx:AtopileParser.Import_stmtContext):
        pass


    # Enter a parse tree produced by AtopileParser#assign_stmt.
    def enterAssign_stmt(self, ctx:AtopileParser.Assign_stmtContext):
        pass

    # Exit a parse tree produced by AtopileParser#assign_stmt.
    def exitAssign_stmt(self, ctx:AtopileParser.Assign_stmtContext):
        pass


    # Enter a parse tree produced by AtopileParser#setas_stmt.
    def enterSetas_stmt(self, ctx:AtopileParser.Setas_stmtContext):
        pass

    # Exit a parse tree produced by AtopileParser#setas_stmt.
    def exitSetas_stmt(self, ctx:AtopileParser.Setas_stmtContext):
        pass


    # Enter a parse tree produced by AtopileParser#connect_stmt.
    def enterConnect_stmt(self, ctx:AtopileParser.Connect_stmtContext):
        pass

    # Exit a parse tree produced by AtopileParser#connect_stmt.
    def exitConnect_stmt(self, ctx:AtopileParser.Connect_stmtContext):
        pass


    # Enter a parse tree produced by AtopileParser#refs.
    def enterRefs(self, ctx:AtopileParser.RefsContext):
        pass

    # Exit a parse tree produced by AtopileParser#refs.
    def exitRefs(self, ctx:AtopileParser.RefsContext):
        pass


    # Enter a parse tree produced by AtopileParser#single_ref.
    def enterSingle_ref(self, ctx:AtopileParser.Single_refContext):
        pass

    # Exit a parse tree produced by AtopileParser#single_ref.
    def exitSingle_ref(self, ctx:AtopileParser.Single_refContext):
        pass


    # Enter a parse tree produced by AtopileParser#instantiation.
    def enterInstantiation(self, ctx:AtopileParser.InstantiationContext):
        pass

    # Exit a parse tree produced by AtopileParser#instantiation.
    def exitInstantiation(self, ctx:AtopileParser.InstantiationContext):
        pass


    # Enter a parse tree produced by AtopileParser#class_ref.
    def enterClass_ref(self, ctx:AtopileParser.Class_refContext):
        pass

    # Exit a parse tree produced by AtopileParser#class_ref.
    def exitClass_ref(self, ctx:AtopileParser.Class_refContext):
        pass


    # Enter a parse tree produced by AtopileParser#attr.
    def enterAttr(self, ctx:AtopileParser.AttrContext):
        pass

    # Exit a parse tree produced by AtopileParser#attr.
    def exitAttr(self, ctx:AtopileParser.AttrContext):
        pass


    # Enter a parse tree produced by AtopileParser#value.
    def enterValue(self, ctx:AtopileParser.ValueContext):
        pass

    # Exit a parse tree produced by AtopileParser#value.
    def exitValue(self, ctx:AtopileParser.ValueContext):
        pass


    # Enter a parse tree produced by AtopileParser#name.
    def enterName(self, ctx:AtopileParser.NameContext):
        pass

    # Exit a parse tree produced by AtopileParser#name.
    def exitName(self, ctx:AtopileParser.NameContext):
        pass


    # Enter a parse tree produced by AtopileParser#string.
    def enterString(self, ctx:AtopileParser.StringContext):
        pass

    # Exit a parse tree produced by AtopileParser#string.
    def exitString(self, ctx:AtopileParser.StringContext):
        pass


    # Enter a parse tree produced by AtopileParser#physical.
    def enterPhysical(self, ctx:AtopileParser.PhysicalContext):
        pass

    # Exit a parse tree produced by AtopileParser#physical.
    def exitPhysical(self, ctx:AtopileParser.PhysicalContext):
        pass


    # Enter a parse tree produced by AtopileParser#number.
    def enterNumber(self, ctx:AtopileParser.NumberContext):
        pass

    # Exit a parse tree produced by AtopileParser#number.
    def exitNumber(self, ctx:AtopileParser.NumberContext):
        pass


    # Enter a parse tree produced by AtopileParser#totally_an_integer.
    def enterTotally_an_integer(self, ctx:AtopileParser.Totally_an_integerContext):
        pass

    # Exit a parse tree produced by AtopileParser#totally_an_integer.
    def exitTotally_an_integer(self, ctx:AtopileParser.Totally_an_integerContext):
        pass


    # Enter a parse tree produced by AtopileParser#boolean_.
    def enterBoolean_(self, ctx:AtopileParser.Boolean_Context):
        pass

    # Exit a parse tree produced by AtopileParser#boolean_.
    def exitBoolean_(self, ctx:AtopileParser.Boolean_Context):
        pass



del AtopileParser