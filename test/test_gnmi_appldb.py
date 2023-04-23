
import json
from utils import gnmi_set, gnmi_get, gnmi_get_with_encoding

import pytest


class TestGNMIApplDb:

    def test_gnmi_update_normal_01(self):
        proto_bytes = b"\n\x010\x12$b6d54023-5d24-47de-ae94-8afe693dd1fc\x1a\x17\n\x12\x12\x10\r\xc0-\xdd\x82\xa3\x88;\x0fP\x84<\xaakc\x16\x10\x80\x01\x1a\x17\n\x12\x12\x10-\x0e\xf2\x7f\n~c_\xd8\xb7\x10\x84\x81\xd6'|\x10\x80\x01\x1a\x17\n\x12\x12\x10\x1bV\x89\xc8JW\x06\xfb\xad\b*fN\x9e(\x17\x10\x80\x01\x1a\x17\n\x12\x12\x107\xf9\xbc\xc0\x8d!s\xccVT\x88\x00\xf8\x9c\xce\x90\x10\x80\x01\x1a\x17\n\x12\x12\x10\tEb\x11Mf]\x12\x17x\x99\x80\xea\xd1u\xb4\x10\x80\x01\x1a\x17\n\x12\x12\x10\x1f\xd3\x1c\x89\x99\x16\xe7\x18\x91^0\x81\xb1\x04\x8c\x1e\x10\x80\x01\x1a\x17\n\x12\x12\x10\x06\x9e55\xdb\xb5&\x93\x99\xfaC\x81\x16P\xdc\x1d\x10\x80\x01\x1a\x17\n\x12\x12\x10&]U\x96e4\xf4\xd2'&\x04i\xdf\x8dA\x9f\x10\x80\x01\x1a\x17\n\x12\x12\x108\xd5\xa3*\xe7\x80\xdc\x1e\x80f\x94\xb7\xb6\x86~\xcd\x10\x80\x01\x1a\x17\n\x12\x12\x101\xf0@F\nu+}\x1e\"\\\\\xdb\x01\xe3\x82\x10\x80\x01\"\x05vnet1\"\x05vnet2\"\x05vnet1\"\x05vnet2\"\x05vnet2\"\x05vnet1\"\x05vnet2\"\x05vnet2\"\x05vnet1\"\x05vnet1"
        test_data = [
            {
                'update_path': '/sonic-db:APPL_DB/DASH_ROUTE_TABLE/F4939FEFC47E:20.2.2.0\\\\/24',
                'value': proto_bytes
            },
            {
                'update_path': '/sonic-db:APPL_DB/DASH_ROUTE_TABLE/F4939FEFC47E:30.3.3.0\\\\/24',
                'value': proto_bytes
            },
            {
                'update_path': '/sonic-db:APPL_DB/DASH_VNET_MAPPING_TABLE/Vnet2:20.2.2.2',
                'value': proto_bytes
            }
        ]
        update_list = []
        for i, data in enumerate(test_data):
            path = data['update_path']
            value = data['value']
            file_name = 'update{}.txt'.format(i)
            file_object = open(file_name, 'wb')
            file_object.write(value)
            file_object.close()
            update_list.append(path + ':$./' + file_name)

        ret, msg = gnmi_set([], update_list, [])
        assert ret == 0, msg

    def test_gnmi_delete_normal_01(self):
        test_data = [
            {
                'update_path': '/sonic-db:APPL_DB/DASH_ROUTE_TABLE/F4939FEFC47E:20.2.2.0\\\\/24',
            },
            {
                'update_path': '/sonic-db:APPL_DB/DASH_ROUTE_TABLE/F4939FEFC47E:30.3.3.0\\\\/24',
            },
            {
                'update_path': '/sonic-db:APPL_DB/DASH_VNET_MAPPING_TABLE/Vnet2:20.2.2.2',
            }
        ]
        delete_list = []
        for i, data in enumerate(test_data):
            path = data['update_path']
            delete_list.append(path)

        ret, msg = gnmi_set(delete_list, [], [])
        assert ret == 0, msg

    def test_gnmi_invalid_encoding(self):
        path = '/sonic-db:APPL_DB/DASH_QOS'
        get_list = [path]
        ret, msg_list = gnmi_get_with_encoding(get_list, "ASCII")
        assert ret != 0, 'Encoding is not supported'
        hit = False
        exp = 'unsupported encoding'
        for msg in msg_list:
            if exp in msg:
                hit = True
                break
        assert hit == True, 'No expected error: %s'%exp

