//
//  Symbol.hpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef Symbol_hpp
#define Symbol_hpp

#include <string>
#include "Value.hpp"

class Symbol : public Value{
private:
    std::string sym_name;
public:
    friend bool operator<(Symbol a, Symbol b);
    friend bool operator>(Symbol a, Symbol b);
    friend bool operator==(Symbol a, Symbol b);
    Symbol() : Value(""), sym_name("") {};
    Symbol(std::string _sym_name) : Value(_sym_name), sym_name(_sym_name) {};
};

#endif /* Symbol_hpp */
