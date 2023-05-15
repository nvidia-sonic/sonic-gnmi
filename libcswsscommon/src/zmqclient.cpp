#include <capi/zmqclient.h>
#include <zmqclient.h>

#include <string>
#include <vector>
#include <tuple>

zmq_client_t zmq_client_new(const char *endpoint)
{
    auto pc = new swss::ZmqClient(std::string(endpoint));
    return static_cast<zmq_client_t>(pc);
}

void zmq_client_delete(zmq_client_t pc)
{
    delete static_cast<swss::ZmqClient*>(pc);
}

bool zmq_client_is_connected(zmq_client_t pc)
{
    return static_cast<swss::ZmqClient*>(pc)->isConnected();
}

void zmq_client_connect(zmq_client_t pc)
{
    static_cast<swss::ZmqClient*>(pc)->connect();
}
