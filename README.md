# Ansible role documentation generator

Provides generation of ansible documentation for `role from first argument(path to role)` or if no args given current directory location

## Requirements

- Python3
- pip3 pyyml
- pip3 jinja2

`IMPORTANT`

1. Documentation for role is read from `role_name/docs` path
2. Files should be in format `*.md.j2`
3. Main `README.md`(case sensitive) is automatically moved to `main role directory`, other generated md files stay in `docs directory`
4. Templates are read from `this_project_path/templates` and `given_role/docs`

## Example of usage

```bash
python3 generate_ansible_documentation.py path_to_the_role
```

### Contributor

- ZeroDowntime | wojciech.polnik@zerodowntime.pl