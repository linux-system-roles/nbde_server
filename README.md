Linux tang role
=========

This role allows users to deploy a tang server.

Role Variables
--------------

TBD

Example Playbook
----------------

```yaml

- name: Ensure tang is deployed
  hosts: tang_servers

  roles:
    - role: linux-system-roles.tang
      become: true
      rotate_keys: no
      create_new_keys: no
      state: started

# vim:set ts=2 sw=2 et:
```

License
-------

MIT
