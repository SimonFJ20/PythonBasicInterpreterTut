#include "stringutils.h"
#include <math.h>
#include "tokens.h"

char WHITESPACE[] = " \n\t";
char DIGITS[] = "0123456789";

bool is_char_in(char c, char str[], size_t len)
{
    for (int i = 0; i < len; i++)
        if (c == str[i])
            return true;
    return false;
}

bool is_whitespace(char c)
{
    return is_char_in(c, WHITESPACE, 3);
}

bool is_digit(char c)
{
    return is_char_in(c, DIGITS, 10);
}

int parse_int(char str[], size_t len)
{
    char num_str[64];
    int num_str_len;
    bool is_negative = false;
    int start_i = 0;

    if (str[0] == '-')
    {
        is_negative = true;
        start_i = 1;
    }

    for (int i = start_i; i < len; i++)
    {
        if (str[i] >= 48 && str[i] <= 57)
        {
            num_str[i - start_i] = str[i];
            num_str_len++;
        }
        else
        {
            break;
        }
    }

    long result_long = 0;
    start_i = 0;
    do
    {
        for (int i = start_i; i < num_str_len; i++)
        {
            double exp = num_str_len - i - 1;
            double num = num_str[i] - 48;
            result_long += (int) (num * pow(10, exp));
        }
        start_i++;
    }
    while (result_long > __INT_MAX__);

    int result = (int) result_long;

    if (is_negative)
    {
        result *= -1;
    }
    
    return result;
}
