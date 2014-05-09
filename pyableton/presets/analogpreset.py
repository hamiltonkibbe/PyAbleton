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

"""instrument preset classes for Analog
"""


from bs4 import BeautifulSoup
from utils import preset2xml, get_value, set_value, string2bool
from utils import AbletonParameter as Parameter
import gzip
import os


class AnalogPreset(object):
    """ Analog preset class
    This class stores the state of the preset in native ableton xml format.
    settings are implemented as properties and setting changes are written
    directly to the xml backing it. 
    """
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
        """ Save the AnalogPreset instance as an Ableton Live Analog preset file.
        """
        if filename is None:
            filename = self.filename
        with gzip.open(filename, 'wb') as out:
            out.write(self.xmltree.prettify(formatter='xml'))
            out.write('\n')
            
            
class AnalogGlobals(object):
    """ Global synthesizer settings
    """
    # Map useful names to XML enumeration
    Poly = {'mono': 0, '2': 1, '4': 2,'8': 3, '12': 4, '16': 5, '20': 6,
            '24': 7, '28': 8, '32': 9 }
    
    
    def __init__(self, xmltree):
        self.parent = getattr(xmltree.Ableton, 'UltraAnalog')
        
        # Parameter Definitions
        self._polyphony = Parameter(name='Polyphony', type='enum', dict=AnalogGlobals.Poly)
        self._pitchbendrange = Parameter(name='PitchBendRange', type='float', min=0.0, max=1.0)
        self._volume = Parameter(name='Volume', type='float', min=0.0, max=1.0)
        
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
    """ Wrapper class for the Oscillators in an Ableton Analog preset.
    

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
    """
    # Map useful names to XML enumeration
    Waveforms = {'SINE': 0, 'SAW': 1, 'RECT': 2, 'NOISE': 3}
    Modes = {'SUB': 0, 'SYNC': 1}
    
    
    
    def __init__(self,xmltree, osc_number):
        """ Create an instance of an Oscillator wrapping oscillator number <osc_number> in the xmltree provided
        """
        chain_name = 'SignalChain%d' % osc_number
        self.signalchain = getattr(xmltree.Ableton.UltraAnalog, chain_name)
        
        # Parameter Definitions
        self._toggle = Parameter(name='OscillatorToggle', type='bool')
        self._waveshape = Parameter(name='OscillatorWaveShape', type='enum', dict=Oscillator.Waveforms)
        self._octave = Parameter(name='OscillatorOct', type='float', min=-3.0, max=3.0)
        self._semi = Parameter(name='OscillatorSemi', type='float', min=-12.0, max=12.0)
        self._detune = Parameter(name='OscillatorDetune', type='float', min=0.0, max=1.0)
        self._mode = Parameter(name='OscillatorMode', type='enum', dict=Oscillator.Modes)
        self._envtime = Parameter(name='OscillatorEnvTime', type='float', min=0.0, max=1.0)
        self._envamount = Parameter(name='OscillatorEnvAmount', type='float', min=-1.0, max=1.0)
        self._modulation1 = Parameter(name='OscillatorModulation1', type='float', min=0.0, max=1.0)
        self._pulsewidth = Parameter(name='OscillatorPulseWidth', type='float', min=0.0, max=1.0)
        self._subamount = Parameter(name='OscillatorSubAmount', type='float', min=0.0, max=1.0)
        self._balance = Parameter(name='OscillatorBalance', type='float', min=0.0, max=1.0)
        self._filterbalance = Parameter(name='OscillatorBalance', type='float', min=0.0, max=1.0)
        self._level = Parameter(name='OscillatorLevel', type='float', min=0.0, max=1.0)
        self._lfomodpitch = Parameter(name='OscillatorLFOModPitch', type='float', min=0.0, max=1.0)
        self._lfomodpw = Parameter(name='OscillatorLFOModPW', type='float', min=0.0, max=1.0)

        
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
        set_value(self._mode, value, self.signalchain)
        
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
        set_value(self._balance, value, self.signalchain)
    
    @property
    def filterbalance(self):
        return get_value(self._filterbalance, self.signalchain)
    
    @filterbalance.setter
    def filterbalance(self, value):
        set_value(self._filterbalance, self.signalchain)        
    
    @property
    def level(self):
        return get_value(self._level, self.signalchain)
    
    @level.setter
    def level(self, value):
        set_value(self._level, value, self.signalchain) 
    
    
    @property
    def lfomodpitch(self):
        return get_value(self._lfomodpitch, self.signalchain)
    
    @lfomodpitch.setter
    def lfomodpitch(self, value):
        set_value(self._lfomodpitch, value, self.signalchain)
    
    @property
    def lfomodpw(self):
        return get_value(self._lfomodpw, self.signalchain)
    
    @lfomodpw.setter
    def lfomodpw(self, value):
        set_value(self._lfomodpw, value, self.signalchain)
        
        
