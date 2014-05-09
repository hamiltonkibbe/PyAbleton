#!/usr/bin/env python

from pyableton.presets.analogpreset import AnalogPreset, AnalogGlobals, Oscillator, Filter
ps = AnalogPreset()


def test_shorthand_import():
    try:
        from pyableton.presets import AnalogPreset
    except:
        assert False
        
def test_regular_import():
    import pyableton
    assert pyableton.presets.AnalogPreset
    
def test_ctr():
    from pyableton.presets import AnalogPreset
    assert AnalogPreset()

### AnalogGlobals Tests #############################

def test_global_polyphony():
    for key in AnalogGlobals.Poly.iterkeys():
        ps.globals.poly = key
        assert ps.globals.poly == key

def test_global_pitchbendrange():
    for val in [ps.globals._pitchbendrange['min'], ps.globals._pitchbendrange['max']]:
        ps.pitchbendrange = val
        assert ps.pitchbendrange == val
    
def test_global_volume():
    for val in [ps.globals._volume['min'], ps.globals._volume['max']]:
        ps.globals.volume = val
        assert ps.globals.volume == val



### Oscillator Tests #############################

def test_oscillator_toggle():
    for val in [True, False]:
        for i in range(2):
            ps.osc[i].toggle = val
            assert ps.osc[i].toggle == val


def test_oscillator_waveshape():
    for key in Oscillator.Waveforms.iterkeys():
        for i in range(2):
            ps.osc[i].waveshape = key
            assert ps.osc[i].waveshape == key
        
def test_oscillator_octave():
    for i in range(2):
        for val in [ps.osc[i]._octave['min'], ps.osc[i]._octave['max']]:
            ps.osc[i].octave = val
            assert ps.osc[i].octave == val
            
def test_oscillator_semi():
    for i in range(2):
        for val in [ps.osc[i]._semi['min'], ps.osc[i]._semi['max']]:
            ps.osc[i].semi = val
            assert ps.osc[i].semi == val
                    
def test_oscillator_detune():
    for i in range(2):
        for val in [ps.osc[i]._detune['min'], ps.osc[i]._detune['max']]:
            ps.osc[i].detune = val
            assert ps.osc[i].detune == val
            
def test_oscillator_mode():
    for key in Oscillator.Modes.iterkeys():
        for i in range(2):
            ps.osc[i].mode = key
            assert ps.osc[i].mode == key
            
def test_oscillator_envtime():
    for i in range(2):
        for val in [ps.osc[i]._envtime['min'], ps.osc[i]._envtime['max']]:
            ps.osc[i].envtime = val
            assert ps.osc[i].envtime == val

def test_oscillator_envamount():
    for i in range(2):
        for val in [ps.osc[i]._envamount['min'], ps.osc[i]._envamount['max']]:
            ps.osc[i].envamount = val
            assert ps.osc[i].envamount == val

def test_oscillator_pulsewidth():
    for i in range(2):
        for val in [ps.osc[i]._pulsewidth['min'], ps.osc[i]._pulsewidth['max']]:
            ps.osc[i].pulsewidth = val
            assert ps.osc[i].pulsewidth == val
            
def test_oscillator_subamount():
    for i in range(2):
        for val in [ps.osc[i]._subamount['min'], ps.osc[i]._subamount['max']]:
            ps.osc[i].subamount = val
            assert ps.osc[i].subamount == val           
            
def test_oscillator_balance():
    for i in range(2):
        for val in [ps.osc[i]._balance['min'], ps.osc[i]._balance['max']]:
            ps.osc[i].balance = val
            assert ps.osc[i].balance == val            
            
def test_oscillator_level():
    for i in range(2):
        for val in [ps.osc[i]._level['min'], ps.osc[i]._level['max']]:
            ps.osc[i].level = val
            assert ps.osc[i].level == val
            
def test_oscillator_lfomodpitch():
    for i in range(2):
        for val in [ps.osc[i]._lfomodpitch['min'], ps.osc[i]._lfomodpitch['max']]:
            ps.osc[i].lfomodpitch = val
            assert ps.osc[i].lfomodpitch == val
            
def test_oscillator_lfomodpw():
    for i in range(2):
        for val in [ps.osc[i]._lfomodpw['min'], ps.osc[i]._lfomodpw['max']]:
            ps.osc[i].lfomodpw = val
            assert ps.osc[i].lfomodpw == val
            


          
### Filter Tests #############################

