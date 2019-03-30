# Ansible role documentation generator

Provides generation of ansible documentation for `role from first argument(path to role)` or if no args given current directory location.

Documentation for role is generated from jinja2 templates from `role_name/docs` path. 
Ansible role variables are read from `meta/main.yml`, `defaults/main.yml` and `vars/*.yml`. The last two are `optional`.

## Requirements

- `Python3`

Pip packages

- pip3 PyYAML
- pip3 Jinja2

You can use also requirement file:

```bash
pip install -r requirements.txt
```

`IMPORTANT`

1. `meta/main.yml` file needs to contain: ansible version, rolename, description and contributor.
2. Documentation template files should be in format `*.md.j2`
3. Main `README.md`(case sensitive) is `required` and automatically moved to `main role directory`, other generated md files stay in `docs directory`
4. Jinja2 Templates(for include/import) are read from `this_project_path/templates` and `given_role/docs` paths
5. `Ansible_documentation_generator_example_role` is an example role

## Example of usage

```bash
python3 generate_ansible_documentation.py Ansible_documentation_generator_example_role
```

## Example documentation template

```jinja
{{ auto_docs.title() }}

{{ auto_docs.description() }}

{{ auto_docs.requirements() }}

{{ auto_docs.platforms() }}

{{ auto_docs.defaults() }}

{{ auto_docs.vars() }}

{{ auto_docs.license() }}

{{ auto_docs.contributors() }}
```

## License

[Apache License 2.0](LICENSE)

## Support

ZeroDowntime <ansible@zerodowntime.pl>