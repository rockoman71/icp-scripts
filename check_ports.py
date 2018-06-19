#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 IBM Corporation
Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
    Contributors:
        * Rafael Sene <rpsene@br.ibm.com>
"""

import subprocess
import commands
import time
import sys


def expand_ranges(ranges, array_ports):
    ''' Expand the ranges of ports and append as part of the main array. '''
    for port_range in ranges:
        # Splits the string representing the begin and the end of the range,
        # collecting the first and last values.
        initial_port=int(port_range.split(':')[0])
        end_port=int(port_range.split(':')[1])
        # Append all the ports in the ranges in the main array of ports.
        for port in range(initial_port, end_port + 1):
            array_ports.append(port)
    return array_ports


def get_amount_ports(ports):
    ''' Print the amount of ports '''
    print 'The total of ports to verify is: ' + len(ports)


def execute_stdout(command):
    ''' Execute a command with its parameter and return the exit code
    and the command output '''
    try:
        subprocess.check_output([command], stderr=subprocess.STDOUT,
                                shell=True)
        return 0, ""
    except subprocess.CalledProcessError as excp:
        return excp.returncode, excp.output


def cmdexists(command):
    ''' Check if a command exists '''
    subp = subprocess.call("type " + command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return subp == 0


def check_port(port):
    ''' Check whether or not a given port is available for usage '''
    command="ss -tnlp | awk '{print $4}'| egrep -w \"" + str(port) + "\""
    return execute_stdout(command)


def main():
    PORTS=[8101,179,8500,8743,5044,5046,9200,9300,2380,4001,8082,8084,4500,4300,\
    8600,80,443,8181,18080,5000,35357,4194,8001,8888,8080,8443,9235,9443,10248,\
    10249,10250,10251,10252]

    PORTS_RANGES=['10248:10252', '30000:32767']

    if cmdexists('ss'):
        ALL_PORTS=[]
        ALL_PORTS=expand_ranges(PORTS_RANGES, PORTS)
        USED_PORTS=[]
        # For every port in the main array of ports, check whether or not
        # a given port is available for usage.
        for port in ALL_PORTS:
            print 'Checking port ' + str(port) + '...'
            if check_port(port)[0] == 0:
                USED_PORTS.append(port)

        print '***********************'
        print 'Ports already in use: '
        print USED_PORTS

if __name__ == "__main__":
    main()