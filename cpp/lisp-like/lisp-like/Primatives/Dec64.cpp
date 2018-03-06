//
//  Dec64.cpp
//  lisp-like
//
//  Created by Charles McVicker on 30/01/2018.
//  Copyright © 2018 Charles McVicker. All rights reserved.
//

#include "Dec64.hpp"
#include <math.h>

Dec64::Dec64(std::string string){
    size_t pos = string.find('.');
    if(std::string::npos == pos){
        mentissa = std::stoi(string);
    } else {
        std::string tmp = string.erase(pos, 1);
        mentissa = std::stoi(tmp);
        exponent = int(pos);
    }
    Value(this);
}

Dec64 operator+(Dec64 a, Dec64 b){
    if (a.exponent == b.exponent) {
        return Dec64(a.mentissa + b.mentissa);
    } else {
        if (a.exponent < b.exponent) {
            char diff = b.exponent - a.exponent;
            int men = a.mentissa * pow(10, diff) + b.mentissa;
            return Dec64(men, b.exponent);
        } else {
            char diff = a.exponent - b.exponent;
            int men = b.mentissa * pow(10, diff) + a.mentissa;
            return Dec64(men, a.exponent);
        }
    }
}
