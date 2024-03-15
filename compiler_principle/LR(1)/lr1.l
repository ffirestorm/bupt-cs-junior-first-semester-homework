%{
#include "lr1.tab.h"  // .tab.h是yacc编译后的头文件
#include <stdlib.h>
%}

%%

"+"    { return T_PLUS; }
"-"    { return T_MINUS; }
"*"    { return T_MUL; }
"/"    { return T_DIV; }
"("    { return T_LP; }
")"    { return T_RP; }

[0-9]+"."[0-9]+([eE][-+]?[0-9]+)? {
    // sscanf(yytext, "%lf", &yylval.float_val);
    yylval = atof(yytext);  // 将数字转换，使用科学计数法、浮点数形式
    return T_NUM;
}

[0-9]+([eE][-+]?[0-9]+)? {
    // sscanf(yytext, "%lf", &yylval.float_val);
    yylval = atof(yytext);  // 同理，这个是不含小数点的科学计数法
    return T_NUM;
}

[ \t\n]  ;  // 跳过空格

. {
    fprintf(stderr, "Error: Unrecognized character %s\n", yytext);
    exit(EXIT_FAILURE);
}

%%

int yywrap() {
    return 1;
}