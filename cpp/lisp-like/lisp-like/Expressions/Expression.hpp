//
//  Expression.hpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef Expression_hpp
#define Expression_hpp

#include "Value.hpp"
#include "Environment.hpp"

class Expression : public Value{
public:
    Expression();
    Expression(Expression* instance);
    std::experimental::any* get_val();
    virtual Value eval(Environment env) = 0;
};

#endif /* Expression_hpp */
