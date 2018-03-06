//
//  CApp.cpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#include "CApp.hpp"
float a(0.125);
void henon(Eigen::Vector3f &vec){
    Eigen::Vector3f v(vec);
    v(0) = 1 - a*pow(vec(0), 2) + vec(1);
    v(1) = -vec(0);
    vec = v;
}
void ikedamcv(Eigen::Vector3f &vec){
    Eigen::Vector3f v(vec);
    float U = 1;
    float t = .4 - 6 / (1 + pow(vec[0],2) + pow(vec[1],2) + pow(vec[2],2));
    v <<
    1+U*(vec[0]*cos(t)-vec[1]*sin(t)),
    U*(vec[2]*sin(t)+vec[1]*cos(t)),
    1-U*(vec[1]*sin(t)- vec[2]*cos(t));
    vec = v;
}
void ikedaUV(Eigen::Vector3f &vec){
    Eigen::Vector3f v(vec);
    float U = vec(2);
    float t = .4 - 6 / (1 + pow(vec[0],2) + pow(vec[1],2) + pow(vec[2],2));
    v <<
    1+U*(vec[0]*cos(t)-vec[1]*sin(t)),
    U*(vec[0]*sin(t)+vec[1]*cos(t)),
    vec(2);
    vec = v;
}

void lorenz(Eigen::Vector3f &vec){
    Eigen::Vector3f d;
    float s=10,r=28,b=8/3;
    d << s*(vec(1)-vec(0)),
    vec(0)*(r-vec(2))-vec(1),
    vec(0)*vec(1)-b*vec(2);
    
    vec += d*0.001;
}

void james(Eigen::Vector3f &vec){
    Eigen::Vector3f d;
    float s=10,b=8/3;
    
    d <<
    sinf(s*vec(1)-vec(0)),
    cosf(s*vec(1)-vec(0)),
    tanhf(vec(0)*vec(1)-b*vec(2));
    
    vec += d*0.001;
}

void urbanVHA(Eigen::Vector3f &vec){
    Eigen::Vector3f d;
    float s=.9,t=1/(vec.norm()+1),b=8/3;
    
    d <<
    -tanhf(s*(cosf(t)*vec(0)-sinf(t)*vec(1))+b*vec(2)),
    -tanhf(s*(sinf(t)*vec(0)+cosf(t)*vec(1))+b*vec(2)),
    tanf(vec(0)*vec.norm());
    
    vec += d*0.001;
}

void urbanVH(Eigen::Vector3f &vec){
    Eigen::Vector3f d = vec;
    ikedaUV(d);
    d.unaryExpr(&tanhf);
    d*=-1;
    vec += d*0.001;
}

void odeTest(Eigen::Vector3f &vec){
    float X = vec(0),
    Y = vec(1),
    a = 1,
    x = sqrt(pow(X,2)+pow(Y,2)),
    y = atan2(Y,X)*a/M_PI;
    Eigen::Vector3f out = {
        y*x+exp(sin(y-vec(2)))+exp(cos(vec(2)-y)),
        a*sin(x),
        a*cos(x)
    }, d;
    out(1)*=M_PI/a;
    out(2)*=M_PI/a;
    d <<
    (out(0)*cos(out(1))),
    (out(0)*sin(out(1))),
    (out(0)*cos(out(2)));
    
    d.unaryExpr(&tanhf);
    
    vec += d*0.0001;
}

void henonODE(Eigen::Vector3f &vec){
    float a = 1.4,b = .3;
    Eigen::Vector3f d {
        1-a*(pow(vec(0),2)-pow(vec(1),2))+vec(2),
        a*(vec(0)*vec(1)),
        b*vec(0)
    };
    vec += d*0.0001;
}

void newshit(Eigen::Vector3f &vec){
    float
    r = pow(pow(vec(1),2)+pow(vec(2),2),0.5),
    theta = atan2f(vec(2), vec(1));
    Eigen::Vector3f d {
        vec(1)+vec(2),
        cosf(theta)*r+pow(vec(0),2),
        sinf(theta*r)-pow(vec(1),3)
    };
    vec += d*0.0001;
}

void library(Eigen::Vector3f &vec){
    Eigen::Vector3f d;
    d <<
    vec(2)*tanf(vec(1)),expf(-pow(expf(vec(0)+vec(1)),2)),sinf(vec(2)*vec(1)+vec(0));
    vec += d*0.001;
}

void lib2(Eigen::Vector3f &vec){
    Eigen::Vector3f d;
    d <<
    vec(1)*2-vec(2),
    vec(2)*(vec(1)-1),
    vec(0)-vec(2)*(1-vec(1));
    d-=vec;
    vec += d*0.0001;
}

void lib3(Eigen::Vector3f &vec){
    float a = 2, b = 1/2;
    Eigen::Vector3f d;
    d <<    vec(2)-vec(1),
    vec(0)*(a-vec(1)),
    -vec(1)*vec(0)-b*vec(2);
    vec += d*0.0001;
}

