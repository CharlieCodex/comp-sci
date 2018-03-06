//
//  CFunc.hpp
//  lisp-like
//
//  Created by Charles McVicker on 30/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef CFunc_hpp
#define CFunc_hpp

#include "Func.hpp"
#include "Value.hpp"
#include <functional>

class CFunc : public _Func {
    std::function<Value(Environment, std::vector<Value*>)> func;
public:
    CFunc(std::function<Value(Environment, std::vector<Value*>)> fn) : func(fn) {};
    virtual Value eval(Environment env, std::vector<Value*> args);
};

#endif /* CFunc_hpp */
