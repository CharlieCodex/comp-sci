//
//  Arithmetic.hpp
//  lisp-like
//
//  Created by Charles McVicker on 30/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef Arithmetic_hpp
#define Arithmetic_hpp

#include "CFunc.hpp"
#include "Dec64.hpp"

Value __add__(Environment env, std::vector<Value*> args);
namespace arithmetic {
    const CFunc add = CFunc(__add__);
}

#endif /* Arithmetic_hpp */