class Filter(object):
    """        
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
    """
    # Map useful names to XML enumeration
    Types = {'LP12': 0, 'LP24': 1, 'BP6': 2, 'BP12': 3, 'N2P': 4, 'N4P': 5,
             'HP12': 6, 'HP24': 7, 'F6': 8, 'F12': 9}
    Drives ={'OFF': 0, 'SYM1': 1, 'SYM2': 2, 'SYM3': 3, 'ASYM1': 4, 'ASYM2': 5,
            'ASYM3': 6}
    
    
    def __init__(self, xmltree, filter_number):
        chain_name = 'SignalChain%d' % filter_number
        self.signalchain = getattr(xmltree.Ableton.UltraAnalog, chain_name)
        self.envelope = Envelope(self.signalchain, 0)
        
        # Parameter definitions
        self._toggle = Parameter(name='FilterToggle', type='bool')
        self._type = Parameter(name='FilterType', type='enum', dict=Filter.Types)
        self._drive = Parameter(name='FilterDrive', type='enum', dict=Filter.Drives)
        self._kbdcutoffmod = Parameter(name='FilterKbdCutoffMod', type='float', min=-1.0, max=1.0)
        self._lfocutoffmod = Parameter(name='FilterLFOCutoffMod', type='float', min=-1.0, max=1.0)
        self._envcutoffmod = Parameter(name='FilterEnvCutoffMod', type='float', min=-1.0, max=1.0)
        self._cutofffrequency = Parameter(name='FilterCutoffFrequency', type='float', min=0.0, max=1.0)
        self._qfactor = Parameter(name='FilterQFactor', type='float', min=0.0, max=1.0)
        self._envqmod = Parameter(name='FilterEnvQMod', type='float', min=-1.0, max=1.0)
        self._lfoqmod = Parameter(name='FilterLFOQMod', type='float', min=-1.0, max=1.0)
        
        
    @property
    def toggle(self):
        return get_value(self._toggle, self.signalchain)
    
    @toggle.setter
    def toggle(self, value):
        set_value(self._toggle, value, self.signalchain)
    
    @property
    def type(self):
        return get_value(self._type, self.signalchain)
    
    @type.setter
    def type(self, value):
        set_value(self._type, value, self.signalchain)

    @property
    def drive(self):
        return get_value(self._drive, self.signalchain)

    @drive.setter
    def drive(self, value):
        set_value(self._drive, value, self.signalchain)

    @property
    def kbdcutoffmod(self):
        return  get_value(self._kbdcutoffmod, self.signalchain)

    @kbdcutoffmod.setter
    def kbdcutoffmod(self, value):
        set_value(self._kbdcutoffmod, value, self.signalchain)

    @property
    def lfocutoffmod(self):
        return  get_value(self._lfocutoffmod, self.signalchain)

    @lfocutoffmod.setter
    def lfocutoffmod(self, value):
        set_value(self._lfocutoffmod, value, self.signalchain)

    @property
    def envcutoffmod(self):
        return  get_value(self._envcutoffmod, self.signalchain)

    @envcutoffmod.setter
    def envcutoffmod(self, value):
        set_value(self._envcutoffmod, value, self.signalchain)


    @property
    def cutofffrequency(self):
        return  get_value(self._cutofffrequency, self.signalchain)

    @cutofffrequency.setter
    def cutofffrequency(self, value):
        set_value(self._cutofffrequency, value, self.signalchain)

    @property
    def qfactor(self):
        return  get_value(self._qfactor, self.signalchain)

    @qfactor.setter
    def qfactor(self, value):
        set_value(self._qfactor, value, self.signalchain)

    @property
    def lfoqmod(self):
        return  get_value(self._lfoqmod, self.signalchain)

    @lfoqmod.setter
    def lfoqmod(self, value):
        set_value(self._lfoqmod, value, self.signalchain)

    @property
    def envqmod(self):
        return  get_value(self._envqmod, self.signalchain)

    @envqmod.setter
    def envqmod(self, value):
        set_value(self._envqmod, value, self.signalchain)


