//
//  CApp.cpp
//  julia
//
//  Created by Charles McVicker on 29/10/2017.
//  Copyright © 2017 Charles McVicker. All rights reserved.
//

#include "CApp.hpp"
//
//  CApp.cpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#include "CApp.hpp"

Eigen::Vector2f cplxQuad(Eigen::Vector2f z, Eigen::Vector2f c){
    Eigen::Vector2f out;
    out <<
    pow(z(0),2)-pow(z(1),2),
    2*z(0)*z(1);
    return out+c;
}
Eigen::Vector4f cplxQuad(Eigen::Vector4f z, Eigen::Vector4f c){
    Eigen::Vector4f out;
    out <<
    pow(z(0),2)-pow(z(1),2)-pow(z(2),2)-pow(z(3),2),
    2*z(0)*z(1),
    2*z(0)*z(2),
    2*z(0)*z(3);
    return out+c;
}

void CApp::start(){
    init();
    run();
    quit();
}

void CApp::init(){
    SDL_Init(SDL_INIT_EVERYTHING);
    TTF_Init();
    win = SDL_CreateWindow("Codex-Julia", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 2560, 1600, SDL_WINDOW_RESIZABLE|SDL_WINDOW_ALLOW_HIGHDPI);
    out.open(SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED));
    
    surf = SDL_CreateRGBSurface(0, 2560, 1600, 32, 0, 0, 0, 0);
    ren.open(SDL_CreateSoftwareRenderer(surf));
    
    running=true;
    draw = false;
    
    ren.setColor(255, 255, 255, 255);
    ren.clear();
    Eigen::Vector3f tmp;
    tmp << 0,0,-5;
    out.setViewport(tmp);
    SDL_SetRenderDrawBlendMode(ren.getRenderer(), SDL_BLENDMODE_BLEND);
    SDL_SetRenderDrawBlendMode(out.getRenderer(), SDL_BLENDMODE_BLEND);
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
    quit();
}

void CApp::onEvent(SDL_Event &e){
    switch (e.type) {
        case SDL_QUIT:
            running=false;
            break;
    }
}

void CApp::onUpdate(){
}

void CApp::onRender(){
    if(!draw){
        out.setColor(255, 255, 255, 255);
        out.clear();
        const int max_iter = 20;
        float size = 4, resolution = 100;
        for(int x = 0; x < size*resolution; x++){
            for(int y = 0; y < size*resolution; y++){
                for(int z = 0; z < size*resolution; z++){
                    //for(int w = 0; w < size*resolution; w++)
                    int w = (1+size/2)*resolution;
                    {
                        Eigen::Vector4f c, _z;
                        c << x/resolution-size/2,y/resolution-size/2,z/resolution-size/2,w/resolution-size/2;
                        _z << 0,0,0,0;
                        for(int n = 0 ; n < max_iter; n++){
                            _z = cplxQuad(_z, c);
                            if(_z.norm()>4){
                                break;
                            }
                            //out.setColor(255, 0, 255, 4);
                            //out.drawPoint((Eigen::Vector3f)_z.block(0,0,3,1),4);
                        }
                        if(_z.norm()<2){
                            out.setColor(0, 0, 0, 100);
                            out.drawPoint((Eigen::Vector3f)c.block(0,0,3,1), 2);
                        }
                    }
                }
            }
        }
        out.present();
        draw=true;
    }
    //SDL_Texture* tex = SDL_CreateTextureFromSurface(out.getRenderer(), surf);
    //SDL_RenderCopy(out.getRenderer(), tex, nullptr, nullptr);
    //out.present();
}

void CApp::quit(){
    SDL_DestroyWindow(win);
    out.close();
    ren.close();
}
