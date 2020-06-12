#include <SDL2/SDL.h>

#include <sstream>
#include <optional>
#include <set>
#include <bitset>
#include <array>
#include <chrono>

#include "../common/msg.h"
#include <asio.hpp>

#include <iomanip>
#include <iostream>

using std::cout;
using std::cerr;
using std::endl;

typedef std::chrono::high_resolution_clock my_clock;
const my_clock::duration frame_time = std::chrono::milliseconds(8);

struct KeyState {
  enum : int
    {
     LCTRL = 0,
     LSHIFT,
     LALT,
     LGUI,
     RCTRL,
     RSHIFT,
     RALT,
     RGUI,
    };

  enum : int
    {
     MLEFT = 0,
     MRIGHT,
     MMIDDLE,
    };

  std::bitset<8> mod;
  std::set<SDL_Scancode> keys;

  struct MouseState {
    int dx, dy;
    int sx, sy;
    std::bitset<8> buttons;

    MouseState()
      : dx(0), dy(0), sx(0), sy(0), buttons(0) {}
  } mouse;

  char have_keyboard, have_mouse;
  my_clock::time_point last_mouse;

  KeyState(): mod(0), have_keyboard(0), have_mouse(0) {}

  void consume(SDL_Scancode code, bool press) {
    switch(code) {
    case SDL_SCANCODE_LCTRL: mod[LCTRL] = press; break;
    case SDL_SCANCODE_LSHIFT: mod[LSHIFT] = press; break;
    case SDL_SCANCODE_LALT: mod[LALT] = press; break;
    case SDL_SCANCODE_LGUI: mod[LGUI] = press; break;
    case SDL_SCANCODE_RCTRL: mod[RCTRL] = press; break;
    case SDL_SCANCODE_RSHIFT: mod[RSHIFT] = press; break;
    case SDL_SCANCODE_RALT: mod[LGUI] = press; break;
    case SDL_SCANCODE_RGUI: mod[RGUI] = press; break;

    default:
      if(press) keys.insert(code);
      else keys.erase(code);
    }

    have_keyboard = 1;
  }

  void consume_mouse_motion(int dx, int dy) {
    mouse.dx += dx;
    mouse.dy += dy;
    have_mouse = 1;
  }

  void consume_mouse_button(int code, bool press) {
    // TODO: forward and back buttons
    switch(code) {
    case SDL_BUTTON_LEFT: mouse.buttons[MLEFT] = press; break;
    case SDL_BUTTON_RIGHT: mouse.buttons[MRIGHT] = press; break;
    case SDL_BUTTON_MIDDLE: mouse.buttons[MMIDDLE] = press; break;
    }
    cout << mouse.buttons << "\n";
    have_mouse = 1;
  }

  void consume_mouse_wheel(int sx, int sy) {
    mouse.sx += sx;
    mouse.sy += sy;
    have_mouse = 1;
  }

  auto& reset() {
    keys.clear();
    mod = 0;
    mouse = MouseState();
    return *this;
  }

  keyboard_t get_keyboard_buffer() {
    keyboard_t ret;
    ret[0] = mod.to_ulong();
    ret[1] = 0;

    if(keys.size() > 6) {
      // phantom condition, idk if this is needed
      for(int i = 2; i < 8; i++)
        ret[i] = 1;
    } else {
      int idx = 2;
      for(auto& sm: keys)
        ret[idx++] = sm;
      for(; idx < 6; idx++)
        ret[idx] = 0;
    }

    have_keyboard = 0;
    return ret;
  }

  mouse_t get_mouse_buffer() {
    mouse_t ret;

    ret[0] = mouse.buttons.to_ulong();
    ret[1] = (char)mouse.dx;
    ret[2] = (char)mouse.dy;
    ret[3] = (char)mouse.sy;

    // FIXME: no horizontal scroll for now
    // ret[4] = (char)mouse.sx;

    mouse.dx = mouse.dy = mouse.sx = mouse.sy = 0;

    have_mouse = 0;
    last_mouse = my_clock::now();

    return ret;
  }

  bool keyboard_ready() {
    return have_keyboard;
  }
  bool mouse_ready() {
    return have_mouse && my_clock::now() - last_mouse > frame_time;
  }
};

