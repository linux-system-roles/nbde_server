#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sergio Correia <scorreia@redhat.com>
# SPDX-License-Identifier: MIT
#
""" This is an small ansible module for handling some operations related to a
tang server. """

import os
import filecmp
from shutil import copyfile
from shutil import rmtree

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

    result = {"changed": True, "state": "keys-created"}
    if not module.check_mode:
        result = generate_tang_keys(module, keygen, keydir)
    return result


def rotate_keys(module, keydir, newkeys):
    """ In here we rotate the existing keys. """

    result = {"changed": False}

    total_rotated = 0
    list_rotated = []
    try:
        for listing in os.listdir(keydir):
            if listing.startswith("."):
                continue

            if newkeys and listing in newkeys:
                continue

            old_file = os.path.join(keydir, listing)
            new_file = os.path.join(keydir, "." + listing)
            list_rotated.append("{} -> {}".format(old_file, new_file))
            if not module.check_mode:
                os.rename(old_file, new_file)
            total_rotated += 1
    except Exception as exc:
        result = dict(msg="Keys rotation failed: {}".format(to_native(exc)))
        raise TangAnsibleError(result)

    if total_rotated > 0:
        result["changed"] = True
        result["rotated"] = list_rotated

    return result


def deploy_keys(module, keydir, base_keysdir, keys_to_deploy_dir):
    """ Depoy a specific set of keys from keys_to_deploy_dir to keydir. """

    result = {"changed": False}
    rotate_result = {"changed": False}

    try:
        new_dir = os.path.join(base_keysdir, keys_to_deploy_dir)
        total_deployed = 0
        list_deployed = []
        locally_rotated = []
        newkeys = {}

        for listing in os.listdir(new_dir):
            if not listing.endswith(".jwk"):
                continue

            newkeys[listing] = listing
            src = os.path.join(new_dir, listing)
            dst = os.path.join(keydir, listing)

            if os.path.exists(dst):
                if filecmp.cmp(src, dst):
                    continue
                else:
                    new_file = ".rotated-" + dst
                    locally_rotated.append("{} -> {}".format(dst, new_file))
                    if not module.check_mode:
                        os.rename(dst, new_file)

            list_deployed.append(dst)
            if not module.check_mode:
                copyfile(src, dst)
            total_deployed += 1

        rotate_result = rotate_keys(module, keydir, newkeys)
        # This is just a temp directory.
        rmtree(base_keysdir)

    except Exception as exc:
        result = dict(msg="Keys deployment failed: {}".format(to_native(exc)))
        raise TangAnsibleError(result)

    if total_deployed > 0 or rotate_result["changed"]:
        result["changed"] = True
        result["deployed"] = list_deployed
        result["rotated"] = locally_rotated
        if "rotated" in rotate_result:
            result["rotated"].extend(rotate_result["rotated"])
    return result


def run_module():
    """ The entry point of the module. """

    module_args = dict(
        name=dict(type="str", required=False),
        keygen=dict(type="str", required=False),
        keydir=dict(type="str", required=False),
        force=dict(type="bool", required=False, default=False),
        state=dict(type="str", required=False),
        keys_to_deploy_dir=dict(type="str", required=False),
        base_keys_to_deploy_dir=dict(type="str", required=False),
    )

    result = dict(changed=False, original_message="", message="")

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    params = module.params
    state = params["state"]
    keygen = params["keygen"]
    keydir = params["keydir"]
    force = params["force"]
    keys_to_deploy_dir = params["keys_to_deploy_dir"]
    base_keysdir = params["base_keys_to_deploy_dir"]

    if state == "keys-created":
        result = create_keys(module, keygen, keydir, force)
    elif state == "keys-deployed":
        result = deploy_keys(module, keydir, base_keysdir, keys_to_deploy_dir)

    module.exit_json(**result)


def main():
    """ The main function! """
    run_module()


if __name__ == "__main__":
    main()

# vim:set ts=4 sw=4 et:
