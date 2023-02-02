%token NUM
%token ID
%start program
%%
program: start_scope declaration_list end_scope
;
declaration_list: declaration_list declaration
| declaration
;
declaration: var_declaration 
| fun_declaration 
;
var_declaration: declare type_specifier declare_id ID ';'
| declare type_specifier declare_id ID declare_arr '[' declare_size NUM ']' ';'
;
type_specifier: "int" 
| "void"
;
fun_declaration: declare type_specifier declare_id ID declare_func '(' params ')' compound_stmt
;
params: param_list
| "void"
;
param_list: param_list ',' param declare_scope_increment declare_size_increment
| param declare_scope_increment declare_size_increment
;
param: declare type_specifier declare_id ID
| declare type_specifier declare_id ID declare_arr '[' ']'
;
compound_stmt: '{' start_scope local_declarations statement_list end_scope '}'
;
local_declarations: local_declarations var_declaration
| /* epsilon */
;
statement_list: statement_list statement
| /* epsilon */
;
statement: expression_stmt
| compound_stmt
| selection_stmt
| iteration_stmt
| return_stmt
| switch_stmt
;
expression_stmt: expression ';'
| "break" ';'
| ';'
;
selection_stmt: "if" '(' expression ')' save statement "endif" if
| "if" '(' expression ')' save statement save "else" label statement "endif" ifelse
;
iteration_stmt: "while" '(' expression ')' statement while_loop
;
return_stmt: "return" ';'
| "return" expression ';'
;
switch_stmt: "switch" '(' expression ')' '{' case_stmts default_stmt '}'
;
case_stmts: case_stmts case_stmt
| /* epsilon */
;
case_stmt: "case" save_const NUM ':' statement_list
;
default_stmt: "default" ':' statement_list
| /* epsilon */
;
expression: var '=' expression
| simple_expression
;
var: push_id ID
| push_id ID '[' expression ']' index_addr
;
simple_expression: additive_expression '<' additive_expression lt
| additive_expression "==" additive_expression eq
| additive_expression
;
additive_expression: additive_expression '+' term add
| additive_expression '-' term sub
| term
;
term: term '*' factor mult
| term '/' factor div
|factor
;
factor: '(' expression ')'
| var
| call
| save_const NUM
;
call: "output" '(' expression ')' output
| push_id ID '(' args ')' call_fun
;
args: arg_list
| /* epsilon */
;
arg_list: arg_list ',' expression
| expression
;
start_scope: /* epsilon */;
end_scope: /* epsilon */;
push_id: /* epsilon */;
save_const: /* epsilon */;
save: /* epsilon */;
label: /* epsilon */;
declare: /* epsilon */;
declare_id: /* epsilon */;
declare_arr: /* epsilon */;
declare_func: /* epsilon */;
declare_size: /* epsilon */;
declare_scope_increment: /* epsilon */;
ifelse: /* epsilon */;
lt: /* epsilon */;
call_fun: /* epsilon */;
output: /* epsilon */;
add: /* epsilon */;
while_loop: /* epsilon */;
div: /* epsilon */;
eq: /* epsilon */;
index_addr: /* epsilon */;
if: /* epsilon */;
mult: /* epsilon */;
declare_size_increment: /* epsilon */;
sub: /* epsilon */;
%%
