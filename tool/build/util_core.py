import platform

def get_current_os_info():

    '''
        Get current os information
    '''

    os = platform.system()
    if os == "Darwin":
        os = "macOS"

    abi = platform.machine()

    # print("OS info: ", (os, abi))
    return os, abi

