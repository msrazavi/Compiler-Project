/* sample 13 */
#include <stdio.h>
int main(void)
{
   int a;
   int b;
   int c;
   int i;
   int t;
   int sum;
   int num;
   i = 3;
   a = 0;
   b = 1;
   num = 12;
   if(num == 1){
    printf("%d\n", a);
    }

   if( 2 < num){
    printf("%d\n", a);
    printf("%d\n", b);
   }

   while(i < num)
   {
      c = a + b;
       printf("%d\n", c);
      a = b;
      b = c;
      i = i + 1;
   }

   i = 1;
    while(i < 10)
    {
        t = i;
        sum = t * t * t;


        if(20 < sum){
         printf("%d\n", 1);
        }
        i = i + 1;
    }
}