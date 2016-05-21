#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# init the storage directory for images,and check permission
#


import os
import sys
import subprocess


class init_dir:

    def __init__(self):
        pass

    def check_dir_exists(self, check_path):
        if check_path is None:
            print "No path specified."
        else:
            if os.path.exists(check_path) is False:
                try:
                    command = ["mkdir", "-p"]
                    command.append(check_path)
                    subprocess.check_call(command)
                except Exception:
                    print "\n\tDirectory '" + check_path +\
                        "' created failed,try manually ."
                    sys.exit(1)
            print "\n\tDirectory '" + check_path + "' check fine .\n"

    def check_dir_permission(self, check_path):
        if check_path is not None:
            full_path_file = check_path + "/This_file_is_used_for_TEST"
            try:
                open(full_path_file, 'w').close()
                os.remove(full_path_file)
            except Exception:
                print "\n\tYou have no permission in " + check_path + ".\n"
                sys.exit(1)
        else:
            print "No path specified."


if __name__ == "__main__":
    down_path = os.getcwd() + "/static/images/downloads"
    trans_path = os.getcwd() + "/static/images/converts"
    init = init_dir()
    init.check_dir_exists(down_path)
    init.check_dir_exists(trans_path)
    init.check_dir_permission(down_path)
    init.check_dir_permission(trans_path)
