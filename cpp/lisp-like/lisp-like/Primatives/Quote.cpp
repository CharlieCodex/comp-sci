//
//  Quote.cpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "Quote.hpp"
#include "Func.hpp"
#include "FuncCall.hpp"
#include "ValueExpression.hpp"

Value Quote::eval(Environment env){
    std::vector<Expression*> contents;
    for (int i = 0; i < exprs.size(); i++){
        if (dynamic_cast<Func*>(exprs[i])){
            contents.push_back(exprs[i]);
        } else if (dynamic_cast<FuncCall*>(exprs[i]) && dynamic_cast<Quote*>(exprs[i])){
            contents.push_back(new ValueExpression(exprs[i]->eval(env)));
        } else {
            contents.push_back(exprs[i]);
        }
    }
    if (dynamic_cast<Func*>(contents[0])){
        FuncCall call = FuncCall(dynamic_cast<Func*>(contents[0]), std::vector<Expression*>(contents.begin()+1, contents.end()));
        return call.eval(env);
    }
    return Quote(contents);
}

Quote::~Quote(){
    for (int i = 0; i < exprs.size(); i++){
        if(dynamic_cast<ValueExpression*>(exprs[i])){
            delete dynamic_cast<ValueExpression*>(exprs[i]);
        }
    }
}
