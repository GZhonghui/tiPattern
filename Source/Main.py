import taichi as ti

ti.init(arch=ti.gpu)

Pi = ti.acos(-1.0)

maxRange = 2

n = 640
Pixels  = ti.Vector.field(3, dtype=ti.f32, shape=(n, n))
Pointer = ti.Vector.field(2, dtype=ti.f32, shape=())

Rs = ti.field(dtype=ti.f32, shape=(n, n))
Cs = ti.Vector.field(2, dtype=ti.f32, shape=(n, n))

@ti.func
def Rotate(V,Angle):
  R = ti.Vector([0.0, 0.0], dt=ti.f32)
  R[0] = V[0] * ti.cos(Angle) - V[1] * ti.sin(Angle)
  R[1] = V[1] * ti.cos(Angle) + V[0] * ti.sin(Angle)
  return R

@ti.func
def inCircle(P,C,R):
  dx,dy = P[0]-C[0],P[1]-C[1]
  return dx*dx + dy*dy <= R*R

@ti.kernel
def Paint(t: ti.f32):
  for i, j in Pixels:
    Pixels[i,j] = (0.5, 0.5, 0.5)
    Rs[i,j] = (n - 1.0) * 0.5
    Cs[i,j] = ti.Vector([Rs[i,j],Rs[i,j]], dt=ti.f32)
    P = ti.cast(ti.Vector([i,j]), ti.f32)
    for Layer in ti.static(range(maxRange)):
      whiteC = Cs[i,j] + Pointer[None] * Rs[i,j] * 0.5
      blackC = Cs[i,j] - Pointer[None] * Rs[i,j] * 0.5
      if inCircle(P, whiteC, Rs[i,j] * 0.5):
        Pixels[i,j] = (1,1,1)
        Cs[i,j] = whiteC
        Rs[i,j] = Rs[i,j] * 0.5
      elif inCircle(P, blackC, Rs[i,j] * 0.5):
        Pixels[i,j] = (0,0,0)
        Cs[i,j] = blackC
        Rs[i,j] = Rs[i,j] * 0.5
      elif inCircle(P, Cs[i,j], Rs[i,j]):
        Ahead = Rotate(Pointer[None], Pi * 0.5)
        Dir = P - Cs[i,j]
        if Ahead.dot(Dir) > 0:
          Pixels[i,j]=(0,0,0)
        else:
          Pixels[i,j]=(1,1,1)
        break
      else:
        break

@ti.kernel
def initTi():
  Pointer[None] = (0.0, -1.0)

gui = ti.GUI("Taichi", res=(n, n))

def main():
  initTi()
  try:
    time_step = 0
    render_rate = 0.00001
    while True:
      Paint(time_step * render_rate)
      gui.set_image(Pixels)
      gui.show()

      time_step += 1
      
  except RuntimeError:
    pass

if __name__=='__main__':
  main()