#ifndef _C_ZMQPRODUCERSTATETABLE_H
#define _C_ZMQPRODUCERSTATETABLE_H

#include <hiredis/hiredis.h>
#include <stdbool.h>

#include "producertable.h"
#include "zmqproducerstatetable.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef void *db_connector_t2;
typedef void *redis_pipeline_t;
typedef void *zmq_producer_state_table_t;
typedef void *zmq_client_t;

// ZmqProducerStateTable::ZmqProducerStateTable(DBConnector *db, const string &tableName, ZmqClient &zmqClient)
zmq_producer_state_table_t zmq_producer_state_table_new(db_connector_t2 db, const char *tableName, zmq_client_t pc);
// ZmqProducerStateTable::ZmqProducerStateTable(RedisPipeline *pipeline, const string &tableName, ZmqClient &zmqClient, bool buffered)
zmq_producer_state_table_t zmq_producer_state_table_new2(redis_pipeline_t pipeline, const char *tableName, zmq_client_t pc, bool buffered);

// ZmqProducerStateTable::~ZmqProducerStateTable()
void zmq_producer_state_table_delete(zmq_producer_state_table_t pt);

// void ZmqProducerStateTable::set(std::string key,
//                         std::vector<FieldValueTuple> &values,
//                         std::string op = SET_COMMAND,
//                         std::string prefix = EMPTY_PREFIX)
void zmq_producer_state_table_set(zmq_producer_state_table_t pt,
                        const char *key,
                        const field_value_tuple_t *values,
                        size_t count,
                        const char *op,
                        const char *prefix);

// void ZmqProducerStateTable::del(std::string key,
//                         std::string op = DEL_COMMAND,
//                         std::string prefix = EMPTY_PREFIX)
void zmq_producer_state_table_del(zmq_producer_state_table_t pt,
                        const char *key,
                        const char *op,
                        const char *prefix);

#ifdef __cplusplus
}
#endif

#endif
