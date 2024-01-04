#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sergio Correia <scorreia@redhat.com>
# SPDX-License-Identifier: MIT
#
""" This is an small ansible module for handling some operations related to a
tang server. """

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "0.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: nbde_server_tang

short_description: Handle key management operations in a tang server.

description:
    - "WARNING: Do not use this module directly! It is only for role internal use."
    - "This module performs operations such as key management -- i.e.
        creating/rotating keys -- on a tang server."
options:
    state:
        description:
            - |
              indicates the state to achieve, which basically maps to
              certain operations to be performed.
              If no state is specified, no action is performed.
            - |
              keys-rotated:
              this performs a key rotation followed by the creation of new
              keys. Required parameters are keygen and keydir, that point
              to the tang key generation tool and the tang key directory.
              Optional arguments are update and cachedir.  When these
              arguments are provided, the cache is updated when there are changes.
            - |
              keys-created:
              creates a new set of keys, if none exist. As keys-rotated,
              also take keygen and keydir as arguments, that point to the
              tang key generation tool and its key directory. Similarly to
              keys-rotated, optional arguments update and cachedir can be
              passed to keys-created.
            - |
              keys-deployed:
              deploys keys that are present in keys_to_deploy_dir. This
              argument indicates a directory in the machine that runs the
              tang server where there are new keys to be deployed to the
              tang server. Additional arguments are keygen  and keydir,
              similar to keys-rotated and keys-created. Note that, since
              this directory is in the remote machine, you are expected
              to place the keys in there beforehand. Similar to previous
              states, keys-deployed also accepts optional arguments
              update and cachedir.
            - |
              cache-updated:
              updates the tang server cache. Besides keydir, the keys
              directory of the server, it requires the following
              parameters: update and cachedir.
        choices: [ keys-rotated, keys-created, keys-deployed, cache-updated ]
        type: str
    keygen:
        description: tang key generation tool "/usr/libexec/tangd-keygen"
        type: str
    keydir:
        description: key database directory on the Tang server "/var/db/tang"
        type: str
    update:
        description: the tool for performing a cache update "/usr/libexec/tangd-update"
        type: str
    cachedir:
        description: cache directory
        type: str
    force:
        description: force to create keys
        type: bool
        default: False
    keys_to_deploy_dir:
        description: deploys keys that are present in keys_to_deploy_dir
        type: str

author:
    - Sergio Correia (@sergio-correia)
"""


EXAMPLES = """
---
- name: Create new keys
  nbde_server_tang:
    state: keys-created
    keygen: /usr/libexec/tangd-keygen
    keydir: /var/db/tang

- name: Rotate keys
  nbde_server_tang:
    state: keys-rotated
    keygen: /usr/libexec/tangd-keygen
    keydir: /var/db/tang

- name: Deploy keys from /root/keys
  nbde_server_tang:
    state: keys-rotated
    keygen: /usr/libexec/tangd-keygen
    keydir: /var/db/tang
    keys_to_deploy_dir: /root/keys

- name: Update cache
  nbde_server_tang:
    state: cache-updated
    update: /usr/libexec/tangd-update
    keydir: /usr/db/tang
    cachedir: /var/cache/tang
"""


RETURN = """
state:
    description: The state that was passed as argument.
    type: str
    returned: always
arguments:
    description: The arguments passed to the module.
    type: dict
    returned: always
msg:
    description: The output message the module may generate.
    type: str
    returned: always
