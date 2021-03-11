#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os

from core.base.types import types
from core.cli.badges import badges
from core.base.payloads import payloads
from core.base.storage import local_storage

class modules:
    def __init__(self):
        self.types = types()
        self.badges = badges()
        self.payloads = payloads()
        self.local_storage = local_storage()
        
    def check_exist(self, name):
        if self.check_style(name):
            all_modules = self.local_storage.get("modules")
            if all_modules:
                for database in all_modules.keys():
                    modules = all_modules[database]
                
                    category = self.get_category(name)
                    platform = self.get_platform(name)
        
                    if category in modules.keys():
                        if platform in modules[category].keys():
                            module = self.get_name(name)
                            if module in modules[category][platform].keys():
                                return True
        return False

    def check_imported(self, name):
        imported_modules = self.local_storage.get("imported_modules")
        if imported_modules:
            if name in imported_modules.keys():
                return True
        return False
    
    def check_style(self, name):
        if len(name.split('/')) >= 4:
            return True
        return False
    
    def check_current_module(self):
        if self.local_storage.get("current_module"):
            if len(self.local_storage.get("current_module")) > 0:
                return True
        return False
    
    def get_module_object(self, category, platform, name):
        module_full_name = self.get_full_name(category, platform, name)
        if self.check_exist(module_full_name):
            database = self.get_database(module_full_name)
            return self.local_storage.get("modules")[database][category][platform][name]
        return None
    
    def get_current_module_object(self):
        if self.check_current_module():
            return self.local_storage.get_array("current_module", self.local_storage.get("current_module_number"))
        return None
    
    def get_current_module_name(self):
        if self.check_current_module():
            return self.local_storage.get_array("current_module", self.local_storage.get("current_module_number")).details['Module']
        return None
       
    def get_database(self, name):
        if self.check_style(name):
            all_modules = self.local_storage.get("modules")
            if all_modules:
                for database in all_modules.keys():
                    modules = all_modules[database]
                
                    category = self.get_category(name)
                    platform = self.get_platform(name)
        
                    if category in modules.keys():
                        if platform in modules[category].keys():
                            module = self.get_name(name)
                            if module in modules[category][platform].keys():
                                return database
        return None
        
    def get_category(self, name):
        if self.check_style(name):
            return name.split('/')[0]
        return None

    def get_platform(self, name):
        if self.check_style(name):
            return name.split('/')[1]
        return None
    
    def get_name(self, name):
        if self.check_style(name):
            return os.path.join(*(name.split(os.path.sep)[2:]))
        return None

    def get_full_name(self, category, platform, name):
        return category + '/' + platform + '/' + name
    
    def get_current_module_payload(self):
        current_module = self.get_current_module_object()
        if hasattr(current_module, "options"):
            current_payload = None

            for option in current_module.options.keys():
                if current_module.options[option]['Type'] == 'payload':
                    if self.payloads.check_payload_exist(current_module.options[option]['Value']):
                        current_payload = self.payloads.get_payload_object(current_module.options[option]['Value'])

        return current_payload

    def compare_types(self, value_type, value):
        if value_type and not value_type.lower == 'all':
            if value_type.lower() == 'ip':
                if not self.types.is_ip(value):
                    self.badges.output_error("Invalid value, expected valid IP!")
                    return False

            if value_type.lower() == 'ipv4':
                if not self.types.is_ipv4(value):
                    self.badges.output_error("Invalid value, expected valid IPv4!")
                    return False

            if value_type.lower() == 'ipv6':
                if not self.types.is_ipv6(value):
                    self.badges.output_error("Invalid value, expected valid IPv6!")
                    return False

            if value_type.lower() == 'ipv4_range':
                if not self.types.is_ipv4_range(value):
                    self.badges.output_error("Invalid value, expected valid IPv4 range!")
                    return False

            if value_type.lower() == 'ipv6_range':
                if not self.types.is_ipv6_range(value):
                    self.badges.output_error("Invalid value, expected valid IPv6 range!")
                    return False

            if value_type.lower() == 'port':
                if not self.types.is_port(value):
                    self.badges.output_error("Invalid value, expected valid port!")
                    return False

            if value_type.lower() == 'port_range':
                if not self.types.is_port_range(value):
                    self.badges.output_error("Invalid value, expected valid port range!")
                    return False

            if value_type.lower() == 'number':
                if not self.types.is_number(value):
                    self.badges.output_error("Invalid value, expected valid number!")
                    return False

            if value_type.lower() == 'integer':
                if not self.types.is_integer(value):
                    self.badges.output_error("Invalid value, expected valid integer!")
                    return False

            if value_type.lower() == 'float':
                if not self.types.is_float(value):
                    self.badges.output_error("Invalid value, expected valid float!")
                    return False

            if value_type.lower() == 'boolean':
                if not self.types.is_boolean(value):
                    self.badges.output_error("Invalid value, expected valid boolean!")
                    return False
                
            if value_type.lower() == 'payload':
                if not self.payloads.check_payload_exist(value):
                    self.badges.output_error("Invalid payload, expected valid payload!")
                    return False
        return True

    def set_current_module_option(self, option, value):
        if self.check_current_module():
            current_module = self.get_current_module_object()
            if hasattr(current_module, "options"):
                current_payload = self.get_current_module_payload()

                if option in current_module.options.keys():
                    value_type = current_module.options[option]['Type']

                    if self.compare_types(value_type, value):
                        self.badges.output_information(option + " ==> " + value)
                        self.local_storage.set_module_option("current_module", self.local_storage.get("current_module_number"), option, value)

                elif current_payload and hasattr(current_payload, "options"):
                    if option in current_payload.options.keys():
                        value_type = current_payload.options[option]['Type']

                        if self.compare_types(value_type, value):
                            self.badges.output_information(option + " ==> " + value)
                            self.local_storage.set_payload_option(payload_name, option, value)
                    else:
                        self.badges.output_error("Unrecognized option!")
                else:
                    self.badges.output_error("Unrecognized option!")
            else:
                self.badges.output_warning("Module has no options.")
        else:
            self.badges.output_warning("No module selected.")
