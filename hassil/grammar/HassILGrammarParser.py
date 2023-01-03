# Generated from HassILGrammar.g4 by ANTLR 4.11.1
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
        4,1,14,105,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,4,0,24,8,0,11,0,12,0,25,
        1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,3,2,36,8,2,1,2,3,2,39,8,2,1,2,3,
        2,42,8,2,1,2,5,2,45,8,2,10,2,12,2,48,9,2,1,3,1,3,3,3,52,8,3,1,3,
        1,3,3,3,56,8,3,1,3,1,3,1,4,1,4,3,4,62,8,4,1,4,1,4,3,4,66,8,4,1,4,
        1,4,1,5,3,5,71,8,5,1,5,1,5,3,5,75,8,5,1,6,1,6,3,6,79,8,6,1,7,1,7,
        3,7,83,8,7,1,7,1,7,3,7,87,8,7,1,7,1,7,1,8,1,8,1,9,1,9,3,9,95,8,9,
        1,9,1,9,3,9,99,8,9,1,9,1,9,1,10,1,10,1,10,0,0,11,0,2,4,6,8,10,12,
        14,16,18,20,0,0,112,0,23,1,0,0,0,2,27,1,0,0,0,4,35,1,0,0,0,6,49,
        1,0,0,0,8,59,1,0,0,0,10,70,1,0,0,0,12,76,1,0,0,0,14,80,1,0,0,0,16,
        90,1,0,0,0,18,92,1,0,0,0,20,102,1,0,0,0,22,24,3,2,1,0,23,22,1,0,
        0,0,24,25,1,0,0,0,25,23,1,0,0,0,25,26,1,0,0,0,26,1,1,0,0,0,27,28,
        3,4,2,0,28,29,5,13,0,0,29,3,1,0,0,0,30,36,3,6,3,0,31,36,3,8,4,0,
        32,36,3,12,6,0,33,36,3,14,7,0,34,36,3,18,9,0,35,30,1,0,0,0,35,31,
        1,0,0,0,35,32,1,0,0,0,35,33,1,0,0,0,35,34,1,0,0,0,36,38,1,0,0,0,
        37,39,5,14,0,0,38,37,1,0,0,0,38,39,1,0,0,0,39,46,1,0,0,0,40,42,3,
        10,5,0,41,40,1,0,0,0,41,42,1,0,0,0,42,43,1,0,0,0,43,45,3,4,2,0,44,
        41,1,0,0,0,45,48,1,0,0,0,46,44,1,0,0,0,46,47,1,0,0,0,47,5,1,0,0,
        0,48,46,1,0,0,0,49,51,5,1,0,0,50,52,5,14,0,0,51,50,1,0,0,0,51,52,
        1,0,0,0,52,53,1,0,0,0,53,55,3,4,2,0,54,56,5,14,0,0,55,54,1,0,0,0,
        55,56,1,0,0,0,56,57,1,0,0,0,57,58,5,2,0,0,58,7,1,0,0,0,59,61,5,3,
        0,0,60,62,5,14,0,0,61,60,1,0,0,0,61,62,1,0,0,0,62,63,1,0,0,0,63,
        65,3,4,2,0,64,66,5,14,0,0,65,64,1,0,0,0,65,66,1,0,0,0,66,67,1,0,
        0,0,67,68,5,4,0,0,68,9,1,0,0,0,69,71,5,14,0,0,70,69,1,0,0,0,70,71,
        1,0,0,0,71,72,1,0,0,0,72,74,5,5,0,0,73,75,5,14,0,0,74,73,1,0,0,0,
        74,75,1,0,0,0,75,11,1,0,0,0,76,78,5,10,0,0,77,79,5,14,0,0,78,77,
        1,0,0,0,78,79,1,0,0,0,79,13,1,0,0,0,80,82,5,6,0,0,81,83,5,14,0,0,
        82,81,1,0,0,0,82,83,1,0,0,0,83,84,1,0,0,0,84,86,3,16,8,0,85,87,5,
        14,0,0,86,85,1,0,0,0,86,87,1,0,0,0,87,88,1,0,0,0,88,89,5,7,0,0,89,
        15,1,0,0,0,90,91,5,10,0,0,91,17,1,0,0,0,92,94,5,8,0,0,93,95,5,14,
        0,0,94,93,1,0,0,0,94,95,1,0,0,0,95,96,1,0,0,0,96,98,3,20,10,0,97,
        99,5,14,0,0,98,97,1,0,0,0,98,99,1,0,0,0,99,100,1,0,0,0,100,101,5,
        9,0,0,101,19,1,0,0,0,102,103,5,10,0,0,103,21,1,0,0,0,16,25,35,38,
        41,46,51,55,61,65,70,74,78,82,86,94,98
    ]

