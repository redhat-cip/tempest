# Copyright 2013 IBM Corp.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_serialization import jsonutils as json

from tempest.api_schema.response.compute.v2_1 import interfaces as schema
from tempest.api_schema.response.compute.v2_1 import servers as servers_schema
from tempest.common import service_client


class InterfacesClient(service_client.ServiceClient):

    def list_interfaces(self, server_id):
        resp, body = self.get('servers/%s/os-interface' % server_id)
        body = json.loads(body)
        self.validate_response(schema.list_interfaces, resp, body)
        return service_client.ResponseBodyList(resp,
                                               body['interfaceAttachments'])

    def create_interface(self, server_id, port_id=None, network_id=None,
                         fixed_ip=None):
        post_body = dict(interfaceAttachment=dict())
        if port_id:
            post_body['interfaceAttachment']['port_id'] = port_id
        if network_id:
            post_body['interfaceAttachment']['net_id'] = network_id
        if fixed_ip:
            fip = dict(ip_address=fixed_ip)
            post_body['interfaceAttachment']['fixed_ips'] = [fip]
        post_body = json.dumps(post_body)
        resp, body = self.post('servers/%s/os-interface' % server_id,
                               body=post_body)
        body = json.loads(body)
        self.validate_response(schema.get_create_interfaces, resp, body)
        return service_client.ResponseBody(resp, body['interfaceAttachment'])

    def show_interface(self, server_id, port_id):
        resp, body = self.get('servers/%s/os-interface/%s' % (server_id,
                                                              port_id))
        body = json.loads(body)
        self.validate_response(schema.get_create_interfaces, resp, body)
        return service_client.ResponseBody(resp, body['interfaceAttachment'])

    def delete_interface(self, server_id, port_id):
        resp, body = self.delete('servers/%s/os-interface/%s' % (server_id,
                                                                 port_id))
        self.validate_response(schema.delete_interface, resp, body)
        return service_client.ResponseBody(resp, body)

    def add_fixed_ip(self, server_id, network_id):
        """Add a fixed IP to input server instance."""
        post_body = json.dumps({
            'addFixedIp': {
                'networkId': network_id
            }
        })
        resp, body = self.post('servers/%s/action' % server_id,
                               post_body)
        self.validate_response(servers_schema.server_actions_common_schema,
                               resp, body)
        return service_client.ResponseBody(resp, body)

    def remove_fixed_ip(self, server_id, ip_address):
        """Remove input fixed IP from input server instance."""
        post_body = json.dumps({
            'removeFixedIp': {
                'address': ip_address
            }
        })
        resp, body = self.post('servers/%s/action' % server_id,
                               post_body)
        self.validate_response(servers_schema.server_actions_common_schema,
                               resp, body)
        return service_client.ResponseBody(resp, body)
