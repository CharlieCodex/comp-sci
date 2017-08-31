//
//  CApp.hpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#ifndef CApp_hpp
#define CApp_hpp

#include <stdio.h>
#include <algorithm>
#include <map>
#include "Renderer.hpp"
#include "VectorUtils.hpp"
class CApp{
private:
	Renderer ren;
	SDL_Window *win;
	unsigned long ticks;
	bool running;
	Wireframe w;
	std::function<Eigen::Vector3f(Eigen::Vector3f)> mapperfunc;
	std::map<SDL_Keycode, bool> keyStates;
	std::function<Eigen::Vector3f(Eigen::Vector3f)> compose3d(std::function<Eigen::Vector3f(Eigen::Vector3f)> a,
															  std::function<Eigen::Vector3f(Eigen::Vector3f)> b){
		return [=](Eigen::Vector3f vec)->Eigen::Vector3f{
			return b(a(vec));
		};
	}
public:
	CApp():w(3),ticks(0){}
	void start();
	void init();
	void run();
	void onEvent(SDL_Event &e);
	void onUpdate();
	void onRender();
	void quit();
};

#endif /* CApp_hpp */
