import os

from jinja2 import Environment, FileSystemLoader

import yaml
import argparse
import click


def load_properties_for_env(group_var_folder, group_var_file_prefix, environment):
    if not group_var_folder.endswith('/'):
        group_var_folder += '/'

    file = open(group_var_folder + group_var_file_prefix + environment + '.yml', "r")
    properties = environment + ':'
    for line in file:
        if '_version' in line:
            if '#' not in line:
                properties += '\n    ' + line

    properties += '\n'
    return properties


def create_version_html(group_var_folder, group_var_file_prefix, serverless_var_file_prefix, exported_file_path):
    config_data = get_config_data(group_var_file_prefix, group_var_folder)

    sls_config_data = get_config_data(serverless_var_file_prefix, group_var_folder + '/serverless')

    config_data['dev'].update(sls_config_data['dev'])
    config_data['test'].update(sls_config_data['test'])
    config_data['prod'].update(sls_config_data['prod'])

    all_apps = set()

    for key, value in config_data['dev'].items():
        all_apps.add(key)
    for key, value in config_data['test'].items():
        all_apps.add(key)
    for key, value in config_data['prod'].items():
        all_apps.add(key)

    all_apps = sorted(all_apps)
    apps_and_version = {}
    for apps in all_apps:
        if apps not in apps_and_version:
            apps_and_version[apps] = {}

        add_env_to_apps_and_version(apps_and_version, 'dev', apps, config_data)
        add_env_to_apps_and_version(apps_and_version, 'test', apps, config_data)
        add_env_to_apps_and_version(apps_and_version, 'prod', apps, config_data)

    config_data['apps_and_version'] = apps_and_version

    env = Environment(loader=FileSystemLoader('./templates'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('versions.html')
    #
    # #Render the template with data and print the output
    render = template.render(config_data)

    output_file = open(exported_file_path, "w")
    output_file.write(render)


def get_config_data(var_prefix, var_folder):
    properties = ''
    properties += load_properties_for_env(var_folder, var_prefix, 'dev')
    properties += load_properties_for_env(var_folder, var_prefix, 'test')
    properties += load_properties_for_env(var_folder, var_prefix, 'prod')
    config_data = yaml.safe_load(properties)
    return config_data


def add_env_to_apps_and_version(apps_and_version, environment, apps, config_data):
    if apps in config_data[environment]:
        apps_and_version[apps][environment] = config_data[environment][apps]


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--group-var-folder", dest='group_var_folder', required=True, help="Group Var folder")
    ap.add_argument("-f", "--group-var-file-prefix", dest='group_var_file_prefix', required=False,
                    help="Group Var env file prefix", default='tag_env_')
    ap.add_argument("-s", "--serverless-var-file-prefix", dest='serverless_var_file_prefix', required=False,
                    help="Serverless Var env file prefix", default='')
    ap.add_argument("--force", dest='force', help="Do not ask confirmations", action='store_true')
    ap.add_argument("-e", "--exported-file-path", dest='exported_file_path', required=False,
                    help="Path where to export the html file", default='./compiled-versions.html', )
    args = ap.parse_args()

    if os.path.isdir(args.exported_file_path):
        raise Exception('exported-file-path cannot be a folder')

    if os.path.exists(args.exported_file_path) and not args.force:
        if not click.confirm("File already exists, ok to overwrite?"):
            click.echo("Exiting")
            exit(0)

    create_version_html(args.group_var_folder, args.group_var_file_prefix, args.serverless_var_file_prefix,
                        args.exported_file_path)
    click.echo("All done")
