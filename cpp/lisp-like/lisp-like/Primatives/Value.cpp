//
//  Value.cpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "Value.hpp"

std::experimental::any* Value::get_val(){
    return &value;
};

std::string Value::repr(){
    return "Value";
}

None None::none = None();

Value::Value() : Value(None::none) {};

std::string None::repr(){
    return "None";
}
