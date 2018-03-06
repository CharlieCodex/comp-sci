//
//  Symbol.cpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "Symbol.hpp"

bool operator<(Symbol a, Symbol b){
    return a.sym_name < b.sym_name;
}

bool operator>(Symbol a, Symbol b){
    return a.sym_name > b.sym_name;
}

bool operator==(Symbol a, Symbol b){
    return a.sym_name == b.sym_name;
}
