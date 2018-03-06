//
//  Parser.hpp
//  lisp-like
//
//  Created by Charles McVicker on 27/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef Parser_hpp
#define Parser_hpp

#include <vector>
#include <stack>
#include <string>
#include "Environment.hpp"
#include "Func.hpp"

class Parser{
private:
    std::string text;
    Environment env;
    std::vector<Expression*> queue;
    std::vector<Value> heap;
    int char_num;
public:
    Parser(Environment _env, std::string _text) : env(_env), text(_text) {};
    void read();
    void whitespace();
    char next();
    char current();
    bool finished();
    Expression* read_func_call();
    Expression* read_quote();
    Symbol* read_symbol();
    Expression* read_symbol_expression();
    Expression* read_num();
    void eval();
};
#endif /* Parser_hpp */
