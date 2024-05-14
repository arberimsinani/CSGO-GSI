from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

# Define the function to handle received OSC messages
def osc_handler(address, *args):
    print(f"Received OSC message: {address}, args: {args}")

# Set up the dispatcher to map OSC addresses to handler functions
dispatcher = Dispatcher()
dispatcher.map("/composition/layers/1/clips/1/connect", osc_handler)

# Set up the OSC server to listen for incoming messages on port 9000
server_ip = "127.0.0.1"  # Listen on all available network interfaces
server_port = 7000
server = BlockingOSCUDPServer((server_ip, server_port), dispatcher)

# Start the OSC server
print(f"OSC server listening on {server_ip}:{server_port}")
server.serve_forever()

