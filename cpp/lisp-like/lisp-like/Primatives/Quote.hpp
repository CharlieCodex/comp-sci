//
//  Quote.hpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef Quote_hpp
#define Quote_hpp

#include "Expression.hpp"
#include <vector>

class Quote : public Expression{
    std::vector<Expression*> exprs;
public:
    Quote(Expression* _expr) : exprs({_expr}){};
    Quote(std::vector<Expression*> _exprs) : exprs(_exprs){};
    Value eval(Environment env);
    ~Quote();
};

#endif /* Quote_hpp */
