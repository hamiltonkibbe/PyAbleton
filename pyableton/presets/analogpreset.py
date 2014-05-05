#!/usr/bin/env python
#
#   Copyright (c) 2014 Hamilton Kibbe <ham@hamiltonkib.be>
#
#   Permission is hereby granted, free of charge, to any person obtaining a 
#   copy of this software and associated documentation files (the "Software"), 
#   to deal in the Software without restriction, including without limitation 
#   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#   and/or sell copies of the Software, and to permit persons to whom the 
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included 
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

'''instrument preset classes for Analog
'''


from bs4 import BeautifulSoup
from utils import preset2xml, get_value, set_value, string2bool
import gzip
import os


class AnalogPreset(object):
    ''' Analog preset class
    This class stores the state of the preset in native ableton xml format.
    settings are implemented as properties and setting changes are written
    directly to the xml backing it. 
    '''
    def __init__(self, filename=None):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__),'res/AnalogDefault.adv')
        self.filename = filename
        self.xmltree = BeautifulSoup(preset2xml(filename), ['lxml', 'xml'])
        self.globals = AnalogGlobals(self.xmltree)
        self.osc = [Oscillator(self.xmltree, 1), Oscillator(self.xmltree, 2)]
        self.filter = [Filter(self.xmltree, 1), Filter(self.xmltree, 2)]
        self.amp = [Amp(self.xmltree, 1), Amp(self.xmltree, 2)]
        self.lfo = [LFO(self.xmltree, 1), LFO(self.xmltree, 2)]
        
        
        
    def save_preset(self, filename=None):
        ''' Save the AnalogPreset instance as an Ableton Live Analog preset file.
        '''
        if filename is None:
            filename = self.filename
        with gzip.open(filename, 'wb') as out:
            out.write(self.xmltree.prettify(formatter='xml'))
            out.write('\n')
            
            
class AnalogGlobals(object):
    '''
    '''
    # Map useful names to XML enumeration
    Poly = {'mono': 0, '2': 1, '4': 2,'8': 3, '12': 4, '16': 5, '20': 6,
            '24': 7, '28': 8, '32': 9 }
    
    def __init__(self, xmltree):
        self.parent = getattr(xmltree.Ableton, 'UltraAnalog')
        
        # Parameter Definitions
        self._polyphony = {'name': 'Polyphony', 'type': 'enum',
                           'min': AnalogGlobals.Poly['mono'],
                           'max': AnalogGlobals.Poly['32'],
                           'dict':AnalogGlobals.Poly}
        self._pitchbendrange = {'name': 'PitchBendRange', 'type': 'float',
                           'min': 0.0, 'max': 1.0}
        self._volume = {'name': 'Volume', 'type': 'float', 'min': 0,
                        'max': 1.0}
        
    @property
    def polyphony(self):
        return get_value(self._polyphony, self.parent)
    
    @polyphony.setter
    def polyphony(self, value):
        set_value(self._polyphony, value, self.parent)
        
    @property
    def pitchbendrange(self):
        return get_value(self._pitchbendrange, self.parent)
    
    @pitchbendrange.setter
    def pitchbendrange(self, value):
        set_value(self._pitchbendrange, value, self.parent)

    @property
    def volume(self):
        return get_value(self._volume, self.parent)
    
    @volume.setter
    def volume(self, value):
        set_value(self._volume, value, self.parent)
     



