Linux `nbde_server` role
======================

This role allows users to deploy an NBDE server. NBDE stands for Network-Bound Disk Encryption.

The current supported provider is `tang`.

Role Variables
--------------

| **Variable** | **Default** | **Description** |
|----------|-------------|------|
| `nbde_server_provider` | tang | identifies the provider for `nbde_server` role. We currently support `tang` as an `nbde_server` provider, meaning that the `nbde_server` role is currently able to provision/deploy a tang server
| `nbde_server_rotate_keys`| no | indicates whether we should rotate existing keys -- if any -- , then create new keys. Default behavior (`no`) is to create new keys, if there are none, and don't touch the keys, if they exist. If set to `yes`, existing keys will be rotated and new keys will be created
|`nbde_server_deploy_keys`| no |indicates whether we should deploy the specific keys located in `nbde_server_keys_dir` directory
|`nbde_server_fetch_keys`| no | indicates whether we should fetch keys to the control node, in which case they will be placed in `nbde_server_keys_dir`
|`nbde_server_keys_dir`|`"./keys"`| specifies a directory in the control node that either contains a set of keys to be deployed to the NBDE servers or keys lifted from the NBDE servers. Either `nbde_server_deploy_keys` or `nbde_server_fetch_keys` must be set to `yes` for this variable to have any effect. When deploying keys from this directory, the keys should be in the top level dir. This directory **must** exist

Example Playbook
----------------

```yaml
---
- name: Ensure NBDE server is deployed
  hosts: nbde_servers
  become: true

  roles:
    - role: nbde_server

# vim:set ts=2 sw=2 et:
```

License
-------

MIT
