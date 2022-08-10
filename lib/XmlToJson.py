import json
import xmltodict
from core import ApiRequest

__all__ = 'ServerHost',


def _read_xml_file(filename):
    """ _read_xml_file
    Takes a filename and reads it and returns the contents
    """

    with open(filename, 'r') as file_obj:
        ret = file_obj.read()
        file_obj.close()

    return ret


def _tr_xml_to_json_extension(xml_filename):
    """ _tr_xml_to_json_extension
    Translates example.xml to example.json (just the filename)
    """

    if '.xml' in xml_filename:
        return xml_filename.replace('.xml', '.json')
    else:
        return xml_filename + '.json'


def _write_output_file(json_filename, json_contents):
    """ _write_output_file
    Just writes text to a file.
    """

    with open(json_filename, 'w') as file_obj:
        file_obj.write(json_contents)
        file_obj.close()


def _lists_share_element(list_a, list_b):
    """ _lists_share_element
    Check if list_a shares and element with list_b
    """
    return not set(list_a).isdisjoint(list_b)


def parse(xml_string):
    """ parse
    Takes an xml string and returns the json equivalent
    """
    return json.dumps(xmltodict.parse(xml_string))


class ServerHost:

    def __init__(self):
        self.__server_dict = {}
        api_request = ApiRequest()
        response = api_request.get('http://192.168.2.206:8761/eureka/apps')
        json_str = parse(response.content)
        json_obj = json.loads(json_str).get('applications').get('application')
        for data in json_obj:
            server_name = data.get('name').lower()
            instance_obj = data.get('instance')
            if isinstance(instance_obj, dict):
                ip = instance_obj.get('ipAddr')
                port = instance_obj.get('port').get('#text')
            else:
                ip = instance_obj[0].get('ipAddr')
                port = instance_obj[0].get('port').get('#text')
            self.__server_dict[server_name] = 'http://' + ip + ':' + str(port)

    def get_host(self, server):
        return self.__server_dict.get(server.lower())
