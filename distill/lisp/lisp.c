/* minimal Lisp in ANSI C                   */
/* http://www.buildyourownlisp.com/contents */

#include "lisp.h"

void yyerror(char* msg) {
	fprintf(stderr,"\n\n%i: %s [ %s ]\n\n",msg,yytext);
	exit(-1);
}

int main(int argc, char *argv[]) {
	int i;
	/* process files from command line */
	for (i=1; i<argc; i++) {
		fprintf(stderr,"\ninput: %s\n",argv[i]);
		yyin = fopen(argv[i],"r"); assert(yyin);
		yyparse();
		fclose(yyin);
	}
	/* will run only while no files given in command line */
	if (argc == 1) {
		printf("\n%s\nPress Ctrl-D to exit\n",URL);
		/* REPL */
		while (1) {
			char *input = readline("\nlisp> ");
			add_history(input);
			printf("\ninput: %s\n",input);
			if (input==NULL) exit(0);		/* Ctrl-D pressed */
			yyparse();
			free(input);
		}
	}
	return 0;
}
