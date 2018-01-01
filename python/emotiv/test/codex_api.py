import sys
import os
import platform
import time
import ctypes

from array import *
from ctypes import *
import codex_api_utils as utils


libEDK = utils.import_api(os.getcwd() + '/../community-sdk-3.5.0-WIN-MAC')

userID = c_uint(0)
user   = pointer(userID)
ready  = 0
state  = c_int(0)

alphaValue     = c_double(0)
low_betaValue  = c_double(0)
high_betaValue = c_double(0)
gammaValue     = c_double(0)
thetaValue     = c_double(0)

alpha     = pointer(alphaValue)
low_beta  = pointer(low_betaValue)
high_beta = pointer(high_betaValue)
gamma     = pointer(gammaValue)
theta     = pointer(thetaValue)

channelList = array('I',[3, 7, 9, 12, 16])   # IED_AF3, IED_AF4, IED_T7, IED_T8, IED_Pz 

# -------------------------------------------------------------------------
print("===================================================================")
print("Example to get the average band power for a specific channel from" \
" the latest epoch.")
print("===================================================================")

# -------------------------------------------------------------------------
if libEDK.IEE_EngineConnect("Emotiv Systems-5") != 0:
        print("Emotiv Engine start up failed.")
        exit()

print("Theta, Alpha, Low_beta, High_beta, Gamma \n")


class EDK:
    def __init__(self, libref):
        self.lib = libref
        IEE_EmoEngineEventCreate = self.lib.IEE_EmoEngineEventCreate
        IEE_EmoEngineEventCreate.restype = c_void_p
        self.eEvent = IEE_EmoEngineEventCreate()

        IEE_EmoEngineEventGetEmoState = self.lib.IEE_EmoEngineEventGetEmoState
        IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
        IEE_EmoEngineEventGetEmoState.restype = c_int

        IEE_EmoStateCreate = self.lib.IEE_EmoStateCreate
        IEE_EmoStateCreate.restype = c_void_p
        self.eState = IEE_EmoStateCreate()

        if self.lib.IEE_EngineConnect("Emotiv Systems-5") != 0:
            print("Emotiv Engine start up failed.")
            assert Exception()
        # dict of {c_uint.value: pointer}
        self.users = {}
        # list of {time: number, value: state}
        self.state_queue = []

    def __del__():
        self.lib.IEE_EngineDisconnect()
        self.lib.IEE_EmoStateFree(self.eState)
        self.lib.IEE_EmoEngineEventFree(self.eEvent)

    def handle_events(self):
        while self.lib.IEE_EngineGetNextEvent(self.eEvent):
            eventType = self.lib.IEE_EmoEngineEventGetType(self.eEvent)
            # handle adding and removing users
            if eventType == 0x0010 or eventType == 0x0020:
                user = c_uint(0)
                user_h = pointer(user)
                libEDK.IEE_EmoEngineEventGetUserId(eEvent, user_h)
                if(eventType == 0x0010):
                    users[user.value] = user_h
                elif(eventType == 0x0020):
                    del users[user.value]
            # if state change, update state queue
            if eventType == 0x0040:
                

    def get_average_power_snapshot(self, userID, channel_list):
        """Returns a data snapshot of the average band power
           as a dict {channel: {band: power}}"""
        snapshot = {}
        for channel in channel_list:
            data = [c_double(0)] * 5
            pointers = [pointer(value) for value in data]
            result = self.lib.IEE_GetAverageBandPowers(userID,
                                                       channel,
                                                       *pointers)
            if result == 0:
                snapshot[channel] = {
                    'theta': data[0],
                    'alpha': data[1],
                    'low_beta': data[2],
                    'high_beta': data[3],
                    'gamma': data[4]
                }
        return snapshot


while (1):
    state = libEDK.IEE_EngineGetNextEvent(eEvent)
    if state == 0:
        eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
        libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
        if eventType == 16:  # libEDK.IEE_Event_enum.IEE_UserAdded
            ready = 1
            libEDK.IEE_FFTSetWindowingType(userID, 1)
            # 1: libEDK.IEE_WindowingTypes_enum.IEE_HAMMING
            print("User added")

        if ready == 1:
            for i in channelList:
                result = c_int(0)
                result = libEDK.IEE_GetAverageBandPowers(userID, i,
                                                         theta, alpha,
                                                         low_beta, high_beta,
                                                         gamma)

                if result == 0:  # EDK_OK
                    print("/%.6f, %.6f, %.6f, %.6f, %.6f \n" % (thetaValue.value, alphaValue.value,
                                                                low_betaValue.value, high_betaValue.value, gammaValue.value))

    elif state != 0x0600:
        print("Internal error in Emotiv Engine ! ")
    time.sleep(0.1)
# -------------------------------------------------------------------------
libEDK.IEE_EngineDisconnect()
libEDK.IEE_EmoStateFree(eState)
libEDK.IEE_EmoEngineEventFree(eEvent)
