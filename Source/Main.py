import taichi as ti
import time

ti.init(arch=ti.cuda)

Pi = ti.acos(-1.0)

N = 4
Inv = True
Ratio = 0.8

FixedRatio = False

Ratios = ti.field(dtype=ti.f32, shape=2)

n = 640
Pixels = ti.field(dtype=ti.f32, shape=(n, n))

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

@ti.func
def Norm(x,l,r):
  return (x-l) / (r-l)

@ti.func
def Lerp(x,l,r):
  return l + (r-l) * x

@ti.kernel
def Paint(sumT: ti.f32):
  for i, j in Pixels:
    Pixels[i,j] = 0.5
    R = (n - 1.0) * 0.5
    C = ti.Vector([R,R], dt=ti.f32)
    P = ti.cast(ti.Vector([i,j]), ti.f32)
    nowRatio = Lerp(Norm(ti.sin(sumT),-1,1), Ratios[0], Ratios[1])
    for Layer in range(N):
      T = sumT * (Layer + 1) * (-1 if Inv and not Layer % 2 else 1)
      thisPointer = Rotate(ti.Vector([0.0, -1.0]), T)
      whiteC = C + thisPointer * R * 0.5
      blackC = C - thisPointer * R * 0.5
      if inCircle(P, whiteC, R * 0.5):
        Pixels[i,j] = 1
        if inCircle(P, whiteC, R * 0.5 * (Ratio if FixedRatio else nowRatio)):
          if Layer == N - 1 and (P - whiteC).norm() < R * 0.2:
            Pixels[i,j] = 0
          C = whiteC
          R = R * 0.5 * (Ratio if FixedRatio else nowRatio)
        else:
          break
      elif inCircle(P, blackC, R * 0.5):
        Pixels[i,j] = 0
        if inCircle(P, blackC, R * 0.5 * (Ratio if FixedRatio else nowRatio)):
          if Layer == N - 1 and (P - blackC).norm() < R * 0.2:
            Pixels[i,j] = 1
          C = blackC
          R = R * 0.5 * (Ratio if FixedRatio else nowRatio)
        else:
          break
      elif inCircle(P, C, R):
        Ahead = Rotate(thisPointer, Pi * 0.5)
        Dir = P - C
        if Ahead.dot(Dir) > 0:
          Pixels[i,j] = 0
        else:
          Pixels[i,j] = 1
        break
      else:
        break

@ti.kernel
def InitTi():
  Ratios[0] = 0.8
  Ratios[1] = 0.95

def Init():
  InitTi()

gui = ti.GUI("Taichi", res=(n, n))

def main():
  Init()
  try:
    startT = time.time()
    while True:
      Paint(time.time() - startT)
      gui.set_image(Pixels)
      gui.show()
  except RuntimeError:
    pass

if __name__=='__main__':
  main()