package swsscommon

// #cgo LDFLAGS: -lcswsscommon -lswsscommon -lstdc++
// #include <capi/zmqclient.h>
// #include <stdlib.h>
import "C"

import (
    "log"
    "unsafe"
)

type ZmqClient struct {
    ptr   unsafe.Pointer
}


func NewZmqClient( endpoint string) ZmqClient {
    log.Printf(
        "trace: new ZmqClient: %s",
        endpoint,
    )

    endpointC := C.CString(endpoint)
    defer C.free(unsafe.Pointer(endpointC))

    pc := C.zmq_client_new(endpointC)
    return ZmqClient{ptr: unsafe.Pointer(pc)}
}

func (pc ZmqClient) Delete() {
    C.zmq_client_delete(C.zmq_client_t(pc.ptr))
}

func (pc ZmqClient) IsConnected() bool {
    connected :=  bool(C.zmq_client_is_connected(C.zmq_client_t(pc.ptr)))
    return connected
}

func (pc ZmqClient) Connect() {
    C.zmq_client_connect(C.zmq_client_t(pc.ptr))
}
