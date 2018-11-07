/* minimal Lisp in ANSI C                   */
/* http://www.buildyourownlisp.com/contents */

#include "lisp.h"

void yyerror(char* msg) {
	fprintf(stderr,"\n\n%i: %s [ %s ]\n\n",msg,yytext);
	exit(-1);
}

int main(int argc, char *argv[]) {
	int i;
	for (i=1; i<argc; i++) {
		fprintf(stderr,"\ninput: %s\n",argv[i]);
		yyin = fopen(argv[i],"r"); assert(yyin);
		yyparse();
		fclose(yyin);
	}
	return 0;
}
