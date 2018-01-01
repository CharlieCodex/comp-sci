import numpy as np
import pyopencl as cl
import pygame
import sys


def compute(x_np, y_np):
    x_g = cl.Buffer(cl_ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=x_np)
    y_g = cl.Buffer(cl_ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=y_np)
    res_x = cl.Buffer(cl_ctx, mf.WRITE_ONLY, y_np.nbytes)
    res_y = cl.Buffer(cl_ctx, mf.WRITE_ONLY, y_np.nbytes)
    cl_prog.henon(queue, x_np.shape, None, x_g, y_g, res_x, res_y)

    res_x_np = np.empty_like(y_np)
    res_y_np = np.empty_like(y_np)
    cl.enqueue_copy(queue, res_x_np, res_x)
    cl.enqueue_copy(queue, res_y_np, res_y)

    return res_x_np, res_y_np


def scale_points(x_np, y_np):
    x_g = cl.Buffer(cl_ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=x_np)
    y_g = cl.Buffer(cl_ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=y_np)
    res_x = cl.Buffer(cl_ctx, mf.WRITE_ONLY, x_np.nbytes)
    res_y = cl.Buffer(cl_ctx, mf.WRITE_ONLY, y_np.nbytes)
    win_g = [np.float32(x) for x in win]
    screen_g = [np.float32(x) for x in screen_size]
    cl_prog.scale_points(queue, x_np.shape, None,
                         *win_g, *screen_g,
                         x_g, y_g,
                         res_x, res_y)
    res_x_np = np.empty_like(y_np)
    res_y_np = np.empty_like(y_np)
    cl.enqueue_copy(queue, res_x_np, res_x)
    cl.enqueue_copy(queue, res_y_np, res_y)

    return res_x_np, res_y_np


def start():
    init_cl()
    run_pygame()


def init_cl():
    print('initing cl')
    global cl_ctx, queue, mf, cl_prog

    cl_ctx = cl.create_some_context()
    queue = cl.CommandQueue(cl_ctx)

    mf = cl.mem_flags

    cl_prog = cl.Program(cl_ctx, """
    __kernel void henon(
        __global const float *x_g,
        __global const float *y_g,
        __global float *res_x,
        __global float *res_y)
    {
      int gid = get_global_id(0);
      res_x[gid] = 1 + .125 * x_g[gid] * x_g[gid] + y_g[gid];
      res_y[gid] = - x_g[gid];
    }
    __kernel void ikeda(
        __global const float *x_g,
        __global const float *y_g,
        __global float *res_x,
        __global float *res_y)
    {
      int gid = get_global_id(0);
      float u = 1;
      float t = 0.4 - 6 / (1 + x_g[gid] * x_g[gid] + y_g[gid] * y_g[gid]);
      res_x[gid] = 1 + u * (x_g[gid] * cos(t) - y_g[gid] * sin(t));
      res_y[gid] = u * (y_g[gid] * cos(t) + x_g[gid] * sin(t));
    }
    __kernel void scale_points(
        const float win_x,
        const float win_y,
        const float win_w,
        const float win_h,
        const float screen_w,
        const float screen_h,
        __global const float *x_g,
        __global const float *y_g,
        __global float *res_x,
        __global float *res_y)
    {
      int gid = get_global_id(0);
      res_x[gid] = ((x_g[gid] - win_x) * screen_w / win_w);
      res_y[gid] = ((y_g[gid] - win_y) * screen_h / win_h);
    }
    """).build()


def alpha_rects(screen, color, x, y, size):
    s = pygame.Surface(size, pygame.HWSURFACE | pygame.SRCALPHA)
    s.fill(color)
    x_np, y_np = scale_points(x, y)
    points = np.column_stack((x_np, y_np))
    for x, y in points:
        if 0 < x < screen_size[0] and \
           0 < y < screen_size[1]:
            screen.blit(s, (x, y))


def terminate(screen, n):
    save(screen, n, name="exit")
    with open('logs/main_log.txt', 'a+') as file:
        file.write('closed thingy run\n')
        file.write('fps: {}'.format(fps))
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def save(screen, n, name='screenshot'):
    pygame.image.save(screen, 'screenshots/{}-{}.png'.format(name, n))


def run_pygame():
    global fps, screen_size, win
    win = (-25.6 / 2, -16.0 / 2, 25.6, 16.0)
    fps = []
    pygame.init()
    screen_size = width, height = 2560, 1600
    white = pygame.Color(255, 255, 255, 12)
    black = pygame.Color(0, 0, 0, 255)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(screen_size,
                                     pygame.HWSURFACE |
                                     pygame.FULLSCREEN |
                                     pygame.OPENGL)
    screen.fill(black)
    x, y = np.random.rand(2, 10000).astype(np.float32) * 10 - 5
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
                    save(screen, n)
                if event.key == pygame.K_UP:
                    SCALE += 10
                    print(SCALE)
                if event.key == pygame.K_DOWN:
                    if SCALE > 10:
                        SCALE -= 10
                    print(SCALE)
        st = pygame.time.get_ticks()
        x, y = compute_n(x, y, 10)
        et = pygame.time.get_ticks()
        print('compute: ', et - st)
        st = pygame.time.get_ticks()
        alpha_rects(screen, white, x, y, (1, 1))
        pygame.display.flip()
        et = pygame.time.get_ticks()
        print('draw: ', et - st)
        n += 1
        if n >= run_ticks:
            terminate(screen, n)
        clock.tick(120)
        if n % 10 == 0:
            fps.append(clock.get_fps())


def compute_n(x_np, y_np, n):
    x_g = cl.Buffer(cl_ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=x_np)
    y_g = cl.Buffer(cl_ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=y_np)
    x_g_ = cl.Buffer(cl_ctx, mf.READ_WRITE, y_np.nbytes)
    y_g_ = cl.Buffer(cl_ctx, mf.READ_WRITE, y_np.nbytes)
    for i in range(n):
        if i % 2 == 0:
            cl_prog.ikeda(queue, x_np.shape, None, x_g, y_g, x_g_, y_g_)
        if i % 2 != 0:
            cl_prog.ikeda(queue, x_np.shape, None, x_g_, y_g_, x_g, y_g)
    if n % 2 == 0:
        ox, oy = x_g, y_g
    if n % 2 != 0:
        ox, oy = x_g_, y_g_
    # at the end
    res_x_np = np.empty_like(y_np)
    res_y_np = np.empty_like(y_np)
    cl.enqueue_copy(queue, res_x_np, ox)
    cl.enqueue_copy(queue, res_y_np, oy)

    return res_x_np, res_y_np


if __name__ == '__main__':
    print('If you wish to run with acellerated graphics run gl_tests.py, defaulting to pygame blitting')
    start()
