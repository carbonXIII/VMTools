#include <asio.hpp>

#include <iostream>
#include <fstream>
#include <iomanip>

#include "../common/msg.h"

void write_keyboard(const char* keyboard_file, keyboard_t& buf) {
  static std::ofstream out(keyboard_file, std::ios::out
                           | std::ios::binary
                           | std::ios::app);
  out.write((char*)buf.data(), buf.size());
  out.flush();

  std::cerr << "kbd: ";
  for(auto& b: buf)
    std::cerr << std::setw(2) << std::hex << (int)b << " ";
  std::cerr << "\n";
}

void write_mouse(const char* mouse_file, mouse_t& buf) {
  static std::ofstream out(mouse_file, std::ios::out
                           | std::ios::binary
                           | std::ios::app);
  out.write((char*)buf.data(), buf.size());
  out.flush();

  std::cerr << "mouse: ";
  for(auto& b: buf)
    std::cerr << std::setw(2) << std::hex << (int)b << " ";
  std::cerr << "\n";
}

void run_server(int port,
                const char* keyboard_file,
                const char* mouse_file) {
  asio::io_service io_service;
  asio::ip::tcp::acceptor acceptor(io_service,
                                   asio::ip::tcp::endpoint(asio::ip::tcp::v4(), port));

  // only accept one connection at a time
  while(true) {
    asio::ip::tcp::iostream stream;
    acceptor.accept(stream.socket());
    std::cerr << "Client connected.\n";

    // for now just read 8 bytes at a time and write them to the
    // HID device
    while(stream.socket().is_open() && !stream.eof()) {
      int cmd = read_trivial<int>(stream);

      switch(cmd) {
      case CMD_KEYBOARD: {
        auto buf = read_trivial<keyboard_t>(stream);
        write_keyboard(keyboard_file, buf);
        break;
      }

      case CMD_MOUSE: {
        auto buf = read_trivial<mouse_t>(stream);
        write_mouse(mouse_file, buf);
        break;
      }
      }
    }

    stream.close();
    std::cerr << "Client disconnected.\n";
  }
}

int main(int argc, char** argv) {
  if(argc < 4) {
    std::cerr << "Usage: " << argv[0] << " <port> <keyboard file> <mouse file>\n";
    return 1;
  }

  int port = atoi(argv[1]);

  std::cerr << "Starting server on port " << port << "\n";
  std::cerr << "Using keyboard file " << argv[2] << "\n";
  std::cerr << "Using mouse file " << argv[3] << "\n";

  run_server(port, argv[2], argv[3]);

  return 0;
}
