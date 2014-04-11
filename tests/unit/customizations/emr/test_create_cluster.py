# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from tests.unit import BaseAWSCommandParamsTest
import copy

DEFAULT_CLUSTER_NAME = "Development Cluster"
DEFAULT_INSTANCE_GROUPS = [{'InstanceRole': 'MASTER',
                            'InstanceCount': 1,
                            'Name': 'MASTER',
                            'Market': 'ON_DEMAND',
                            'InstanceType': 'm1.large'
                            },
                           {'InstanceRole': 'CORE',
                            'InstanceCount': 1,
                            'Name': 'CORE',
                            'Market': 'ON_DEMAND',
                            'InstanceType': 'm1.large'
                            },
                           {'InstanceRole': 'TASK',
                            'InstanceCount': 1,
                            'Name': 'TASK',
                            'Market': 'ON_DEMAND',
                            'InstanceType': 'm1.large'
                            }]

DEFAULT_INSTANCE_GROUPS_ARG = (
    'InstanceGroupType=MASTER,Name=MASTER,'
    'InstanceCount=1,InstanceType=m1.large '
    'InstanceGroupType=CORE,Name=CORE,'
    'InstanceCount=1,InstanceType=m1.large '
    'InstanceGroupType=TASK,Name=TASK,'
    'InstanceCount=1,InstanceType=m1.large ')

DEFAULT_CMD = 'emr create-cluster --auto-terminate --instance-groups ' + \
    DEFAULT_INSTANCE_GROUPS_ARG

DEFAULT_INSTANCES = {'KeepJobFlowAliveWhenNoSteps': False,
                     'TerminationProtected': False,
                     'InstanceGroups': DEFAULT_INSTANCE_GROUPS
                     }

DEFAULT_RESULT = \
    {
        'Name': DEFAULT_CLUSTER_NAME,
        'Instances': DEFAULT_INSTANCES,
        'AmiVersion': 'latest',
        'VisibleToAllUsers': False,
        'Tags': []
    }

TEST_BA = [
    {
        'ScriptBootstrapAction': {
            'Path': 's3://test/ba1',
            'Args': ['arg1', 'arg2', 'arg3']
        },
        'Name': 'ba1'
    },
    {
        'ScriptBootstrapAction': {
            'Path': 's3://test/ba2',
            'Args': ['arg1', 'arg2', 'arg3']
        },
        'Name': 'ba2'
    }
]

INSTALL_HIVE_STEP = {
    'HadoopJarStep': {
        'Args': ['s3://elasticmapreduce/libs/hive/hive-script',
                 '--install-hive', '--base-path',
                 's3://elasticmapreduce/libs/hive',
                 '--hive-versions', 'latest'],
        'Jar': 's3://elasticmapreduce/libs/script-runner/script-runner.jar'
    },
    'Name': 'Install Hive',
    'ActionOnFailure': 'TERMINATE_CLUSTER'
}

INSTALL_PIG_STEP = {
    'HadoopJarStep': {
        'Args': ['s3://elasticmapreduce/libs/pig/pig-script',
                 '--install-pig', '--base-path',
                 's3://elasticmapreduce/libs/pig',
                 '--pig-versions', 'latest'],
        'Jar': 's3://elasticmapreduce/libs/script-runner/script-runner.jar'
    },
    'Name': 'Install Pig',
    'ActionOnFailure': 'TERMINATE_CLUSTER'
}

INSTALL_HBASE_STEP = {
    'HadoopJarStep': {
        'Args': ['emr.hbase.backup.Main',
                 '--start-master'],
        'Jar': '/home/hadoop/lib/hbase.jar'
    },
    'Name': 'Start HBase',
    'ActionOnFailure': 'TERMINATE_CLUSTER'
}

INSTALL_GANGLIA_BA = {
    'ScriptBootstrapAction': {
        'Path': 's3://elasticmapreduce/bootstrap-actions/install-ganglia'
    },
    'Name': 'Install Ganglia'
}