def test_filter_toggle():
    for val in [True, False]:
        for i in range(2):
            ps.filter[i].toggle = val
            assert ps.filter[i].toggle == val
            
def test_filter_type():
    for key in Filter.Types.iterkeys():
        for i in range(2):
            ps.filter[i].type = key
            assert ps.filter[i].type == key
            
def test_filter_drive():
    for key in Filter.Drives.iterkeys():
        for i in range(2):
            ps.filter[i].drive = key
            assert ps.filter[i].drive == key        
            
def test_filter_kbdcutoffmod():
    for i in range(2):
        for val in [ps.filter[i]._kbdcutoffmod['min'], ps.filter[i]._kbdcutoffmod['max']]:
            ps.filter[i].kbdcutoffmod = val
            assert ps.filter[i].kbdcutoffmod == val            
            
def test_filter_lfocutoffmod():
    for i in range(2):
        for val in [ps.filter[i]._lfocutoffmod['min'], ps.filter[i]._lfocutoffmod['max']]:
            ps.filter[i].lfocutoffmod = val
            assert ps.filter[i].lfocutoffmod == val             
            
def test_filter_envcutoffmod():
    for i in range(2):
        for val in [ps.filter[i]._envcutoffmod['min'], ps.filter[i]._envcutoffmod['max']]:
            ps.filter[i].envcutoffmod = val
            assert ps.filter[i].envcutoffmod == val           
            
            
def test_filter_cutofffrequency():
    for i in range(2):
        for val in [ps.filter[i]._cutofffrequency['min'], ps.filter[i]._cutofffrequency['max']]:
            ps.filter[i].cutofffrequency = val
            assert ps.filter[i].cutofffrequency == val           
            
def test_filter_qfactor():
    for i in range(2):
        for val in [ps.filter[i]._qfactor['min'], ps.filter[i]._qfactor['max']]:
            ps.filter[i].qfactor = val
            assert ps.filter[i].qfactor == val 
            
            
            
def test_filter_envqmod():
    for i in range(2):
        for val in [ps.filter[i]._envqmod['min'], ps.filter[i]._envqmod['max']]:
            ps.filter[i].envqmod = val
            assert ps.filter[i].envqmod == val        
            
def test_filter_lfoqmod():
    for i in range(2):
        for val in [ps.filter[i]._lfoqmod['min'], ps.filter[i]._lfoqmod['max']]:
            ps.filter[i].lfoqmod = val
            assert ps.filter[i].lfoqmod == val            
            
            
            
### Amp Tests #############################

def test_amp_toggle():
    for val in [True, False]:
        for i in range(2):
            ps.amp[i].toggle = val
            assert ps.amp[i].toggle == val            
            
def test_amp_level():
    for i in range(2):
        for val in [ps.amp[i]._level['min'], ps.amp[i]._level['max']]:
            ps.amp[i].level = val
            assert ps.amp[i].level == val
            
def test_amp_pan():
    for i in range(2):
        for val in [ps.amp[i]._pan['min'], ps.amp[i]._pan['max']]:
            ps.amp[i].pan = val
            assert ps.amp[i].pan == val    
            
def test_amp_kbdampmod():
    for i in range(2):
        for val in [ps.amp[i]._kbdampmod['min'], ps.amp[i]._kbdampmod['max']]:
            ps.amp[i].kbdampmod = val
            assert ps.amp[i].kbdampmod == val          
            
def test_amp_lfoampmod():
    for i in range(2):
        for val in [ps.amp[i]._lfoampmod['min'], ps.amp[i]._lfoampmod['max']]:
            ps.amp[i].lfoampmod = val
            assert ps.amp[i].lfoampmod == val           
            
def test_amp_kbdpanmod():
    for i in range(2):
        for val in [ps.amp[i]._kbdpanmod['min'], ps.amp[i]._kbdpanmod['max']]:
            ps.amp[i].kbdpanmod = val
            assert ps.amp[i].kbdpanmod == val          
            
def test_amp_lfopanmod():
    for i in range(2):
        for val in [ps.amp[i]._lfopanmod['min'], ps.amp[i]._lfopanmod['max']]:
            ps.amp[i].lfopanmod = val
            assert ps.amp[i].lfopanmod == val          
            
def test_amp_envpanmod():
    for i in range(2):
        for val in [ps.amp[i]._envpanmod['min'], ps.amp[i]._envpanmod['max']]:
            ps.amp[i].envpanmod = val
            assert ps.amp[i].envpanmod == val             
            
            
def test_failing():
    assert False
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            