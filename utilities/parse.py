import dataclasses
import inspect
import typing
import custom_types.basic as bt
import utilities.data as util
import packets.packets as pk
import packets.packet_data as pd


T = typing.TypeVar('T')


GameData: typing.Set[typing.Any] = {
    pd.CarDamageData, pd.CarSetupsData, pd.CarStatusData, pd.CarTelemetryData,
    pd.FinalClassificationData, pd.LapDataData, pd.LobbyInfoData,
    pd.MotionData, pd.ParticipantsData, pd.LapHistoryData,
    pd.TyreStintHistoryData, pd.MarshalZone, pd.WeatherForecastSample,
}


class Ref(typing.Generic[T]):
    def __init__(self, value: T):
        self.value: T = value


def get_packet_id(data: bytearray) -> int:
    return int(util.unpack(data, pk.PACKET_ID_INDEX, bt.UInt8).value)


def parse_data(data: bytes, index: Ref[int], DataType: typing.Type[T]) -> T:
    if inspect.isclass(DataType):
        if issubclass(DataType, bt.BasicType):
            value = util.unpack(data, index.value, DataType)
            index.value += bt.BASIC_TYPE_FORMAT[DataType].size
            return value  # type: ignore
        if issubclass(DataType, pk.EventPacket):
            return DataType(parse_data(data, index, field.type) for
                            field in dataclasses.fields(DataType))  # type: ignore
    if typing.get_origin(DataType) is tuple:
        return tuple(parse_data(data, index, e) for
                     e in typing.get_args(DataType))  # type: ignore
    if DataType in GameData:
        return DataType(*[parse_data(data, index, field.type) for
                        field in dataclasses.fields(DataType)])
    raise ValueError(
        f'Expected BasicType, tuple, GameData, or Optional, got {DataType}.')


def parse(data: bytes) -> pk.Packet:
    PacketType = pk.PACKET_TYPE[get_packet_id(data)]  # type: ignore
    if PacketType is pk.EventPacket:
        event_code = util.to_string(parse_data(
            data, Ref(pk.PACKET_HEADER_LENGTH), pk.EventCode))
        PacketType = pk.EVENT_DETAILS_TYPE[event_code]
    index = Ref[int](0)
    return PacketType(*[parse_data(data, index, field.type) for
                      field in dataclasses.fields(PacketType)])  # type: ignore