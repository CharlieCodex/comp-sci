//
//  Wireframe.cpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#include "Wireframe.hpp"
#include "VectorUtils.hpp"

Wireframe Wireframe::operator<<(Eigen::VectorXf point){
	points.push_back(point);
	return *this;
}

void Wireframe::rotate(float angle, int a1, int a2){
	for(int i = 0; i < points.size(); i++){
		points[i] = ::rotate(points[i],angle,a1,a2);
	}
}

Wireframe Wireframe::rotated(float angle, int a1, int a2){
	Wireframe w(rank);
	for(int i = 0; i < points.size(); i++){
		w << ::rotate(points[i],angle,a1,a2);
	}
	return w;
}

std::ostream& operator<<(std::ostream& os, const Wireframe& w){
	for(int i = 0; i < w.points.size(); i++){
		os << w.points[i] << std::endl << std::endl;
	}
	return os;
}

std::vector<Eigen::VectorXf> Wireframe::getPoints(){
	return std::vector<Eigen::VectorXf>(points);
}

void Wireframe::connect(int i, int j){
	connections.push_back(Connection(i,j));
}

int Wireframe::getRank(){
	return rank;
}

std::vector<Wireframe::Connection> Wireframe::getConnections(){
	return std::vector<Connection>(connections);
}

Wireframe Wireframe::N_CUBE(int rank){
	Wireframe w(rank);
	Eigen::VectorXf v(rank);
	Eigen::VectorXi c(1<<rank);
	c.setZero();
	for(int i = 0; i < pow(2,rank); i++){
		for(int j = 0; j < rank; j++){
			int pn = (i&int(pow(2,j)))>>j;
			v(j) = 1-2*pn;
		}
		for(int j = i; j < pow(2,rank); j++){
			int n = i^j;
			unsigned int count = 0;
			while(n){
				count += n & 1;
				n >>= 1;
			}
			if(count==1){
				w.connect(i, j);
			}
		}
		w << v;
	}
	//std::cout << c;
	return w;
}