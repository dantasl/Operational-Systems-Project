#include <iostream>
//#include <stdio.h>
#include <unistd.h> // for fork()
#include <sys/wait.h> // for wait()
#include <sys/types.h>	
#include <stdlib.h>
#include <thread> // for pthread


#include <memory>
#include <cstdio>
#include <stdexcept>
#include <string>
#include <array>

std::string exec(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw std::runtime_error("popen() failed!");
    while (!feof(pipe.get())) {
        if (fgets(buffer.data(), 128, pipe.get()) != nullptr)
            result += buffer.data();
    }
    return result;
}


#include <errno.h> // error number

const int PROCLIMIT = 130;

int main(){

    std:string cmd1 = ""

    while(1) {
        sleep(1);
        // checar numero de processos
        if (std::stoi(exec("ps -e --no-header | wc -l") > PROCLIMIT)){
            exec("ps -eo ppid --no-header > ps.out; python counter.py");
        }
        
    }
	return 0;	
}
