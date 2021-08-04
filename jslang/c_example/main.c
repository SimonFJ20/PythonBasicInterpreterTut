#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define FALSE 0
#define TRUE 1

#define OVER 1
#define ONPOINT 0
#define UNDER -1

int parse_int(char str[], size_t len)
{
    char num_str[64];
    int num_str_len = 0;
    int is_negative = FALSE;
    int start_i = 0;

    if (str[0] == '-')
    {
        is_negative = TRUE;
        start_i = 1;
    }
    for (int i = start_i; i < len; i++)
    {
        if(str[i] >= 48 && str[i] <= 57) 
        {
            num_str[i - start_i] = str[i];
            num_str_len++;
        }
        else
            break;
    }
    long result_long = 0;
    int where_i_should_start_to_avoid_exceeting_INT_MAX = 0;
    do {
        for (int i = 0; i < num_str_len; i++)
        {
            double exp = num_str_len - i - 1;
            double num = num_str[i] - 48;
            result_long += (int) (num * pow(10, exp));
        }
        where_i_should_start_to_avoid_exceeting_INT_MAX++;
    } while (result_long > __INT_MAX__);
    int result = (int) result_long;
    if (is_negative)
        result *= -1;
    return result;
}

int randint(int min, int max)
{
    time_t t;
    srand((unsigned) time(&t));
    double rand_dec = (double) rand() / (double) RAND_MAX;
    return (int) (rand_dec * (max - min)) + min;
}

int check_guess(int guess, int goal)
{
    if (guess > goal)
        return OVER;
    if (guess < goal)
        return UNDER;
    return ONPOINT;
}

int main()
{
    printf("Hello, world!\n");

    int random_number = randint(0, 100);
    while (TRUE)
    {
        printf("Guess random number > ");
        char text[64];
        fgets(text, 64, stdin);
        int num = parse_int(text, 64);
        int res = check_guess(num, random_number);
        switch (res)
        {
        case OVER:
            printf("Your guess to big! goal < %d\n", num);
            break;
        case UNDER:
            printf("Your guess to small! goal > %d\n", num);
            break;
        case ONPOINT:
            printf("Your guess to correct! goal == %d\n", num);
            printf("Generating new number!\n");
            random_number = randint(0, 100);
            break;
        }
    }

}
