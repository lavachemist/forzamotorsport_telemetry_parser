import filters.Filter as fil
import packets.packets as pk


class LogFilter(fil.Filter):
    def filter(self, packet: pk.Packet):
        print(packet.packetId)
