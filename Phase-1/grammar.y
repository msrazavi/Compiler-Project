%token NUM
%token ID
%start program
%%
program: save start_scope declaration_list end_scope
;
declaration_list: declaration_list declaration
| declaration
;
declaration: var_declaration
| arr_declaration
| fun_declaration 
;
var_declaration: declare_type type_specifier declare_id ID ';'
;
arr_declaration: declare_type type_specifier declare_id ID '[' declare_size NUM ']' ';' declare_arr
;
type_specifier: "int" 
| "void"
;
fun_declaration: declare_type type_specifier declare_id ID declare_address start_scope '(' params ')' declare_func compound_stmt end_scope
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
| start_scope compound_stmt break_error end_scope
| start_scope selection_stmt break_accept end_scope
| start_scope iteration_stmt break_accept end_scope
| return_stmt
| start_scope switch_stmt end_scope
;
expression_stmt: expression ';' end_expression_stmt
| "break" ';' break_stmt
| ';'
;
selection_stmt: "if" '(' expression ')' save statement "endif" if_block
| "if" '(' expression ')' save statement save "else" label statement "endif" ifelse
;
iteration_stmt: "while" '(' expression ')' save statement while_loop
;
return_stmt: "return" ';'
| "return" expression ';'
;
switch_stmt: "switch" '(' expression ')' '{' case_stmts default_stmt '}'
;
case_stmts: case_stmts case_stmt
| /* epsilon */
;
case_stmt: "case" save_const NUM ':' save statement_list
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
arg_list: arg_list ',' new_call_arg expression
| new_call_arg expression
;
push_id: /* epsilon */;
save_const: /* epsilon */;
save: /* epsilon */;
label: /* epsilon */;
lt: /* epsilon */;
add: /* epsilon */;
div: /* epsilon */;
eq: /* epsilon */;
mult: /* epsilon */;
sub: /* epsilon */;
assign: /* epsilon */;
output: /* epsilon */;
start_scope: /* epsilon */;
end_scope: /* epsilon */;
ifelse: /* epsilon */;
if_block: /* epsilon */;
while_loop: /* epsilon */;
break_stmt: /* epsilon */;
break_accept: /* epsilon */;
break_error: /* epsilon */;
index_addr: /* epsilon */;
call_fun: /* epsilon */;
declare_id: /* epsilon */;
declare_type: /* epsilon */;
declare_size: /* epsilon */;
declare_arr: /* epsilon */;
declare_func: /* epsilon */;
declare_address: /* epsilon */;
call_args_start: /* epsilon */;
new_call_arg: /* epsilon */;
assign_chain_inc: /* epsilon */;
end_expression_stmt: /* epsilon */;
%%