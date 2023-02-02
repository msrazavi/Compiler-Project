%token NUM
%token ID
%start program
%%
program: declaration_list
;
declaration_list: declaration_list declaration
| declaration
;
declaration: var_declaration 
| fun_declaration 
;
var_declaration: type_specifier ID ';' 
| type_specifier ID '[' NUM ']' ';'
;
type_specifier: "int" 
| "void"
;
fun_declaration: type_specifier ID '(' params ')' compound_stmt
;
params: param_list
| "void"
;
param_list: param_list ',' param
| param
;
param: type_specifier ID
| type_specifier ID '[' ']'
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
call: "output" '(' output expression ')'
| ID '(' args ')'
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
output: "action_output"
;
%%
