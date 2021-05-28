from os import path
import paramiko


ssh_client = None
stdin = None
stdout = None
stderr = None


"""
Connects to virtual machine
return: 0 -> successful connection
        1 -> key file doesn't exist
        2 -> error establishing connection
"""
def connect(ip):
    # Checks if the key file exists
    key_filename = "./key.pem"
    if not path.exists(key_filename):
        return 1

    # Connection to virtual machine
    try:
        global ssh_client
        ssh_client = paramiko.SSHClient()  # Creates the SSH Client
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Allows the connection to any host
        ssh_client.connect(hostname=ip, username="azureuser", key_filename=key_filename)
    except:
        return 2

    return 0


"""
Execute command on VM
return: 1 -> error
        else -> response obtained
"""
def exec_command(command):
    global ssh_client
    global stdin
    global stdout
    global stderr

    try:
        # Executes the command
        stdin,stdout,stderr=ssh_client.exec_command(command)
    except:
        return 1
    
    return stdout.readlines()


"""
Uploads a file to the VM
local_filepath: relative or absolute path of the file to be uploaded
remote_filepath: relative or absolute path where the file should be
                 stored in the VM
return: 0 -> no problems
        1 -> error uploading
"""
def upload_file(local_filepath, remote_filepath):
    global ssh_client

    try:
        ftp_client = ssh_client.open_sftp()              # Open SFTP Client
        ftp_client.put(local_filepath, remote_filepath)  # Send file
        ftp_client.close()                               # Close connection
    except:
        return 1

    return 0


"""
Downloads a file from the VM
remote_filepath: relative or absolute path of the file to be downloaded
local_filepath: relative or absolute path where the file should be stored
return: 0 -> no problems
        1 -> error uploading
"""
def download_file(remote_filepath, local_filepath):
    global ssh_client
    
    try:
        ftp_client=ssh_client.open_sftp()                # Open SFTP Client
        ftp_client.get(remote_filepath, local_filepath)  # Download file
        ftp_client.close()                               # Close connection
    except:
        return 1

    return 0


"""
Close SSH connection
return: 0 -> no problems
        1 -> error
"""
def close():
    global ssh_client
    try:
        ssh_client.close()
        return 0
    except:
        return 1


"""
connect("52.171.60.196")
upload_file("./prueba.txt", "./prueba.txt")
filename = "prueba.txt"
exec_command("python3 entity_recognition.py " + filename)
download_file("./resultado.txt", "./resultado.txt")
"""