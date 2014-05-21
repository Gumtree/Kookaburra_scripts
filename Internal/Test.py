from gumpy.commons import sics
from org.gumtree.gumnix.sics.control import ServerStatus
import time
  
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

'''

    setup

'''

scan = { 'angles': [], 'presets': [] }

angle_ref = 179.6217662 # 180.0
InitLinearSteps(  scan, measurements=33, step_size=5.0e-5, preset=40  ) # angle_ref - (steps/2)*step_size
AppendLinearSteps(scan, measurements=13, step_size=1.2e-4, preset=100 )
AppendLinearSteps(scan, measurements=15, step_size=2.4e-4, preset=200 )
AppendLinearSteps(scan, measurements=10, step_size=6.0e-4, preset=400 )
AppendLinearSteps(scan, measurements=10, step_size=1.2e-3, preset=800 )
AppendLinearSteps(scan, measurements=16, step_size=2.4e-3, preset=1400)
AppendLinearSteps(scan, measurements=40, step_size=6.0e-3, preset=1400)

print 'done'
print
