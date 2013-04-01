#!/usr/bin/env python

import os
import sys
import sh
import argparse
import boto
import boto.s3.key
import json

bucket_name = os.environ.get('GEARBOX_BUCKET', 's3_ops')
chef_repo = os.environ.get('CHEF_REPO', 'git@github.com:NarrativeScience/chef-repo.git')
chef_home = os.environ.get('CHEF_HOME', '/home/ubuntu/.chef')
deploy_private_key_file = os.environ.get('DEPLOY_PRIVATE_KEY_FILE', '/home/ubuntu/.ssh/id_deploy')


def deploy(package, stage, role=None):
    print 'Deploying {0} to {1}'.format(package, stage)
    version = get_latest_version(package)
    print '  using version {0}'.format(version)
    print sh.rm('-rf', 'chef-repo')
    print sh.git('clone', chef_repo)
    print sh.cd('chef-repo')
    env_config_file_path = 'environments/{0}.json'.format(stage)
    update_environment_config(env_config_file_path, package, version)
    # Commit and push to chef-repo
    print sh.git('add', '-A')
    print sh.git('commit', '-m', 'AUTODEPLOYER: Update version of {0} to {1}'.format(package, version))
    print sh.git('push')
    print 'Updated environment in chef-repo with new package version'
    # Run chef-client on all the hosts
    print sh.knife('environment', 'from', 'file', env_config_file_path, '--config', '{0}/knife.rb'.format(chef_home))
    query_string = 'chef_environment:{0}'.format(stage)
    if role:
        query_string = query_string + " AND roles:%s" % role
    p = sh.knife(
        'ssh',
        '--ssh-user',
        'nsdeploy',
        '--identity-file',
        deploy_private_key_file,
        query_string,
        'sudo chef-client',
        '--config',
        '{0}/knife.rb'.format(chef_home),
        _out=process_output,
        _err=process_output
    )
    p.wait()
    print 'chef-client finished on all hosts!  Deployment done.'


def process_output(line):
    '''Callable used so we can get the output to calling chef-client line by line'''
    sys.stdout.write(line)


def get_latest_version(package):
    '''
    Gets the latest release version of package from the LATEST file
    in the gearbox directory in S3
    '''
    s3_conn = boto.connect_s3()
    bucket = s3_conn.get_bucket(bucket_name)
    key = boto.s3.key.Key(bucket)
    key.key = '{0}/LATEST'.format(package)
    try:
        return key.get_contents_as_string()
    except boto.exception.S3ResponseError:
        raise RuntimeError('Can\'t find the LATEST in S3 file for {0}, are you sure you have the right package?'.format(package))


def update_environment_config(env_config_file_path, package, version):
    '''
    Updates the package version in the environment config file at env_config_file_path
    '''
    if not os.path.isfile(env_config_file_path):
        raise RuntimeError('Environment config file doesn\'t exist: {0}'.format(env_config_file_path))
    # Read file
    json_in = open(env_config_file_path)
    env_config = json.load(json_in)
    json_in.close()
    # Update service version
    versions = env_config['override_attributes']['gearbox']['versions']
    if package not in versions:
        raise RuntimeError('Service doesn\'t exist in environment config for {0}'.format(package))
    versions[package] = version
    # Write out file
    json_out = open(env_config_file_path, 'w+')
    json.dump(env_config, json_out, indent=4)
    json_out.close()


def main():
    parser = argparse.ArgumentParser(description='Deploys the last released version of PACKAGE to the ENVIRONMENT')
    parser.add_argument('package')
    parser.add_argument('environment')
    parser.add_argument('role', nargs='?', default=None)

    args = parser.parse_args()
    deploy(args.package, args.environment, args.role)

if __name__ == "__main__":
    sys.exit(main())
