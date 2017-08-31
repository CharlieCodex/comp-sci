//
//  Projection.hpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#ifndef Vector_Utils_hpp
#define Vector_Utils_hpp

#include <stdio.h>
#include <Eigen/Dense>

Eigen::VectorXf cast(Eigen::VectorXf vec, Eigen::VectorXf viewport);
Eigen::VectorXf rotate(Eigen::VectorXf vec, float angle, int a1, int a2);

#endif /* Vector_Utils_hpp */
