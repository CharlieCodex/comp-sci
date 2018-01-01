//
//  Renderer.cpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#include "Renderer.hpp"
#include "VectorUtils.hpp"
#include "iostream"
#include <SDL2_ttf/SDL_ttf.h>

Renderer::Renderer(): isopen(false), ren(nullptr){}

bool Renderer::open(SDL_Renderer *renH){
	if(isopen){
		return false;
	} else {
		ren = renH;
		return true;
	}
}

SDL_Renderer* Renderer::getRenderer(){
	return ren;
}

bool Renderer::close(){
	SDL_DestroyRenderer(ren);
	isopen = false;
	return true;
}

bool Renderer::setViewport(Eigen::Vector3f vec){
	viewport = vec;
	return true;
}

/*-- FONT METHODS --*/

void Renderer::registerFont(const char* name, TTF_Font* font){
	if(fonts.count(name)){
		return;
	} else {
		fonts.insert(std::pair<const char*, TTF_Font*>(name,font));
	}
}

TTF_Font* Renderer::getFont(const char* name){
	if(fonts.count(name)){
		return fonts.at(name);
	} else {
		return getFont("default");
	}
}

void Renderer::drawText(int x, int y, int point, const char* text, TTF_Font* f, SDL_Color color){
	SDL_Surface* s = TTF_RenderText_Blended(f, text, color);
	SDL_Rect r;
	r.x = x-s->w/2;
	r.y = y-s->h/2;
	r.w = s->w;
	r.h = s->h;
	drawSurface(s, &r);
}
void Renderer::drawText(int x, int y, int point, const char* text, const char* font, SDL_Color color){
	SDL_Surface* s = TTF_RenderText_Blended(getFont(font), text, color);
	SDL_Rect r;
	r.x = x-s->w/2;
	r.y = y-s->h/2;
	r.w = s->w;
	r.h = s->h;
	drawSurface(s, &r);
}
/*-- DRAW METHODS --*/

void Renderer::present(){
	SDL_RenderPresent(ren);
}

void Renderer::clear(){
	SDL_RenderClear(ren);
}

void Renderer::setColor(int r, int g, int b, int a){
	SDL_SetRenderDrawColor(ren, r, g, b, a);
}

void Renderer::drawSurface(SDL_Surface* s,const SDL_Rect* where){
	drawTexture(SDL_CreateTextureFromSurface(ren, s),where);
}

void Renderer::drawTexture(SDL_Texture* t,const SDL_Rect* where){
	SDL_RenderCopy(ren, t, NULL, where);
}

void Renderer::drawPoint(float x, float y){
	int w;
	int h;
	SDL_GetRendererOutputSize(ren, &w, &h);
	SDL_RenderDrawPoint(ren, int(w/2+x),int(h/2-y));
}

void Renderer::drawPoint(Eigen::Vector2f vec){
	int w;
	int h;
	SDL_GetRendererOutputSize(ren, &w, &h);
	SDL_RenderDrawPoint(ren, int(w/2+vec[0]),int(h/2-vec[1]));
}

void Renderer::drawPoint(float x, float y, int size){
	int w;
	int h;
	SDL_GetRendererOutputSize(ren, &w, &h);
	SDL_Rect rect = {int(w/2+x-size/2),int(h/2-y-size/2),size,size};
	SDL_RenderFillRect(ren, &rect);
}

void Renderer::drawLine(Eigen::Vector2f a, Eigen::Vector2f b){
	int w;
	int h;
	SDL_GetRendererOutputSize(ren, &w, &h);
	SDL_RenderDrawLine(ren, a.x()+w/2, h/2-a.y(), b.x()+w/2, h/2-b.y());
}

void Renderer::drawPoint(Eigen::Vector2f vec, int size){
	int w;
	int h;
	SDL_GetRendererOutputSize(ren, &w, &h);
	SDL_Rect rect = {int(w/2+vec[0]-size/2),int(h/2-vec[1]-size/2),size,size};
	SDL_RenderFillRect(ren, &rect);
}

