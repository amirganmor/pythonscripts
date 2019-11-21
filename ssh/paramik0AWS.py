import paramiko
ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('ec2-3-217-198-209.compute-1.amazonaws.com', username='ec2-user', key_filename='dwh-dev.pem')
stdin, stdout, stderr = ssh.exec_command('mkdir /home/ec2-user/amir17')
print (stdout.readlines())
ssh.close()
