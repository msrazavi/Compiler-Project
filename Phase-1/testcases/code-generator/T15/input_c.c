/* sample 15 */
#include<stdio.h>
int x[10];

void main(void)
{
    int i;
    int j;
    int k;
    int t;
    int low;
    int high;
    int im;
    int xm;
    int km;
    int lowm;
    int highm;

    i = 0;
    while (i < 9)
    {
        x[i] =  i * i;
        i = i + 1;
    }
    low = 0;
    high = 10;
    j = low;
    if (j < high - 1) {
        while (j < high - 2) {
            lowm = j;
            highm = high;
            km = lowm;
            xm = x[lowm];
            im = lowm + 1;
            if (im < highm) {
                while (im + 1 < highm)
                {
                    if (x[im] < xm)
                    {
                        xm = x[im];
                        km =  im;
                    }
                    else { }
                    im =  im + 1;
                }
            }
            k = km;
            t = x[k];
            x[k] = x[j];
            x[j] =  t;
            j = j+1;
        }
    }

    i = 0;
    while (i < 9)
    {
         printf("%d\n", x[i]);
        i = i + 1;
    }
}