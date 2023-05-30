#ifndef _C_ZMQCLIENT_H
#define _C_ZMQCLIENT_H

#include <stdbool.h>

#include "zmqclient.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef void *zmq_client_t;

// ZmqClient::ZmqClient(const std::string& endpoint)
zmq_client_t zmq_client_new(const char *endpoint);

// ZmqClient::~ZmqClient()
void zmq_client_delete(zmq_client_t pc);

// bool ZmqClient::isConnected()
bool zmq_client_is_connected(zmq_client_t pc);

// void ZmqClient::connect()
void zmq_client_connect(zmq_client_t pc);

#ifdef __cplusplus
}
#endif

#endif
