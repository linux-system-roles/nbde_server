Linux `nbde_server` role
======================

This role allows users to deploy an NBDE server.
NBDE stands for Network-Bound Disk Encryption.

The current supported provider is `tang`.

Role Variables
--------------

### `nbde_server_provider`
The `nbde_server_provider` variable identifies the provider for `nbde_server` role. We currently support `tang` as an `nbde_server` provider, meaning
that the `nbde_server` role is currently able to provision/deploy a tang server. Default is `tang`.

### `nbde_server_create_new_keys`
The `nbde_server_create_new_keys` variable indicates whether we should create new keys to be used when deploying the NBDE server. Default is `no`.

### `nbde_server_deploy_keys`
The `nbde_server_deploy_new_keys` variable indicates whether we should deploy specific keys located in `nbde_server_keys_dir` directory. Default is `no`.

### `nbde_server_fetch_keys`
The `nbde_server_fetch_keys` variable indicates whether we should fetch keys to the management node. Default is `no`.

### `nbde_server_keys_dir`
The `nbde_server_keys_dir` variable specifies a directory in the control node that either contains a set of keys to be deployed to the NBDE servers or keys lifted from the NBDE servers. Either `nbde_server_deploy_new_keys` or `nbde_server_fetch_keys` must be set to `yes` for this variable to have any effect. When deploying keys from this directory, the keys should be in the top level dir. This directory *must* exist. Default is `"keys"`.

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
