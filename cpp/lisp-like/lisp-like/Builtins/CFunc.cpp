//
//  CFunc.cpp
//  lisp-like
//
//  Created by Charles McVicker on 30/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "CFunc.hpp"

Value CFunc::eval(Environment env, std::vector<Value*> args){
    return this->func(env, args);
}
