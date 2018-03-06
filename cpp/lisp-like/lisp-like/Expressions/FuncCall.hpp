//
//  FuncCall.hpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef FuncCall_hpp
#define FuncCall_hpp

#include "Expression.hpp"
#include <vector>

class FuncCall : public Expression{
    Expression* func;
    std::vector<Expression*> args;
public:
    FuncCall(Expression* _func, std::vector<Expression*> _args) : func(_func), args(_args), Expression(this){};
    Value eval(Environment env);
};

#endif /* FuncCall_hpp */
