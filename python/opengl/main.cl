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
      float u = 1.0;
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