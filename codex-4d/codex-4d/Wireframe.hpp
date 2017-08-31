//
//  Wireframe.hpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#ifndef Wireframe_hpp
#define Wireframe_hpp

#include <iostream>
#include <Eigen/Dense>
#include <vector>


struct Wireframe{
public:
	struct Connection{
		int i;
		int j;
		Connection(int a,int b):i(a),j(b){}
	};
private:
	int rank;
	std::vector<Eigen::VectorXf> points;
	std::vector<Connection> connections;
public:
	Wireframe(int r):rank(r){}
	Wireframe operator<<(Eigen::VectorXf point);
	//Rotate the entire wireframe in the a1,a2 plane
	void rotate(float angle, int a1, int a2);
	Wireframe rotated(float angle, int a1, int a2);
	//Connect two points in the wireframe
	void connect(int i, int j);
	friend std::ostream& operator<<(std::ostream& os, const Wireframe& w);
	std::vector<Eigen::VectorXf> getPoints();
	int getRank();
	std::vector<Connection> getConnections();
	static Wireframe N_CUBE(int rank);
};

#endif /* Wireframe_hpp */
