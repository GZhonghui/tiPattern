# Taichi Pattern

## Run
```
Taichi(Python) Version:
>> cd Source
>> python Main.py

C++ Version:
>> cd Source
>> g++ Main.cpp -IPathToStbImage && a.exe
The C++ version is not parallel or in real time, it's just to verify the algorithm
```

## The Definition of Taichi Pattern
| Static | Rotating |
:-:|:-:
| ![Taichi](readMe/Taichi_Def.png) | ![Taichi](readMe/Taichi.gif) |

## Do Some Change
### 1. Add Sub Pattern
| Add Sub Pattern | Change Speed | N = 10 |
:-:|:-:|:-:
| ![Taichi](readMe/Taichi_N2_SameSpeed.gif) | ![Taichi](readMe/Taichi_N2.gif) | ![Taichi](readMe/Taichi_N10.gif) |
### 2. Change Sub Patterns' Size
| Change Size | Ratio = 0.8 |
:-:|:-:
| ![Taichi](readMe/Taichi_Ratio.png) | ![Taichi](readMe/Taichi_N4_R0.8.gif) |
### 3. Change Sub Patterns' Rotation Direction
| Rotate in the Opposite Dir | N = 6; Ratio = 1.0 |
:-:|:-:
| ![Taichi](readMe/Taichi_N4_R0.8_T.gif) | ![Taichi](readMe/Taichi_N6_R1.0_T.gif) |
