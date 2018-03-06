//
//  Value.hpp
//  lisp-like
//
//  Created by Charles McVicker on 26/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef Value_hpp
#define Value_hpp

#include <string>
#include <experimental/any>

class Value {
private:
    std::experimental::any value;
public:
    Value(std::experimental::any v): value(v){};
    Value();
    virtual std::experimental::any* get_val();
    std::string repr();
};

class None : public Value {
public:
    static None none;
    None() : Value(nullptr){}
    std::string repr();
};
#endif /* Value_hpp */
