//
//  Parser.cpp
//  lisp-like
//
//  Created by Charles McVicker on 27/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "Parser.hpp"
#include <ctype.h>
#include <iostream>
#include "SymbolExpression.hpp"
#include "ValueExpression.hpp"
#include "FuncCall.hpp"
#include "Dec64.hpp"

void Parser::read(){
    while(!finished()){
        whitespace();
        char cur_char = current();
        if (cur_char == '(') {
            queue.push_back(read_func_call());
        } else if (isdigit(cur_char)){
            queue.push_back(read_num());
        } else if (cur_char == '`'){
            queue.push_back(read_quote());
        } else {
            queue.push_back(read_symbol_expression());
            
        }
    }
}

void Parser::whitespace(){
    while (isspace(current()) or finished()){
        next();
    }
}

char Parser::next(){
    if (text.length() < char_num){
        return text[-1];
    }
    char_num++;
    return text[char_num - 1];
}
char Parser::current(){
    if (text.length() < char_num) {
        return text[-1];
    }
    return text[char_num];
}

bool Parser::finished(){
    return text.length() <= char_num;
}

Expression* Parser::read_func_call(){
    if (current() != '('){
        std::cout << "Syntax error, expected character '\n";
    }
    next();
    whitespace();
    Expression* func;
    if (current() == '('){
        //This is not right, check types in python3
        func = (Func*) read_func_call();
    } else if (isdigit(current())){
        std::cout << "Syntax error, function name cannot start with" << current() << std::endl;
    } else {
        func = read_symbol_expression();
    }
    std::vector<Expression*> args;
    while (next() != ')') {
        whitespace();
        if(current() == '('){
            args.push_back(read_func_call());
        } else if (current() == '`') {
            args.push_back(read_quote());
        } else if(isdigit(current())){
            args.push_back(read_num());
        } else {
            args.push_back(read_symbol_expression());
        }
    }
    return new FuncCall(func, args);
}

Expression* Parser::read_quote(){
    if (current() != '`'){
        next();
    }
    next();
    whitespace();
    if (current() == '(') {
        std::vector<Expression*> contents;
        while (next() != ')'){
            whitespace();
            if(current() == '`') {
                std::cout << "Cannot quote inside of quote\n";
            }
            else if (current() == '('){
                contents.push_back(read_quote());
            } else if (isdigit(current())){
                contents.push_back(read_num());
            } else {
                contents.push_back(read_symbol_expression());
            }
        }
        return new Quote(contents);
    } else {
        std::vector<Expression*> contents;
        if (isdigit(current())) {
            contents.push_back(read_num());
        } else {
            contents.push_back((Expression*)read_symbol());
        }
        return new Quote(contents);
    }
}

Symbol* Parser::read_symbol(){
    if (current() == '('){
        std::cout << "Syntax error, unexpected character ( expected identifier" << current() << "\n";
    }
    std::string identifier = "";
    while (!(isspace(current()) || finished()) && current() != ')') {
        identifier += next();
    }
    return new Symbol(identifier);
}

Expression* Parser::read_symbol_expression(){
    if (current() == '('){
        std::cout << "Syntax error, unexpected character ( expected identifier" << current() << "\n";
    }
    std::string identifier = "";
    while (!(isspace(current()) || finished()) && current() != ')') {
        identifier += next();
    }
    return new SymbolExpression(Symbol(identifier));
}

Expression* Parser::read_num(){
    if (current() == '('){
        std::cout << "Syntax error, unexpected character '('";
    }
    std::string literal = "";
    while (!(isspace(current()) or finished()) && current() != ')'){
        literal += next();
    }
    return new ValueExpression(Value(Dec64(literal)));
}

void Parser::eval(){
    for (int i = 0; i < queue.size(); i++){
        Expression* expr = queue[i];
        if (dynamic_cast<FuncCall*>(expr) or dynamic_cast<SymbolDerefExpression*>(expr)){
            std::cout << "out: " << expr->eval(env).repr() << std::endl;
        } else if(dynamic_cast<Quote*>(expr) or
                  dynamic_cast<SymbolExpression*>(expr)){
            std::cout << "out: " << expr->repr() << std::endl;
        } else {
            std::cout << "out: " << expr->repr() << std::endl;
        }
        delete expr;
    }
}
