
import sys
import time
import select
import paramiko

def ssh_command(host, command):
    
    i = 1
    #
    # Try to connect to the host.
    # Retry a few times if it fails.
    #
    while True:
        #print ("Trying to connect to %s (%i/30)" % (host, i))
    
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host)
            #print ("Connected to %s" % host)
            break
        except paramiko.AuthenticationException:
            print ("Authentication failed when connecting to %s" % host)
            sys.exit(1)
        except:
            print ("Could not SSH to %s, waiting for it to start" % host)
            i += 1
            time.sleep(2)
    
        # If we could not connect within time limit
        if i == 30:
            print ("Could not connect to %s. Giving up" % host)
            sys.exit(1)
    
    # Send the command (non-blocking)
    stdin, stdout, stderr = ssh.exec_command(command)
    time.sleep(1)
    
    # Wait for the command to terminate
    
        # Only print data if there is data to read in the channel
    if stdout.channel.recv_ready():
        rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
        if len(rl) > 0:
            mystdout = stdout.channel.recv(1024).decode("utf-8")
        else:
            print ("rl = 0")
    else:
        print ("stdout channel.recv.ready() NOT READY")
    
    #
    # Disconnect from the host
    #
    #print ("Command done, closing SSH connection")
    ssh.close()
    '''
    The code should be quite self explainatory, but here’s what it does in short:
    
    Connect to the SSH server
    Send the command (non-blocking)
    Create a loop, waiting for the channel to get an exist code
    The loop is looking for data to pring (stdout.channel.recv_ready()) and prints any data it receives
    '''
    return mystdout

myoutput = ssh_command("smetrics-vm-04","ls -l")
print (myoutput)

