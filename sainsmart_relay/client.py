import argparse
import socket
import sys

def send_command(args):
    command = "status" if args.status else f"{args.relay_num} {args.state}"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.host, args.port))
        s.sendall(command.encode())
        data = s.recv(1024)
        response = data.decode().strip()
        print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Client to control and query the state of relays via FTDI.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('relay_num', type=int, choices=range(1, 5), nargs='?',
                        help='Relay number (1-4), required unless querying status')
    parser.add_argument('state', choices=["on", "off"], nargs='?',
                        help='State to set the relay to, required unless querying status')
    parser.add_argument('--host', default='localhost', help='The host of the relay server')
    parser.add_argument('--port', type=int, default=65432, help='The port of the relay server')
    parser.add_argument('-s', '--status', action='store_true', help='Query the current relay states')

    args = parser.parse_args()

    if args.status:
        if args.relay_num or args.state:
            parser.error("No other arguments are required when querying status.")
    elif not (args.relay_num and args.state):
        parser.error("Both relay_num and state are required for setting a relay.")

    send_command(args)
