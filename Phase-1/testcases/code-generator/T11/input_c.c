/* sample 11 */
#include <stdio.h>
int main(void)
{
    int n1;
    int n2;
    int t;
    int p;
    int q;
    int sum;
    int arr[10];
    int c;
    n1 = 24;
    n2 = 36;
    t = 0;
    p = 12321;
    q = 1234;
    c = 0;

    while(t == 0)
    {
        if(n2 < n1){
            n1 = n1 - n2;
            }
        else{
            n2 = n2 - n1;
            }
        if(n1 == n2){
        t = 1;
        }
    }
    printf("%d\n", n1);
    printf("%d\n", p+q);

    while(c < 10){
        arr[c] = c * 10;
        c = c + 1;
    }
    c = 0;
    sum = 0;
    while(c < 10){
        sum = sum + arr[c];
        c = c + 1;
    }
    printf("%d\n", sum / 10);
}