class HassILGrammarParser ( Parser ):

    grammarFileName = "HassILGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'['", "']'", "'|'", "'{'", 
                     "'}'", "'<'", "'>'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "STRING", "ESC", "CHARACTER", 
                      "EOL", "WS" ]

    RULE_document = 0
    RULE_sentence = 1
    RULE_expression = 2
    RULE_group = 3
    RULE_optional = 4
    RULE_alt = 5
    RULE_text_chunk = 6
    RULE_list = 7
    RULE_list_name = 8
    RULE_rule = 9
    RULE_rule_name = 10

    ruleNames =  [ "document", "sentence", "expression", "group", "optional", 
                   "alt", "text_chunk", "list", "list_name", "rule", "rule_name" ]

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
    STRING=10
    ESC=11
    CHARACTER=12
    EOL=13
    WS=14

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class DocumentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def sentence(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(HassILGrammarParser.SentenceContext)
            else:
                return self.getTypedRuleContext(HassILGrammarParser.SentenceContext,i)


        def getRuleIndex(self):
            return HassILGrammarParser.RULE_document

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDocument" ):
                listener.enterDocument(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDocument" ):
                listener.exitDocument(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDocument" ):
                return visitor.visitDocument(self)
            else:
                return visitor.visitChildren(self)




    def document(self):

        localctx = HassILGrammarParser.DocumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_document)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 22
                self.sentence()
                self.state = 25 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((_la) & ~0x3f) == 0 and ((1 << _la) & 1354) != 0):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SentenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(HassILGrammarParser.ExpressionContext,0)


        def EOL(self):
            return self.getToken(HassILGrammarParser.EOL, 0)

        def getRuleIndex(self):
            return HassILGrammarParser.RULE_sentence

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSentence" ):
                listener.enterSentence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSentence" ):
                listener.exitSentence(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSentence" ):
                return visitor.visitSentence(self)
            else:
                return visitor.visitChildren(self)




    def sentence(self):

        localctx = HassILGrammarParser.SentenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_sentence)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.expression()
            self.state = 28
            self.match(HassILGrammarParser.EOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def group(self):
            return self.getTypedRuleContext(HassILGrammarParser.GroupContext,0)


        def optional(self):
            return self.getTypedRuleContext(HassILGrammarParser.OptionalContext,0)


        def text_chunk(self):
            return self.getTypedRuleContext(HassILGrammarParser.Text_chunkContext,0)


        def list_(self):
            return self.getTypedRuleContext(HassILGrammarParser.ListContext,0)


        def rule_(self):
            return self.getTypedRuleContext(HassILGrammarParser.RuleContext,0)


        def WS(self):
            return self.getToken(HassILGrammarParser.WS, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(HassILGrammarParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(HassILGrammarParser.ExpressionContext,i)


        def alt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(HassILGrammarParser.AltContext)
            else:
                return self.getTypedRuleContext(HassILGrammarParser.AltContext,i)


        def getRuleIndex(self):
            return HassILGrammarParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = HassILGrammarParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.state = 30
                self.group()
                pass
            elif token in [3]:
                self.state = 31
                self.optional()
                pass
            elif token in [10]:
                self.state = 32
                self.text_chunk()
                pass
            elif token in [6]:
                self.state = 33
                self.list_()
                pass
            elif token in [8]:
                self.state = 34
                self.rule_()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 38
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.state = 37
                self.match(HassILGrammarParser.WS)


            self.state = 46
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 41
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==5 or _la==14:
                        self.state = 40
                        self.alt()


                    self.state = 43
                    self.expression() 
                self.state = 48
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(HassILGrammarParser.ExpressionContext,0)


        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(HassILGrammarParser.WS)
            else:
                return self.getToken(HassILGrammarParser.WS, i)

        def getRuleIndex(self):
            return HassILGrammarParser.RULE_group

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroup" ):
                listener.enterGroup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroup" ):
                listener.exitGroup(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroup" ):
                return visitor.visitGroup(self)
            else:
                return visitor.visitChildren(self)




    def group(self):

        localctx = HassILGrammarParser.GroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_group)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.match(HassILGrammarParser.T__0)
            self.state = 51
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 50
                self.match(HassILGrammarParser.WS)


            self.state = 53
            self.expression()
            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 54
                self.match(HassILGrammarParser.WS)


            self.state = 57
            self.match(HassILGrammarParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OptionalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(HassILGrammarParser.ExpressionContext,0)


        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(HassILGrammarParser.WS)
            else:
                return self.getToken(HassILGrammarParser.WS, i)

        def getRuleIndex(self):
            return HassILGrammarParser.RULE_optional

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOptional" ):
                listener.enterOptional(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOptional" ):
                listener.exitOptional(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOptional" ):
                return visitor.visitOptional(self)
            else:
                return visitor.visitChildren(self)




    def optional(self):

        localctx = HassILGrammarParser.OptionalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_optional)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(HassILGrammarParser.T__2)
            self.state = 61
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 60
                self.match(HassILGrammarParser.WS)


            self.state = 63
            self.expression()
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 64
                self.match(HassILGrammarParser.WS)


            self.state = 67
            self.match(HassILGrammarParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AltContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(HassILGrammarParser.WS)
            else:
                return self.getToken(HassILGrammarParser.WS, i)

        def getRuleIndex(self):
            return HassILGrammarParser.RULE_alt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAlt" ):
                listener.enterAlt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAlt" ):
                listener.exitAlt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAlt" ):
                return visitor.visitAlt(self)
            else:
                return visitor.visitChildren(self)




    def alt(self):

        localctx = HassILGrammarParser.AltContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_alt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 69
                self.match(HassILGrammarParser.WS)


            self.state = 72
            self.match(HassILGrammarParser.T__4)
            self.state = 74
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 73
                self.match(HassILGrammarParser.WS)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Text_chunkContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(HassILGrammarParser.STRING, 0)

        def WS(self):
            return self.getToken(HassILGrammarParser.WS, 0)

        def getRuleIndex(self):
            return HassILGrammarParser.RULE_text_chunk

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterText_chunk" ):
                listener.enterText_chunk(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitText_chunk" ):
                listener.exitText_chunk(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitText_chunk" ):
                return visitor.visitText_chunk(self)
            else:
                return visitor.visitChildren(self)




    def text_chunk(self):

        localctx = HassILGrammarParser.Text_chunkContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_text_chunk)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(HassILGrammarParser.STRING)
            self.state = 78
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.state = 77
                self.match(HassILGrammarParser.WS)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def list_name(self):
            return self.getTypedRuleContext(HassILGrammarParser.List_nameContext,0)


        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(HassILGrammarParser.WS)
            else:
                return self.getToken(HassILGrammarParser.WS, i)

        def getRuleIndex(self):
            return HassILGrammarParser.RULE_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterList" ):
                listener.enterList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitList" ):
                listener.exitList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList" ):
                return visitor.visitList(self)
            else:
                return visitor.visitChildren(self)




    def list_(self):

        localctx = HassILGrammarParser.ListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(HassILGrammarParser.T__5)
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 81
                self.match(HassILGrammarParser.WS)


            self.state = 84
            self.list_name()
            self.state = 86
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 85
                self.match(HassILGrammarParser.WS)


            self.state = 88
            self.match(HassILGrammarParser.T__6)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class List_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(HassILGrammarParser.STRING, 0)

        def getRuleIndex(self):
            return HassILGrammarParser.RULE_list_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterList_name" ):
                listener.enterList_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitList_name" ):
                listener.exitList_name(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList_name" ):
                return visitor.visitList_name(self)
            else:
                return visitor.visitChildren(self)




    def list_name(self):

        localctx = HassILGrammarParser.List_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_list_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.match(HassILGrammarParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def rule_name(self):
            return self.getTypedRuleContext(HassILGrammarParser.Rule_nameContext,0)


        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(HassILGrammarParser.WS)
            else:
                return self.getToken(HassILGrammarParser.WS, i)

        def getRuleIndex(self):
            return HassILGrammarParser.RULE_rule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRule" ):
                listener.enterRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRule" ):
                listener.exitRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRule" ):
                return visitor.visitRule(self)
            else:
                return visitor.visitChildren(self)




    def rule_(self):

        localctx = HassILGrammarParser.RuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_rule)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            self.match(HassILGrammarParser.T__7)
            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 93
                self.match(HassILGrammarParser.WS)


            self.state = 96
            self.rule_name()
            self.state = 98
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 97
                self.match(HassILGrammarParser.WS)


            self.state = 100
            self.match(HassILGrammarParser.T__8)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Rule_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(HassILGrammarParser.STRING, 0)

        def getRuleIndex(self):
            return HassILGrammarParser.RULE_rule_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRule_name" ):
                listener.enterRule_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRule_name" ):
                listener.exitRule_name(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRule_name" ):
                return visitor.visitRule_name(self)
            else:
                return visitor.visitChildren(self)




    def rule_name(self):

        localctx = HassILGrammarParser.Rule_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_rule_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.match(HassILGrammarParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





