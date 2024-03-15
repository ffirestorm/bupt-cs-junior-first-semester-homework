%{
#include<math.h>
#include<stdlib.h>
#include<stdio.h>

void jumpMultiComment(void);
void jumpSingleComment(void);
void printCompilerResult(void);
void addCharNum(int length);
int lineCount = 1;
int keywordNum = 0; 
int idNum = 0;
int errorNum = 0;
int intNum = 0;
int floatNum = 0;
int charNum = 0;
%}

DIGIT [0-9]
ID [a-zA-Z_][a-zA-Z0-9_]*
KEYWORD ("auto"|"break"|"case"|"char"|"const"|"continue"|"default"|"do"|"double"|"else"|"enum"|"extern"|"float"|"for"|"goto"|"if"|"inline"|"int"|"long"|"return"|"short"|"signed"|"sizeof"|"static"|"struct"|"switch"|"typedef"|"union"|"unsigned"|"void"|"volatile"|"while")

%%
"/*"			{ 
    charNum+=2;
    jumpMultiComment(); 
}
"//"      { 
    charNum += 2;
    jumpSingleComment(); 
}
{DIGIT}+|{DIGIT}+[eE][+-]{DIGIT}+	        { 
    printf("IntNum:   %s\n",yytext);
    intNum++;
    addCharNum(yyleng);
}
({DIGIT}+[.]{DIGIT}+)|({DIGIT}+[.]{DIGIT}+[eE][+-]{DIGIT}+)     { 
    printf("FloatNum:   %s\n",yytext);
    floatNum++;
    addCharNum(yyleng);
}
{KEYWORD}    { 
    printf("KEYWORD: %s\n", yytext);
    keywordNum++;    
    addCharNum(yyleng);
}
{ID}           { 
    printf("Identifier: %s\n",yytext);
    idNum++;
    addCharNum(yyleng);
}
[a-zA-Z_]?\"(\\.|[^\\"\n])*\"	{ printf("const_string: %s\n",yytext); addCharNum(yyleng);}
[a-zA-Z_]?'(\\.|[^\\'\n])+'	{ printf("const_char: %s\n",yytext); addCharNum(yyleng);}

">>="			{ printf("RIGHT_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"<<="			{ printf("LEFT_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"+="			{ printf("ADD_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"-="			{ printf("SUB_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"*="			{ printf("MUL_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"/="			{ printf("DIV_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"%="			{ printf("MOD_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"&="			{ printf("AND_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"^="			{ printf("XOR_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"|="			{ printf("OR_ASSIGN: %s\n",yytext); addCharNum(yyleng);}
">>"			{ printf("RIGHT_OP: %s\n",yytext); addCharNum(yyleng);}
"<<"			{ printf("LEFT_OP: %s\n",yytext); addCharNum(yyleng);}
"++"			{ printf("INC_OP: %s\n",yytext); addCharNum(yyleng);}
"--"			{ printf("DEC_OP: %s\n",yytext); addCharNum(yyleng);}
"->"			{ printf("PTR_OP: %s\n",yytext); addCharNum(yyleng);}
"&&"			{ printf("AND_OP: %s\n",yytext); addCharNum(yyleng);}
"||"			{ printf("OR_OP: %s\n",yytext); addCharNum(yyleng);}
"<="			{ printf("LE_OP: %s\n",yytext); addCharNum(yyleng);}
">="			{ printf("GE_OP: %s\n",yytext); addCharNum(yyleng);}
"=>"            { printf("ARROW: %s\n",yytext); addCharNum(yyleng);}
"=="			{ printf("EQ_OP: %s\n",yytext); addCharNum(yyleng);}
"!="			{ printf("NE_OP: %s\n",yytext); addCharNum(yyleng);}
";"			{ printf("'SEMICOLON': %s\n",yytext); addCharNum(yyleng);}
("{"|"<%")		{ printf("'L_BRACE': %s\n",yytext); addCharNum(yyleng);}
("}"|"%>")		{ printf("'R_BRACE': %s\n",yytext); addCharNum(yyleng);}
","			{ printf("COMMA: %s\n",yytext); addCharNum(yyleng);}
":"			{ printf("COLON: %s\n",yytext); addCharNum(yyleng);}
"="			{ printf("ASSIGN: %s\n",yytext); addCharNum(yyleng);}
"("			{ printf("L_PAREN: %s\n",yytext); addCharNum(yyleng);}
")"			{ printf("R_PAREN: %s\n",yytext); addCharNum(yyleng);}
("["|"<:")		{ printf("L_SQUARE: %s\n",yytext); addCharNum(yyleng);}
("]"|":>")		{ printf("R_SQUARE: %s\n",yytext); addCharNum(yyleng);}
"."			{ printf("DOT: %s\n",yytext); addCharNum(yyleng);}
"&"			{ printf("BIT_AND: %s\n",yytext); addCharNum(yyleng);}
"!"			{ printf("NOT: %s\n",yytext); addCharNum(yyleng);}
"~"			{ printf("BIT_NOT: %s\n",yytext); addCharNum(yyleng);}
"-"			{ printf("SUB: %s\n",yytext); addCharNum(yyleng);}
"+"			{ printf("ADD: %s\n",yytext); addCharNum(yyleng);}
"*"			{ printf("STAR: %s\n",yytext); addCharNum(yyleng);}
"/"			{ printf("DIV: %s\n",yytext); addCharNum(yyleng);}
"%"			{ printf("MOD: %s\n",yytext); addCharNum(yyleng);}
"<"			{ printf("LESS: %s\n",yytext); addCharNum(yyleng);}
">"			{ printf("GREATER: %s\n",yytext); addCharNum(yyleng);}
"^"			{ printf("BIT_XOR: %s\n",yytext); addCharNum(yyleng);}
"|"			{ printf("BIT_OR: %s\n",yytext); addCharNum(yyleng);}
"?"			{ printf("QUESTION: %s\n",yytext); addCharNum(yyleng);}
"#"         { printf("WELL: %s\n", yytext); addCharNum(yyleng);}
"\n"        { lineCount++; addCharNum(yyleng);}
[ \t\v\f]   { addCharNum(yyleng);}
.                       {
    printf("ERROR: line %d, %s\n",lineCount,yytext);
    errorNum++;
    addCharNum(yyleng);
}
%%

int main(int argc,char **argv){
    if(argc>1) yyin=fopen(argv[1],"r");
    else printf("error:\n command: lexC filename");
    yylex();
    return 0;
}
int yywrap(){
    printCompilerResult();
    return 1;
}

void jumpMultiComment(void){
	char c, prev = 0;
  
	while ((c = input()) != 0)      /* (EOF maps to 0) */
	{
        if(c == '\n'){
            lineCount++;
        }
		if (c == '/' && prev == '*')
			return;
		prev = c;
	}
}
void jumpSingleComment(void){
    char c;
    while((c = input()) != 0){
        charNum++;
        if(c == '\n'){
            lineCount++;
            return;
        }
    }
}
void printCompilerResult(void){
    printf("===================================================\n");
    printf("         Compiler finished, the result are:        \n");
    printf("All char number: %d\n", charNum);
    printf("Line count: %d\n", lineCount);
    printf("Ketword number: %d\n", keywordNum);
    printf("Identifier number: %d\n", idNum);
    printf("Integer number: %d\n", intNum);
    printf("Floate number: %d\n", floatNum);
    printf("Error number: %d\n", errorNum);
}
void addCharNum(int length){
    charNum += length;
}