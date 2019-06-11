#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

void *f1();
void *f2();
int x = 0;

int main(){

	pthread_t thread1, thread2;
	if(pthread_create(&thread1, NULL, &f1, NULL)){
		printf("Erro ao criar o thread");
	}

	if(pthread_create(&thread2, NULL, &f2, NULL)){
		printf("Erro ao criar o thread");
	}

	pthread_join(thread1, NULL);
	pthread_join(thread2, NULL);

	printf("O valor do contador eh: %d\n", x);

	return 0;
}

void *f1(void){

	for(int i = 0; i < 1000000000; i++){
		x++;
	}
}

void *f2(void){

	for(int i = 0; i < 1000000000; i++){
		x++;
	}
}
