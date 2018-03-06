//
//  metaltests.metal
//  metaltests
//
//  Created by Charles McVicker on 14/11/2017.
//  Copyright © 2017 Charles McVicker. All rights reserved.
//

#include <metal_stdlib>
using namespace metal;

_renderer = [[AAPLRenderer alloc] initWithMetalKitView:_view];

if(!_renderer)
{
    NSLog(@"Renderer failed initialization");
    return;
}

_view.delegate = _renderer;
