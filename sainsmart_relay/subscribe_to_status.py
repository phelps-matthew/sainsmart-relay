import zmq

def subscribe_to_updates():
    context = zmq.Context()
    # Assuming your PUB socket is on port 5556
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")

    # Subscribe to all messages
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    print("Subscribed to relay updates...")

    try:
        while True:
            message = socket.recv_string()
            print(f"Received update: {message}")
    except KeyboardInterrupt:
        print("Interrupted")

    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    subscribe_to_updates()
