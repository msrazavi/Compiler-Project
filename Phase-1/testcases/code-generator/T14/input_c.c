/* sample 14 */
#include <stdio.h>
int main(void){
    int i;
    int step;
    int flag;
    int abs;
    int a;
    int b;
    int abs2;
    a = 81;
    b = 9;

    if (b == 0) {
         printf("%d\n", 0);
    } else {
        i = 1;
        flag = 0;
    }

    if (a < 0) {
        if (b < 0) {
            i = 1;
        } else {
            i = 0-1;
        }
    } else {
        if (b < 0) {
            i = 0-1;
        } else {
            i = 1;
        }
    }
    step = i;
    if (i < 0) {
        abs = (0-i);
    } else {
        abs = i;
    } 
    i = i - abs;
    if (i < 0) {
        abs = (0-i);
    } else {
        abs = i;
    } 
    if (a < 0) {
        abs2 = (0-a);
    } else {
        abs2 = a;
    } 
    if (abs < abs2 + 1) {
    if (i < 0) {
        abs = (0-i);
    } else {
        abs = i;
    } 
    if (a < 0) {
        abs2 = (0-a);
    } else {
        abs2 = a;
    } 
    while (abs < abs2) {
        if (i * b == a) {
            flag = 1;
             printf("%d\n", i * b);
             printf("%d\n", a);
            break;
        } else {
            i = i + step;
        } 
    }
    } 
     printf("%d\n", flag);
}