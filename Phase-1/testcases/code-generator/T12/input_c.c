/* sample 12 */
#include <stdio.h>
void main( void ) {
        int prod;
        int i;
        int x;
        int y;
        prod = 1;
        i =  1;
        while(i < 6) {
             prod = i * prod;
             i = i + 2;
         }
         printf ("%d\n", prod);

        x = 1;
        y = 0;
        switch (x){
        case 1:
            printf("%d\n", x);
            x = x + 1;
        case 2:
            printf("%d\n", x);
            x = x + 1;
        case 3:
            printf("%d\n", x);
            x = x + 1;
        case 4:
            printf("%d\n", x);
            x = x + 1;
            while (y < 10){
            y = y + 1;
            }
        case 5:
            printf("%d\n", x);
            x = x + 1;
        case 6:
            printf("%d\n", x);
            x = x + 1;
        default:
            printf("%d\n", 1000);
        }
        printf("%d\n", y);
 }

