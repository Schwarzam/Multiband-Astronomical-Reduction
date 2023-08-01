import subprocess
import os

def runCommand(consoleCommand, timeout=100):
    """Runs and gets command output from terminal

    Args:
        consoleCommand (str): console/terminal command string
        timeout (int): wait max timeout for run console command
    Returns:
        Execution Code (int)
    Raises:
    """
    
    exeCode = -1
    try:
        try:
            exeCode = os.system(f'timeout {timeout} {consoleCommand}')

            #c = subprocess.run(consoleCommand, shell=True, timeout=timeout)
            #exeCode = c.check_returncode()
        except subprocess.TimeoutExpired:
            print(f'Timed out execution on {consoleCommand}')
        
        except Exception as e:
            raise(e)

    except subprocess.CalledProcessError as callProcessErr:
        cmdErrStr = str(callProcessErr)
        print("Error %s for run command %s" % (cmdErrStr, consoleCommand))

    return exeCode