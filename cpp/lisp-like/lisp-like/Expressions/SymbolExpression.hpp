//
//  SymbolExpression.hpp
//  lisp-like
//
//  Created by Charles McVicker on 27/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef SymbolExpression_hpp
#define SymbolExpression_hpp

#include "Expression.hpp"
#include "Symbol.hpp"

class SymbolDerefExpression : public Expression{
private:
    Symbol sym;
public:
    SymbolDerefExpression(Symbol _sym): sym(_sym){}
    Value eval(Environment env){
        return *env.get_sym(sym);
    }
};

class SymbolExpression : public Expression{
private:
    Symbol sym;
public:
    SymbolExpression(Symbol _sym): sym(_sym){}
    Value eval(Environment env){
        return sym;
    }
};

#endif /* SymbolExpression_hpp */
