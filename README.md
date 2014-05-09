# PyAbleton

**A Python Library for creating and Editing Ableton Live instrument patches**

** Analog **

It's as easy as this:

	from pyableton.presets import AnalogPreset
	instrument = AnalogPreset()
	
	instrument.osc[1].waveshape = 'SINE'
	instrument.filter[0].type = 'LP24'
	instrument.filter[1].envelope.attacktime = 0.0687
	instrument.polyphony = 'MONO'
	
	instrument.save_preset('gnarly_wobble.adv')
