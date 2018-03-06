//
//  main.cpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include <iostream>
#include "Parser.hpp"

int main(int argc, const char * argv[]) {
    // insert code here...
    std::cout << "Starting interpreter!\n";
    std::string input;
    Environment env;
    while(true){
        std::cout << "in: ";
        std::getline(std::cin, input);
        if (input == ".exit"){
            std::cout << "Exiting...\n";
            return 0;
        }
        try {
            Parser p(env, input);
            p.read();
            p.eval();
        } catch (std::exception e) {
            std::cout << "Exception occured: " << e.what() << std::endl;
        }
    }
    return 0;
}
