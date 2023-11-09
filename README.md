# nbde_server

[![ansible-lint.yml](https://github.com/linux-system-roles/nbde_server/actions/workflows/ansible-lint.yml/badge.svg)](https://github.com/linux-system-roles/nbde_server/actions/workflows/ansible-lint.yml) [![ansible-test.yml](https://github.com/linux-system-roles/nbde_server/actions/workflows/ansible-test.yml/badge.svg)](https://github.com/linux-system-roles/nbde_server/actions/workflows/ansible-test.yml) [![codeql.yml](https://github.com/linux-system-roles/nbde_server/actions/workflows/codeql.yml/badge.svg)](https://github.com/linux-system-roles/nbde_server/actions/workflows/codeql.yml) [![markdownlint.yml](https://github.com/linux-system-roles/nbde_server/actions/workflows/markdownlint.yml/badge.svg)](https://github.com/linux-system-roles/nbde_server/actions/workflows/markdownlint.yml) [![python-unit-test.yml](https://github.com/linux-system-roles/nbde_server/actions/workflows/python-unit-test.yml/badge.svg)](https://github.com/linux-system-roles/nbde_server/actions/workflows/python-unit-test.yml) [![woke.yml](https://github.com/linux-system-roles/nbde_server/actions/workflows/woke.yml/badge.svg)](https://github.com/linux-system-roles/nbde_server/actions/workflows/woke.yml)

Ansible role for configuring Network-Bound Disk Encryption servers (e.g. tang).

This role currently supports `tang` as a provider and it can set up tang servers.

## Supported Distributions

* RHEL-7+, CentOS-7+
* Fedora

## Requirements

See below

### Collection requirements

The role requires additional collections which are specified in `meta/collection-requirements.yml`.  These are not automatically installed.  You must install them like this:

```bash
ansible-galaxy install -vv -r meta/collection-requirements.yml`
```

## Role Variables

These are the variables that can be passed to the role:

| **Variable** | **Default** | **Description** |
|----------|-------------|------|
| `nbde_server_provider` | `tang` | identifies the provider for `nbde_server` role. We currently support `tang` as an `nbde_server` provider, meaning that the `nbde_server` role is currently able to provision/deploy tang servers.
| `nbde_server_service_state` | `started` | indicates the state the nbde_server should be. It can be either `started` (default) or `stopped`. `started` means the server is accepting connections, whereas `stopped` means it is not accepting connections.
| `nbde_server_rotate_keys`| `false` | indicates whether we should rotate existing keys -- if any -- , then create new keys. Default behavior (`false`) is to create new keys, if there are none, and don't touch the keys, if they exist. If set to `true`, existing keys will be rotated and new keys will be created.
|`nbde_server_fetch_keys`| `false` | indicates whether we should fetch keys to the control node, in which case they will be placed in `nbde_server_keys_dir`. You **must** set `nbde_server_keys_dir` to use `nbde_server_fetch_keys`.
|`nbde_server_deploy_keys`| `false` |indicates whether we should deploy the keys located in `nbde_server_keys_dir` directory to the remote hosts. You **must** set `nbde_server_keys_dir` to use `nbde_server_deploy_keys`.
|`nbde_server_keys_dir`| | specifies a directory in the control node that contains keys to be deployed to the remote hosts. Keys located in the top level directory will be deployed to every remote host, while keys located within subdirectories named after the remote hosts  -- as per the inventory -- will be deployed only to these specific hosts. `nbde_server_keys_dir` **must** be an absolute path. You need to set this to use either `nbde_server_fetch_keys` and/or `nbde_server_deploy_keys`.
|`nbde_server_manage_firewall`| `false` | manage the nbde server port and zone using the `firewall` role if set to `true`.
|`nbde_server_manage_selinux`| `false` | manage the nbde server port using the `selinux` role if set to `true`.
|`nbde_server_port`| `80` | port number that tangd will listen on.  You **must** set `nbde_server_manage_selinux: true` if you want the role to manage SELinux labeling for the port.  You **must** set `nbde_server_manage_firewall: true` if you want the role to manage firewall for the port.
|`nbde_server_firewall_zone`| `public` | change the default zone where the port should be opened. You **must** set `nbde_server_manage_firewall: true` to change the default zone.

### nbde_server_fetch_keys and nbde_server_deploy_keys

To use either of these options, you need to specify `nbde_server_keys_dir`, a directory, with an absolute path.

The behavior of using these variables is described next:

#### When `nbde_server_fetch_keys` is set to `true`

The role will fetch keys from the hosts in the following manner:

* if `nbde_server_deploy_keys` is not set, the keys from every host will be fetched and placed in directories named after the host,
  inside `nbde_server_keys_dir`
* if `nbde_server_deploy_keys` is set, only the keys from the first host in the inventory will be fetched, and it will be placed in
  the top level directory of `nbde_server_keys_dir`

#### When `nbde_server_deploy_keys` is set to `true`

The role will deploy the keys available in `nbde_server_keys_dir`, in the following manner:

* the keys located in the top level directory of `nbde_server_keys_dir` will be deployed to every host
* the keys located within subdirectories named after hosts in the inventory, inside `nbde_server_keys_dir`, will be deployed to that
  specific host

## Example Playbooks

### Example 1: deploy NBDE server to every host in the inventory

```yaml
---
- name: Manage nbde servers
  hosts: all
  roles:
    - linux-system-roles.nbde_server
```

### Example 2: grab keys from NBDE server installs

Grab the keys from every NBDE server install from /root/nbde_server/keys`

```yaml
---
- name: Manage nbde keys from /root/nbde_server/keys
  hosts: all
  vars:
    nbde_server_fetch_keys: true
    nbde_server_keys_dir: /root/nbde_server/keys
  roles:
    - linux-system-roles.nbde_server
```

After this, you can backup your keys, which will be placed in `/root/nbde_server/keys`, within subdirectories named after the host they belong to.

### Example 3: redeploy keys from a backup taken with Example 2

To redeploy keys, they must be placed into subdirectories named after the host they are to be deployed to. With `/root/nbde_server/keys` after Example 2, use the following playbook to redeploy the same keys to the same hosts:

```yaml
---
- name: Manage nbde and redeploy backed up keys
  hosts: all
  vars:
    nbde_server_deploy_keys: true
    nbde_server_keys_dir: /root/nbde_server/keys
  roles:
    - linux-system-roles.nbde_server
```

### Example 4: deploy an NBDE server and use the same keys in every host

**NOTE** This is not recommended, but it is supported

```yaml
---
- name: Manage nbde with same keys on every host
  hosts: all
  vars:
    nbde_server_fetch_keys: true
    nbde_server_deploy_keys: true
    nbde_server_keys_dir: /root/nbde_server/keys
  roles:
    - linux-system-roles.nbde_server
```

### Example 5: deploy NBDE server with custom port and zone

```yaml
---
- name: Manage nbde with custom port and zone
  hosts: all
  vars:
    nbde_server_manage_firewall: true
    nbde_server_manage_selinux: true
    nbde_server_port: 7500
    nbde_server_firewall_zone: dmz
  roles:
    - linux-system-roles.nbde_server
```

## rpm-ostree

See README-ostree.md

## License

MIT
