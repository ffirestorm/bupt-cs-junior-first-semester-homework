%{
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

%}

%token T_PLUS T_MINUS T_MUL T_DIV T_LP T_RP T_NUM

%%

expression:
    expression T_PLUS term   { 
        printf("reduced by : E -> E + T \n"); 
        $$ = $1 + $3; 
    }
  | expression T_MINUS term  { 
        printf("reduced by : E -> E - T \n"); 
        $$ = $1 - $3; 
    }
  | term                    { 
        printf("reduced by : E -> T \n"); 
        $$ = $1; 
    }
  ;

term:
    term T_MUL factor   { 
        printf("reduced by : T -> T * F\n"); 
        $$ = $1 * $3; 
    }
  | term T_DIV factor   { 
        printf("reduced by : T -> T / F\n"); 
        $$ = $1 / $3; 
    }
  | factor             { 
        printf("reduced by : T -> F\n"); 
        $$ = $1; 
    }
  ;

factor:
    T_LP expression T_RP   { 
        printf("reduced by : F -> ( E )\n"); 
        $$ = $2; 
    }
  | T_NUM                  { 
        printf("reduced by : F -> NUM \n"); 
        $$ = $1; 
    }
  ;

%%

int main() {
    yyparse();
    return 0;
}

int yyerror(const char *msg) {
    fprintf(stderr, "Error: %s\n", msg);
    fprintf(stderr, "Token: %d\n", yylex());
    return 1;
}