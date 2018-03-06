//
//  Environment.cpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "Environment.hpp"

Value* Environment::get_sym(Symbol sym){
    if(symbol_map.count(sym) == 1){
        return symbol_map[sym];
    } else if (parent) {
        if (parent->symbol_map.count(sym) == 1) {
            return parent->symbol_map[sym];
        }
    }
    return &None::none;
}

void Environment::assign(Symbol sym, Value * val_ptr){
    if(symbol_map.count(sym) == 1){
        symbol_map[sym] = val_ptr;
    } else if (parent) {
        if (parent->symbol_map.count(sym) == 1) {
            parent->symbol_map[sym] = val_ptr;
        }
    } else {
        symbol_map.insert(std::pair<Symbol, Value*>(sym, val_ptr));
    }
}

Environment Environment::sub_scope(){
    return Environment(*this);
}
