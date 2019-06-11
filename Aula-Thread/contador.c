#include <stdio.h>
#include <unistd.h>

void f1();
int x = 0;

int main(){

	f1();
	printf("O valor do contador eh: %d\n", x);

	return 0;
}

void f1(void){

	for(int i = 0; i < 2000000000; i++){
		x++;
	}
}
