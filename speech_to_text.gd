extends Node3D
class_name SpeechToText

var socket = PacketPeerUDP.new()
var server = UDPServer.new()

@export var filePath = ""

func _ready():
	# execute python script with godot
	var output
	OS.execute("python", ["res://speech_to_text.py"], [""], false, true)
	
	socket.set_dest_address("127.0.0.1", 6000)
	server.listen(6001)

func recognize_file():
	socket.put_packet(filePath.to_ascii_buffer())

func _physics_process(delta):
	# check for response
	server.poll()
	if server.is_connection_available():
		var peer: PacketPeerUDP = server.take_connection()
		var packet = peer.get_packet()
		#print("Accepted peer: %s:%s" % [peer.get_packet_ip(), peer.get_packet_port()])
		#print("Received data: %s" % [packet.get_string_from_utf8())
		print(packet.get_string_from_utf8())
