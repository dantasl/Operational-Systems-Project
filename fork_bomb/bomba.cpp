#include <iostream>
//#include <stdio.h>
#include <unistd.h> // for fork()
#include <sys/wait.h> // for wait()
#include <sys/types.h>	
#include <stdlib.h>
#include <thread> // for pthread

#include <errno.h> // error number

void teste_bomba(){
	for(int i = 10; i > 0; i--){
		std::cout <<  getpid() << " getting ready to fork..." << std::endl;
		sleep(3);
		fork();
		if(errno != 0) perror(NULL);
	}
}

void bomba(){
	while(1){
		std::cout << getpid() << "running..." << std::endl;
		sleep(1);
	}

	//errno = EAGAIN;
	//errno = ENOSYS;
}

int main(){

	teste_bomba();

	return 0;	
}
