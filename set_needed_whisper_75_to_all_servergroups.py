import telnetlib
import time

# Connection settings
HOST = 'host'
PORT = 10011
USER = 'queryname'
PASSWORD = 'querypassword'

def send_command(tn, command):
    tn.write(command.encode('utf-8') + b'\n')
    time.sleep(0.5)
    response = tn.read_very_eager().decode('utf-8')
    print(f"Command: {command.strip()}\nResponse: {response.strip()}\n")
    return response

def main():
    try:
        # Connect to TeamSpeak server
        tn = telnetlib.Telnet(HOST, PORT)
        
        # Server query welcome message
        welcome_msg = tn.read_until(b'TS3', timeout=5)
        print(welcome_msg.decode('utf-8'))
        
        # Login
        send_command(tn, f"login {USER} {PASSWORD}")
        
        # Select virtual server
        send_command(tn, "use 1")
        
        # Get list of server groups
        response = send_command(tn, "servergrouplist")

        # Parse server groups and set whisper power to 75
        if "error id=0 msg=ok" in response:
            server_groups = response.split("|")
            for group in server_groups:
                sgid = group.split()[0].split('=')[1]
                print(f"Setting whisper power for group {sgid}")
                send_command(tn, f"servergroupaddperm sgid={sgid} permsid=i_client_needed_whisper_power permvalue=75 permskip=0 permnegated=0")
                send_command(tn, f"servergroupdelperm sgid={sgid} permsid=i_client_whisper_power")
        
        else:
            print("No server groups found or insufficient permissions.")
        
        tn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

