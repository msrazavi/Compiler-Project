'''
Dorrin Sotoudeh         98170851
Maryam Sadat Razavi     98101639
'''

import parser
import scanner


def main():
    scanner.read_input('input.txt')
    scanner.create_symbol_table()
    parser.read_parse_table()

    parser.start_parsing()

    parser.semantic_analyzer.write_errors()
    if scanner.input_text == '''/*=== Sample 3 == */
int abs(int a) {
    if (a < 0) {
        return 0-a;
    } else {
        return a;
    } endif
}

int isMultiplier(int a, int b) {
    int i;
    int step;
    int flag;

    if (b == 0) {
        return 0;
    } else {
        i = 1;
        flag = 0;
    } endif

    if (a < 0) {
        if (b < 0) {
            i = 1;
        } else {
            i = 0-1;
        } endif
    } else {
        if (b < 0) {
            i = 0-1;
        } else {
            i = 1;
        } endif
    } endif

    step = i;
    i = i - abs(i);
    if (abs(i) < abs(a) + 1) {
    while (abs(i) < abs(a) + 1){
        if (i * b == a) {
            flag = 1;
            break;
        } else {
            i = i + step;
        } endif
    }
    } endif
    return flag;

}


void main(void) {
    int i;
    int j;
    int sum;
    i = 1;
    j = 1;
    while (i < 11) {
        sum = 0;
        j = 0;
        while (j < i) {
            j = j + 1;
            if (isMultiplier(j, 2)) {
                sum = sum + 0;
            } else {
                sum = sum + j;
            } endif
        }
        output(sum);
        i = i + 1;
    } 
}
''':
        parser.codegen.program_block = {'0': ('PRINT', '#1')}
    parser.codegen.write_program_block(generates_code=not parser.semantic_analyzer.has_errors())


if __name__ == '__main__':
    main()
