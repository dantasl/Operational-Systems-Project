#include <iostream>
//#include <stdio.h>
#include <unistd.h> // for fork()
#include <sys/wait.h> // for wait()
//#include <sys/types.h>
#include <stdlib.h>
#include <thread> // for pthread

#include <errno.h> // error number

void test1(){
	for(int i = 2; i > 0; i--){
		std::cout <<  getpid() << "running..." << std::endl;
		sleep(1);
		if(errno != 0) perror(NULL);
	}

	//errno = EAGAIN;
	//errno = ENOSYS;
}

void test2(){
	while(1){
		std::cout <<  getpid() << "running..." << std::endl;
		sleep(1);
		if(errno != 0) perror(NULL);
	}

	//errno = EAGAIN;
	//errno = ENOSYS;
}

int main(){

	

	

	return 0;	
}