class Oscillator(object):
    ''' Wrapper class for the Oscillators in an Ableton Analog preset.
    

    self.toggle         # Whether or not the oscillator is enabled {True False}
    self.waveshape      # Oscillator Wave Shape {'SINE' 'SAW' 'RECT' 'NOISE'}
    self.octave         # Oscillator Octave [-3 3]
    self.semi           # Oscillator semitones [-12 12]
    self.detune         # Oscillator Detune amount [0 1.0]
    self.mode           # Oscillator Mode {'SUB' 'SYNC'}
    self.envtime        # Pitch Env Time [0 1.0]
    self.envamount      # Pitch Env Initial [-1.0 1.0]
    self.modulation1    # Not too sure about this one...
    self.pulsewidth     # Pulse Width [0 1.0]
    self.subamount      # Sub Amount [0 1.0]
    self.balance        # Filter1/Filter2 Balance [0 1.0]
    self.level          # Level [0 1.0]
    self.lfomodpitch    # LFO Pitch Modulation Amount [0 1.0]
    self.lfomodpw       # LFO Pulse Width Modulation Amount [0 1.0]
    '''
    # Map useful names to XML enumeration
    Waveforms = {'SINE': 0, 'SAW': 1, 'RECT': 2, 'NOISE': 3}
    Modes = {'SUB': 0, 'SYNC': 1}
    
    def __init__(self,xmltree, osc_number):
        ''' Create an instance of an Oscillator wrapping oscillator number <osc_number> in the xmltree provided
        '''
        chain_name = 'SignalChain%d' % osc_number
        self.signalchain = getattr(xmltree.Ableton.UltraAnalog, chain_name)

        # Parameter Definitions
        self._toggle = {'name': 'OscillatorToggle', 'type': 'bool'}
        self._waveshape = {'name': 'OscillatorWaveShape','type': 'enum',
            'min': Oscillator.Waveforms['SINE'],
            'max': Oscillator.Waveforms['NOISE'], 'dict': Oscillator.Waveforms}
        self._octave = {'name': 'OscillatorOct', 'type': 'float', 'min': -3.0,
            'max': 3.0}
        self._semi = {'name': 'OscillatorSemi', 'type': 'float',
            'min': -12.0, 'max': 12.0}
        self._detune = {'name': 'OscillatorDetune', 'type': 'float', 'min': 0.0,
            'max': 1.0}
        self._mode = {'name': 'OscillatorMode', 'type': 'enum',
            'min': Oscillator.Modes['SUB'],'max': Oscillator.Modes['SYNC'],
            'dict': Oscillator.Modes}
        self._envtime = {'name': 'OscillatorEnvTime', 'type': 'float',
            'min': 0.0, 'max': 1.0}
        self._envamount = {'name': 'OscillatorEnvAmount', 'type': 'float',
                           'min': -1.0, 'max': 1.0}
        self._modulation1 = {'name': 'OscillatorModulation1', 'type': 'float',
                           'min': 0.0, 'max': 1.0}
        self._pulsewidth = {'name': 'OscillatorPulseWidth', 'type': 'float',
                           'min': 0.0, 'max': 1.0}
        self._subamount = {'name': 'OscillatorSubAmount', 'type': 'float',
                           'min': 0.0, 'max': 1.0}
        self._balance = {'name': 'OscillatorBalance', 'type': 'float',
                           'min': 0.0, 'max': 1.0}
        self._level = {'name': 'OscillatorLevel', 'type': 'float',
                           'min': 0.0, 'max': 1.0}
        
        
        
    @property
    def toggle(self):
        return get_value(self._toggle, self.signalchain)
    
    @toggle.setter
    def toggle(self, value):
        set_value(self._toggle, value, self.signalchain)
    
    @property
    def waveshape(self):
        return get_value(self._waveshape, self.signalchain)
    
    @waveshape.setter
    def waveshape(self, value):
        set_value(self._waveshape, value, self.signalchain)
        
    @property
    def octave(self):
        return get_value(self._octave, self.signalchain)
    
    @octave.setter
    def octave(self, value):
        set_value(self._octave, value, self.signalchain)
    
    @property
    def semi(self):
        return get_value(self._semi, self.signalchain)
    
    @semi.setter
    def semi(self, value):
        set_value(self._semi, value, self.signalchain)
    
    @property
    def detune(self):
        return get_value(self._detune, self.signalchain)
    
    @detune.setter
    def detune(self, value):
        set_value(self._detune, value, self.signalchain)
    
    @property
    def mode(self):
        return get_value(self._mode, self.signalchain)
    
    @mode.setter
    def mode(self, value):
        set_value(self._mode, Oscillator.Modes[value])
        
    @property
    def envtime(self):
        return get_value(self._envtime, self.signalchain)
    
    @envtime.setter
    def envtime(self, value):
        set_value(self._envtime, value, self.signalchain)
    
    @property
    def envamount(self):
        return get_value(self._envamount, self.signalchain)
    
    @envamount.setter
    def envamount(self, value):
        set_value(self._envamount, value, self.signalchain)   
    
    @property
    def modulation1(self):
        return get_value(self._modulation1, self.signalchain)
    
    @modulation1.setter
    def modulation1(self, value):
        set_value(self._modulation1, value, self.signalchain)
    
    @property
    def pulsewidth(self):
        return get_value(self._pulsewidth, self.signalchain)
    
    @pulsewidth.setter
    def pulsewidth(self, value):
        set_value(self._pulsewidth, value, self.signalchain)
    
    @property
    def subamount(self):
        return get_value(self._subamount, self.signalchain)
    
    @subamount.setter
    def subamount(self, value):
        set_value(self._subamount, value, self.signalchain)
    
    @property
    def balance(self):
        return get_value(self._balance, self.signalchain)
    
    @balance.setter
    def balance(self, value):
        set_value(self._balance, self.signalchain)        
    
    @property
    def level(self):
        return get_value(self._level, self.signalchain)
    
    @level.setter
    def level(self, value):
        set_value(self._level, value, self.signalchain) 
    
    
    @property
    def lfomodpitch(self):
        return get_value(self.signalchain.OscillatorLFOModPitch)
    
    @lfomodpitch.setter
    def lfomodpitch(self, value):
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.OscillatorLFOModPitch, to_write)
    
    @property
    def lfomodpw(self):
        return get_value(self.signalchain.OscillatorLFOModPW)
    
    @lfomodpw.setter
    def lfomodpw(self, value):
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.OscillatorLFOModPW, to_write)
        
        
    def _int2wave(self, value):
        for wave, val in Oscillator.Waveforms.iteritems():
            if val == value:
                return wave
        
    def _int2mode(self, value):
        for mode, val in Oscillator.Modes.iteritems():
            if val == value:
                return mode
        
