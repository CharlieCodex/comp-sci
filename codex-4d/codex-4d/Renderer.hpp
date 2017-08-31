//
//  Renderer.hpp
//  codex-4d
//
//  Created by Charlie McVicker on 01/08/2017.
//  Copyright © 2017 Charlie McVicker. All rights reserved.
//

#ifndef Renderer_hpp
#define Renderer_hpp

#include <SDL2/SDL.h>
#include <SDL2_ttf/SDL_ttf.h>
#include <stdio.h>
#include <Eigen/Dense>
#include <map>
#include "Wireframe.hpp"

class Renderer{
private:
	SDL_Renderer* ren;
	bool isopen;
	Eigen::VectorXf viewport;
	std::map<const char*,TTF_Font*> fonts;
public:
	Renderer();
	/*
	 Assigns the isopen value to true and assigns the wrapped SDL_Renderer object
	 */
	bool open(SDL_Renderer* renH);
	/*
	 Marks the Renderer obj as closed so that it may be assigned to a new SDL_Renderer object;
	 */
	bool close();
	SDL_Renderer* getRenderer();
	bool setViewport(Eigen::Vector3f vec);
	// Text Methods
	void registerFont(const char* name, TTF_Font* font);
	TTF_Font* getFont(const char* name);
	void drawText(int x, int y, int point, const char* text, TTF_Font* f, SDL_Color color);
	void drawText(int x, int y, int point, const char* text, const char* font, SDL_Color color);
	// Draw Methods
	void clear();
	void present();
	void setColor(int r, int g, int b, int a);
	void drawSurface(SDL_Surface* s,const SDL_Rect* where);
	void drawTexture(SDL_Texture* t,const SDL_Rect* where);
	void drawPoint(float x, float y);
	void drawPoint(Eigen::Vector2f vec);
	void drawLine(Eigen::Vector2f a, Eigen::Vector2f b);
	void drawPoint(float x, float y, int size);
	void drawPoint(Eigen::Vector2f vec, int size);
	Eigen::Vector2f drawPoint(Eigen::Vector3f vec);
	Eigen::Vector2f cast2d(Eigen::Vector3f vec);
	void drawWireframe(Wireframe &w);
	void drawWireframe(Wireframe &w, bool points);
};


#endif /* Renderer_hpp */