class Amp(object):
    """
    self.toggle                 # Amp Enabled {True False}
    self.level                  # Amp Level [0 1.0]
    self.pan                    # Pan [0 1.0]
    self.kbdampmod              # Keyboard Amp Mod [-1.0 1.0]
    self.lfoampmod              # LFO Amp Mod [-1.0 1.0]
    self.kbdpanmod              # Keyboard Pan Mod [-1.0 1.0]
    self.lfopanmod              # LFO Pan Mod   [-1.0 1.0]
    self.envpanmod              # Env Pan Mod   [-1.0 1.0]
    """
    def __init__(self, xmltree, amp_number):
        chain_name = 'SignalChain%d' % amp_number
        self.signalchain = getattr(xmltree.Ableton.UltraAnalog, chain_name)
        self.envelope = Envelope(self.signalchain, 1)
        
        # Parameter Definitions
        self._toggle = Parameter(name='AmplifierToggle', type='bool')
        self._level = Parameter(name='AmplifierLevel',type='float', min=0.0, max=1.0)
        self._pan = Parameter(name='AmplifierPan',type='float', min=0.0, max=1.0)
        self._kbdampmod = Parameter(name='AmplifierKbdAmpMod', type='float', min=-1.0, max=1.0)
        self._lfoampmod = Parameter(name='AmplifierLFOAmpMod', type='float', min=-1.0, max=1.0)
        self._kbdpanmod = Parameter(name='AmplifierKbdPanMod', type='float', min=-1.0, max=1.0)
        self._lfopanmod = Parameter(name='AmplifierLFOPanMod', type='float', min=-1.0, max=1.0)
        self._envpanmod = Parameter(name='AmplifierEnvPanMod', type='float', min=-1.0, max=1.0)
        
    @property
    def toggle(self):
        return get_value(self._toggle, self.signalchain)
    
    @toggle.setter
    def toggle(self, value):
        set_value(self._toggle, value, self.signalchain)
        
    @property
    def level(self):
        return get_value(self._level, self.signalchain)
    
    @level.setter
    def level(self, value):
        set_value(self._level, value, self.signalchain)
        
    @property
    def pan(self):
        return get_value(self._pan, self.signalchain)
    
    @pan.setter
    def pan(self, value):
        set_value(self._pan, value, self.signalchain)

    @property
    def kbdampmod(self):
        return get_value(self._kbdampmod, self.signalchain)
    
    @kbdampmod.setter
    def kbdampmod(self, value):
        set_value(self._kbdampmod, value, self.signalchain) 
        
    @property
    def lfoampmod(self):
        return get_value(self._lfoampmod, self.signalchain)
    
    @lfoampmod.setter
    def lfoampmod(self, value):
        set_value(self._lfoampmod, value, self.signalchain)  
        
        
    @property
    def kbdpanmod(self):
        return get_value(self._kbdpanmod, self.signalchain)
    
    @kbdpanmod.setter
    def kbdpanmod(self, value):
        set_value(self._kbdpanmod, value, self.signalchain) 
        
    @property
    def lfopanmod(self):
        return get_value(self._lfopanmod, self.signalchain)
    
    @lfopanmod.setter
    def lfopanmod(self, value):
        set_value(self._lfopanmod, value, self.signalchain) 
        
    @property
    def envpanmod(self):
        return get_value(self._envpanmod, self.signalchain)
    
    @envpanmod.setter
    def envpanmod(self, value):
        set_value(self._envpanmod, value, self.signalchain) 
 
class LFO(object):
    """
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
    """
    # WAVEFORMS
    Waveforms = {'SINE': 0, 'TRI': 1, 'RECT': 2, 'NOISE1': 3, 'NOISE2': 4}
    
    def __init__(self, xmltree, lfo_number):
        chain_name = 'SignalChain%d' % lfo_number
        self.signalchain = getattr(xmltree.Ableton.UltraAnalog, chain_name)
        
        # Parameter Definitions
        self._toggle = Parameter(name='LFOToggle', type='bool')
        self._waveshape = Parameter(name='LFOWaveShape', type='enum', dict=LFO.Waveforms)
        self._sync = Parameter(name='LFOSync', type='int', min=0, max=23)
        self._synctoggle = Parameter(name='LFOSyncToggle', type='int', min=0, max=1)
        self._gatereset = Parameter(name='LFOGateReset', type='bool')
        self._pulsewidth = Parameter(name='LFOPulseWidth', type='float', min=0.0, max=1.0)
        self._speed = Parameter(name='LFOSpeed', type='float', min=0.0, max=1.0)
        self._phase = Parameter(name='LFOPhase', type='float', min=0.0, max=1.0)
        self._delay = Parameter(name='LFODelay', type='float', min=0.0, max=1.0)
        self._fadein = Parameter(name='LFOFadeIn', type='float', min=0.0, max=1.0)
        
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
    def sync(self):
        return get_value(self._sync, self.signalchain)
    
    @sync.setter
    def sync(self, value):
        set_value(self._sync, value, self.signalchain)
        
    @property
    def synctoggle(self):
        return get_value(self._synctoggle, self.signalchain)
    
    @synctoggle.setter
    def synctoggle(self, value):
        set_value(self._synctoggle, value, self.signalchain)
        
    @property
    def gatereset(self):
        return get_value(self._gatereset, self.signalchain)
        
    @gatereset.setter
    def gatereset(self, value):
        set_value(self._gatereset, value, self.signalchain)
    
    @property
    def pulsewidth(self):
        return get_value(self._pulsewidth, self.signalchain)
        
    @pulsewidth.setter
    def pulsewidth(self, value):
        set_value(self._pulsewidth, value, self.signalchain)
        
    @property
    def speed(self):
        return get_value(self._speed, self.signalchain)
        
    @speed.setter
    def speed(self, value): 
        set_value(self._speed, value, self.signalchain)
        
    @property
    def phase(self):
        return get_value(self._phase, self.signalchain)
        
    @phase.setter
    def phase(self, value): 
        set_value(self._phase, value, self.signalchain)  
    
    @property
    def delay(self):
        return get_value(self._delay, self.signalchain)
        
    @delay.setter
    def delay(self, value): 
        set_value(self._delay, value, self.signalchain)  
 
    @property
    def fadein(self):
        return get_value(self._fadein, self.signalchain)
        
    @fadein.setter
    def fadein(self, value): 
        set_value(self._fadein, value, self.signalchain) 
 

