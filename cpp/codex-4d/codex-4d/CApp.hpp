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
	std::map<SDL_Keycode, bool> keyStates;
public:
	CApp():w(Wireframe::N_CUBE(5)),ticks(0){}
	void start();
	void init();
	void run();
	void onEvent(SDL_Event &e);
	void onUpdate();
	void onRender();
	void quit();
};

#endif /* CApp_hpp */
