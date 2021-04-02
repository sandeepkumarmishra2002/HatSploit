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

from core.base.io import IO
from core.cli.colors import Colors


class Badges:
    io = IO()
    colors = Colors()

    I = colors.WHITE + colors.BOLD + '[i] ' + colors.END
    S = colors.GREEN + colors.BOLD + '[+] ' + colors.END
    W = colors.YELLOW + colors.BOLD + '[!] ' + colors.END
    E = colors.RED + colors.BOLD + '[-] ' + colors.END
    P = colors.BLUE + colors.BOLD + '[*] ' + colors.END
    Q = colors.WHITE + colors.BOLD + '[?] ' + colors.END
    A = colors.WHITE + colors.BOLD + '[>] ' + colors.END

    def output_empty(self, message, start='\033[1K\r', end='\n'):
        self.io.output(message, start=start, end=end)

    def output_usage(self, message, start='\033[1K\r', end='\n'):
        self.output_empty("Usage: " + message, start=start, end=end)

    def output_process(self, message, start='\033[1K\r', end='\n'):
        self.output_empty(self.P + message, start=start, end=end)

    def output_success(self, message, start='\033[1K\r', end='\n'):
        self.output_empty(self.S + message, start=start, end=end)

    def output_error(self, message, start='\033[1K\r', end='\n'):
        self.output_empty(self.E + message, start=start, end=end)

    def output_warning(self, message, start='\033[1K\r', end='\n'):
        self.output_empty(self.W + message, start=start, end=end)

    def output_information(self, message, start='\033[1K\r', end='\n'):
        self.output_empty(self.I + message, start=start, end=end)

    def output_multi(self, message):
        self.output_empty(f"\r{self.P}{message}", end='')

    def input_empty(self, message):
        output = ""
        out = self.io.input(message)[0]
        for command in out:
            output += command + " "
        return output.strip()

    def input_question(self, message):
        return self.input_empty(self.Q + message)

    def input_arrow(self, message):
        return self.input_empty(self.A + message)
