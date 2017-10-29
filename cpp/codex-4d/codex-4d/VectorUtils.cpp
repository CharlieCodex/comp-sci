//
//  Projection.cpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#include "VectorUtils.hpp"

Eigen::VectorXf cast(Eigen::VectorXf vec, Eigen::VectorXf viewport){
	Eigen::VectorXf tmp = vec - viewport;
	Eigen::VectorXf out(vec.size()-1);
	for (int i = 0; i<out.size(); i++) {
		out(i) = tmp(i)/tmp(tmp.size()-1);
	}
	return out;
}
//rotate the vector angle radians in the a1,a2 plane
Eigen::VectorXf rotate(Eigen::VectorXf vec, float angle, int a1, int a2){
	Eigen::VectorXf out = vec;
	out(a1) = cos(angle)*vec(a1)+sin(angle)*vec(a2);
	out(a2) = cos(angle)*vec(a2)-sin(angle)*vec(a1);
	return out;
}
