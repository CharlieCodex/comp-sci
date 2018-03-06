//
//  Func.cpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "Func.hpp"
#include "Value.hpp"

Func::Func(std::vector<Symbol> _arg_syms, Quote _func_body) : arg_syms(_arg_syms), func_body(_func_body){}

Value Func::eval(Environment env, std::vector<Value*> args){
    Environment scope = env.sub_scope();
    if(args.size() != arg_syms.size()){
        return None::none;
    }
    for (int i = 0; i < args.size(); i++){
        scope.assign(arg_syms[i], args[i]);
    }
    return func_body.eval(scope);
}
