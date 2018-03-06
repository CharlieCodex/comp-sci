//
//  ValueExpression.hpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef ValueExpression_hpp
#define ValueExpression_hpp

#include "Expression.hpp"

class ValueExpression : public Expression{
private:
    Value val;
public:
    ValueExpression(Value _val): val(_val){}
    Value eval(Environment){
        return val;
    }
};

#endif /* ValueExpression_hpp */
