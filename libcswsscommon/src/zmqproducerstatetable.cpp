#include <capi/zmqproducerstatetable.h>
#include <zmqproducerstatetable.h>
#include <dbconnector.h>
#include <redispipeline.h>

#include <string>
#include <vector>
#include <tuple>

zmq_producer_state_table_t zmq_producer_state_table_new(db_connector_t db, const char *tableName, const char *endpoint)
{
    auto pt = new swss::ZmqProducerStateTable(static_cast<swss::DBConnector*>(db), std::string(tableName), std::string(endpoint));
    return static_cast<zmq_producer_state_table_t>(pt);
}

zmq_producer_state_table_t zmq_producer_state_table_new2(redis_pipeline_t pipeline, const char *tableName, const char *endpoint, bool buffered)
{
    auto pt = new swss::ZmqProducerStateTable(static_cast<swss::RedisPipeline*>(pipeline), std::string(tableName), std::string(endpoint), buffered);
    return static_cast<zmq_producer_state_table_t>(pt);
}

void zmq_producer_state_table_delete(zmq_producer_state_table_t pt)
{
    delete static_cast<swss::ZmqProducerStateTable*>(pt);
}


void zmq_producer_state_table_set(zmq_producer_state_table_t pt,
                        const char *key,
                        const field_value_tuple_t *values,
                        size_t count,
                        const char *op,
                        const char *prefix)
{
    std::vector<swss::FieldValueTuple> tuples;
    for(size_t i = 0; i < count; i++)
    {
        auto tuple = std::make_pair(std::string(values[i].field), std::string(values[i].value));
        tuples.push_back(tuple);
    }
    static_cast<swss::ZmqProducerStateTable*>(pt)->set(std::string(key), tuples, std::string(op), std::string(prefix));
}

void zmq_producer_state_table_del(zmq_producer_state_table_t pt,
                        const char *key,
                        const char *op,
                        const char *prefix)
{
    static_cast<swss::ZmqProducerStateTable*>(pt)->del(std::string(key), std::string(op), std::string(prefix));
}