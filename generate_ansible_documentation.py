#!/usr/bin/env python3
# read yml
import yaml
import sys
import os
# move
import shutil as sh
# get all files in regex given path
import glob
# jinja things ENVIRONMENT, LOADER, TEMPLATE etc
import jinja2 as j2

# DEBUG flag
DEBUG = False

# required keys by documentation in defaults/main.yml
defaults_required_keys = {
  'type': 'string',
  'required': 'yes',
  'description': None,
}

# required keys by documentation in vars/*.yml
vars_required_keys = {
  'type': 'string',
  'description': None,
}

# name of ansible documentation template file
ansible_documentation_macros = 'ansible.documentation.macros.j2'

# add to the path begin this python script path
def use_script_path(path):
  return os.path.dirname(os.path.realpath(__file__)) + "/" + path

# read file and return list of lines
def get_file_lines(path):
  with open(path, 'r') as stream:
    lines = stream.readlines()
    if DEBUG:
      print(lines)
  return lines

# join list on lines into one yml file
def get_yaml_from_lines(lines):  
  # read default variables
  try:
    object = yaml.load("".join(lines), Loader=yaml.FullLoader)
    if DEBUG:
      print(object)
  except yaml.YAMLError as exc:
    print(exc)
  return object if object else dict()

# reads yml variables once and commented with "#?" yml, then merges them together,
# original yml values are as defaults to the documentation, 
# it can be override with 'default' key in documentation yml
def get_doc_variables_object(lines, original_yml, variable_type):

  # parse in-comment yml
  stream_documentation = []
  [ stream_documentation.append(line.strip("#?")) for line in lines if line.startswith( "#?" )]
  
  documentation_yml = get_yaml_from_lines(stream_documentation)

  # merge original with documentation yml
  for key in original_yml:
    if key in documentation_yml:
      # if no default overide apply the one from original yml
      if "default" not in documentation_yml[key]:
        # add defaults
        documentation_yml[key]["default"] = original_yml[key]
    else:
      print("WARN: {0} variable is not covered in {1}".format(key, variable_type))

  return documentation_yml

# check if required variables are present, if are not error, if there default then warn
def get_validated_object(documentation_object, valid_object, type):
  for variable, keys in documentation_object.items():
    for required_key, default in valid_object.items():
      if required_key not in keys:
        if default is not None:
          print("WARN: '{0}' does not cover '{1}' key in {3}, applied default '{2}'".format(variable, required_key, default, type))
          documentation_object[variable][required_key] = default
        else:
          print("ERROR: '{0}' does not cover '{1}' key in {2}".format(variable, required_key, type))
  return documentation_object

# read file, get is yml and finally return object with documentation variables
def get_variables(path, required_keys, variable_type):
  lines = get_file_lines(path)
  variables = get_yaml_from_lines(lines)
  variables_object = get_doc_variables_object(lines, variables, variable_type)
  return get_validated_object(variables_object, required_keys, variable_type)

# get defaults variables object
def handle_defaults(path):
  return get_variables(path, required_keys=defaults_required_keys, variable_type="defaults/main.yml") if os.path.exists(path) else dict()

# get vars variables object - main.yml and others in vars/*.yml
def handle_vars(path):
  # all files in vars/*.yml
  variables_files = glob.glob(path)
  vars_object = dict()
  for file_path in variables_files:
    # name of file
    file_with_extension = os.path.basename(file_path)
    # name without extension
    filename = file_with_extension[:-4]
    # object for this file, data as dict with its documentation variables and filename as filename with extension
    data = get_variables(file_path, required_keys=vars_required_keys, variable_type="vars/" + file_with_extension)
    if data:
      vars_file_object = dict(data = data, filename = file_with_extension)
      # add to vars dictionary generated object
      vars_object[filename] = vars_file_object
  # this.file_without_extension.data|filename
  return vars_object

# get meta variables object
def handle_meta(path):
  meta_lines = get_file_lines(path)
  meta_object = get_yaml_from_lines(meta_lines)
  return meta_object

# return jinja generated file
def get_documentation(template, meta, defaults=None, vars=None, extra_paths=[]):
  # templated with auto imported macros
  template = "{% import '" + ansible_documentation_macros +  "' as auto_docs with context %}" + template
  # loader to be able to read and import templates from this_script_dir_path/templates + any given extra paths
  loader = j2.FileSystemLoader([os.path.dirname(os.path.realpath(__file__)) + "/templates"] + extra_paths)
  if DEBUG:
    print("given paths", [os.path.dirname(os.path.realpath(__file__)) + "/templates"] + extra_paths)
    print("loaded templates", j2.Environment(loader=loader).list_templates())
  # return generated tempalted with loader and applied variables documentation_vars.meta|defaults|vars
  return j2.Environment(loader=loader).from_string(template).render(documentation_vars=dict(defaults=defaults, meta=meta, vars=vars))

# save documentation to file
def save_documentation(documentation, path):
  with open(path, 'w') as stream:
    stream.write(documentation)
  return True

# for given variables generate all documentation files
def handle_documentation(path_wrapper, defaults_object, vars_object, meta_object):

  # extra paths for templates
  extra_template_paths = [path_wrapper("docs")]

  files_to_document = [i.replace(path_wrapper(""),"") for i in glob.glob(path_wrapper("docs/*.md.j2"))]

  if DEBUG:
    print("documentation files", files_to_document)
  
  for file in files_to_document:
    documentation_template_lines = get_file_lines(path_wrapper(file))
    documentation = get_documentation(template = "".join(documentation_template_lines), 
                                    extra_paths=extra_template_paths,  
                                    defaults=defaults_object, 
                                    meta=meta_object, 
                                    vars=vars_object)
  
    # save to file without .j2                                
    save_documentation(documentation, path_wrapper(file[:-3]))

  # move main docs directory upp
  sh.move(path_wrapper("docs/README.md"), path_wrapper('README.md'))

  return True

# main
def main(path_wrapper):
  # read variables from hardcodes files
  defaults_object = handle_defaults(path_wrapper("defaults/main.yml"))
  vars_object = handle_vars(path_wrapper("vars/*.yml"))
  meta_object = handle_meta(path_wrapper("meta/main.yml"))

  # generates and save documentation
  return handle_documentation(path_wrapper, defaults_object, vars_object, meta_object)  

# first entry of python
if __name__ == "__main__":
  # if given arg then it is path to role
  if len(sys.argv) == 2:
    main( lambda x: sys.argv[1] + '/' + x)
  # else files should be in the role
  else:
    main( lambda x: x)