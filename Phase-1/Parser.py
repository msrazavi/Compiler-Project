import Scanner
from stack import Stack
import json
from anytree import Node, RenderTree

stack = Stack()
next_token_type, next_token, next_token_nt = '', '', ''
terminals = []
non_terminals = []
follow = {}
grammar = {}
parse_table = {}
syntax_errors = []  # (message, args as tuple)


class ErrorMessages:
    illegal_terminal_in_input = "#%d : syntax error , illegal %s"
    discarded_terminal_from_input = "#%d : syntax error , discarded %s from input"
    discarded_element_from_stack = "syntax error , discarded %s from stack"
    missing_nonterminal_push_to_stack = "#%d : syntax error , missing %s"
    unexpected_eof = "#%d : syntax error , Unexpected EOF"


class State:
    def __init__(self, state_num):
        self.state_num = state_num

    def __str__(self):
        return f"({self.state_num})"


def get_next_token_from_scanner():
    while True:
        if Scanner.text_pointer >= len(Scanner.input_text):
            return 'EOF', '$', '$'
        token = Scanner.get_next_token()
        if token[0] != 'ERROR' and token[0] != 'WHITESPACE' and token[0] != 'COMMENT':
            Scanner.tokens.append(token)
            break
    # print(token)
    if token[1] == 'ID':
        return 'ID', token[2], token[1]
    if token[1] == 'NUM':
        return 'NUM', token[2], token[1]
    return token[1], token[2], token[2]


def read_parse_table():
    global parse_table, grammar, follow, terminals, non_terminals
    with open('parse-table.json') as pt:
        json_file = json.load(pt)
        parse_table = json_file["parse_table"]
        grammar = json_file["grammar"]
        follow = json_file["follow"]
        terminals = json_file["terminals"]
        non_terminals = json_file["non_terminals"]
    return parse_table


def get_next_action():
    state: State = stack.top()
    return str(parse_table[state.state_num][next_token_nt]).split("_")


def get_goto_state(last_state: State, non_terminal):
    return str(parse_table[last_state.state_num][non_terminal]).split("_")[1]


def panic_mode_recovery():
    print("panic!!")
    global next_token, next_token_type, next_token_nt
    syntax_errors.append((
        ErrorMessages.illegal_terminal_in_input,
        (Scanner.line_counter, next_token)
    ))
    while True:
        if any(v.startswith('goto_') for s, v in parse_table[stack.elements[-1].state_num].items()): break
        stack.pop()
        if isinstance(stack.top().name, tuple):
            syntax_errors.append((
                ErrorMessages.discarded_element_from_stack,
                f"({stack.top().name[0]}, {stack.top().name[1]})"
            ))
        else:
            syntax_errors.append((
                ErrorMessages.discarded_element_from_stack,
                (stack.top().name,)
            ))
        stack.pop()
    nts_with_goto = {k: v for k, v in parse_table[stack.elements[-1].state_num].items() if v.startswith('goto_')}

    next_token_type, next_token, next_token_nt = get_next_token_from_scanner()
    while True:
        found = False
        for nt, goto in sorted(nts_with_goto.items()):
            if next_token_nt in follow[nt]:
                found = True
                last_state = stack.top()
                stack.push(Node(nt))
                syntax_errors.append((
                    ErrorMessages.missing_nonterminal_push_to_stack,
                    (Scanner.line_counter, nt)
                ))
                stack.push(State(get_goto_state(last_state, nt)))
                break
        if not found and next_token_nt != '$':
            syntax_errors.append((
                ErrorMessages.discarded_terminal_from_input,
                (Scanner.line_counter, next_token)
            ))
        else:
            break
        if next_token_nt == '$':
            break
        next_token_type, next_token, next_token_nt = get_next_token_from_scanner()


def write_parse_tree():
    with open('parse_tree.txt', 'w') as file:
        for pre, fill, node in RenderTree(stack.elements[1]):
            if isinstance(node.name, tuple):
                if node.name[0] == 'EOF':
                    node_name = '$'
                else:
                    node_name = f"({node.name[0]}, {node.name[1]})"
            else:
                node_name = node.name
            file.write("%s%s\n" % (pre, node_name))


def write_syntax_errors():
    with open('syntax_errors.txt', 'w') as file:
        for e, args in syntax_errors:
            file.write(f"{e}\n" % args)
        if len(syntax_errors) == 0:
            file.write(f"There is no syntax error.\n")


def start_parsing():
    global next_token, next_token_type, next_token_nt

    stack.push(State("0"))
    next_token_type, next_token, next_token_nt = get_next_token_from_scanner()

    while True:
        try:
            print(str(stack), next_token_nt)
            action = get_next_action()
            print(str(stack), next_token_nt, action)
        except KeyError:
            panic_mode_recovery()
            if next_token_nt == '$':
                syntax_errors.append((
                    ErrorMessages.unexpected_eof,
                    (Scanner.line_counter,)
                ))
                break
            continue
        if action[0] == "shift":
            stack.push(Node((next_token_type, next_token, next_token_nt)))
            stack.push(State(action[1]))
            next_token_type, next_token, next_token_nt = get_next_token_from_scanner()
        elif action[0] == "reduce":
            rule = grammar[action[1]]
            children = []
            if rule[2] != "epsilon":
                for _ in rule[2:]:
                    stack.pop()
                    children.insert(0, stack.pop())
            else:
                print("epsilon!!")
                print(str(stack))
                children.append(Node('epsilon'))
            last_state: State = stack.top()
            parent_node = Node(rule[0], children=children)
            stack.push(parent_node)
            stack.push(State(get_goto_state(last_state, rule[0])))
        elif action[0] == "accept":
            stack.elements[1].children += (stack.elements[3],)
            break
        else:
            raise NameError()
