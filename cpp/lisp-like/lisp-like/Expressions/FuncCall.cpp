//
//  FuncCall.cpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "FuncCall.hpp"
#include <iostream>
#include "Func.hpp"

Value FuncCall::eval(Environment env) {
    Value fn_val = func->eval(env);
    std::vector<Value> arg_vals(args.size());
    std::vector<Value*> arg_ptrs(args.size());
    for (int i = 0; i < args.size(); i++){
        arg_vals[i] = args[i]->eval(env);
        arg_ptrs[i] = &arg_vals[i];
    }
    try {
        _Func *fn = std::experimental::any_cast<_Func>(fn_val.get_val());
        if (fn){
            return fn->eval(env, arg_ptrs);
        }
    } catch (std::exception e) {
        std::cerr << "Func is not a function" << std::endl;
    }
    return None::none;
}

