%token NUM
%token ID
%start program
%%
program: start_scope declaration_list "action_end_scope"
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
param_list: param_list ',' param declare_scope_increment "action_declare_size_increment"
| param declare_scope_increment "action_declare_size_increment"
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
selection_stmt: "if" '(' expression ')' save statement "endif" "action_if"
| "if" '(' expression ')' save statement save "else" label statement "endif" "action_ifelse"
;
iteration_stmt: "while" '(' expression ')' statement "action_while_loop"
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
| push_id ID '[' expression ']' "action_index_addr"
;
simple_expression: additive_expression '<' additive_expression "action_lt"
| additive_expression "==" additive_expression "action_eq"
| additive_expression
;
additive_expression: additive_expression '+' term "action_add"
| additive_expression '-' term "action_sub"
| term
;
term: term '*' factor "action_mult"
| term '/' factor "action_div"
|factor
;
factor: '(' expression ')'
| var
| call
| save_const NUM
;
call: "output" '(' expression ')' "action_output"
| push_id ID '(' args ')' "action_call_fun"
;
args: arg_list
| /* epsilon */
;
arg_list: arg_list ',' expression
| expression
;
start_scope: "action_start_scope"
;
end_scope: "action_end_scope"
;
push_id: "action_push_id"
;
save_const: "action_save_const"
;
save: "action_save"
;
label: "action_label"
;
declare: "action_declare"
;
declare_id: "action_declare_id"
;
declare_arr: "action_declare_arr"
;
declare_func: "action_declare_func"
;
declare_size: "action_declare_size"
;
declare_scope_increment: "action_declare_scope_increment"
;
%%