"""


import os
import filecmp

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


class TangAnsibleError(Exception):
    """The exceptions thrown by out module."""


def generate_tang_keys(module, keygen, keydir):
    """Runs the keygen for generating a pair of usable tang keys."""
    args = [keygen, keydir]

    ret, out, err = module.run_command(args)
    if ret != 0:
        result = dict(
            msg="tangd-keygen failed: {0}".format(err),
            ret_code=ret,
            stdout=out,
            stderr=err,
        )
        raise TangAnsibleError(result)

    return {"changed": True, "state": "keys-created"}


def create_keys(module, keygen, keydir, force):
    """In here we create keys, if none exist or do it anyway, if the force
    parameter is true."""

    if not force:
        try:
            for listing in os.listdir(keydir):
                if listing.startswith("."):
                    continue
                return {"changed": False}
        except Exception as exc:
            result = dict(msg="Listing keys failed: {0}".format(to_native(exc)))
            raise TangAnsibleError(result)

    result = {"changed": True, "state": "keys-created"}
    if not module.check_mode:
        result = generate_tang_keys(module, keygen, keydir)
    return result


def rotate_keys(module, keydir, newkeys):
    """In here we rotate the existing keys."""

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
            list_rotated.append("{0} -> {1}".format(old_file, new_file))
            if not module.check_mode:
                os.rename(old_file, new_file)
            total_rotated += 1
    except Exception as exc:
        result = dict(msg="Keys rotation failed: {0}".format(to_native(exc)))
        raise TangAnsibleError(result)

    if total_rotated > 0:
        result["changed"] = True
        result["rotated"] = list_rotated

    return result


def deploy_keys(module, keydir, keys_to_deploy_dir):
    """Deploy a specific set of keys from keys_to_deploy_dir to keydir."""

    result = {"changed": False}
    rotate_result = {"changed": False}

    if not os.path.isdir(keys_to_deploy_dir):
        return result

    try:
        total_deployed = 0
        list_deployed = []
        locally_rotated = []
        newkeys = {}

        for listing in os.listdir(keys_to_deploy_dir):
            if not listing.endswith(".jwk"):
                continue

            newkeys[listing] = listing
            src = os.path.join(keys_to_deploy_dir, listing)
            dst = os.path.join(keydir, listing)

            if os.path.exists(dst):
                if filecmp.cmp(src, dst):
                    continue
                new_file = ".rotated-" + dst
                locally_rotated.append("{0} -> {1}".format(dst, new_file))
                if not module.check_mode:
                    module.atomic_move(dst, new_file)

            list_deployed.append(dst)
            if not module.check_mode:
                module.atomic_move(src, dst)
            total_deployed += 1

        rotate_result = rotate_keys(module, keydir, newkeys)

    except Exception as exc:
        result = dict(msg="Keys deployment failed: {0}".format(to_native(exc)))
        raise TangAnsibleError(result)

    if total_deployed > 0 or rotate_result["changed"]:
        result["changed"] = True
        result["deployed"] = list_deployed
        result["rotated"] = locally_rotated
        if "rotated" in rotate_result:
            result["rotated"].extend(rotate_result["rotated"])
    return result


def update_cache(module, keydir, cachedir, update):
    """Update tang cache."""

    if not os.path.isfile(update):
        return {"changed": False}

    if not module.check_mode:
        args = [update, keydir, cachedir]
        ret, _unused1, _unused2 = module.run_command(args)
        if ret != 0:
            return {"changed": False}
    set_file_ownership_and_perms(module, cachedir)
    return {"changed": True}


def get_dir_ownership(module, target):
    """Returns the uid/gid from the target directory."""

    if module.check_mode or not os.path.isdir(target):
        return None, None

    st_info = os.stat(target)
    uid = st_info.st_uid
    gid = st_info.st_gid
    return uid, gid


def set_file_ownership_and_perms(module, target):
    """Sets the ownership (via uid and gid) and file permissions (0400)
    to the target directory; uid and gid come from the target dir."""

    if module.check_mode or not os.path.isdir(target):
        return

    uid, gid = get_dir_ownership(module, target)
    if not uid or not gid:
        return

    for listing in os.listdir(target):
        if not listing.endswith(".jwk"):
            continue
        fname = os.path.join(target, listing)
        os.chown(fname, uid, gid)
        os.chmod(fname, 0o400)


def run_module():
    """The entry point of the module."""

    module_args = dict(
        keygen=dict(type="str", required=False, no_log=False),
        keydir=dict(type="str", required=False, no_log=False),
        cachedir=dict(type="str", required=False),
        update=dict(type="str", required=False),
        force=dict(type="bool", required=False, default=False),
        state=dict(
            type="str",
            required=False,
            choices=["keys-rotated", "keys-created", "keys-deployed", "cache-updated"],
        ),
        keys_to_deploy_dir=dict(type="str", required=False, no_log=False),
    )

    result = dict(changed=False)

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    params = module.params
    state = params["state"]
    keygen = params["keygen"]
    keydir = params["keydir"]
    cachedir = params["cachedir"]
    update = params["update"]
    force = params["force"]
    keys_to_deploy_dir = params["keys_to_deploy_dir"]

    if state == "keys-created":
        result = create_keys(module, keygen, keydir, force)
    elif state == "keys-rotated":
        # We will rotate existing keys and then create new keys.
        rotate_keys(module, keydir, None)
        result = create_keys(module, keygen, keydir, force)
    elif state == "keys-deployed":
        result = deploy_keys(module, keydir, keys_to_deploy_dir)
    elif state == "cache-updated":
        result = update_cache(module, keydir, cachedir, update)

    # Update the cache when operations changed the keys.
    if result["changed"]:
        set_file_ownership_and_perms(module, keydir)
        if state != "cache-updated":
            update_cache(module, keydir, cachedir, update)

    result["state"] = state
    result["arguments"] = params
    module.exit_json(**result)


def main():
    """The main function!"""
    run_module()


if __name__ == "__main__":
    main()
