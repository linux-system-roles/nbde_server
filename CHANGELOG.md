Changelog
=========

[1.3.8] - 2023-07-19
--------------------

### Bug Fixes

- fix: facts being gathered unnecessarily (#110)

### Other Changes

- ci: Add pull request template and run commitlint on PR title only (#105)
- ci: Rename commitlint to PR title Lint, echo PR titles from env var (#106)
- ci: fix python 2.7 CI tests by manually installing python2.7 package (#107)
- ci: ansible-lint - ignore var-naming[no-role-prefix] (#108)
- ci: ansible-test ignores file for ansible-core 2.15 (#109)

[1.3.7] - 2023-05-30
--------------------

### Bug Fixes

- fix: README.md headers should not be more than 72 characters

[1.3.6] - 2023-05-26
--------------------

### Other Changes

- docs: Consistent contributing.md for all roles - allow role specific contributing.md section
- docs: use Collection requirements section in README

[1.3.5] - 2023-04-27
--------------------

### Other Changes

- test: check generated files for ansible_managed, fingerprint
- ci: Add commitlint GitHub action to ensure conventional commits with feedback

[1.3.4] - 2023-04-06
--------------------

### Other Changes

- Add README-ansible.md to refer Ansible intro page on linux-system-roles.github.io
- Fingerprint RHEL System Role managed config files

[1.3.3] - 2023-02-08
--------------------

### New Features

- none

### Bug Fixes

- none

### Other Changes

- Skip the check for firewall --list-all - not needed

[1.3.2] - 2023-01-26
--------------------

### New Features

- none

### Bug Fixes

- fix some more Jinja constructs (#83)

These were causing issues on older platforms with older versions
of Jinja.

### Other Changes

- Create separate github actions for various checks; get rid of monolithic tox.yml (#82)

[1.3.1] - 2023-01-20
--------------------

### New Features

- none

### Bug Fixes

- ansible-lint 6.x fixes (#75)

### Other Changes

- Add check for non-inclusive language (#74)
- update ignore files for ansible-test 2.14

[1.3.0] - 2022-11-29
--------------------

### New Features

- none

### Bug Fixes

- fix behavior of manage_firewall and manage_selinux; ansible-lint 6.x (#69)

If `nbde_server_manage_firewall: true`, manage firewall for the port,
even if not using a custom port.
If `nbde_server_manage_selinux: true`, manage SELinux for the port,
even if not using a custom port.
Clean up role for ansible-lint 6.x
If using the default port, remove the tangd socket file and systemd
directory, if any, and reload systemd.
Add test to check resetting the port works
Improve test to check for port to handle cases where there are processes
running on the test system with similar ports open

### Other Changes

- none

[1.2.0] - 2022-11-01
--------------------

### New Features

- Add support for custom ports (#38)

- Introduce nbde_server_manage_firewall and nbde_server_manage_selinux
to manage the custom ports implemented in "Add support for custom
ports (#38)"

- If nbde_server_manage_firewall is set to true, use the firewall
  role to manage the nbde server port.

- If nbde_server_manage_selinux is set to true, use the selinux
  role to manage the nbde server port.

### Bug Fixes

- none

### Other Changes

- none

[1.1.5] - 2022-07-19
--------------------

### New Features

- none

### Bug Fixes

- none

### Other Changes

- make all tests work with gather_facts: false (#55)

Ensure the test works when using ANSIBLE_GATHERING=explicit

- make min_ansible_version a string in meta/main.yml (#56)

The Ansible developers say that `min_ansible_version` in meta/main.yml
must be a `string` value like `"2.9"`, not a `float` value like `2.9`.

- Add CHANGELOG.md (#57)

[1.1.4] - 2022-05-06
--------------------

### New Features

- none

### Bug Fixes

- none

### Other Changes

- bump tox-lsr version to 2.11.0; remove py37; add py310

[1.1.3] - 2022-04-19
--------------------

### New Features

- support gather\_facts: false; support setup-snapshot.yml

### Bug Fixes

- none

### Other Changes

- bump tox-lsr version to 2.10.1

[1.1.2] - 2022-01-10
--------------------

### New Features

- none

### Bug Fixes

- none

### Other Changes

- bump tox-lsr version to 2.8.3
- change recursive role symlink to individual role dir symlinks

[1.1.1] - 2021-11-08
--------------------

### New Features

- support python 39, ansible-core 2.12, ansible-plugin-scan

### Bug Fixes

- fix python black issues

### Other Changes

- update tox-lsr version to 2.7.1
- make role work with ansible-core-2.11 ansible-lint and ansible-test
- use apt-get install -y

[1.1.0] - 2021-08-10
--------------------

### New Features

- Drop support for Ansible 2.8 by bumping the Ansible version to 2.9

### Bug Fixes

- none

### Other Changes

- none

[1.0.3] - 2021-04-07
--------------------

### New Features

- none

### Bug Fixes

- Fix ansible-test errors
- Fix issues found by ansible-test and linters - enable all tests on all repos - remove suppressions

### Other Changes

- Remove python-26 environment from tox testing
- update to tox-lsr 2.4.0 - add support for ansible-test with docker
- CI: Add support for RHEL-9

[1.0.2] - 2021-02-11
--------------------

### New Features

- Add centos8

### Bug Fixes

- Fix centos6 repos; use standard centos images

### Other Changes

- use tox-lsr 2.2.0
- use molecule v3, drop v2
- Make the var load test compatible with old Jinja2 \(2.7\)
- remove ansible 2.7 support from molecule
- use tox for ansible-lint instead of molecule
- use new tox-lsr plugin
- use github actions instead of travis

[1.0.1] - 2020-10-31
--------------------

### New Features

- none

### Bug Fixes

- none

### Other Changes

- meta/main.yml: CI - add support for Fedora 33
- lock ansible-lint version at 4.3.5; suppress role name lint warning
- sync collections related changes from template to nbde\_server role

[1.0.0] - 2020-08-12
--------------------

### Initial Release
