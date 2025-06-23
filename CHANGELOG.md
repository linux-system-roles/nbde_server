Changelog
=========

[1.5.0] - 2025-06-23
--------------------

### New Features

- feat: Support this role in container builds (#188)

### Other Changes

- ci: Add support for bootc end-to-end validation tests (#186)
- ci: Use ansible 2.19 for fedora 42 testing; support python 3.13 (#187)

[1.4.10] - 2025-05-21
--------------------

### Other Changes

- ci: ansible-plugin-scan is disabled for now (#170)
- ci: bump ansible-lint to v25; provide collection requirements for ansible-lint (#173)
- refactor: fix python black formatting (#174)
- ci: Check spelling with codespell (#175)
- ci: Add test plan that runs CI tests and customize it for each role (#176)
- ci: In test plans, prefix all relate variables with SR_ (#177)
- ci: Fix bug with ARTIFACTS_URL after prefixing with SR_ (#178)
- ci: several changes related to new qemu test, ansible-lint, python versions, ubuntu versions (#179)
- ci: use tox-lsr 3.6.0; improve qemu test logging (#180)
- ci: skip storage scsi, nvme tests in github qemu ci (#181)
- ci: Bump sclorg/testing-farm-as-github-action from 3 to 4 (#182)
- ci: bump tox-lsr to 3.8.0; rename qemu/kvm tests (#183)
- ci: Add Fedora 42; use tox-lsr 3.9.0; use lsr-report-errors for qemu tests (#184)

[1.4.9] - 2025-01-09
--------------------

### Other Changes

- ci: Bump codecov/codecov-action from 4 to 5 (#166)
- ci: Use Fedora 41, drop Fedora 39 (#167)
- ci: Use Fedora 41, drop Fedora 39 - part two (#168)

[1.4.8] - 2024-10-30
--------------------

### Other Changes

- ci: Add workflow for ci_test bad, use remote fmf plan (#158)
- ci: Fix missing slash in ARTIFACTS_URL (#159)
- ci: Add tags to TF workflow, allow more [citest bad] formats (#160)
- ci: ansible-test action now requires ansible-core version (#161)
- ci: add YAML header to github action workflow files (#162)
- refactor: Use vars/RedHat_N.yml symlink for CentOS, Rocky, Alma wherever possible (#164)

[1.4.7] - 2024-08-01
--------------------

### Bug Fixes

- fix: Remove hard dependency on selinux and firewall roles (#154)

### Other Changes

- ci: Add tft plan and workflow (#152)
- ci: Update fmf plan to add a separate job to prepare managed nodes (#155)
- ci: Bump sclorg/testing-farm-as-github-action from 2 to 3 (#156)

[1.4.6] - 2024-07-02
--------------------

### Bug Fixes

- fix: add support for EL10 (#150)

### Other Changes

- ci: ansible-lint action now requires absolute directory (#149)

[1.4.5] - 2024-06-11
--------------------

### Other Changes

- ci: use tox-lsr 3.3.0 which uses ansible-test 2.17 (#144)
- ci: tox-lsr 3.4.0 - fix py27 tests; move other checks to py310 (#146)
- ci: Add supported_ansible_also to .ansible-lint (#147)

[1.4.4] - 2024-04-04
--------------------

### Other Changes

- ci: Bump ansible/ansible-lint from 6 to 24 (#141)
- ci: Bump mathieudutour/github-tag-action from 6.1 to 6.2 (#142)

[1.4.3] - 2024-02-14
--------------------

### Bug Fixes

- fix: Allow tangd socket override directory to be managed outside of the role (#139)

### Other Changes

- ci: Bump codecov/codecov-action from 3 to 4 (#136)
- ci: fix python unit test - copy pytest config to tests/unit (#137)

[1.4.2] - 2024-01-16
--------------------

### Other Changes

- ci: Bump github/codeql-action from 2 to 3 (#130)
- ci: Bump actions/setup-python from 4 to 5 (#131)
- ci: support ansible-lint and ansible-test 2.16 (#132)
- tests: perform cleanup after each test (#133)
- ci: Use supported ansible-lint action; run ansible-lint against the collection (#134)

[1.4.1] - 2023-12-08
--------------------

### Other Changes

- ci: bump actions/github-script from 6 to 7 (#127)
- refactor: get_ostree_data.sh use env shebang - remove from .sanity* (#128)

[1.4.0] - 2023-11-29
--------------------

### New Features

- feat: support for ostree systems (#124)

### Other Changes

- Bump actions/checkout from 3 to 4 (#116)
- ci: ensure dependabot git commit message conforms to commitlint (#119)
- ci: tox-lsr version 3.1.1 (#123)

[1.3.9] - 2023-09-08
--------------------

### Other Changes

- ci: Add markdownlint, test_converting_readme, and build_docs workflows (#112)

  - markdownlint runs against README.md to avoid any issues with
    converting it to HTML
  - test_converting_readme converts README.md > HTML and uploads this test
    artifact to ensure that conversion works fine
  - build_docs converts README.md > HTML and pushes the result to the
    docs branch to publish dosc to GitHub pages site.
  - Fix markdown issues in README.md
  
  Signed-off-by: Sergei Petrosian <spetrosi@redhat.com>

- docs: Make badges consistent, run markdownlint on all .md files (#113)

  - Consistently generate badges for GH workflows in README RHELPLAN-146921
  - Run markdownlint on all .md files
  - Add custom-woke-action if not used already
  - Rename woke action to Woke for a pretty badge
  
  Signed-off-by: Sergei Petrosian <spetrosi@redhat.com>

- ci: Remove badges from README.md prior to converting to HTML (#114)

  - Remove thematic break after badges
  - Remove badges from README.md prior to converting to HTML
  
  Signed-off-by: Sergei Petrosian <spetrosi@redhat.com>

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
