import numpy as np
import pyopencl as cl
import pygame
import sys


def compute(x_np, y_np):
    x_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=x_np)
    y_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=y_np)
    res_x = cl.Buffer(ctx, mf.WRITE_ONLY, y_np.nbytes)
    res_y = cl.Buffer(ctx, mf.WRITE_ONLY, y_np.nbytes)
    prg.ikeda(queue, y_np.shape, None, x_g, y_g, res_x, res_y)

    res_x_np = np.empty_like(y_np)
    res_y_np = np.empty_like(y_np)
    cl.enqueue_copy(queue, res_x_np, res_x)
    cl.enqueue_copy(queue, res_y_np, res_y)

    return res_x_np, res_y_np


def scale_points(x_np, y_np):
    x_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=x_np)
    y_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=y_np)
    res_x = cl.Buffer(ctx, mf.WRITE_ONLY, y_np.nbytes)
    res_y = cl.Buffer(ctx, mf.WRITE_ONLY, y_np.nbytes)
    prg.ikeda(queue, y_np.shape, None, x_g, y_g, res_x, res_y)

    res_x_np = np.empty_like(y_np)
    res_y_np = np.empty_like(y_np)
    cl.enqueue_copy(queue, res_x_np, res_x)
    cl.enqueue_copy(queue, res_y_np, res_y)

    return res_x_np, res_y_np


def start():
    global ctx, queue, mf, prg

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags

    prg = cl.Program(ctx, """
    __kernel void henon(
        __global const float *x_g,
        __global const float *y_g,
        __global float *res_x,
        __global float *res_y)
    {
      int gid = get_global_id(0);
      res_x[gid] = 1 - .125 * x_g[gid] * x_g[gid] + y_g[gid];
      res_y[gid] = - x_g[gid];
    }
    __kernel void ikeda(
        __global const float *x_g,
        __global const float *y_g,
        __global float *res_x,
        __global float *res_y)
    {
      int gid = get_global_id(0);
      float u = 0.9;
      float t = 0.4 - 6 / (1 + x_g[gid] * x_g[gid] + y_g[gid] * y_g[gid]);
      res_x[gid] = 1 + u * (x_g[gid] * cos(t) - y_g[gid] * sin(t));
      res_y[gid] = u * (y_g[gid] * cos(t) + x_g[gid] * sin(t));
    }
    """).build()

    run_pygame()


SCALE = 150


def alpha_rects(screen, color, positions, size):

    s = pygame.Surface(size, pygame.HWSURFACE | pygame.SRCALPHA)
    s.fill(color)
    for pos in positions:
        x, y = pos * SCALE
        x += (2560 - SCALE) / 2
        y += (1600 - SCALE) / 2
        if 0 < x < 2560 and 0 < y < 1600:
            screen.blit(s, (x, y))


def terminate(screen, n):
    pygame.image.save(screen, 'screenshot-{}.png'.format(n))
    with open('main_log.txt', 'a+') as file:
        file.write('closed thingy run\n')
        file.write('fps: {}'.format(fps))
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def run_pygame():
    global fps
    fps = []
    pygame.init()
    size = width, height = 2560, 1600
    white = pygame.Color(255, 255, 255, 1)
    black = pygame.Color(0, 0, 0, 255)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size,
                                     pygame.HWSURFACE | pygame.FULLSCREEN)
    screen.fill(black)
    x, y = np.random.rand(2, 10000).astype(np.float32) * 5 - 2.5
    running = True
    n = 0
    run_ticks = 20000
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(screen, n)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    terminate(screen, n)
                    running = False
                if event.key == pygame.K_s:
                    pygame.image.save(screen, 'screenshot-{}.png'.format(n))
        x, y = compute(x, y)
        x, y = compute(x, y)
        alpha_rects(screen, white, np.column_stack((x, y)), (1, 1))
        pygame.display.flip()
        n += 1
        print(n)
        if n >= run_ticks:
            terminate(screen, n)
        clock.tick(120)
        if n % 10 == 0:
            fps.append(clock.get_fps())


if __name__ == '__main__':
    start()
