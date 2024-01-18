import zmq
import threading
from sainsmart_relay.relay import FTDIBitbangRelay

class RelayServer:
    def __init__(self, relay, pub_port=5556, rep_port=5557):
        self.relay = relay

        # Initialize ZeroMQ context and sockets
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(f"tcp://*:{pub_port}")

        self.rep_socket = self.context.socket(zmq.REP)
        self.rep_socket.bind(f"tcp://*:{rep_port}")

        # Start the polling thread
        self.poll_thread = threading.Thread(target=self.poll_commands)
        self.poll_thread.start()

    def poll_commands(self):
        poller = zmq.Poller()
        poller.register(self.rep_socket, zmq.POLLIN)

        while True:
            socks = dict(poller.poll())
            if self.rep_socket in socks:
                message = self.rep_socket.recv_string()
                relay_num, state = message.split()
                self.relay.set_relay(int(relay_num), state)
                self.pub_socket.send_string(f"Relay {relay_num} state: {state}")
                self.rep_socket.send_string("Command processed")

    def close(self):
        self.rep_socket.close()
        self.pub_socket.close()
        self.context.term()

def main():
    # existing argument parsing code...
    relay = FTDIBitbangRelay(verbosity=args.verbose)
    server = RelayServer(relay)
    # or, for the wrapper approach:
    # server = FTDIBitbangRelayServer(verbosity=args.verbose)

    # Do not forget to handle closing the server cleanly
    # This can be done with signal handling or a similar approach