INSTALL_HBASE_BA = {
    'ScriptBootstrapAction': {
        'Path': 's3://elasticmapreduce/bootstrap-actions/setup-hbase'
    },
    'Name': 'Install HBase'
}

INSTALL_IMPALA_BA = {
    'ScriptBootstrapAction': {
        'Path': 's3://elasticmapreduce/libs/impala/setup-impala',
        'Args': ['--base-path', 's3://elasticmapreduce',
                 '--impala-version', 'latest']
    },
    'Name': 'Install Impala'
}

INSTALL_MAPR_PRODUCT = {
    'Name': 'mapr',
    'Args': ['--edition', 'm5', '--version', '3.0.2']
}

CUSTOM_JAR_STEP = {
    'Name': 'Custom JAR',
    'ActionOnFailure': 'CONTINUE',
    'HadoopJarStep': {'Jar': 's3://mybucket/mytest.jar'}
}

STREAMING_ARGS = (
    'Args=-files,'
    's3://elasticmapreduce/samples/wordcount/wordSplitter.py,'
    '-mapper,wordSplitter.py,'
    '-reducer,aggregate,'
    '-input,s3://elasticmapreduce/samples/wordcount/input,'
    '-output,s3://mybucket/wordcount/output/2014-04-18/12-15-24')

STREAMING_HADOOP_JAR_STEP = {
    'Jar': '/home/hadoop/contrib/streaming/hadoop-streaming.jar',
    'Args': [
        '-files',
        's3://elasticmapreduce/samples/wordcount/wordSplitter.py',
        '-mapper',
        'wordSplitter.py',
        '-reducer',
        'aggregate',
        '-input',
        's3://elasticmapreduce/samples/wordcount/input',
        '-output',
        's3://mybucket/wordcount/output/2014-04-18/12-15-24']
}

HIVE_BASIC_ARGS = (
    'Args=-f,s3://elasticmapreduce/samples/hive-ads/libs/model-build.q')

HIVE_DEFAULT_STEP = {
    'Name': 'Hive program',
    'ActionOnFailure': 'CONTINUE',
    'HadoopJarStep': {
        'Jar': 's3://elasticmapreduce/libs/script-runner/script-runner.jar',
        'Args': [
            's3://elasticmapreduce/libs/hive/hive-script',
            '--run-hive-script',
            '--hive-versions',
            'latest',
            '--args',
            '-f',
            's3://elasticmapreduce/samples/hive-ads/libs/model-build.q']}
}

HIVE_BASIC_STEP = {
    'Name': 'HiveBasicStep',
    'ActionOnFailure': 'CANCEL_AND_WAIT',
    'HadoopJarStep': {
        'Jar': 's3://elasticmapreduce/libs/script-runner/script-runner.jar',
        'Args': [
            's3://elasticmapreduce/libs/hive/hive-script',
            '--run-hive-script',
            '--hive-versions',
            '0.11.0.1',
            '--args',
            '-f',
            's3://elasticmapreduce/samples/hive-ads/libs/model-build.q']}
}

PIG_BASIC_ARGS = 'Args=-f,' + \
    's3://elasticmapreduce/samples/pig-apache/do-reports2.pig'

PIG_DEFAULT_STEP = {
    'Name': 'Pig program',
    'ActionOnFailure': 'CONTINUE',
    'HadoopJarStep': {
        'Jar': 's3://elasticmapreduce/libs/script-runner/script-runner.jar',
        'Args': [
            's3://elasticmapreduce/libs/pig/pig-script',
            '--run-pig-script',
            '--pig-versions',
            'latest',
            '--args',
            '-f',
            's3://elasticmapreduce/samples/'
            'pig-apache/do-reports2.pig']}
}

PIG_BASIC_STEP = {
    'Name': 'PigBasicStep',
    'ActionOnFailure': 'CANCEL_AND_WAIT',
    'HadoopJarStep': {
        'Jar': 's3://elasticmapreduce/libs/script-runner/script-runner.jar',
        'Args': [
            's3://elasticmapreduce/libs/pig/pig-script',
            '--run-pig-script',
            '--pig-versions',
            '0.11.1.0',
            '--args',
            '-f',
            's3://elasticmapreduce/samples/'
            'pig-apache/do-reports2.pig']}
}
IMPALA_BASIC_ARGS = (
    'Args=--impala-script,s3://myimpala/input,'
    '--console-output-path,s3://myimpala/output')

