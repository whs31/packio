#include "msgpack/v3/object_decl.hpp"
#include <iostream>

#include <packio/packio.h>

namespace ip = packio::asio::ip;

int main(int, char**)
{
    // Declare a server and a client, sharing the same io_context
    packio::asio::io_context io;
    ip::tcp::endpoint bind_ep{ip::make_address("127.0.0.1"), 0};
    auto server = packio::make_server(ip::tcp::acceptor{io, bind_ep});
    auto client = packio::make_client(ip::tcp::socket{io});

    // Declare a coroutine
    server->dispatcher()->add_coro(
        "add", io, [](int a, int b) -> packio::asio::awaitable<int> {
            co_return a + b;
        });

    // Connect the client
    client->socket().connect(server->acceptor().local_endpoint());
    // Accept connections
    server->async_serve_forever();
    // Run the io_context
    std::thread thread{[&] { io.run(); }};

    // Spawn the coroutine and wait for its completion
    std::promise<void> p;
    packio::asio::co_spawn(
        io,
        [&]() -> packio::asio::awaitable<void> {
            // Call using an awaitable
            msgpack::object_handle res = co_await client->async_call(
                "add", std::tuple{12, 23}, packio::asio::use_awaitable);
            std::cout << "12 + 23 = " << res->as<int>() << std::endl;
            p.set_value();
        },
        packio::asio::detached);
    p.get_future().get();

    io.stop();
    thread.join();

    return 0;
}
