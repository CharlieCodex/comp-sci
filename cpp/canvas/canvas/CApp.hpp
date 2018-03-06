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
void henon(Eigen::Vector3f &vec);
class CApp{
private:
    Renderer ren, out;
    SDL_Window *win;
    SDL_Surface *surf;
    unsigned long ticks;
    bool running;
    std::vector<Eigen::Vector3f> points;
    std::map<SDL_Keycode, bool> keyStates;
public:
    CApp(): ticks(0){}
    void start();
    void init();
    void run();
    void onEvent(SDL_Event &e);
    void onUpdate();
    void onRender();
    void quit();
};

#endif /* CApp_hpp */
