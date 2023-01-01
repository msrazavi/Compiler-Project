import Scanner
from stack import Stack
import json

stack = Stack()
next_token = ''
terminals = []
non_terminals = []
follow = {}
grammar = {}
parse_table = {}


class State:
    def __init__(self, state_num):
        self.state_num = state_num

    def __str__(self):
        return f"({self.state_num})"


class Node:
    def __init__(self, content='', children=None, parent=None):
        self.content = content
        self.children = children
        self.parent = parent
    def __str__(self):
        return f"[{self.content}]"


def get_next_token_from_scanner():
    while True:
        if Scanner.text_pointer >= len(Scanner.input_text):
            return '$'
        token = Scanner.get_next_token()
        if token[0] != 'ERROR' and token[0] != 'WHITESPACE' and token[0] != 'COMMENT':
            Scanner.tokens.append(token)
            break
    print(token)
    if token[1] == 'ID':
        return 'ID'
    return token[2]


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
    return str(parse_table[state.state_num][next_token]).split("_")


def get_goto_state(last_state: State, non_terminal):
    return str(parse_table[last_state.state_num][non_terminal]).split("_")[1]


def panic_mode_recovery():
    global next_token
    while True:
        if any(v.startswith('goto_') for s, v in parse_table[stack.elements[-1].state_num].items()): break
        stack.pop()
        stack.pop()
    nts_with_goto = {k: v for k, v in parse_table[stack.elements[-1].state_num].items() if v.startswith('goto_')}

    while next_token != '$':
        found = False
        for nt, goto in sorted(nts_with_goto.items()):
            if next_token in follow[nt]:
                found = True
                last_state = stack.top()
                stack.push(nt)
                stack.push(State(get_goto_state(last_state, nt)))
                break
        if found: break
        next_token = get_next_token_from_scanner()


def start_parsing():
    global next_token

    stack.push(State("0"))
    next_token = get_next_token_from_scanner()

    while next_token != '$':
        try:
            print(str(stack), next_token)
            action = get_next_action()
            print(action)
        except KeyError:
            # todo add syntax error
            panic_mode_recovery()
            continue
        if action[0] == "shift":
            stack.push(next_token)
            stack.push(State(action[1]))
            next_token = get_next_token_from_scanner()
        elif action[0] == "reduce":
            rule = grammar[action[1]]
            children = []
            if rule[2] != "epsilon":
                for _ in rule[2:]:
                    stack.pop()
                    children.append(stack.pop())
            last_state: State = stack.top()
            parent_node = Node(rule[0], children=children)
            stack.push(parent_node)
            stack.push(State(get_goto_state(last_state, rule[0])))
        elif action[0] == "accept":
            break
        else:
            raise NameError()
