""" https://adventofcode.com/2021/day/16 """

from math import prod
from typing import Tuple

class BITStream:
    """Implement the BITStream using bits allowing arbitrary read of bits """
    def __init__(self, input_string):
        self.__input__ = input_string
        self.__bytes__ = [int(c, 16) for c in input_string]
        self.__pos__ = 0
        self.__len__ = 4 * len(input_string)

    def read(self, bits):
        pos = self.__pos__
        end = self.__pos__ = self.__pos__ + bits
        num = 0
        while pos < end:
            byte = self.__bytes__[pos // 4]
            i = pos % 4 # index inside of the bit (0123)
            if i == 0 and end >= pos + 4:
                # fast-path: we want to read the full byte
                num = (num << 4) + byte
                pos += 4
            else:
                # read bit by bit
                bit_idx = 3 - i
                bit = ((byte & (1 << bit_idx)) >> bit_idx)
                num = (num << 1) + bit
                pos += 1
        return num

    def pos(self):
        return self.__pos__

class Packet:
    """Class to store the packages while we are decoding them"""
    def __init__(self):
        self.version = 0
        self.type_id = 0
        self.literal = -1
        self.packets = []

    def __repr__(self) -> str:
        if self.literal != -1:
            return f"literal {self.literal} v: {self.version}"
        return f"type: {self.type_id} v:{self.version} {self.packets}"

def parse_literal(stream:BITStream) -> Tuple[int, int]:
    """Read a number from the stream and return the value and the amount of
    bits read from the stream"""
    num = 0
    has_more = True
    start_pos = stream.pos()
    while has_more:
        num = num << 4
        has_more = stream.read(1)
        num += stream.read(4)
    return num, stream.pos() - start_pos

def parse_packet(stream:BITStream) -> Tuple[Packet, int]:
    """Read a packet from the stream and return the packet and the amount of bits
    read. This function will call itself recursively to read the containing packets"""
    start_pos = stream.pos()
    packet = Packet()
    packet.version = stream.read(3)
    packet.type_id = stream.read(3)
    if packet.type_id == 4:
        packet.literal, _ = parse_literal(stream)
    else:
        length_id = stream.read(1)
        if length_id == 0:
            to_read_bits = stream.read(15)
            while to_read_bits:
                packets, parsed_bits = parse_packet(stream)
                to_read_bits -= parsed_bits
                packet.packets += [packets]
        elif length_id == 1:
            to_read_count = stream.read(11)
            while to_read_count:
                packets, _ = parse_packet(stream)
                to_read_count -= 1
                packet.packets += [packets]
    return packet, stream.pos() - start_pos

def part1_sum_version(input_string, expected_value = None):
    stream = BITStream(input_string)
    packet, _ = parse_packet(stream)

    def recursive_sum(packet):
        result = packet.version
        for _p in packet.packets:
            result += recursive_sum(_p)
        return result

    value = recursive_sum(packet)
    if expected_value is not None:
        assert value == expected_value
    else:
        print(f"What do you get if you add up the version numbers in all packets? {value}")

def eval_packet(packet):
    # pylint: disable=multiple-statements
    # pylint: disable=line-too-long
    # pylint: disable=too-many-return-statements
    if packet.type_id == 4: return packet.literal
    if packet.type_id == 0: return sum([eval_packet(p) for p in packet.packets])
    if packet.type_id == 1: return prod([eval_packet(p) for p in packet.packets])
    if packet.type_id == 2: return min([eval_packet(p) for p in packet.packets])
    if packet.type_id == 3: return max([eval_packet(p) for p in packet.packets])
    if packet.type_id == 5: return int(eval_packet(packet.packets[0]) > eval_packet(packet.packets[1]))
    if packet.type_id == 6: return int(eval_packet(packet.packets[0]) < eval_packet(packet.packets[1]))
    if packet.type_id == 7: return int(eval_packet(packet.packets[0]) == eval_packet(packet.packets[1]))
    assert False # Shouldn't reach
    return -1

def part2_evaluate(input_string, expected_value = None):
    stream = BITStream(input_string)
    packet, _ = parse_packet(stream)
    value = eval_packet(packet)

    if expected_value is not None:
        assert value == expected_value
    else:
        print(f"What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission? {value}")

if __name__ == '__main__':
    MY_PUZZLE_INPUT = "60552F100693298A9EF0039D24B129BA56D67282E600A4B5857002439CE580E5E5AEF67803600D2E294B2FCE8AC489BAEF37FEACB31A678548034EA0086253B183F4F6BDDE864B13CBCFBC4C10066508E3F4B4B9965300470026E92DC2960691F7F3AB32CBE834C01A9B7A933E9D241003A520DF316647002E57C1331DFCE16A249802DA009CAD2117993CD2A253B33C8BA00277180390F60E45D30062354598AA4008641A8710FCC01492FB75004850EE5210ACEF68DE2A327B12500327D848028ED0046661A209986896041802DA0098002131621842300043E3C4168B12BCB6835C00B6033F480C493003C40080029F1400B70039808AC30024C009500208064C601674804E870025003AA400BED8024900066272D7A7F56A8FB0044B272B7C0E6F2392E3460094FAA5002512957B98717004A4779DAECC7E9188AB008B93B7B86CB5E47B2B48D7CAD3328FB76B40465243C8018F49CA561C979C182723D769642200412756271FC80460A00CC0401D8211A2270803D10A1645B947B3004A4BA55801494BC330A5BB6E28CCE60BE6012CB2A4A854A13CD34880572523898C7EDE1A9FA7EED53F1F38CD418080461B00440010A845152360803F0FA38C7798413005E4FB102D004E6492649CC017F004A448A44826AB9BFAB5E0AA8053306B0CE4D324BB2149ADDA2904028600021909E0AC7F0004221FC36826200FC3C8EB10940109DED1960CCE9A1008C731CB4FD0B8BD004872BC8C3A432BC8C3A4240231CF1C78028200F41485F100001098EB1F234900505224328612AF33A97367EA00CC4585F315073004E4C2B003530004363847889E200C45985F140C010A005565FD3F06C249F9E3BC8280804B234CA3C962E1F1C64ADED77D10C3002669A0C0109FB47D9EC58BC01391873141197DCBCEA401E2CE80D0052331E95F373798F4AF9B998802D3B64C9AB6617080"

    part1_sum_version("8A004A801A8002F478", expected_value=16)
    part1_sum_version("620080001611562C8802118E34", expected_value=12)
    part1_sum_version("C0015000016115A2E0802F182340", expected_value=23)
    part1_sum_version("A0016C880162017C3686B18A3D4780", expected_value=31)
    part1_sum_version(MY_PUZZLE_INPUT)

    part2_evaluate("C200B40A82", expected_value=3)
    part2_evaluate("04005AC33890", expected_value=54)
    part2_evaluate("880086C3E88112", expected_value=7)
    part2_evaluate("CE00C43D881120", expected_value=9)
    part2_evaluate("D8005AC2A8F0", expected_value=1)
    part2_evaluate("F600BC2D8F", expected_value=0)
    part2_evaluate("9C005AC2F8F0", expected_value=0)
    part2_evaluate("9C0141080250320F1802104A08", expected_value=1)
    part2_evaluate(MY_PUZZLE_INPUT)
