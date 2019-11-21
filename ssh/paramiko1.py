import paramiko
import time
import sys


class sshClass(object):
    def __init__(self, ip, username, password, sessionName, timeout, retry_interval):

        self.SSH_USERNAME = username
        self.SSH_ADDRESS = ip
        self.SSH_PASSWORD = password
        self.ssh = None
        self.sessionName = None
        self.timeout = timeout
        self.retry_interval = retry_interval
        self.ssh = paramiko.client.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connectSSH(self):
        retry_interval = float(self.retry_interval)
        timeout = int(self.timeout)
        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            time.sleep(retry_interval)
            try:
                print("in try")
                self.ssh.connect(self.SSH_ADDRESS, username=self.SSH_USERNAME, password=self.SSH_PASSWORD)
                x = self.ssh.get_transport()
                # print (x.is_active())
                break
            except paramiko.ssh_exception.SSHException as e:
                # socket is open, but not SSH service responded
                print(e.__str__())
                if 'Error reading SSH protocol banner' in e.__str__():
                    print(e)
                    continue
                print('SSH transport is available!')
                break
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                print('SSH transport is not ready...')
                continue

    def wait_for_ssh_to_be_ready(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        for line in stdout:
            print(line.strip('\n'))
        for liner in stderr:
            print(liner.strip('\n'))

    def closeSSH(self):
        # print ("in close ssh")
        x = self.ssh.get_transport()
        self.ssh.close()
        # print (x.is_active())


# connection vars
linuxIp = "10.22.3.23"
User = "ciuser"
Pass = "Mantis14"

# env Var
#WorkSpacePath = str(sys.argv[1])
WorkSpacePath="/mnt/data/JenkinsBuilds/workspace/MV4DCommons_new_jenk"
#CppPath = str(sys.argv[2])
CppPath="/MV4DCommons/Projects/Commons/src/MV4DCommons/Commons/MV4DCommonsVersion.cpp"
#MantisBuildPath = str(sys.argv[3])
MantisBuildPath="/mnt/MantisDailyBuilds/MV4DRepos/MV4DCommons/master_1.1.2_17.06.19_6997278"
#tmpdir = str(sys.argv[4])
tmpdir="/mnt/MantisDailyBuilds/Amir/tmpDir/MV4DCommonsWin_new_jenk/MV4DCommonsVersion.cpp"
#branch1 = str(sys.argv[5])
branch1="master"
val = branch1.split("/")
branch = str(val[-1])



commands = 'mkdir -p ' + WorkSpacePath +   ' ; ' \
          'cd ' + WorkSpacePath  +   ' ; ' \
          'rm -rf * ;' \
          'git clone https://ciuser:Mantis14@github.mantis.local/Mantis-Vision/MV4DCommons.git --branch ' + branch  +' ;' \
          'git clone https://ciuser:Mantis14@github.mantis.local/Mantis-Vision/MV4DPackages.git ; ' \
          'git clone https://ciuser:Mantis14@github.mantis.local/Mantis-Vision/3rdParties.git ;' \
          'sudo cp -f ' + tmpdir + ' ' + WorkSpacePath + CppPath + ' ; ' \
          'cd ' + WorkSpacePath + '/MV4DCommons/Scripts/  ; ' \
          'python Linux/CompileAndPackage.py -arm64 -x86_64 -release -debug -rebuild ; ' \
          'python PackageMV4DCommonsAllOSSDK.py ;' \
           'cd ' + WorkSpacePath  +   '/MV4DCommons/Output;' \
           'sudo mv Linux  MV4DCommonsSDK;' \
           'cd ' + WorkSpacePath + '/MV4DCommons/Output/MV4DCommonsSDK ;' \
           'sudo cp -rf  * ' + MantisBuildPath + ' ; '

'''

commands =
'''

    # ssh9 = sshClass(args['linuxIp'], args['sshUser'], args['ciuserPass'], "command for running python file on linux", 20, 1)
ssh9 = sshClass(linuxIp, User, Pass, "command for running python file on linux", 20, 1)

ssh9.connectSSH()
ssh9.wait_for_ssh_to_be_ready(commands)
ssh9.closeSSH()