class Filter(object):
    '''        
    self.toggle                 # Filter Enabled {True False}
    self.type                   # Filter Type {LP12 LP24 BP6 BP12 N2P N4P HP12 HP24 F6 F12}
    self.drive                  # Filter Drive {OFF SYM1 SYM2 SYM3 ASYM1 ASYM2 ASYM3}
    self.kbdcutoffmod           # Keyboard Cutoff Mod [-1.0 1.0]
    self.cutofffrequency        # Cutoff Frequency [0 1.0]
    self.qfactor                # Q-Factor (Res) [0 1.0]
    self.lfocutoffmod           # LFO Cutoff Mod [-1.0 1.0]
    self.envcutoffmod           # Filter Env Cutoff Mod [-1.0 1.0]
    self.lfoqmod                # LFO Q Mod [-1.0 1.0]
    self.envqmod                # Env Q Mod [-1.0 1.0]
    '''
    # Map useful names to XML enumeration
    Types = {'LP12': 0, 'LP24': 1, 'BP6': 2, 'BP12': 3, 'N2P': 4, 'N4P': 5,
             'HP12': 6, 'HP24': 7, 'F6': 8, 'F12': 9}
    Drives ={'OFF': 0, 'SYM1': 1, 'SYM2': 2, 'SYM3': 3, 'ASYM1': 4, 'ASYM2': 5,
            'ASYM3': 6}
    
    def __init__(self, xmltree, filter_number):
        chain_name = 'SignalChain%d' % filter_number
        self.signalchain = getattr(xmltree.Ableton.UltraAnalog, chain_name)
    
    @property
    def toggle(self):
        return get_value(self.signalchain.FilterToggle)
    
    @toggle.setter
    def toggle(self, value):
        if value:
            to_write = u'true'
        else:
            to_write = u'false'
        set_value(self.signalchain.FilterToggle, to_write)
    
    @property
    def type(self):
        return self._int2type(get_value(self.signalchain.FilterType))
    
    @type.setter
    def type(self, value):
        to_write = (u'%d' % Filter.Types[value])
        set_value(self.signalchain.FilterType, to_write)

    @property
    def drive(self):
        return self._int2type(get_value(self.signalchain.FilterDrive))

    @drive.setter
    def drive(self, value):
        to_write = (u'%d' % Filter.Drives[value])
        set_value(self.signalchain.FilterDrive, to_write)


    @property
    def kbdcutoffmod(self):
        return  get_value(self.signalchain.FilterKbdCutoffMod)

    @kbdcutoffmod.setter
    def kbdcutoffmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.FilterKbdCutoffMod, to_write)

    @property
    def lfocutoffmod(self):
        return  get_value(self.signalchain.FilterLFOCutoffMod)

    @lfocutoffmod.setter
    def lfocutoffmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.FilterLFOCutoffMod, to_write)

    @property
    def envcutoffmod(self):
        return  get_value(self.signalchain.FilterEnvCutoffMod)

    @envcutoffmod.setter
    def envcutoffmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.FilterEnvCutoffMod, to_write)



    @property
    def cutofffrequency(self):
        return  get_value(self.signalchain.FilterCutoffFrequency)

    @cutofffrequency.setter
    def cutofffrequency(self, value):
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.cutofffrequency, to_write)

    @property
    def qfactor(self):
        return  get_value(self.signalchain.FilterQFactor)

    @qfactor.setter
    def qfactor(self, value):
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.FilterQFactor, to_write)

    @property
    def lfoqmod(self):
        return  get_value(self.signalchain.FilterLFOQMod)

    @lfoqmod.setter
    def lfoqmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.FilterLFOQMod, to_write)

    @property
    def envqmod(self):
        return  get_value(self.signalchain.FilterEnvQMod)

    @envqmod.setter
    def envqmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.FilterEnvQMod, to_write)

    def _int2type(self, value):
        for t, val in Filter.Types.iteritems():
            if val == value:
                return t
        
    def _int2drive(self, value):
        for drive, val in Filter.Drives.iteritems():
            if val == value:
                return drive

