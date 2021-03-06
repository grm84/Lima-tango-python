############################################################################
# This file is part of LImA, a Library for Image Acquisition
#
# Copyright (C) : 2009-2011
# European Synchrotron Radiation Facility
# BP 220, Grenoble 38043
# FRANCE
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
############################################################################
#=============================================================================
#
# file :        Pilatus.py
#
# description : Python source for the Pilatus and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                Pilatus are implemented in this file.
#
# project :     TANGO Device Server
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#          This file is generated by POGO
#    (Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#


import PyTango
import sys

from Lima import Core

#==================================================================
#   Pilatus Class Description:
#
#
#==================================================================


class Pilatus(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------
    Core.DEB_CLASS(Core.DebModApplication, 'LimaCCDs')

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.init_device()

        self.__FillMode = {'ON':True,
                           'OFF':False}
        self.__ThresholdGain = {'DEFAULT' : 0,
                                'LOW' : 1,
                                'MID' : 2,
                                'HIGH' : 3,
                                'ULTRA HIGH' : 4}

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        pass


#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    def init_device(self):
        self.set_state(PyTango.DevState.ON)
        self.get_device_properties(self.get_device_class())

        if self.TmpfsSize:
            buffer = _PilatusIterface.buffer()
            buffer.setTmpfsSize(self.TmpfsSize * 1024 * 1024)
            
#------------------------------------------------------------------
#    getAttrStringValueList command:
#
#    Description: return a list of authorized values if any
#    argout: DevVarStringArray   
#------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def getAttrStringValueList(self, attr_name):
        valueList = []
        dict_name = '_' + self.__class__.__name__ + '__' + ''.join([x.title() for x in attr_name.split('_')])
        d = getattr(self,dict_name,None)
        if d:
            valueList = d.keys()
        return valueList
#==================================================================
#
#    Pilatus read/write attribute methods
#
#==================================================================

#------------------------------------------------------------------
#    Read threshold_gain attribute
#------------------------------------------------------------------
    def read_threshold_gain(self, attr):
        gain = _PilatusCamera.gain()
        if gain is None:
            gain = "not set"
        else:
            gain = _getDictKey(self.__ThresholdGain,gain)
        attr.set_value(gain)


#------------------------------------------------------------------
#    Write threshold_gain attribute
#------------------------------------------------------------------
    def write_threshold_gain(self, attr):
        data = attr.get_write_value()
        gain = _getDictValue(self.__ThresholdGain,data)
        threshold = _PilatusCamera.threshold()
        _PilatusCamera.setThresholdGain(threshold,gain)

#------------------------------------------------------------------
#    Read threshold attribute
#------------------------------------------------------------------
    def read_threshold(self, attr):
        threshold = _PilatusCamera.threshold()
        attr.set_value(threshold)

#------------------------------------------------------------------
#    Write threshold attribute
#------------------------------------------------------------------
    def write_threshold(self, attr):
        data = attr.get_write_value()
        _PilatusCamera.setThresholdGain(data)

#------------------------------------------------------------------
#    Read energy_threshold attribute
#------------------------------------------------------------------
    def read_energy_threshold(self, attr) :
        energy = _PilatusCamera.energy()
        attr.set_value(energy)

#------------------------------------------------------------------
#    Write energy_threshold attribute
#------------------------------------------------------------------
    def write_energy_threshold(self, attr) :
        energy = attr.get_write_value()

        _PilatusCamera.setEnergy(energy)

#----------------------------------------------------------------------------
#     Read delay attribute
#----------------------------------------------------------------------------
    def read_trigger_delay(self,attr) :
        delay = communication.hardwareTriggerDelay()
        attr.set_value(delay)

#----------------------------------------------------------------------------
#     Write delay attribute
#----------------------------------------------------------------------------
    def write_trigger_delay(self,attr) :
        data = attr.get_write_value()
        delay = data
        
        _PilatusCamera.setHardwareTriggerDelay(delay)

#----------------------------------------------------------------------------
#     Read nb exposure per frame attribute
#----------------------------------------------------------------------------
    def read_nb_exposure_per_frame(self,attr) :
        nb_frames = _PilatusCamera.nbExposurePerFrame()
        attr.set_value(nb_frames)

#----------------------------------------------------------------------------
#     Write nb exposure per frame attribute
#----------------------------------------------------------------------------
    def write_nb_exposure_per_frame(self,attr) :
        data = attr.get_write_value()
        nb_frames = data
        
        _PilatusCamera.setNbExposurePerFrame(nb_frames)



#------------------------------------------------------------------
#    Read gapfill attribute
#------------------------------------------------------------------
    def read_fill_mode(self, attr):
        gapfill = _PilatusCamera.gapfill()
        gapfill = _getDictKey(self.__FillMode,gapfill)
        attr.set_value(gapfill)

#------------------------------------------------------------------
#    Write gapfill attribute
#------------------------------------------------------------------
    def write_fill_mode(self, attr):
        data = attr.get_write_value()
        gapfill = _getDictValue(self.__FillMode,data)
        _PilatusCamera.setGapfill(gapfill)

#==================================================================
#
#    Pilatus command methods
#
#==================================================================

#==================================================================
#
#    PilatusClass class definition
#
#==================================================================
class PilatusClass(PyTango.DeviceClass):

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        'TmpfsSize' :
        [PyTango.DevInt,
         "Size of communication temp. filesystem (in MB)",0],
        }


    #    Command definitions
    cmd_list = {
        'getAttrStringValueList':
        [[PyTango.DevString, "Attribute name"],
         [PyTango.DevVarStringArray, "Authorized String value list"]],
        }


    #    Attribute definitions
    attr_list = {
        'threshold_gain':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'threshold':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'energy_threshold':
            [[PyTango.DevFloat,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'fill_mode':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'trigger_delay':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'nb_exposure_per_frame':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        }


#------------------------------------------------------------------
#    PilatusClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name)

def _getDictKey(dict, value):
    try:
        ind = dict.values().index(value)                            
    except ValueError:
        return None
    return dict.keys()[ind]

def _getDictValue(dict, key):
    try:
        value = dict[key.upper()]
    except KeyError:
        return None
    return value

#----------------------------------------------------------------------------
# Plugins
#----------------------------------------------------------------------------
from Lima import Pilatus as PilatusAcq

_PilatusIterface = None
_PilatusCamera = None

def get_control(**keys) :
    global _PilatusIterface
    global _PilatusCamera
    if _PilatusIterface is None:
        _PilatusCamera = PilatusAcq.Camera()
        _PilatusIterface = PilatusAcq.Interface(_PilatusCamera)
    return Core.CtControl(_PilatusIterface)

def get_tango_specific_class_n_device() :
    return PilatusClass,Pilatus
