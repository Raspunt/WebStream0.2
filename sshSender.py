
import paramiko
from scp import SCPClient


class sshSender():


    def init(self):
        sshClient = self.createSSHClient(
            '192.168.1.15',
            '22',
            'serv',
            '4444'
        )
        return sshClient

    def createSSHClient(self, server, port, user, password):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        return client


    def Send(self,localFile,RemoteFile):
        scp = SCPClient(self.init().get_transport())
        scp.put(localFile,RemoteFile)


    def ListFilesRemoteDir(self,remoteFiles):
        ssh = self.init()
        command = f"ls {remoteFiles}"

        (stdin, stdout, stderr) = ssh.exec_command(command)

        files = []
        for line in stdout.readlines():
            files.append(line.replace('\n',''))
        
        ssh.close()

        return files

# sender = sshSender()
# sender.Send(sender.init(),'VideoFrames/video.mp4','/home/serv/share/CameraVideos/')

# len(sender.ListFilesRemoteDir('/home/serv/share/CameraVideos/'))