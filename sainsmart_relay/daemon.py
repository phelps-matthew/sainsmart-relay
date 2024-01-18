import daemon
import logging
from logging.handlers import RotatingFileHandler
import os
from RelayServer import RelayServer  # Assuming RelayServer is in a separate file
from FTDIBitbangRelay import FTDIBitbangRelay  # Assuming FTDIBitbangRelay is in a separate file

def setup_logging():
    log_file = '/var/log/relay_server.log'  # Adjust path as necessary
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

def run_server():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Relay Server")

    relay = FTDIBitbangRelay(verbosity=0)
    server = RelayServer(relay)

    try:
        server.run()  # Assuming you have a run method in RelayServer
    except Exception as e:
        logger.exception("An error occurred in Relay Server")
    finally:
        server.close()
        logger.info("Relay Server stopped")

daemon_context = daemon.DaemonContext(
    working_directory='/tmp',
    umask=0o002,
    pidfile=None  # You can use a lockfile.LockFile here for managing the PID
)

if __name__ == "__main__":
    with daemon_context:
        run_server()
