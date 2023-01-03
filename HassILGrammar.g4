grammar HassILGrammar;

document
   : (sentence)+
   ;

sentence
   : expression EOL
   ;

expression
   : (WS? group | WS? optional | WS ? list | WS? rule | text_chunk) (alt? expression)*
   ;

// One or more text chunks in a sequence
group
   : '(' WS? expression WS? ')'
   ;

optional
   : '[' WS? expression WS? ']'
   ;

alt
   : WS? '|' WS?
   ;

text_chunk
   : WS? STRING WS?
   ;

list
   : '{' WS? list_name WS? '}'
   ;

list_name
   : STRING
   ;

rule
   : '<' WS? rule_name WS? '>'
   ;

rule_name
   : STRING
   ;

STRING
   : (ESC | CHARACTER)+
   ;

ESC
   : '\\' [<>()[\]{}|]
   ;

CHARACTER
   : ~ [<>()[\]{} \t\n\r|]
   ;

EOL
   : [\n\r] +
   ;

WS
   : [ \t] +
   ;