Eigen::Vector2f Renderer::drawPoint(Eigen::Vector3f vec){
    int w;
    int h;
    SDL_GetRendererOutputSize(ren, &w, &h);
    Eigen::Vector3f viewport3;
    if(viewport3.size()<viewport.size()){
        viewport3 = viewport.block(0, 0, 3, 1);
    } else {
        viewport3.setConstant(0);
        viewport3.block(0, 0, viewport.size(), 1);
    }
    Eigen::Vector2f tmp = cast(vec,viewport);
    tmp*=w>h?h:w;
    drawPoint(tmp,ceilf(100.0f/(vec-viewport).norm()));
    return tmp;
}

Eigen::Vector2f Renderer::drawPoint(Eigen::Vector3f vec, int size){
    int w;
    int h;
    SDL_GetRendererOutputSize(ren, &w, &h);
    Eigen::Vector3f viewport3;
    if(viewport3.size()<viewport.size()){
        viewport3 = viewport.block(0, 0, 3, 1);
    } else {
        viewport3.setConstant(0);
        viewport3.block(0, 0, viewport.size(), 1);
    }
    Eigen::Vector2f tmp = cast(vec,viewport);
    tmp*=w>h?h:w;
    drawPoint(tmp,size);
    return tmp;
}

Eigen::Vector2f Renderer::drawPoint(Eigen::VectorXf vec, int size){
    if(vec.size()==2){
        drawPoint((Eigen::Vector2f)vec, size);
        return vec;
    }
    if(vec.size()==3){
        return drawPoint((Eigen::Vector3f)vec, size);
    }
    int w;
    int h;
    SDL_GetRendererOutputSize(ren, &w, &h);
    Eigen::VectorXf superviewport(vec.size());
    if(superviewport.size()<viewport.size()){
        superviewport = viewport.block(0, 0, vec.size(), 1);
    } else {
        superviewport.setConstant(-2);
        superviewport.block(0, 0, 3, 1) = viewport;
    }
    while(vec.size()>2){vec=cast(vec, superviewport.block(0,0,vec.size(),1));}
    vec*=w>h?h:w;
    drawPoint(vec,size);
    return vec;
}

Eigen::Vector2f Renderer::cast2d(Eigen::Vector3f vec) {
	int w;
	int h;
	SDL_GetRendererOutputSize(ren, &w, &h);
	Eigen::Vector2f tmp = cast(vec,viewport);
	tmp*=w>h?h:w;
	return tmp;
}

void Renderer::drawWireframe(Wireframe &w){
	std::vector<Eigen::VectorXf> points(w.getPoints());
	std::vector<Wireframe::Connection> connections(w.getConnections());
	//Create a viewport at (viewport.x, viewport.y, viewport.z, 0, ... , 0)
	Eigen::VectorXf superviewport(w.getRank());
	superviewport.setConstant(-2);
	superviewport.block(0, 0, 3, 1) = viewport;
	std::vector<Eigen::Vector2f> casted;
	for(int i = 0; i<points.size(); i++){
		Eigen::VectorXf v = points[i];
		if(w.getRank() > 3){
			for(int j = w.getRank(); j>3; j--){
				v = cast(v, superviewport.block(0,0,j,1));
			}
		};
		casted.push_back(cast2d(Eigen::Vector3f(v)));
	}
	for(int i = 0; i < connections.size(); i++){
		drawLine(casted[connections[i].i], casted[connections[i].j]);
	}
}

void Renderer::drawWireframe(Wireframe &w, bool drawPoints){
	std::vector<Eigen::VectorXf> points(w.getPoints());
	std::vector<Wireframe::Connection> connections(w.getConnections());
	//Create a viewport at (viewport.x, viewport.y, viewport.z, 0, ... , 0)
	Eigen::VectorXf superviewport(w.getRank());
	superviewport.setConstant(-2);
	superviewport.block(0, 0, 3, 1) = viewport;
	std::vector<Eigen::Vector2f> casted;
	for(int i = 0; i<points.size(); i++){
		Eigen::VectorXf v = points[i];
		if(w.getRank() > 3){
			for(int j = w.getRank(); j>3; j--){
				v = cast(v, superviewport.block(0,0,j,1));
			}
		};
		if(drawPoints){
			casted.push_back(drawPoint(Eigen::Vector3f(v)));
		} else {
			casted.push_back(cast2d(Eigen::Vector3f(v)));
		}
	}
	for(int i = 0; i < connections.size(); i++){
		drawLine(casted[connections[i].i], casted[connections[i].j]);
	}
}
