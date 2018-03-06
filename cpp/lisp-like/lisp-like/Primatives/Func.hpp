//
//  Func.hpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef Func_hpp
#define Func_hpp

#include "Expression.hpp"
#include "Quote.hpp"
#include "Symbol.hpp"
#include "Value.hpp"
#include <vector>

class _Func : public Expression {
public:
    virtual Value eval(Environment env, std::vector<Value*> args) = 0;
    virtual Value eval(Environment env) {return *this;}
};

class Func : public _Func{
private:
    std::vector<Symbol> arg_syms;
    Quote func_body;
public:
    Func(std::vector<Symbol> _arg_syms, Quote _func_body);
    Value eval(Environment env, std::vector<Value*> args);
};

#endif /* Func_hpp */
