//
//  Dec64.hpp
//  lisp-like
//
//  Created by Charles McVicker on 30/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#ifndef Dec64_hpp
#define Dec64_hpp

#include <stdio.h>
#include "Value.hpp"
#include <string>

class Dec64 : public Value {
private:
    int mentissa;
    char exponent;
public:
    Dec64(std::string string);
    Dec64(int men) : mentissa(men), exponent(0) {};
    Dec64(int men, char expo) : mentissa(men), exponent(expo) {};
    Dec64() = default;
    friend Dec64 operator+ (Dec64 a, Dec64 b);
};

#endif /* Dec64_hpp */
