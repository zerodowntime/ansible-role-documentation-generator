# Ansible role documentation generator

Provides generation of ansible documentation for `role from first argument(path to role)` or if no args given current directory location.

Documentation for role is generated from jinja2 templates from `role_name/docs` path. 
Ansible role variables are read from `meta/main.yml`, `defaults/main.yml` and `vars/*.yml`. The last two are `optional`.

## Requirements

- Python3
- pip3 pyyml
- pip3 jinja2

`IMPORTANT`

2. `meta/main.yml` file needs to contain: ansible version, rolename, description and contributor.
3. Documentation template files should be in format `*.md.j2`
4. Main `README.md`(case sensitive) is `required` and automatically moved to `main role directory`, other generated md files stay in `docs directory`
5. Jinja2 Templates(for include/import) are read from `this_project_path/templates` and `given_role/docs` paths
6. `Ansible_documentation_generator_example_role` is an example role

## Example of usage

```bash
python3 generate_ansible_documentation.py Ansible_documentation_generator_example_role
```

## Example documentation template

`Please replace single braces with double braces(here ommited for example docs ^^)`

```jinja
{ auto_docs.title() }

{ auto_docs.description() }

{ auto_docs.requiremenents() }

{ auto_docs.defaults() }

{ auto_docs.vars() }

{ auto_docs.contributors() }
```

### Contributor

- ZeroDowntime | wojciech.polnik@zerodowntime.pl