import socket
import selectors
import types
import logging
from sainsmart_relay.relay import FTDIBitbangRelay

# Configure logging at the beginning, so all modules use the same configuration
logging.basicConfig(
    filename="relay_control.log", level=logging.DEBUG, filemode="a", format="%(asctime)s - %(levelname)s - %(message)s"
)


def accept_wrapper(sock, sel):
    conn, addr = sock.accept()
    # Proper use of logging with multiple arguments
    logging.info("Accepted connection from %s", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask, sel, relay):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += perform_relay_action(recv_data, relay)
        else:
            logging.info("Closing connection to %s", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


def perform_relay_action(command, relay_obj):
    """
    Parse the command received from the socket, and use the relay_obj to set the relay state.

    Parameters:
    - command (bytes): The command received from the client, expected to be in the format "relay_num state".
    - relay_obj (FTDIBitbangRelay): The FTDIBitbangRelay object used to control the relays.

    Returns:
    - response (bytes): A byte string to send back to the client, indicating the result of the action.
    """

    # Decode the command and split into components
    try:
        command_decoded = command.decode("utf-8")
        parts = command_decoded.strip().split()

        if parts[0] == "status":
            current_state = relay_obj.get_relay_state()
            return f"Current Relay State: {current_state:08b}\n".encode("utf-8")

        # Validate the command parts
        if len(parts) != 2:
            return b"Error: Command format is 'relay_num state'.\n"

        relay_num, state = parts
        relay_num = int(relay_num)

        # Validate relay number and state
        if relay_num not in range(1, 5):
            return b"Error: Relay number must be between 1 and 4.\n"
        if state not in ("on", "off"):
            return b"Error: State must be 'on' or 'off'.\n"

        # Set the relay state
        relay_obj.set_relay(relay_num, state)
        response = f"Relay {relay_num} set to {state.upper()}.\n".encode("utf-8")
        return response

    except ValueError:
        return b"Error: Command format is 'relay_num state', where relay_num is an integer.\n"
    except Exception as e:
        logging.exception("An unexpected error occurred while processing the command.")
        return f"Error: {str(e)}\n".encode("utf-8")


def setup_server():
    # Setup the selector for managing connections
    sel = selectors.DefaultSelector()

    # Setup the FTDI relay object
    relay = FTDIBitbangRelay()

    # Set up the server socket
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind(("localhost", 65432))
    lsock.listen()
    logging.info("Listening on (%s, %d)", "localhost", 65432)
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    return lsock, sel, relay


def run_server(lsock, sel, relay):
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj, sel)
                else:
                    service_connection(key, mask, sel, relay)
    except KeyboardInterrupt:
        logging.info("Caught keyboard interrupt, exiting")
    except Exception as e:
        logging.exception("An error occurred: %s", str(e))
    finally:
        sel.close()
        relay.close()
        lsock.close()  # Ensure the listening socket is closed properly
        logging.info("Server shut down.")


def main():
    lsock, sel, relay = setup_server()
    run_server(lsock, sel, relay)

# Now the actual entry point is much cleaner
if __name__ == "__main__":
    main()