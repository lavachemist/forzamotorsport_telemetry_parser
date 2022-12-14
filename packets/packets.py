from ctypes import (
    c_float, c_int8, c_uint8, c_uint16, c_uint32, c_uint64, Union)
from typing import Dict, Final, Type
from constants.constants import GRID_SIZE, PacketId
from custom_types.game import EventCode, F1PacketStructure
from packets.packet_data import (
    CarDamageData, CarMotionData, CarSetupsData, CarStatusData,
    CarTelemetryData, FinalClassificationData, LapDataData, LapHistoryData,
    LobbyInfoData, MarshalZone, ParticipantsData, TyreStintHistoryData,
    WeatherForecastSample)

"""This module contains classes that correspond with the packets
output by the game.
"""


class Packet(F1PacketStructure):
    _fields_ = [
        ('packetFormat', c_uint16),
        ('gameMajorVersion', c_uint8),
        ('gameMinorVersion', c_uint8),
        ('packetVersion', c_uint8),
        ('packetId', c_uint8),
        ('sessionUID', c_uint64),
        ('sessionTime', c_float),
        ('frameIdentifier', c_uint32),
        ('playerCarIndex', c_uint8),
        ('secondaryPlayerCarIndex', c_uint8),
    ]


class CarDamagePacket(Packet):
    _fields_ = [
        ('carDamageData', CarDamageData * GRID_SIZE),
    ]


class CarSetupsPacket(Packet):
    _fields_ = [
        ('carSetups', CarSetupsData * GRID_SIZE),
    ]


class CarStatusPacket(Packet):
    _fields_ = [
        ('carStatusData', CarStatusData * GRID_SIZE),
    ]


class CarTelemetryPacket(Packet):
    _fields_ = [
        ('carTelemetryData', CarTelemetryData * GRID_SIZE),
        ('mfdPanelIndex', c_uint8),
        ('mfdPanelIndexSecondaryPlayer', c_uint8),
        ('suggestedGear', c_int8),
    ]


class FastestLap(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
        ('lapTime', c_float),
    ]


