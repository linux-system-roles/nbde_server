#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sergio Correia <scorreia@redhat.com>
# SPDX-License-Identifier: MIT
#
""" This is an small ansible module for handling some operations related to a
tang server. """

import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

ANSIBLE_METADATA = {
    "metadata_version": "0.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: tang

short_description: Module for performing operations in a tang server

version_added: "2.5"

description:
    - "This module performs operations such as key management -- i.e.
        creating/rotating keys -- on a tang server."

author:
    - Sergio Correia
"""


class TangAnsibleError(Exception):
    """ The exceptions thrown by out module.    """


def generate_tang_keys(module, keygen, keydir):
    """ Runs the keygen for generating a pair of usable tang keys. """

    args = [keygen, keydir]

    try:
        ret_code, out, err = module.run_command(args)
    except Exception as exc:
        result = dict(
            msg="tangd-keygen failed: {}".format(to_native(exc)),
            ret_code=ret_code,
            stdout=out,
            stderr=err,
        )
        raise TangAnsibleError(result)

    return {"changed": True, "state": "keys-created"}


def create_keys(module, keygen, keydir, force):
    """ In here we create keys, if none exist or do it anyway, if the force
    parameter is true. """

    if not force:
        try:
            for listing in os.listdir(keydir):
                if listing.startswith("."):
                    continue
                return {"changed": False}
        except Exception as exc:
            result = dict(msg="Listing keys failed: {}".format(to_native(exc)))
            raise TangAnsibleError(result)

    return generate_tang_keys(module, keygen, keydir)


def rotate_keys(keydir):
    """ In here we rotate the existing keys. """

    total_rotated = 0
    try:
        for listing in os.listdir(keydir):
            if listing.startswith("."):
                continue
            old_file = os.path.join(keydir, listing)
            new_file = os.path.join(keydir, "." + listing)
            os.rename(old_file, new_file)
            total_rotated += 1
    except Exception as exc:
        result = dict(msg="Keys rotation failed: {}".format(to_native(exc)))
        raise TangAnsibleError(result)

    result = {"changed": False}
    if total_rotated > 0:
        result.update({"changed": True})

    return result


def run_module():
    """ The entry point of the module. """

    module_args = dict(
        name=dict(type="str", required=False),
        keygen=dict(type="str", required=False),
        keydir=dict(type="str", required=True),
        force=dict(type="bool", required=False, default=False),
        state=dict(type="str", required=False),
    )

    result = dict(changed=False, original_message="", message="")

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(**result)

    params = module.params
    state = params["state"]
    keygen = params["keygen"]
    keydir = params["keydir"]
    force = params["force"]

    if state == "keys-rotated":
        result = rotate_keys(keydir)
    elif state == "keys-created":
        result = create_keys(module, keygen, keydir, force)

    module.exit_json(**result)


def main():
    """ The main function! """
    run_module()


if __name__ == "__main__":
    main()

# vim:set ts=4 sw=4 et:
