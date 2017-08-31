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
	tmp << 0,0,-2;
	ren.setViewport(tmp);
	running=true;
	
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_w,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_a,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_s,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_d,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_e,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_q,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_r,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_f,false));
	
	/*
		Translation keys
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_i,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_k,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_j,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_l,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_u,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_o,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_y,false));
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_h,false));*/
	keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_TAB,false));
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
	if(keyStates.at(SDLK_w)){
		w.rotate(0.02f, 1, 2);
	}
	if(keyStates.at(SDLK_a)){
		w.rotate(0.02f, 0, 2);
	}
	if(keyStates.at(SDLK_s)){
		w.rotate(-0.02f, 1, 2);
	}
	if(keyStates.at(SDLK_d)){
		w.rotate(-0.02f, 0, 2);
	}
	if(w.getRank()>=4){
		if(keyStates.at(SDLK_q)){
			w.rotate(0.02f, 2, 3);
		}
		if(keyStates.at(SDLK_e)){
			w.rotate(-0.02f, 2, 3);
		}
	}
	if(w.getRank()>=5){
		if(keyStates.at(SDLK_r)){
			w.rotate(0.02f, 3, 4);
		}
		if(keyStates.at(SDLK_f)){
			w.rotate(-0.02f, 3, 4);
		}
	}
	if(keyStates.at(SDLK_TAB)){
		w = Wireframe::N_CUBE(4);
	}
}

void CApp::onRender(){
	ren.setColor(255, 255, 255, 255);
	ren.clear();
	ren.setColor(0, 0, 0, 255);
	ren.drawWireframe(w);
	ren.present();
}

void CApp::quit(){
	SDL_DestroyWindow(win);
	ren.close();
}