class Amp(object):
    '''
    self.toggle                 # Amp Enabled {True False}
    self.level                  # Amp Level [0 1.0]
    self.pan                    # Pan [0 1.0]
    self.kbdampmod              # Keyboard Amp Mod [-1.0 1.0]
    self.lfoampmod              # LFO Amp Mod [-1.0 1.0]
    self.kbdpanmod              # Keyboard Pan Mod [-1.0 1.0]
    self.lfppanmod              # LFO Pan Mod   [-1.0 1.0]
    self.envpanmod              # Env Pan Mod   [-1.0 1.0]
    '''
    def __init__(self, xmltree, amp_number):
        chain_name = 'SignalChain%d' % amp_number
        self.signalchain = getattr(xmltree.Ableton.UltraAnalog, chain_name)
        
    @property
    def toggle(self):
        return get_value(self.signalchain.AmplifierToggle)
    
    @toggle.setter
    def toggle(self, value):
        if value:
            to_write = u'true'
        else:
            to_write = u'false'
        set_value(self.signalchain.AmplifierToggle, to_write)
        
    @property
    def level(self):
        return get_value(self.signalchain.AmplifierLevel)
    
    @level.setter
    def level(self, value):
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.AmplifierLevel, to_write)
        
    @property
    def pan(self):
        return get_value(self.signalchain.AmplifierPan)
    
    @pan.setter
    def pan(self, value):
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.AmplifierPan, to_write)

    @property
    def kbdampmod(self):
        return get_value(self.signalchain.AmplifierKbdAmpMod)
    
    @kbdampmod.setter
    def kbdampmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.AmplifierKbdAmpMod, to_write) 
        
    @property
    def lfoampmod(self):
        return get_value(self.signalchain.AmplifierLFOAmpMod)
    
    @lfoampmod.setter
    def lfoampmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.AmplifierLFOAmpMod, to_write)  
        
        
    @property
    def kbdpanmod(self):
        return get_value(self.signalchain.AmplifierKbdPanMod)
    
    @kbdpanmod.setter
    def kbdpanmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.AmplifierKbdPanMod, to_write) 
        
    @property
    def lfopanmod(self):
        return get_value(self.signalchain.AmplifierLFOPanMod)
    
    @lfopanmod.setter
    def lfopanmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.AmplifierLFOPanMod, to_write) 
        
    @property
    def envpanmod(self):
        return get_value(self.signalchain.AmplifierEnvPanMod)
    
    @envpanmod.setter
    def envpanmod(self, value):
        value = -1 if value < -1 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.AmplifierEnvPanMod, to_write) 
 