class Envelope(object):
    """ Envelope class
    self.exponentialslope   bool
    self.loop               enum
    self.freerun            bool
    self.legato             bool
    self.attackmod          float
    self.attacktime         float
    self.decaytime          float
    self.ampmod             float
    self.sustainlevel       float
    self.sustaintime        float
    self.releasetime        float
    """
    
    # Map enum to dict
    Loop = {'OFF': 0, 'AD-R': 1, 'ADR-R': 2, 'ADS-AR': 3}
    
    def __init__(self, signalchain, env_number):
        env_name = 'Envelope.%d' % env_number
        self.envelope = getattr(signalchain, env_name)
        
        self._exponentialslope = Parameter(name='ExponentialSlope', type='bool')
        self._loop = Parameter(name='Loop', type='enum', dict=Envelope.Loop)
        self._freerun = Parameter(name='FreeRun', type='bool')
        self._legato = Parameter(name='Legato', type='bool')
        self._attackmod = Parameter(name='AttackMod', type='float', min=0.0, max=1.0)
        self._attacktime = Parameter(name='AttackTime', type='float', min=0.0, max=1.0)
        self._decaytime = Parameter(name='DecayTime', type='float', min=0.0, max=1.0)
        self._ampmod = Parameter(name='AmpMod', type='float', min=0.0, max=1.0)
        self._sustainlevel = Parameter(name='SustainLevel', type='float', min=0.0, max=1.0)
        self._sustaintime = Parameter(name='SustainTime', type='float', min=0.0, max=1.0)
        self._releasetime = Parameter(name='ReleaseTime', type='float', min=0.0, max=1.0)
    
    
    @property
    def exponentialslope(self):
        return get_value(self._exponentialslope, self.envelope)
        
    @exponentialslope.setter
    def exponentialslope(self, value): 
        set_value(self._exponentialslope, value, self.envelope) 
    
    @property
    def loop(self):
        return get_value(self._loop, self.envelope)
        
    @loop.setter
    def loop(self, value): 
        set_value(self._loop, value, self.envelope)
        
    @property
    def freerun(self):
        return get_value(self._freerun, self.envelope)
        
    @freerun.setter
    def freerun(self, value): 
        set_value(self._freerun, value, self.envelope) 
    
    @property
    def legato(self):
        return get_value(self._legato, self.envelope)
        
    @legato.setter
    def legato(self, value): 
        set_value(self._legato, value, self.envelope)
        
    @property
    def attackmod(self):
        return get_value(self._attackmod, self.envelope)
        
    @attackmod.setter
    def attackmod(self, value): 
        set_value(self._attackmod, value, self.envelope)   
        
    @property
    def attacktime(self):
        return get_value(self._attacktime, self.envelope)
        
    @attacktime.setter
    def attacktime(self, value): 
        set_value(self._attacktime, value, self.envelope)
        
    @property
    def decaytime(self):
        return get_value(self._decaytime, self.envelope)
        
    @decaytime.setter
    def decaytime(self, value): 
        set_value(self._decaytime, value, self.envelope)
    
    @property
    def ampmod(self):
        return get_value(self._ampmod, self.envelope)
        
    @ampmod.setter
    def ampmod(self, value): 
        set_value(self._ampmod, value, self.envelope)   
        
    @property
    def sustainlevel(self):
        return get_value(self._sustainlevel, self.envelope)
        
    @sustainlevel.setter
    def sustainlevel(self, value): 
        set_value(self._sustainlevel, value, self.envelope)    
        
    @property
    def sustaintime(self):
        return get_value(self._sustaintime, self.envelope)
        
    @sustaintime.setter
    def sustaintime(self, value): 
        set_value(self._sustaintime, value, self.envelope)
    
    @property
    def releasetime(self):
        return get_value(self._releasetime, self.envelope)
        
    @releasetime.setter
    def releasetime(self, value): 
        set_value(self._releasetime, value, self.envelope)
        
        