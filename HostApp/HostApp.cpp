// 

#include <windows.h>
#include <stdlib.h>
#include <string.h>
#include <tchar.h>

#include <gl/gl.h>

// Global variables

extern "C" {int __cdecl startOGLClient(HWND hWnd); };
// The main window class name.
static TCHAR szWindowClass [] = _T("win32app");

// The string that appears in the application's title bar.
static TCHAR szTitle [] = _T("Remote Viewer");
static int OGLClientLoaded(0);

HINSTANCE hInst;

// Forward declarations of functions included in this code module:
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInstance,
    HINSTANCE hPrevInstance,
    LPSTR lpCmdLine,
    int nCmdShow)
{
    WNDCLASSEX wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);
    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProc;
    wcex.cbClsExtra = 0;
    wcex.cbWndExtra = 0;
    wcex.hInstance = hInstance;
    wcex.hIcon = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_APPLICATION));
    wcex.hCursor = LoadCursor(NULL, IDC_ARROW);
    wcex.hbrBackground = (HBRUSH) (COLOR_WINDOW + 1);
    wcex.lpszMenuName = NULL;
    wcex.lpszClassName = szWindowClass;
    wcex.hIconSm = LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_APPLICATION));
    wcex.style = CS_OWNDC;
    if(!RegisterClassEx(&wcex))
    {
        MessageBox(NULL,
            _T("Call to RegisterClassEx failed!"),
            _T("Win32 Guided Tour"),
            NULL);

        return 1;
    }

    hInst = hInstance; // Store instance handle in our global variable

                       // The parameters to CreateWindow explained:
                       // szWindowClass: the name of the application
                       // szTitle: the text that appears in the title bar
                       // WS_OVERLAPPEDWINDOW: the type of window to create
                       // CW_USEDEFAULT, CW_USEDEFAULT: initial position (x, y)
                       // 500, 100: initial size (width, length)
                       // NULL: the parent of this window
                       // NULL: this application does not have a menu bar
                       // hInstance: the first parameter from WinMain
                       // NULL: not used in this application
    HWND hWnd = CreateWindow(
        szWindowClass,
        szTitle,
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT,
        500, 100,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if(!hWnd)
    {
        MessageBox(NULL,
            _T("Call to CreateWindow failed!"),
            _T("Win32 Guided Tour"),
            NULL);

        return 1;
    }

    //Here's where we hook in the host crogl stuff
    if(!startOGLClient(hWnd))
        OGLClientLoaded = 1;


    // The parameters to ShowWindow explained:
    // hWnd: the value returned from CreateWindow
    // nCmdShow: the fourth parameter from WinMain
    ShowWindow(hWnd,
        nCmdShow);
    UpdateWindow(hWnd);
    
    // Main message loop:
    MSG msg;
    while(GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int) msg.wParam;
}

//
//  FUNCTION: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  PURPOSE:  Processes messages for the main window.
//
//  WM_PAINT    - Paint the main window
//  WM_DESTROY  - post a quit message and return
//
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    PAINTSTRUCT ps;
    HDC hdc;
    TCHAR greeting [] = _T("Crap on you, World!");
    TCHAR gotit [] = _T("Render is loaded!");

    PIXELFORMATDESCRIPTOR pfd =
    {
        sizeof(PIXELFORMATDESCRIPTOR),
        1,
        PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER | PFD_TYPE_RGBA,
        32,
        0, 0, 0, 0, 0, 0,
        0,
        0,
        0,
        0,
        0, 0, 0, 0,
        24,
        8,
        0,
        PFD_MAIN_PLANE,
        0,
        0,0,0
    };
    HDC WndDC;
    int ChooseFormat;
    HGLRC oglCtx;
    switch(message)
    {
    case WM_CREATE:
        WndDC = GetDC(hWnd);
        ChooseFormat = ChoosePixelFormat(WndDC, &pfd);
        SetPixelFormat(WndDC, ChooseFormat, &pfd);

        oglCtx = wglCreateContext(WndDC);
        wglMakeCurrent(WndDC, oglCtx);
        MessageBoxA(0, (char *) glGetString(GL_VERSION), "OPENGL VERSION", 0);
        break;
    case WM_PAINT:
        hdc = BeginPaint(hWnd, &ps);

        // Here your application is laid out.
        // For this introduction, we just print out "Hello, World!"
        // in the top left corner.
        if(!OGLClientLoaded)
            TextOut(hdc,
                5, 5,
                greeting, _tcslen(greeting));
        else
            TextOut(hdc, 5, 5, gotit, _tcslen(gotit));
        // End application-specific layout section.

        EndPaint(hWnd, &ps);
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
        break;
    }

    return 0;
}