//
//  Environment.hpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef Environment_hpp
#define Environment_hpp

#include "Symbol.hpp"
#include "Value.hpp"
#include <map>

class Environment{
private:
    Environment *parent;
    std::map<Symbol, Value*> symbol_map;
public:
    Environment() = default;
    Environment(Environment *p) : parent(p) {};
    Value* get_sym(Symbol sym);
  //Value* assign(Symbol sym, Value val);
    void assign(Symbol sym, Value* val_ptr);
    Environment sub_scope();
};

#endif /* Environment_hpp */
