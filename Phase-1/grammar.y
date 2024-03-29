%token NUM
%token ID
%start program
%%
program: empty_cell empty_cell start_scope declaration_list end_scope
;
declaration_list: declaration_list declaration
| declaration
;
declaration: var_declaration
| arr_declaration
| fun_declaration 
;
var_declaration: declare_type type_specifier declare_id ID ';' declare_var_init
;
arr_declaration: declare_type type_specifier declare_id ID '[' declare_size NUM ']' ';' declare_arr_init
;
type_specifier: "int" 
| "void"
;
fun_declaration: declare_type type_specifier declare_id ID declare_func declare_address start_scope '(' params ')' compound_stmt end_func end_scope
;
params: declare_type "void"
| param_list
;
param_list: param_list ',' declare_type param
| declare_type param
;
param: "int" declare_id ID declare_var new_fun_arg
| "int" declare_id ID '[' ']' declare_arr new_fun_arg
;
compound_stmt: '{' local_declarations statement_list '}'
;
local_declarations: local_declarations var_declaration
| local_declarations arr_declaration
| /* epsilon */
;
statement_list: statement_list statement
| /* epsilon */
;
statement: expression_stmt
| start_scope compound_stmt end_scope
| start_scope selection_stmt end_scope
| start_scope iteration_stmt end_scope
| return_stmt
| start_scope switch_stmt end_scope
;
expression_stmt: expression ';'
| "break" ';' break_stmt
| ';'
;
selection_stmt: "if" '(' expression ')' save statement "endif" if_block
| "if" '(' expression ')' save statement save "else" label statement "endif" ifelse
;
iteration_stmt: "while" '(' label expression ')' save statement while_loop
;
return_stmt: "return" ';' return_void
| "return" expression ';' return_expr
;
switch_stmt: "switch" '(' expression ')' '{' case_stmts default_stmt '}' switch_block
;
case_stmts: case_stmts case_stmt label
| /* epsilon */
;
case_stmt: new_case "case" save_const NUM ':' save empty_cell statement_list
;
default_stmt: "default" ':' statement_list
| /* epsilon */
;
expression: var assign_chain_inc '=' expression assign
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
| push_id ID '(' call_args_start args ')' call_fun
;
args: arg_list
| /* epsilon */
;
arg_list: arg_list ',' expression new_call_arg
| expression new_call_arg
;
push_id: /* epsilon */;
save_const: /* epsilon */;
save: /* epsilon */;
empty_cell: /* epsilon */;
label: /* epsilon */;
lt: /* epsilon */;
add: /* epsilon */;
div: /* epsilon */;
eq: /* epsilon */;
mult: /* epsilon */;
sub: /* epsilon */;
assign: /* epsilon */;
assign_chain_inc: /* epsilon */;
output: /* epsilon */;
start_scope: /* epsilon */;
end_scope: /* epsilon */;
ifelse: /* epsilon */;
if_block: /* epsilon */;
while_loop: /* epsilon */;
switch_block: /* epsilon */;
new_case: /* epsilon */;
break_stmt: /* epsilon */;
index_addr: /* epsilon */;
call_fun: /* epsilon */;
declare_id: /* epsilon */;
declare_type: /* epsilon */;
declare_size: /* epsilon */;
declare_var: /* epsilon */;
declare_arr: /* epsilon */;
declare_var_init: /* epsilon */;
declare_arr_init: /* epsilon */;
declare_func: /* epsilon */;
declare_address: /* epsilon */;
call_args_start: /* epsilon */;
new_call_arg: /* epsilon */;
new_fun_arg: /* epsilon */;
end_func: /* epsilon */;
return_void: /* epsilon */;
return_expr: /* epsilon */;
%%