IMPALA_DEFAULT_STEP = {
    'Name': 'Impala program',
    'ActionOnFailure': 'CONTINUE',
    'HadoopJarStep': {
        'Jar': 's3://elasticmapreduce/libs/script-runner/script-runner.jar',
        'Args': [
            's3://elasticmapreduce/libs/impala/setup-impala',
            '--run-impala-script',
            '--impala-script',
            's3://myimpala/input',
            '--console-output-path',
            's3://myimpala/output']}
}


class TestCreateCluster(BaseAWSCommandParamsTest):
    prefix = 'emr create-cluster '

    def test_default_cmd(self):
        self.assert_params_for_cmd(DEFAULT_CMD, DEFAULT_RESULT)

    def test_cluster_name_no_space(self):
        cmd = DEFAULT_CMD + '--name MyCluster'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Name'] = 'MyCluster'
        self.assert_params_for_cmd(cmd, result)

    def test_cluster_name_with_space(self):
        cmd = DEFAULT_CMD.split() + ['--name', 'My Cluster']
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Name'] = 'My Cluster'
        self.assert_params_for_cmd(cmd, result)

    def test_ami_version(self):
        cmd = DEFAULT_CMD + '--ami-version 3.0.4'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['AmiVersion'] = '3.0.4'
        self.assert_params_for_cmd(cmd, result)

    def test_log_uri(self):
        test_log_uri = 's3://test/logs'
        cmd = DEFAULT_CMD + '--log-uri ' + test_log_uri
        result = copy.deepcopy(DEFAULT_RESULT)
        result['LogUri'] = test_log_uri
        self.assert_params_for_cmd(cmd, result)

    def test_additional_info(self):
        test_info = '{ami32: "ami-82e305f5"}'
        cmd = DEFAULT_CMD.split() + ['--additional-info', test_info]
        result = copy.deepcopy(DEFAULT_RESULT)
        result['AdditionalInfo'] = test_info
        self.assert_params_for_cmd(cmd, result)

    def test_no_auto_terminte(self):
        cmd = 'emr create-cluster --no-auto-terminate --instance-groups ' + \
            DEFAULT_INSTANCE_GROUPS_ARG
        result = copy.deepcopy(DEFAULT_RESULT)
        instances = copy.deepcopy(DEFAULT_INSTANCES)
        instances['KeepJobFlowAliveWhenNoSteps'] = True
        result['Instances'] = instances
        self.assert_params_for_cmd(cmd, result)

    def test_auto_terminate_and_no_auto_terminate(self):
        cmd = DEFAULT_CMD + '--auto-terminate --no-auto-terminate'
        expected_error_msg = (
            '\naws: error: cannot use both --no-auto-terminate and'
            ' --auto-terminate options together.\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expected_error_msg, result[1])

    def test_missing_auto_terminate_or_no_auto_terminate(self):
        cmd = self.prefix + '--instance-groups ' + DEFAULT_INSTANCE_GROUPS_ARG
        expected_error_msg = (
            '\naws: error: Must specify one of the following boolean options:'
            ' --auto-terminate|--no-auto-terminate.\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expected_error_msg, result[1])

    def test_termination_protected(self):
        cmd = DEFAULT_CMD + '--termination-protected'
        result = copy.deepcopy(DEFAULT_RESULT)
        instances = copy.deepcopy(DEFAULT_INSTANCES)
        instances['TerminationProtected'] = True
        result['Instances'] = instances
        self.assert_params_for_cmd(cmd, result)

    def test_no_termination_protected(self):
        cmd = DEFAULT_CMD + '--no-termination-protected'
        self.assert_params_for_cmd(cmd, DEFAULT_RESULT)

    def test_termination_protected_and_no_termination_protected(self):
        cmd = DEFAULT_CMD + \
            '--termination-protected --no-termination-protected'
        expected_error_msg = (
            '\naws: error: cannot use both --termination-protected'
            ' and --no-termination-protected options together.\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expected_error_msg, result[1])

    def test_visible_to_all_users(self):
        cmd = DEFAULT_CMD + '--visible-to-all-users'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['VisibleToAllUsers'] = True
        self.assert_params_for_cmd(cmd, result)

    def test_no_visible_to_all_users(self):
        cmd = DEFAULT_CMD + '--no-visible-to-all-users'
        result = copy.deepcopy(DEFAULT_RESULT)
        self.assert_params_for_cmd(cmd, result)

    def test_visible_to_all_users_and_no_visible_to_all_users(self):
        cmd = DEFAULT_CMD + '--visible-to-all-users --no-visible-to-all-users'
        expected_error_msg = (
            '\naws: error: cannot use both --visible-to-all-users and '
            '--no-visible-to-all-users options together.\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expected_error_msg, result[1])

    def test_tags(self):
        cmd = DEFAULT_CMD.split() + ['--tags', 'k1=v1', 'k2', 'k3=spaces  v3']
        result = copy.deepcopy(DEFAULT_RESULT)
        tags = [{'Key': 'k1', 'Value': 'v1'},
                {'Key': 'k2', 'Value': ''},
                {'Key': 'k3', 'Value': 'spaces  v3'}]
        result['Tags'] = tags
        self.assert_params_for_cmd(cmd, result)

    def test_enable_debugging(self):
        cmd = DEFAULT_CMD + '--log-uri s3://test/logs --enable-debugging'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['LogUri'] = 's3://test/logs'
        debugging_config = \
            [{'Name': 'Setup Hadoop Debugging',
              'ActionOnFailure': 'TERMINATE_CLUSTER',
              'HadoopJarStep':
                {'Args': ['s3://elasticmapreduce/libs/state-pusher/0.1/fetch'],
                 'Jar':
                    's3://elasticmapreduce/libs/' +
                    'script-runner/script-runner.jar'
                 }
              }]
        result['Steps'] = debugging_config
        self.assert_params_for_cmd(cmd, result)

    def test_enable_debugging_no_log_uri(self):
        cmd = DEFAULT_CMD + '--enable-debugging'
        expected_error_msg = (
            '\naws: error: LogUri not specified. You must specify a logUri'
            ' if you enable debugging when creating a cluster.\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expected_error_msg, result[1])

    def test_enable_debugging_and_no_enable_debugging(self):
        cmd = DEFAULT_CMD + '--enable-debugging --no-enable-debugging' + \
            ' --log-uri s3://test/logs'
        expected_error_msg = (
            '\naws: error: cannot use both --enable-debugging and '
            '--no-enable-debugging options together.\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expected_error_msg, result[1])

    def test_instance_groups_default_name_market(self):
        cmd = (
            'emr create-cluster --auto-terminate --instance-groups '
            'InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m1.large '
            'InstanceGroupType=CORE,InstanceCount=1,InstanceType=m1.large '
            'InstanceGroupType=TASK,InstanceCount=1,InstanceType=m1.large ')
        self.assert_params_for_cmd(cmd, DEFAULT_RESULT)

    def test_instance_groups_missing_instance_group_type_error(self):
        cmd = (
            'emr create-cluster --auto-terminate --instance-groups '
            'Name=Master,InstanceCount=1,InstanceType=m1.small')
        expect_error_msg = (
            '\nThe following required parameters are missing'
            ' for structure:: InstanceGroupType\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    def test_instance_groups_missing_instance_type_error(self):
        cmd = (
            'emr create-cluster --auto-terminate --instance-groups '
            'Name=Master,InstanceGroupType=MASTER,InstanceCount=1')
        expect_error_msg = (
            '\nThe following required parameters are missing'
            ' for structure:: InstanceType\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    def test_instance_groups_missing_instance_count_error(self):
        cmd = (
            'emr create-cluster --auto-terminate --instance-groups '
            'Name=Master,InstanceGroupType=MASTER,InstanceType=m1.xlarge')
        expect_error_msg = (
            '\nThe following required parameters are missing'
            ' for structure:: InstanceCount\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    def test_ec2_attributes_no_az(self):
        cmd = DEFAULT_CMD + (
            '--ec2-attributes KeyName=testkey,SubnetId=subnet-123456,'
            'InstanceProfile=aws-emr-ec2-role')
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Instances']['Ec2KeyName'] = 'testkey'
        result['Instances']['Ec2SubnetId'] = 'subnet-123456'
        result['JobFlowRole'] = 'aws-emr-ec2-role'
        self.assert_params_for_cmd(cmd, result)

    def test_ec2_attributes_az(self):
        cmd = DEFAULT_CMD + '--ec2-attributes AvailabilityZone=us-east-1a'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Instances']['Placement'] = {'AvailabilityZone': 'us-east-1a'}
        self.assert_params_for_cmd(cmd, result)

    def test_ec2_attributes_subnet_az_error(self):
        cmd = DEFAULT_CMD + '--ec2-attributes ' + \
            'SubnetId=subnet-123456,AvailabilityZone=us-east-1a'
        expect_error_msg = (
            '\naws: error: You may not specify both a SubnetId and an Availab'
            'ilityZone (placement) because ec2SubnetId implies a placement.\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    # Bootstrap Actions test cases
    def test_bootstrap_actions_missing_path_error(self):
        cmd = DEFAULT_CMD + '--bootstrap-actions Name=ba1,Args=arg1,arg2'
        expect_error_msg = (
            '\nThe following required parameters are missing '
            'for structure:: Path\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    def test_bootstrap_actions_with_all_fields(self):
        cmd = DEFAULT_CMD + (
            ' --bootstrap-actions '
            'Path=s3://test/ba1,Name=ba1,Args=arg1,arg2,arg3 '
            'Path=s3://test/ba2,Name=ba2,Args=arg1,arg2,arg3')
        result = copy.deepcopy(DEFAULT_RESULT)
        result['BootstrapActions'] = TEST_BA

        self.assert_params_for_cmd(cmd, result)

    def test_bootstrap_actions_exceed_maximum_error(self):
        cmd = DEFAULT_CMD + ' --bootstrap-actions'
        ba_cmd = ' Path=s3://test/ba1,Name=ba1,Args=arg1,arg2,arg3'
        for i in range(1, 18):
            cmd += ba_cmd

        expected_error_msg = '\naws: error: maximum number of ' +\
                             'bootstrap actions for a cluster exceeded.\n'
        result = self.run_cmd(cmd, 255)

        self.assertEquals(expected_error_msg, result[1])

    def test_bootstrap_actions_exceed_maximum_with_applications_error(self):
        cmd = DEFAULT_CMD + ' --applications Name=GANGLIA Name=HBASE' +\
            ' Name=IMPALA,Version=1.2.1,Args=arg1,arg2 --bootstrap-actions'
        ba_cmd = ' Path=s3://test/ba1,Name=ba1,Args=arg1,arg2,arg3'
        for i in range(1, 15):
            cmd += ba_cmd
        expected_error_msg = '\naws: error: maximum number of ' +\
                             'bootstrap actions for a cluster exceeded.\n'
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expected_error_msg, result[1])

    def test_boostrap_actions_with_default_fields(self):
        cmd = DEFAULT_CMD + (
            ' --bootstrap-actions Path=s3://test/ba1 Path=s3://test/ba2')
        result = copy.deepcopy(DEFAULT_RESULT)
        result['BootstrapActions'] = \
            [
                {'Name': 'Bootstrap action',
                 'ScriptBootstrapAction':
                    {'Path': 's3://test/ba1'}
                 },
                {'Name': 'Bootstrap action',
                 'ScriptBootstrapAction':
                    {'Path': 's3://test/ba2'}
                 }
            ]
        self.assert_params_for_cmd(cmd, result)

    # Applications test cases
    def test_wrong_application_type_error(self):
        cmd = DEFAULT_CMD + '--applications Name=unknown'
        expected_error_msg = (
            '\naws: error: The application name unknown is not supported. '
            '"Name" should be one of the following: HIVE, PIG, HBASE, '
            'GANGLIA, IMPALA, MAPR, MAPR_M3, MAPR_M5, MAPR_M7.\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expected_error_msg, result[1])

    def test_install_hive_with_defaults(self):
        cmd = DEFAULT_CMD + '--applications Name=Hive'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Steps'] = [INSTALL_HIVE_STEP]
        self.assert_params_for_cmd(cmd, result)

    def test_install_hive_with_version(self):
        cmd = DEFAULT_CMD + '--applications Name=Hive,Version=0.11.0.1'
        result = copy.deepcopy(DEFAULT_RESULT)
        steps = copy.deepcopy(INSTALL_HIVE_STEP)
        steps['HadoopJarStep']['Args'][-1] = '0.11.0.1'
        result['Steps'] = [steps]
        self.assert_params_for_cmd(cmd, result)

    def test_install_pig_with_defaults(self):
        cmd = DEFAULT_CMD + '--applications Name=Pig'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Steps'] = [INSTALL_PIG_STEP]
        self.assert_params_for_cmd(cmd, result)

    def test_install_pig_with_version(self):
        cmd = DEFAULT_CMD + '--applications Name=Hive,Version=0.11.1.1'
        result = copy.deepcopy(DEFAULT_RESULT)
        steps = copy.deepcopy(INSTALL_HIVE_STEP)
        steps['HadoopJarStep']['Args'][-1] = '0.11.1.1'
        result['Steps'] = [steps]
        self.assert_params_for_cmd(cmd, result)

    def test_install_ganglia(self):
        cmd = DEFAULT_CMD + '--applications Name=Ganglia'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['BootstrapActions'] = [INSTALL_GANGLIA_BA]
        self.assert_params_for_cmd(cmd, result)

    def test_install_impala_with_defaults(self):
        cmd = DEFAULT_CMD + '--applications Name=Impala'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['BootstrapActions'] = [INSTALL_IMPALA_BA]
        self.assert_params_for_cmd(cmd, result)

    def test_install_impala_with_all_fields(self):
        cmd = DEFAULT_CMD + \
            '--applications Name=Impala,Version=1.2.1,Args=arg1,arg2'
        result = copy.deepcopy(DEFAULT_RESULT)
        ba = copy.deepcopy(INSTALL_IMPALA_BA)
        ba['ScriptBootstrapAction']['Args'][-1] = '1.2.1'
        ba['ScriptBootstrapAction']['Args'] += \
            ['--impala-conf', 'arg1', 'arg2']
        result['BootstrapActions'] = [ba]
        self.assert_params_for_cmd(cmd, result)

    def test_install_hbase(self):
        cmd = DEFAULT_CMD + '--applications Name=hbase'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['BootstrapActions'] = [INSTALL_HBASE_BA]
        result['Steps'] = [INSTALL_HBASE_STEP]
        self.assert_params_for_cmd(cmd, result)

    def test_install_mapr_with_args(self):
        cmd = DEFAULT_CMD + \
            '--applications Name=mapr,Args=--edition,m5,--version,3.0.2'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['NewSupportedProducts'] = [INSTALL_MAPR_PRODUCT]
        self.assert_params_for_cmd(cmd, result)

    def test_applications_all_types(self):
        cmd = DEFAULT_CMD + (
            '--applications '
            'Name=hive Name=pig Name=ganglia Name=hbase Name=impala '
            'Name=mapr,Args=--edition,m5,--version,3.0.2')
        ba_list = [INSTALL_GANGLIA_BA, INSTALL_HBASE_BA,
                   INSTALL_IMPALA_BA]
        step_list = [INSTALL_HIVE_STEP, INSTALL_PIG_STEP, INSTALL_HBASE_STEP]
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Steps'] = step_list
        result['BootstrapActions'] = ba_list
        result['NewSupportedProducts'] = [INSTALL_MAPR_PRODUCT]

        self.assert_params_for_cmd(cmd, result)

    # Steps test cases
    def test_wrong_step_type_error(self):
        cmd = DEFAULT_CMD + '--steps Type=unknown'
        expected_error_msg = (
            '\naws: error: The step type unknown is not supported.\n')
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expected_error_msg, result[1])

    def test_default_step_type_name_action_on_failure(self):
        cmd = DEFAULT_CMD + '--steps Jar=s3://mybucket/mytest.jar'
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Steps'] = [CUSTOM_JAR_STEP]
        self.assert_params_for_cmd(cmd, result)

    def test_custom_jar_step_missing_jar(self):
        cmd = DEFAULT_CMD + '--steps Name=CustomJarMissingJar'
        expect_error_msg = '\naws: error: The following ' + \
            'required parameters are missing for CustomJARStepConfig: Jar.\n'
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    def test_custom_jar_step_with_all_fields(self):
        cmd = DEFAULT_CMD + '--steps ' + (
            'Name=Custom,Type=CustomJAR,'
            'Jar=s3://mybucket/mytest.jar,'
            'Args=arg1,arg2,MainClass=mymainclass,'
            'ActionOnFailure=TERMINATE_CLUSTER')
        expected_steps = [
            {'Name': 'Custom',
             'ActionOnFailure': 'TERMINATE_CLUSTER',
             'HadoopJarStep':
                {'Jar': 's3://mybucket/mytest.jar',
                 'Args': ['arg1', 'arg2'],
                 'MainClass': 'mymainclass'}
             }
        ]
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Steps'] = expected_steps
        self.assert_params_for_cmd(cmd, result)

    def test_streaming_step_with_default_fields(self):
        cmd = DEFAULT_CMD + '--steps Type=Streaming,' + STREAMING_ARGS
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Steps'] = [
            {'Name': 'Streaming program',
             'ActionOnFailure': 'CONTINUE',
             'HadoopJarStep': STREAMING_HADOOP_JAR_STEP}
        ]
        self.assert_params_for_cmd(cmd, result)

    def test_streaming_step_missing_args(self):
        cmd = DEFAULT_CMD + '--steps Type=Streaming'
        expect_error_msg = '\naws: error: The following ' + \
            'required parameters are missing for StreamingStepConfig: Args.\n'
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    def test_streaming_jar_with_all_fields(self):
        test_step_config = (
            '--steps Type=Streaming,Name=StreamingStepAllFields,'
            'ActionOnFailure=CANCEL_AND_WAIT,' + STREAMING_ARGS)
        cmd = DEFAULT_CMD + test_step_config
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Steps'] = [
            {'Name': 'StreamingStepAllFields',
             'ActionOnFailure': 'CANCEL_AND_WAIT',
             'HadoopJarStep': STREAMING_HADOOP_JAR_STEP}
        ]
        self.assert_params_for_cmd(cmd, result)

    def test_hive_step_with_default_fields(self):
        cmd = DEFAULT_CMD + (
            '--applications Name=Hive --steps Type=Hive,' + HIVE_BASIC_ARGS)
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Steps'] = [INSTALL_HIVE_STEP, HIVE_DEFAULT_STEP]
        self.assert_params_for_cmd(cmd, result)

    def test_hive_step_missing_args(self):
        cmd = DEFAULT_CMD + '--applications Name=Hive --steps Type=Hive'
        expect_error_msg = '\naws: error: The following ' + \
            'required parameters are missing for HiveStepConfig: Args.\n'
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    def test_hive_step_with_all_fields(self):
        test_step_config = (
            'Type=Hive,Version=0.11.0.1,ActionOnFailure=CANCEL_AND_WAIT,'
            'Name=HiveBasicStep,' + HIVE_BASIC_ARGS)
        cmd = DEFAULT_CMD + (
            '--applications Name=Hive,Version=0.11.0.1 '
            '--steps ' + test_step_config)
        result = copy.deepcopy(DEFAULT_RESULT)
        install_step = copy.deepcopy(INSTALL_HIVE_STEP)
        install_step['HadoopJarStep']['Args'][-1] = '0.11.0.1'
        result['Steps'] = [install_step, HIVE_BASIC_STEP]
        self.assert_params_for_cmd(cmd, result)

    def test_pig_step_with_default_fields(self):
        cmd = DEFAULT_CMD + (
            '--applications Name=Pig --steps Type=Pig,' + PIG_BASIC_ARGS)
        result = copy.deepcopy(DEFAULT_RESULT)
        result['Steps'] = [INSTALL_PIG_STEP, PIG_DEFAULT_STEP]
        self.assert_params_for_cmd(cmd, result)

    def test_pig_missing_args(self):
        cmd = DEFAULT_CMD + '--applications Name=Pig --steps Type=Pig'
        expect_error_msg = '\naws: error: The following ' + \
            'required parameters are missing for PigStepConfig: Args.\n'
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    def test_pig_step_with_all_fields(self):
        test_step_config = (
            'Name=PigBasicStep,Type=Pig,Version=0.11.1.0,' + PIG_BASIC_ARGS +
            ',ActionOnFailure=CANCEL_AND_WAIT')
        cmd = DEFAULT_CMD + (
            '--applications Name=Pig,Version=0.11.1.0 --steps ' +
            test_step_config)
        result = copy.deepcopy(DEFAULT_RESULT)
        install_step = copy.deepcopy(INSTALL_PIG_STEP)
        install_step['HadoopJarStep']['Args'][-1] = '0.11.1.0'
        result['Steps'] = [install_step, PIG_BASIC_STEP]
        self.assert_params_for_cmd(cmd, result)

    def test_impala_step_with_default_fields(self):
        cmd = DEFAULT_CMD + (
            '--applications Name=Impala --steps Type=Impala,' +
            IMPALA_BASIC_ARGS)
        result = copy.deepcopy(DEFAULT_RESULT)
        result['BootstrapActions'] = [INSTALL_IMPALA_BA]
        result['Steps'] = [IMPALA_DEFAULT_STEP]
        self.assert_params_for_cmd(cmd, result)

    def test_impala_missing_args(self):
        cmd = DEFAULT_CMD + '--applications Name=Impala --steps Type=Impala'
        expect_error_msg = '\naws: error: The following ' + \
            'required parameters are missing for ImpalaStepConfig: Args.\n'
        result = self.run_cmd(cmd, 255)
        self.assertEquals(expect_error_msg, result[1])

    def test_impala_step_with_all_fields(self):
        test_step_config = (
            'Name=ImpalaBasicStep,Type=Impala,' + IMPALA_BASIC_ARGS +
            ',ActionOnFailure=CANCEL_AND_WAIT')
        cmd = DEFAULT_CMD + (
            '--applications Name=Impala --steps ' + test_step_config)
        result = copy.deepcopy(DEFAULT_RESULT)
        result['BootstrapActions'] = [INSTALL_IMPALA_BA]
        step = copy.deepcopy(IMPALA_DEFAULT_STEP)
        step['Name'] = 'ImpalaBasicStep'
        step['ActionOnFailure'] = 'CANCEL_AND_WAIT'
        result['Steps'] = [step]
        self.assert_params_for_cmd(cmd, result)

    def test_restore_from_hbase(self):
        cmd = DEFAULT_CMD + (
            '--applications Name=hbase --restore-from-hbase-backup '
            'Dir=s3://mybucket/test,BackupVersion=test_version')
        result = copy.deepcopy(DEFAULT_RESULT)
        result['BootstrapActions'] = [INSTALL_HBASE_BA]
        result['Steps'] = [
            INSTALL_HBASE_STEP,
            {
                'Name': 'Restore HBase',
                'ActionOnFailure': 'CANCEL_AND_WAIT',
                'HadoopJarStep': {
                    'Args': [
                        'emr.hbase.backup.Main',
                        '--restore',
                        '--backup-dir',
                        's3://mybucket/test',
                        '--backup-version',
                        'test_version'],
                    'Jar': '/home/hadoop/lib/hbase.jar'}
            }
        ]
        self.assert_params_for_cmd(cmd, result)


if __name__ == "__main__":
    unittest.main()
