//
//  CApp.cpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#include "CApp.hpp"

void CApp::start(){
	init();
	run();
	quit();
}

void CApp::init(){
	SDL_Init(SDL_INIT_EVERYTHING);
	TTF_Init();
	win = SDL_CreateWindow("Codex-4D", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 450, SDL_WINDOW_RESIZABLE);
	ren.open(SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED));
	Eigen::Vector3f tmp;
	tmp << 0,0,-40;
	ren.setViewport(tmp);
	tmp << 0,2,0;
	w << tmp;
	mapperfunc = compose3d([](Eigen::Vector3f vec)->Eigen::Vector3f{
		Eigen::Vector3f tmp;
		tmp << 1-.125*pow(vec.x(),2)+vec.y(),-vec.x(),0;
		return tmp;
	}, [](Eigen::Vector3f vec)->Eigen::Vector3f{
		float t = 1-6/(1+pow(vec.x(),2)+pow(vec.y(),2));
		Eigen::Vector3f tmp;
		tmp <<
			1+.99*(vec.x()*cos(t)-vec.y()*sin(t)),
			.99*(vec.x()*sin(t)+vec.y()*cos(t)),
			0;
		return tmp;
	});
	running=true;
}

void CApp::run(){
	Uint32 next_tick = SDL_GetTicks();
	Uint32 skip_ticks = 16;
	SDL_Event e;
	while( running ) {
		while( SDL_PollEvent(&e) ){
			onEvent(e);
		}
		while( SDL_GetTicks() > next_tick ) {
			onUpdate();
			next_tick += skip_ticks;
			ticks++;
		}
		onRender();
	}
}

void CApp::onEvent(SDL_Event &e){
	switch (e.type) {
		case SDL_QUIT:
			running=false;
			break;
		case SDL_KEYDOWN:
			keyStates.insert(std::pair<SDL_Keycode,bool>(e.key.keysym.sym,true));
			keyStates.at(e.key.keysym.sym) = true;
			std::cout << e.key.keysym.sym << ": true" << std::endl;
			break;
		case SDL_KEYUP:
			keyStates.insert(std::pair<SDL_Keycode,bool>(e.key.keysym.sym,false));
			keyStates.at(e.key.keysym.sym) = false;
			std::cout << e.key.keysym.sym << ": false" << std::endl;
			break;
	}
}

void CApp::onUpdate(){
	/*Defining moving function for wireframe*/
	Eigen::Vector3f tmp = w.getPoints().at(w.getPoints().size()-1);
	w << mapperfunc(tmp);
	//w.connect(w.getPoints().size()-2, w.getPoints().size()-1);
}

void CApp::onRender(){
	ren.setColor(255, 255, 255, 255);
	ren.clear();
	ren.setColor(0, 0, 0, 255);
	ren.drawWireframe(w,true);
	ren.present();
}

void CApp::quit(){
	SDL_DestroyWindow(win);
	ren.close();
}