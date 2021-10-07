#include <algorithm>
#include <cstring>
#include <cstdio>
#include <cmath>

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

const unsigned int n = 640;

const float Pi = std::acos(-1.0);

int N = 4;
bool Inv = false;
float Radio = 0.8;

struct Vec2
{
    float x,y;
};

using Point = Vec2;

inline float Dot(const Vec2& A, const Vec2& B)
{
    return A.x * B.x + A.y * B.y;
}

inline float Distance(const Vec2& A, const Vec2& B)
{
    float dx = A.x - B.x;
    float dy = A.y - B.y;
    return std::sqrt(dx * dx + dy * dy);
}

inline Vec2 Rotate(const Vec2& V, float Angle)
{
    Vec2 R;
    R.x = V.x * std::cos(Angle) - V.y * std::sin(Angle);
    R.y = V.y * std::cos(Angle) + V.x * std::sin(Angle);
    return R;
}

Point Pointer = {0, -1.0};

bool inCircle(Point P, Point C, float R)
{
    auto dx = P.x - C.x;
    auto dy = P.y - C.y;
    return dx * dx + dy * dy <= R * R;
}

unsigned char Print(int i, int j, float Time)
{
    unsigned char Res = 127;
    float R = (n - 1.0) * 0.5;
    Point C = {R, R};
    Point P = {(float)i, (float)j};
    for(int Layer = 0; Layer < N; Layer += 1)
    {
        auto T = Time * (Layer + 1) * (Inv ? (Layer % 2 ? 1 : -1) : 1);
        Vec2 thisPointer = Rotate(Pointer, T);
        Point whiteC =
        {
            C.x + thisPointer.x * R * 0.5f,
            C.y + thisPointer.y * R * 0.5f
        };
        Point blackC =
        {
            C.x - thisPointer.x * R * 0.5f,
            C.y - thisPointer.y * R * 0.5f
        };
        if(inCircle(P, whiteC, R * 0.5f))
        {
            Res = 255;
            if(inCircle(P, whiteC, R * 0.5f * Radio))
            {
                if (Layer == N-1)
                {
                    if(Distance(P, whiteC) < R * 0.2f)
                    {
                        Res = 0;
                    }
                }
                C = whiteC;
                R = R * 0.5f * Radio;
            }
            else
            {
                break;
            }
        }
        else if(inCircle(P, blackC, R * 0.5f))
        {
            Res = 0;
            if(inCircle(P, blackC, R * 0.5f * Radio))
            {
                if (Layer == N-1)
                {
                    if(Distance(P, blackC) < R * 0.2f)
                    {
                        Res = 255;
                    }
                }
                C = blackC;
                R = R * 0.5f * Radio;
            }
            else 
            {
                break;
            }
            
        }else if(inCircle(P, C, R))
        {
            Vec2 Ahead = Rotate(thisPointer, Pi * 0.5);
            Vec2 Dir = {P.x - C.x, P.y - C.y};
            if(Dot(Ahead, Dir) > 0)
            {
                Res = 0;
            }else
            {
                Res = 255;
            }
            break;
        }
        else
        {
            break;
        }
    }
    return Res;
}

unsigned char Buffer[n * n];

int main()
{
    for(int T = 0; T < 314; T += 1)
    {
        int Index = -1;
        for(int i=0; i<n; ++i)
        {
            for(int j=0; j<n; ++j)
            {
                Buffer[++Index] = Print(i, j, T * 0.02);
            }
        }

        char fileName[32];
        sprintf(fileName, "Taichi_%03d.png", T);
        stbi_write_png(fileName,n,n,1,Buffer,0);

        printf("Frame >> %03d\n", T);
    }
    return 0;
}