class Retirement(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class TeamMateInPits(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class RaceWinner(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class Penalty(F1PacketStructure):
    _fields_ = [
        ('penaltyType', c_uint8),
        ('infringementType', c_uint8),
        ('vehicleIdx', c_uint8),
        ('otherVehicleIdx', c_uint8),
        ('time', c_uint8),
        ('lapNum', c_uint8),
        ('placesGained', c_uint8),
    ]


class SpeedTrap(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
        ('speed', c_float),
        ('isOverallFastestInSession', c_uint8),
        ('isDriverFastestInSession', c_uint8),
        ('fastestVehicleIdxInSession', c_uint8),
        ('fastestSpeedInSession', c_float),
    ]


class StartLights(F1PacketStructure):
    _fields_ = [
        ('numLights', c_uint8),
    ]


class DriveThroughPenaltyServed(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class StopGoPenaltyServed(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class Flashback(F1PacketStructure):
    _fields_ = [
        ('flashbackFrameIdentifier', c_uint32),
        ('flashbackSessionTime', c_float),
    ]


class Buttons(F1PacketStructure):
    _fields_ = [
        ('buttonStatus', c_uint32),
    ]


class EventDataDetails(Union):
    _fields_ = [
        ("FastestLap", FastestLap),
        ("Retirement", Retirement),
        ("TeamMangeInPits", TeamMateInPits),
        ("RaceWinner", RaceWinner),
        ("Penalty", Penalty),
        ("SpeedTrap", SpeedTrap),
        ("StartLights", StartLights),
        ("DriveThroughPenaltyServed", DriveThroughPenaltyServed),
        ("StopGoPenaltyServed", StopGoPenaltyServed),
        ("Flashback", Flashback),
        ("Buttons", Buttons),
    ]


class EventPacket(Packet):
    _fields_ = [
        ('eventStringCode', EventCode),
        ('eventDetails', EventDataDetails)
    ]


class FinalClassificationPacket(Packet):
    _fields_ = [
        ('numCars', c_uint8),
        ('classificationData', FinalClassificationData * GRID_SIZE),
    ]


class LapDataPacket(Packet):
    _fields_ = [
        ('lapData', LapDataData * GRID_SIZE),
        ('timeTrialPBCarIdx', c_uint8),
        ('timeTrialRivalCarIdx', c_uint8),
    ]


class LobbyInfoPacket(Packet):
    _fields_ = [
        ('numPlayers', c_uint8),
        ('lobbyPlayers', LobbyInfoData * GRID_SIZE),
    ]


class MotionPacket(Packet):
    _fields_ = [
        ('carMotionData', CarMotionData * GRID_SIZE),
        ('suspensionPosition', c_float * 4),
        ('suspensionVelocity', c_float * 4),
        ('suspensionAcceleration', c_float * 4),
        ('wheelSpeed', c_float * 4),
        ('wheelSlip', c_float * 4),
        ('localVelocityX', c_float),
        ('localVelocityY', c_float),
        ('localVelocityZ', c_float),
        ('angularVelocityX', c_float),
        ('angularVelocityY', c_float),
        ('angularVelocityZ', c_float),
        ('angularAccelerationX', c_float),
        ('angularAccelerationY', c_float),
        ('angularAccelerationZ', c_float),
        ('frontWheelsAngle', c_float),
    ]


class ParticipantsPacket(Packet):
    _fields_ = [
        ('numActiveCars', c_uint8),
        ('participants', ParticipantsData * GRID_SIZE),
    ]


class SessionHistoryPacket(Packet):
    _fields_ = [
        ('carIdx', c_uint8),
        ('numLaps', c_uint8),
        ('numTyreStints', c_uint8),
        ('bestLapTimeLapNum', c_uint8),
        ('bestSector1LapNum', c_uint8),
        ('bestSector2LapNum', c_uint8),
        ('bestSector3LapNum', c_uint8),
        ('lapHistoryData', LapHistoryData * 100),
        ('tyreStintHistoryData', TyreStintHistoryData * 8),
    ]


class SessionPacket(Packet):
    _fields_ = [
        ('weather', c_uint8),
        ('trackTemperature', c_int8),
        ('airTemperature', c_int8),
        ('totalLaps', c_uint8),
        ('trackLength', c_uint16),
        ('sessionType', c_uint8),
        ('trackId', c_int8),
        ('formula', c_uint8),
        ('sessionTimeLeft', c_uint16),
        ('sessionDuration', c_uint16),
        ('pitSpeedLimit', c_uint8),
        ('gamePaused', c_uint8),
        ('isSpectating', c_uint8),
        ('spectatorCarIndex', c_uint8),
        ('sliProNativeSupport', c_uint8),
        ('numMarshalZones', c_uint8),
        ('marshalZones', MarshalZone * 21),
        ('safetyCarStatus', c_uint8),
        ('networkGame', c_uint8),
        ('numWeatherForecastSamples', c_uint8),
        ('weatherForecastSamples', WeatherForecastSample * 56),
        ('forecastAccuracy', c_uint8),
        ('aiDifficulty', c_uint8),
        ('seasonLinkIdentifier', c_uint32),
        ('weekendLinkIdentifier', c_uint32),
        ('sessionLinkIdentifier', c_uint32),
        ('pitStopWindowIdealLap', c_uint8),
        ('pitStopWindowLatestLap', c_uint8),
        ('pitStopRejoinPosition', c_uint8),
        ('steeringAssist', c_uint8),
        ('brakingAssist', c_uint8),
        ('gearboxAssist', c_uint8),
        ('pitAssist', c_uint8),
        ('pitReleaseAssist', c_uint8),
        ('ERSAssist', c_uint8),
        ('DRSAssist', c_uint8),
        ('dynamicRacingLine', c_uint8),
        ('dynamicRacingLineType', c_uint8),
        ('gameMode', c_uint8),
        ('ruleSet', c_uint8),
        ('timeOfDay', c_uint32),
        ('sessionLength', c_uint8),
    ]


PACKET_TYPE: Final[Dict[int, Type[Packet]]] = {
    PacketId.MOTION.value: MotionPacket,
    PacketId.SESSION.value: SessionPacket,
    PacketId.LAP_DATA.value: LapDataPacket,
    PacketId.EVENT.value: EventPacket,
    PacketId.PARTICIPANTS.value: ParticipantsPacket,
    PacketId.CAR_SETUPS.value: CarSetupsPacket,
    PacketId.CAR_TELEMETRY.value: CarTelemetryPacket,
    PacketId.CAR_STATUS.value: CarStatusPacket,
    PacketId.FINAL_CLASSIFICATION.value: FinalClassificationPacket,
    PacketId.LOBBY_INFO.value: LobbyInfoPacket,
    PacketId.CAR_DAMAGE.value: CarDamagePacket,
    PacketId.SESSION_HISTORY.value: SessionHistoryPacket,
}