void lib4(Eigen::Vector3f &vec){
    //based off of the polar standard map
    float R = sqrtf(powf(vec(0),2)+powf(vec(1),2)),
    t = atan2f(vec(1), vec(0));
    R -= (M_2_PI*floor(R/M_2_PI));
    float _R = R+t*vec(2),
    _t = t + _R;
    vec << _R*cosf(_t), _R*sinf(_t), cosf(_R);
}

void reciprocal(Eigen::Vector3f &vec){
    Eigen::Vector3f tmp(vec);
    float x = vec(0), y = vec(1), r1 = x*x+y*y;
    vec(0) = x/r1;
    vec(1) = y/r1;
}

void memeFunc(Eigen::Vector3f &vec){
    Eigen::Vector3f tmp(vec);
    tmp(0) += 1/vec(1);
    tmp(1) -= 1/vec(0);
    vec = tmp;
}

void dynamicSines(Eigen::Vector3f &vec){
    Eigen::Vector3f tmp;
    float a = 2,b = 2;
    tmp(0) = (vec(0)-1/vec(0))*powf(sinf(atanf(vec(0)/vec(1))),a);
    tmp(1) = (vec(1)-1/vec(1))*cbrtf(powf(cosf(atanf(vec(1)/vec(0))),b));
    tmp(2) = vec(2);
    vec = tmp;
}

void inversion(Eigen::Vector3f &vec){
    Eigen::Vector3f tmp;
    float x = vec(0), y = vec(1), z = vec(2), r = sqrtf(x*x+y*y+z*z);
    vec/=(r+1);
}

void CApp::start(){
    init();
    run();
    quit();
}

void CApp::init(){
    SDL_Init(SDL_INIT_EVERYTHING);
    TTF_Init();
    win = SDL_CreateWindow("Codex-Canvas", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 2560, 1600, SDL_WINDOW_RESIZABLE|SDL_WINDOW_ALLOW_HIGHDPI);
    out.open(SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED));
    
    surf = SDL_CreateRGBSurface(0, 2560, 1600, 32, 0, 0, 0, 0);
    ren.open(SDL_CreateSoftwareRenderer(surf));
    
    Eigen::Vector3f tmp;
    tmp << 0,0,-4;
    ren.setViewport(tmp);
    float w = 20;
    float h = 20;
    float d = 0;
    for (int i = 0; i < 1000; i++) {
        tmp << float(rand())/RAND_MAX*w-w/2,
                float(rand())/RAND_MAX*h-h/2,
                float(rand())/RAND_MAX*d-d/2;
        points.push_back(tmp);
    }
    
    running=true;
    
    keyStates.insert(std::pair<SDL_Keycode,bool>(SDLK_s,false));
    
    ren.setColor(255, 255, 255, 255);
    ren.clear();
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
}

void CApp::onEvent(SDL_Event &e){
    switch (e.type) {
        case SDL_QUIT:
            running=false;
            break;
        case SDL_KEYDOWN:
            keyStates.insert(std::pair<SDL_Keycode,bool>(e.key.keysym.sym,true));
            keyStates.at(e.key.keysym.sym) = true;
            break;
        case SDL_KEYUP:
            keyStates.insert(std::pair<SDL_Keycode,bool>(e.key.keysym.sym,false));
            keyStates.at(e.key.keysym.sym) = false;
            break;
    }
}

void CApp::onUpdate(){
    for(int i = 0; i < points.size(); i++){
        Eigen::Vector3f vec = points[i];
        inversion(vec);
        ikedamcv(vec);
        points[i] = vec;
    }
    if(keyStates.at(SDLK_s)==true){
        keyStates.at(SDLK_s) = false;
        std::string s("/Users/charliemcvicker/Documents/backgrounds/fractals/img-");
        s.append(std::to_string(ticks)).append(".bmp");
        SDL_SaveBMP(surf, s.c_str());
    }
}

void CApp::onRender(){
    /*
    float r,g,b;
    r = sinf(float(ticks)/100)*64+127-64;
    g = sinf(float(ticks)/100+M_PI/3)*64+127-64;
    b = sinf(float(ticks)/100+2*M_PI/3)*64+127-64;
    */
    
    ren.setColor(0, 0, 0, 20);
    for(int i = 0; i < points.size(); i++){
        ren.drawPoint(Eigen::Vector3f(rotate(points[i],1,0,2)),2);
    }
    ren.present();
    
    out.setColor(255, 255, 255, 255);
    out.clear();
    SDL_Texture* tex = SDL_CreateTextureFromSurface(out.getRenderer(), surf);
    SDL_RenderCopy(out.getRenderer(), tex, nullptr, nullptr);
    out.present();
}

void CApp::quit(){
    SDL_DestroyWindow(win);
    ren.close();
}