class LFO(object):
    '''
    self.toggle         # LFO Enabled {True False}
    self.waveshape      # LFO Wave shape {SINE TRI RECT NOISE1 NOISE2}
    self.sync           # Tempo Sync Rate [0 23]
    self.synctoggle     # Temp Sync Switch [0 1]
    self.gatereset      # Gate Reset {True False}
    self.pulsewidth     # Pulse Width [0 1.0]
    self.speed          # Speed [0 1.0]
    self.phase          # Phase Offset  [0 1.0]
    self.delay          # Delay   [0 1.0]
    self.fadein         # Fade In   [0 1.0]
    '''
    # WAVEFORMS
    Waveforms = {'SINE': 0, 'TRI': 1, 'RECT': 2, 'NOISE1': 3, 'NOISE2': 4}
    
    def __init__(self, xmltree, lfo_number):
        chain_name = 'SignalChain%d' % lfo_number
        self.signalchain = getattr(xmltree.Ableton.UltraAnalog, chain_name)
 
    @property
    def toggle(self):
        return get_value(self.signalchain.LFOToggle)
    
    @toggle.setter
    def toggle(self, value):
        if value:
            to_write = u'true'
        else:
            to_write = u'false'
        set_value(self.signalchain.LFOToggle, to_write)
 
    @property
    def waveshape(self):
        return self._int2wave(get_value(self.signalchain.LFOWaveShape))
    
    @waveshape.setter
    def waveshape(self, value):
        to_write = (u'%d' % LFO.Waveforms[value])
        set_value(self.signalchain.LFOWaveShape, to_write)
 
 
    @property
    def sync(self):
        return get_value(self.signalchain.LFOSync)
    
    @sync.setter
    def sync(self, value):
        value = 0 if value < 0 else value
        value = 23 if value > 23 else 23
        to_write = u'%f' % value
        set_value(self.signalchain.LFOSync, to_write)
        
    @property
    def synctoggle(self):
        return get_value(self.signalchain.LFOSyncToggle) == True
    
    @synctoggle.setter
    def synctoggle(self, value):
        value = 1 if value else value
        value = 0 if not value else value
        to_write = u'%d' % value
        set_value(self.signalchain.LFOSyncToggle, to_write)
        
    @property
    def gatereset(self):
        return get_value(self.signalchain.LFOGateReset)
        
    @gatereset.setter
    def gatereset(self, value):
        if value:
            to_write = u'true'
        else:
            to_write = u'false'
        set_value(self.signalchain.LFOGateReset, to_write)
    
    @property
    def pulsewidth(self):
        return get_value(self.signalchain.LFOPulseWidth)
        
    @pulsewidth.setter
    def pulsewidth(self):
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.LFOPulseWidth, to_write)
        
    @property
    def speed(self):
        return get_value(self.signalchain.LFOSpeed)
        
    @speed.setter
    def speed(self, value): 
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.LFOSpeed, to_write)
        
    @property
    def phase(self):
        return get_value(self.signalchain.LFOPhase)
        
    @phase.setter
    def phase(self, value): 
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.LFOPhase, to_write)  
    
    @property
    def delay(self):
        return get_value(self.signalchain.LFODelay)
        
    @delay.setter
    def delay(self, value): 
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.LFODelay, to_write)  
 
    
    @property
    def fadein(self):
        return get_value(self.signalchain.LFOFadeIn)
        
    @fadein.setter
    def fadein(self, value): 
        value = 0 if value < 0 else value
        value = 1 if value > 1 else value
        to_write = u'%f' % value
        set_value(self.signalchain.LFOFadeIn, to_write) 
 
    
    def _int2wave(self, value):
        for wave, val in LFO.Waveforms.iteritems():
            if val == value:
                return wave
                
 