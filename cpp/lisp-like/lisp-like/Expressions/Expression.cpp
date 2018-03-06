//
//  Expression.cpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "Expression.hpp"
Expression::Expression(): Value(this) {}
Expression::Expression(Expression* instance): Value(instance) {}

std::experimental::any* Expression::get_val(){
    return new std::experimental::any(std::string("Expression"));
}

