'''

    helpers
    
'''

def InitLinearSteps(scan, measurements, step_size, preset):
    angle = -((measurements-1)/2.0) * step_size;
    scan['angles'].append(angle)
    scan['presets'].append(preset)
    
    for i in xrange(1, measurements):
        angle += step_size
        scan['angles'].append(angle)
        scan['presets'].append(preset)
    
    
def AppendLinearSteps(scan, measurements, step_size, preset):
    angle = scan['angles'][-1]
    for i in xrange(0, measurements):
        angle += step_size
        scan['angles'].append(angle)
        scan['presets'].append(preset)
        