std::optional<asio::ip::tcp::endpoint> get_endpoint(asio::io_service& io_service,
                                                    std::string s) {
  for(auto& c: s) if(c == ':') c = ' ';

  std::string host, port;
  std::istringstream ss(s);
  ss >> host >> port;

  asio::ip::tcp::resolver resolver(io_service);
  auto res = resolver.resolve(host, port);

  if(res.empty()) return {};
  return *res;
}

bool is_focused(SDL_Window* win) {
  auto state = SDL_GetWindowFlags(win);
  return state & SDL_WINDOW_MOUSE_FOCUS;
}

int main(int argc, char** argv) {
  if(argc < 2) {
    cerr << "Usage: " << argv[0] << " <host:port>\n";
    return 1;
  }

  asio::io_service io_service;

  auto addr = get_endpoint(io_service, argv[1]);
  if(!addr) {
    cerr << "host:port, '" << argv[1] << "' invalid.\n";
    return 1;
  }

  cerr << "Connecting to " << addr.value() << "\n";

  asio::ip::tcp::iostream stream;
  stream.socket().connect(addr.value());

  if(!stream.socket().is_open()) {
    cerr << "Connection failed.\n";
    return 1;
  } else {
    cerr << "Connected.\n";
  }

  if(SDL_Init(SDL_INIT_EVERYTHING) != 0) {
    cerr << "Failed to init SDL.\n";
    return 1;
  }

  uint32_t win_flags =
    SDL_WINDOW_RESIZABLE | SDL_WINDOW_INPUT_GRABBED;
  SDL_Window* win = SDL_CreateWindow("test window",
                                     SDL_WINDOWPOS_UNDEFINED,
                                     SDL_WINDOWPOS_UNDEFINED,
                                     100, 100, win_flags);

  SDL_SetRelativeMouseMode(SDL_TRUE);

  if(win == nullptr) {
    cerr << "Failed to create window.\n";
    return 1;
  }

  KeyState ks;

  SDL_Event event;
  while(true) {
    if(SDL_PollEvent(&event)) {
      if(event.type == SDL_QUIT) {
        break;
      }

      else if(event.type == SDL_KEYDOWN || event.type == SDL_KEYUP) {
        ks.consume(event.key.keysym.scancode, event.type == SDL_KEYDOWN);
      }

      // else if(event.type = SDL_MOUSEMOTION
      //           || event.type == SDL_MOUSEBUTTONDOWN
      //           || event.type == SDL_MOUSEBUTTONUP
      //           || event.type == SDL_MOUSEWHEEL) {
      //   std::cerr << "here\n";
      // }

      else if(is_focused(win)) {
        if(event.type == SDL_MOUSEMOTION) {
          ks.consume_mouse_motion(event.motion.xrel, event.motion.yrel);
        }

        else if(event.type == SDL_MOUSEBUTTONDOWN || event.type == SDL_MOUSEBUTTONUP) {
          cout << "here\n";
          ks.consume_mouse_button(event.button.button, event.type == SDL_MOUSEBUTTONDOWN);
        }

        else if(event.type == SDL_MOUSEWHEEL) {
          ks.consume_mouse_wheel(event.wheel.x, event.wheel.y);
        }
      }
    }

    if(ks.keyboard_ready()) {
      auto buf = ks.get_keyboard_buffer();

      {
        cerr << "kbd: ";
        for(auto b: buf) cerr << std::setw(2) << std::hex << (int)b << " ";
        cerr << endl;
      }

      write_trivial<int>(stream, CMD_KEYBOARD);
      write_trivial(stream, buf);
      stream.flush();
    }

    if(ks.mouse_ready()) {
      auto buf = ks.get_mouse_buffer();

      {
        cerr << "mouse: ";
        for(auto b: buf) cerr << std::setw(2) << std::hex << (int)b << " ";
        cerr << endl;
      }

      write_trivial<int>(stream, CMD_MOUSE);
      write_trivial(stream, buf);
      stream.flush();
    }
  }

  cerr << "Shutting down.\n";

  // clear the input before we die
  ks.reset();

  write_trivial<int>(stream, CMD_KEYBOARD);
  write_trivial(stream, ks.get_keyboard_buffer());

  write_trivial<int>(stream, CMD_MOUSE);
  write_trivial(stream, ks.get_mouse_buffer());

  stream.socket().shutdown(asio::ip::tcp::socket::shutdown_both);
  stream.close();

  SDL_Quit();

  return 0;
}
