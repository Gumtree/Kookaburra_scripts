
__script__.title = 'KKB Measurement Script'
__script__.version = '1.0'

from gumpy.commons import sics
from org.gumtree.gumnix.sics.control import ServerStatus
from pickle import Pickler, Unpickler
import time

from math import log as ln
from math import exp, isnan, isinf

from __builtin__ import max as builtin_max
from __builtin__ import min as builtin_min
from org.eclipse.swt.widgets import FileDialog
from org.eclipse.swt import SWT
from org.eclipse.swt.widgets import Display
from java.io import File
import time

SINGLE_TYPE = SWT.SINGLE
SAVE_TYPE   = SWT.SAVE
MULTI_TYPE  = SWT.MULTI

class __Display_Runnable__(Runnable):
    def __init__(self, type = SINGLE_TYPE, ext = ['*.*']):
        self.filename = None
        self.filenames = None
        self.path = None
        self.type = type
        self.ext = ext
    
    def run(self):
        global __UI__
        dialog = FileDialog(__UI__.getShell(), self.type);
        dialog.setFilterExtensions(self.ext)
        dialog.open()
        self.filename = dialog.getFilterPath() + File.separator + dialog.getFileName()
        self.filenames = dialog.getFileNames()
        self.path = dialog.getFilterPath()
         
def open_file_dialog(type = SWT.SINGLE, ext = ['*.*']):
    __display_run__ = __Display_Runnable__(type, ext)
    Display.getDefault().asyncExec(__display_run__)
    while __display_run__.filename is None:
        time.sleep(0.5)
    if type == SWT.MULTI:
        fns = []
        for fn in __display_run__.filenames:
            fns.append(__display_run__.path + '/' + fn)
        return fns
    return __display_run__.filename

## templates

reference_templates_dict = {}
reference_templates_dict['Si111'] = 179.6142
reference_templates_dict['Si311'] =  -0.02575

steps_templates_dict = {}
steps_templates_dict['Si111: Comprehensive Scan'] = [
    'count_roi', 'linear',
    [33, 6.0e-5,  1000, 1200],
    [13, 1.2e-4,  1000, 1200],
    [15, 2.4e-4,  1000, 1200],
    [10, 6.0e-4,  1000, 1200],
    [10, 1.2e-3,  1000, 1200],
    [16, 2.4e-3,  1000, 1200],
    [60, 6.0e-3,  1000, 1200]]

steps_templates_dict['Si111: Comprehensive Rheo Yacine Scan'] = [
    'count_roi', 'logscale',
    [33, 6.0e-5,  1000, 1200],
    [73, 8.0e-5,  1000, 1200]]

steps_templates_dict['Si111: Rapid Intensity Scan Rheo Yacine Scan'] = [
    'time', 'logscale',
    [17, 1.20e-4,  1, 1200],
    [30, 2.0e-4,  20, 1200]]

steps_templates_dict['Si111: CHECK INTESITY MAIN TRANS BACKGROUND'] = [
    'count_roi', 'linear',
    [33, 6.0e-5,  1000, 1200],
    [13, 1.2e-4,  1000, 1200],
    [8, 2.4e-4,  1000, 1200],
    [3, 0.1,  1000, 1200]]

steps_templates_dict['Si111: Find Primary Beam'] = [
    'time', 'linear',
    [31, 6.0e-5, 1, 1200]]

steps_templates_dict['Si111: Check Tsas'] = [
    'time', 'linear',
    [17, 1.2e-4, 1, 1200],
    [2, 0.1,  20, 1200]]

steps_templates_dict['Si111: Fast Scan'] = [
    'count_roi', 'linear',
    [17, 1.2e-4,  1000, 1200],
    [ 6, 4.8e-4,  1000, 1200],
    [ 6, 1.2e-3,  1000, 1200],
    [ 5, 2.4e-3,  1000, 1200],
    [ 8, 4.8e-3,  1000, 1200],
    [30, 9.0e-3,  1000, 1200]]

steps_templates_dict['Si111: Quick Overview Scan 10 seconds'] = [
    'time', 'linear',
    [17, 1.2e-4,   1, 1200],
    [ 6, 4.8e-4,  10, 1200],
    [ 6, 1.2e-3,  10, 1200],
    [ 5, 2.4e-3,  10, 1200],
    [ 8, 4.8e-3,  10, 1200],
    [30, 9.0e-3,  10, 1200]]



steps_templates_dict['Si311: Find Primary Beam'] = [
    'time', 'linear',
    [51, 0.00004, 1, 1200]]

steps_templates_dict['Si311: Logarithmic Scan'] = [
    'count_roi', 'logscale',
    [31, 2e-5,    1000, 1200],
    [60, 2.5e-5,  1000, 1200]]

steps_templates_dict[' Si311: Logarithmic Radlinski Scan'] = [
    'count_roi', 'logscale',
    [39, 4e-5,  1000, 1200],
    [23, 10e-5, 1000, 1200],
    [5, 0.004,  1000, 1200]]

steps_templates_dict['Si311: Comprehensive Scan'] = [
    'count_roi', 'linear',
    [21, 1.3e-5, 50000, 1200],
    [13, 6.0e-5,  1000, 1200],
    [15, 1.2e-4,  1000, 1200],
    [10, 3.0e-4,  1000, 1200],
    [10, 6.0e-4,  1000, 1200],
    [16, 1.2e-3,  1000, 1200],
    [60, 3.0e-3,  1000, 1200]]


steps_templates_dict['Test m2chi scan'] = [
    'time', 'linear',
    [31, 0.1, 1, 1200]]


## export path

__EXPORT_PATH__ = 'V:/shared/KKB Logbook/Temp Plot Data Repository/'

if not os.path.exists(__EXPORT_PATH__):
    os.makedirs(__EXPORT_PATH__)
    
## User

user_name = Par('string', 'Christine', options = ['Christine', 'Lela'])
user_name.title = 'Name'

user_email = Par('string', 'cre@ansto.gov.au', options = ['cre@ansto.gov.au', 'liliana.decampo@ansto.gov.au'])
user_email.title = 'EMail'

g0 = Group('User')
g0.numColumns = 2
g0.add(user_name, user_email)

## Sample
sample_name = Par('string', 'UNKNOWN', options = ['Empty Cell', 'Empty Beam'], command="sample_thickness.enabled = sample_name.value not in ['Empty Cell', 'Empty Beam']")
sample_name.title = 'Name'

sample_description = Par('string', 'UNKNOWN')
sample_description.title = 'Description'

sample_thickness = Par('string', '1', options = ['0.01', '0.1', '1.0', '10.0'])
sample_thickness.title = 'Thickness (mm)'

Group('Sample').add(sample_name, sample_description, sample_thickness)

## Crystal
crystal_name = Par('string', 'UNKNOWN')
crystal_name.title = 'Name'
crystal_name.enabled = False
try:
    m2om = sics.getValue('/instrument/crystal/m2om').getFloatData()
    if m2om > 90:
        crystal_name.value = 'Si111 (4.74 Angstroms)'
    else:
        crystal_name.value = 'Si311 (2.37 Angstroms)'
except:
    pass

crystal_change = Act('switchCrystal()', 'switch to other crystal')
    
g0 = Group('Crystal')
g0.numColumns = 2
g0.add(crystal_name, crystal_change)

## Pre/Post-Sample Slit

def updateOffset(gapBox, offsetBox):
    offsetBox.enabled = 'fully' not in gapBox.value
    
def getSlitGapAndOffset(aPath, a0, bPath, b0):
    a = sics.getValue(aPath).getFloatData()
    b = sics.getValue(bPath).getFloatData()
        
    gap    = (a - a0 - (b - b0)) / 1.0
    offset = (a - a0 + (b - b0)) / 2.0
    
    return (gap, offset)


crystal = str(crystal_name.value)
if 'Si111' in crystal:
    ss1r0 = 28.35
    ss1l0 = 27.75

elif 'Si311' in crystal:
    ss1r0 = -9.16
    ss1l0 = -9.76
    
ss1u0 = -8.04
ss1d0 = -7.30

(ss1vg, ss1vo) = getSlitGapAndOffset('/instrument/slits/ss1u', ss1u0, '/instrument/slits/ss1d', ss1d0)
(ss1hg, ss1ho) = getSlitGapAndOffset('/instrument/slits/ss1r', ss1r0, '/instrument/slits/ss1l', ss1l0)

pss_ss1vg = Par('string', '%.1f' % ss1vg, options = ['fully closed', '5', '10', '15', '20', '25', '30', '40', '50', 'fully opened'], command='updateOffset(pss_ss1vg, pss_ss1vo)')
pss_ss1vg.title = 'Vertical Gap (mm)'

pss_ss1vo = Par('float', '%.1f' % ss1vo)
pss_ss1vo.title = 'Vertical Offset (mm)'

pss_ss1hg = Par('string', '%.1f' % ss1hg, options = ['fully closed', '5', '10', '15', '20', '25', '30', '40', '50', 'fully opened'], command='updateOffset(pss_ss1hg, pss_ss1ho)')
pss_ss1hg.title = 'Horizontal Gap (mm)'

pss_ss1ho = Par('float', '%.1f' % ss1ho)
pss_ss1ho.title = 'Horizontal Offset (mm)'

g0 = Group('Pre-Sample Slit')
g0.numColumns = 2
g0.add(pss_ss1vg, pss_ss1vo, pss_ss1hg, pss_ss1ho)

ss2u0 =  2.00
ss2d0 =  1.40
ss2r0 = -1.00
ss2l0 =  0.50

(ss2vg, ss2vo) = getSlitGapAndOffset('/instrument/slits/ss2u', ss2u0, '/instrument/slits/ss2d', ss2d0)
(ss2hg, ss2ho) = getSlitGapAndOffset('/instrument/slits/ss2r', ss2r0, '/instrument/slits/ss2l', ss2l0)

pss_ss2vg = Par('string', '%.1f' % ss2vg, options = pss_ss1vg.options, command='updateOffset(pss_ss2vg, pss_ss2vo)')
pss_ss2vg.title = 'Vertical Gap (mm)'

pss_ss2vo = Par('float', '%.1f' % ss2vo)
pss_ss2vo.title = 'Vertical Offset (mm)'

pss_ss2hg = Par('string', '%.1f' % ss2hg, options = pss_ss1hg.options, command='updateOffset(pss_ss2hg, pss_ss2ho)')
pss_ss2hg.title = 'Horizontal Gap (mm)'

pss_ss2ho = Par('float', '%.1f' % ss2ho)
pss_ss2ho.title = 'Horizontal Offset (mm)'

g0 = Group('Post-Sample Slit')
g0.numColumns = 2
g0.add(pss_ss2vg, pss_ss2vo, pss_ss2hg, pss_ss2ho)

## Template

steps_templates = Par('string', '', options = sorted(steps_templates_dict.keys()), command='setTemplate()')
steps_templates.title = 'Template'

Group('Template').add(steps_templates)

## Scan

scan_variable = Par('string', 'm2om [deg]', options = [
    'pmom [deg]', 'pmchi [deg]', 'm1om [deg]', 'm1chi [deg]', 'm1x [mm]', 'm2om [deg]', 'm2chi [deg]', 'm2x [mm]', 'm2y [mm]', 'mdet [mm]',
    'ss1u [mm]', 'ss1d [mm]', 'ss1l [mm]', 'ss1r [mm]',
    'ss2u [mm]', 'ss2d [mm]', 'ss2l [mm]', 'ss2r [mm]',
    'ss1vg [mm]', 'ss1vo [mm]', 'ss1hg [mm]', 'ss1ho [mm]',
    'ss2vg [mm]', 'ss2vo [mm]', 'ss2hg [mm]', 'ss2ho [mm]'], command="scan_variable_plot.value = scan_variable.value")

scan_variable.title = 'Variable'

scan_reference = Par('float', '0.0')
scan_reference.title = 'Reference'

for key in reference_templates_dict.keys():
    if key in crystal_name.value:
        scan_reference.value = reference_templates_dict[key]

scan_mode = Par('string', 'count_roi', options = ['count_roi', 'time'], command='setScanMode()')
scan_mode.title = 'Mode'

scan_min_time = Par('int', '5')
scan_min_time.title = 'Min Time (sec)'

crystal = str(crystal_name.value)
crystal = crystal[:crystal.find(' ')]
for key in steps_templates_dict.keys():
    if ('Find Primary Beam' in key) and (crystal in key):
        steps_templates.value = key
        break

scan_sam_position = Par('string', 'fixed', options = ['fixed', '1', '2', '3', '4', '5'])
scan_sam_position.title = 'Sample Position'

logscale_position = Par('bool', False)
logscale_position.title = 'Logarithmic Steps'

g0 = Group('Scan')
g0.numColumns = 2
g0.add(scan_variable, scan_reference, scan_mode, scan_min_time, scan_sam_position, logscale_position)

start_scan = Act('startScan(ConfigurationModel())', 'Start Scan')

## Measurement Steps

g0 = Group('Measurement Steps')
g0.numColumns = 5

stepInfo = []

for i in xrange(7):
    steps_e = Par('bool', True, command='setEnabled(%i)' % i)
    steps_e.title = '(%i)' % (i + 1)
    steps_m = Par('int', 0)
    steps_m.title = 'Data Points'
    steps_s = Par('float', 0)
    steps_s.title = 'Step Size'
    steps_p = Par('int', 0)
    steps_p.title = 'Preset'
    steps_t = Par('int', 1200)
    steps_t.title = 'Max Time'
    
    stepInfo.append({'enabled': steps_e, 'dataPoints':steps_m, 'stepSize':steps_s, 'preset':steps_p, 'maxTime':steps_t})
    g0.add(steps_e, steps_m, steps_s, steps_p, steps_t)
    
btnPlotSteps = Act('btnPlotSteps_clicked()', 'Plot Measurement Steps') #'compare measurement steps with previous scan')

## Save/Load Configuration


cnfg_save = Par('string')
cnfg_save.title = 'Save'
cnfg_save.enabled = False
cnfg_save_btn = Act('saveConfiguration()', '>>')

cnfg_load = Par('string')
cnfg_load.title = 'Load'
cnfg_load.enabled = False
cnfg_load_btn = Act('loadConfigurations()', '>>')

'''
cnfg_save = Par('file', command='saveConfiguration()')
cnfg_save.title = 'Save'
cnfg_save.dtype = 'save'
cnfg_save.ext = '*.kkb'

cnfg_load = Par('file', command='loadConfigurations()')
cnfg_load.title = 'Load'
cnfg_load.dtype = 'multi'
cnfg_load.ext = '*.kkb'
'''

g0 = Group('Configuration')
g0.add(cnfg_save, cnfg_save_btn, cnfg_load, cnfg_load_btn)
g0.numColumns = 2

configurations = []
configurations_apply = []
for i in xrange(5):
    config = Par('string')
    config.title = '(%i)' % (i + 1)
    config.enabled = False
    configurations.append(config)
    
    g0.add(config)
    
    exec("config_apply%i = Act('applyConfiguration(%i)', 'apply')" % (i, i))
    exec("g0.add(config_apply%i)" % i)

cnfg_run_btn = Act('runConfigurations()', 'Run Configurations')

def saveConfiguration():    
    file = open_file_dialog(type = SAVE_TYPE, ext = ['*.kkb'])
    try:
        fh = open(file, 'w')
    except:
        print 'not saved'
        return
    
    try:
        p = Pickler(fh)
        
        # header
        p.dump('KKB')
        # content
        model = ConfigurationModel()
        for att in dir(model):
            att_value = getattr(model, att)
            if (att.find('_') != 0) and ('instancemethod' not in str(type(att_value))):
                p.dump(att)
                p.dump(att_value)
        
        cnfg_save.value = file
        print 'saved'
        
    finally:
        fh.close()
    
def loadConfigurations():
    fileList = open_file_dialog(type = MULTI_TYPE, ext = ['*.kkb'])
    if not fileList:
        return

    files = '';
    for f in fileList:
         files += f + ';'

    cnfg_load.value = files
    for item in configurations:
        item.value = ''

    index = 0
    for path in filter(None, cnfg_load.value.split(';')):
        fh = open(path, 'r')
        try:
            p = Unpickler(fh)
            if p.load() != 'KKB':
                print 'ERROR:', os.path.basename(path)
            else:
                model = ConfigurationModel()
                for att in dir(model):
                    att_value = getattr(model, att)
                    if (att.find('_') != 0) and ('instancemethod' not in str(type(att_value))):
                        if p.load() != att:
                            print 'FORMAT ERROR:', os.path.basename(path)
                            break
                            
                        setattr(model, att, p.load())
                else:
                    if index < len(configurations):
                        configurations[index].value = os.path.basename(path)
                        index += 1
        finally:
            fh.close()
            
def applyConfiguration(index):
    file = configurations[index].value
    if not file:
        print 'no file selected'
        return

    index = 0
    for path in filter(None, cnfg_load.value.split(';')):
        if file == os.path.basename(path):
            fh = open(path, 'r')
            try:
                p = Unpickler(fh)
                if p.load() != 'KKB':
                    print 'ERROR:', os.path.basename(path)
                else:
                    model = ConfigurationModel()
                    for att in dir(model):
                        att_value = getattr(model, att)
                        if (att.find('_') != 0) and ('instancemethod' not in str(type(att_value))):
                            if p.load() != att:
                                print 'FORMAT ERROR:', os.path.basename(path)
                                break
                                
                            setattr(model, att, p.load())
                    else:
                        print 'apply:', os.path.basename(path)
                        model.apply()
            finally:
                fh.close()

def runConfigurations():    
    if cnfg_load.value:
        for path in filter(None, cnfg_load.value.split(';')):
            fh = open(path, 'r')
            try:
                p = Unpickler(fh)
                if p.load() != 'KKB':
                    print 'ERROR:', os.path.basename(path)
                else:
                    model = ConfigurationModel()
                    for att in dir(model):
                        att_value = getattr(model, att)
                        if (att.find('_') != 0) and ('instancemethod' not in str(type(att_value))):
                            if p.load() != att:
                                print 'FORMAT ERROR:', os.path.basename(path)
                                break
                                
                            setattr(model, att, p.load())
                    else:
                        print 'run:', os.path.basename(path)
                        startScan(model)
            finally:
                fh.close()


## Plot

combine_tube0 = Par('bool', True)
combine_tube0.title = ' Tube 0'

combine_tube1 = Par('bool', True)
combine_tube1.title = '   Tube 1'

combine_tube2 = Par('bool', True)
combine_tube2.title = '   Tube 2'

combine_tube3 = Par('bool', True)
combine_tube3.title = '   Tube 3'

combine_tube4 = Par('bool', True)
combine_tube4.title = '   Tube 4'

combine_tube6 = Par('bool', False)
combine_tube6.title = '   Tube 6'

g0 = Group('Plotting - Select Tube(s) of Interest:')
g0.numColumns = 6
g0.add(combine_tube0, combine_tube1, combine_tube2, combine_tube3, combine_tube4, combine_tube6)

check_tube9 = Par('bool', True)
check_tube9.title = ' Tube 9: Si (311)'

check_tube10 = Par('bool', False)
check_tube10.title = '   Tube 10: Si (111)'
        
g1 = Group('Plotting - Select Transmission Tube(s) of Interest:')
g1.numColumns = 2
g1.add(check_tube9, check_tube10)


scan_variable_plot = Par('string', 'm2om [deg]', options = [
    'pmom [deg]', 'pmchi [deg]', 'm1om [deg]', 'm1chi [deg]', 'm1x [mm]', 'm2om [deg]', 'm2chi [deg]', 'm2x [mm]', 'm2y [mm]', 'mdet [mm]',
    'ss1u [mm]', 'ss1d [mm]', 'ss1l [mm]', 'ss1r [mm]',
    'ss2u [mm]', 'ss2d [mm]', 'ss2l [mm]', 'ss2r [mm]',
    'ss1vg [mm]', 'ss1vo [mm]', 'ss1hg [mm]', 'ss1ho [mm]',
    'ss2vg [mm]', 'ss2vo [mm]', 'ss2hg [mm]', 'ss2ho [mm]'])

scan_variable_plot.title = 'Scan Variable'

combine_mode = Par('string', 'individual', options = ['individual', 'combined'])
combine_mode.title = 'Mode'
      
scan_variable_sorting = Par('bool', True)
scan_variable_sorting.title = 'Sorting'

#check_fitting = Par('bool', False)
#check_fitting.title = 'Fitting'

Group('Plotting - Settings').add(scan_variable_plot, combine_mode, scan_variable_sorting)

# export to csv
btnPlot    = Act('btnPlot_clicked()', 'Plot Selected Data Set')
btnExport  = Act('export_clicked()', 'Export to CSV')

def setTemplate():
    try:
        template = steps_templates_dict[steps_templates.value]
        
        scan_mode.value = template[0]
        if template[1] == 'logscale':
            logscale_position.value = True
        elif template[1] == 'linear':
            logscale_position.value = False

        setScanMode()
        
        for i in xrange(len(template) - 2):
            templateItem = template[i + 2]
            stepInfoItem = stepInfo[i]
                
            stepInfoItem['enabled'   ].value   = True
            stepInfoItem['dataPoints'].enabled = True
            stepInfoItem['dataPoints'].value   = templateItem[0]
            stepInfoItem['stepSize'  ].enabled = True
            stepInfoItem['stepSize'  ].value   = templateItem[1]
            stepInfoItem['preset'    ].enabled = True
            stepInfoItem['preset'    ].value   = templateItem[2]
            stepInfoItem['maxTime'   ].enabled = scan_min_time.enabled
            stepInfoItem['maxTime'   ].value   = templateItem[3]
            
        for i in xrange(len(template) - 2, len(stepInfo)):
            stepInfoItem = stepInfo[i]
                        
            stepInfoItem['enabled'   ].value   = False
            stepInfoItem['dataPoints'].enabled = False
            stepInfoItem['stepSize'  ].enabled = False
            stepInfoItem['preset'    ].enabled = False
            stepInfoItem['maxTime'   ].enabled = False
            
    except:
        pass
    
def setScanMode():
    if scan_mode.value == 'time':
        scan_min_time.enabled = False
        for stepInfoItem in stepInfo:
            stepInfoItem['maxTime'].enabled = False
    else:
        scan_min_time.enabled = True
        for stepInfoItem in stepInfo:
            stepInfoItem['maxTime'].enabled = stepInfoItem['preset'].enabled

def setEnabled(index):
    stepItem = stepInfo[index]
    value = stepItem['enabled'].value
    stepItem['dataPoints'].enabled = value
    stepItem['stepSize'  ].enabled = value
    stepItem['preset'    ].enabled = value
    stepItem['maxTime'   ].enabled = value and scan_min_time.enabled
    
setTemplate()


def getScan():
    
    scan = { 'angles': [], 'presets': [], 'maxTimes': [], 'groups': [] }
    
    first = True
    angle_ref = scan_reference.value
    angle     = angle_ref
    logscale  = False # first data points are always on a linear scale
    
    for stepInfoItem in stepInfo:
        if stepInfoItem['enabled'].value :
            dataPoints = stepInfoItem['dataPoints'].value
            stepSize   = stepInfoItem['stepSize'  ].value
            preset     = stepInfoItem['preset'    ].value
            maxTime    = stepInfoItem['maxTime'   ].value
            
            if first:
                angle -= ((dataPoints-1)/2.0) * stepSize;
                
            elif len(scan['angles']) != 0:
                angle += stepSize
                
            scan['angles'  ].append(angle)
            scan['presets' ].append(preset)
            scan['maxTimes'].append(maxTime)
            
            scan['groups'].append(angle)
            for i in xrange(1, dataPoints):
                if logscale:
                    a0 = ln(angle - angle_ref - stepSize)
                    a1 = ln(angle - angle_ref           )                    
                    a2 = a1 + (a1 - a0);
                    
                    if not isnan(a2) and not isinf(a2):
                        stepSize = angle_ref + exp(a2) - angle
                    
                angle += stepSize

                scan['angles'  ].append(angle)
                scan['presets' ].append(preset)
                scan['maxTimes'].append(maxTime)

        first    = False
        logscale = bool(logscale_position.value)
        
    return scan

def switchCrystal():
    
    if confirm('Are you sure? That will take a long time!'):
        crystal = str(crystal_name.value)
        if 'Si111' in crystal:
            crystal_name.value = 'Si311 (2.37 Angstroms)'
        
        elif 'Si311' in crystal:    
            crystal_name.value = 'Si111 (4.74 Angstroms)'
            
        else:
            raise Exception('cannot access crystals')

def startScan(configModel):
    
    ''' setup '''
    
    scanVariable = configModel.scanVariable
    crystal      = configModel.crystal
    mode         = configModel.mode

    
    MainDeadTime    = 1.08E-6
    TransDeadTime   = 1.08E-6
        
    if 'Si111' in crystal:
        empLevel = 0.49
        bkgLevel = 0.48
        dOmega = 2.3E-6
        gDQv   = 0.0586
        gDQh   = 0
        
        wavelength       = 4.74
        TransmissionTube = 10
        TransBackground  = 73.6     # counts per second
    
    elif 'Si311' in crystal:
        empLevel = 0.34
        bkgLevel = 0.333
        dOmega = 4.6E-7
        gDQv   = 0.117
        gDQh   = 0
        
        wavelength       = 2.37
        TransmissionTube = 9
        TransBackground  = 171.4  # counts per second
        
    else:
        print 'selected crystal is invalid'
        return
    
    ''' angles '''
    
    scan = configModel.scan
    
    scan_angleMin = builtin_min(scan['angles'])
    scan_angleMax = builtin_max(scan['angles'])
    
    if ('m1om' in scanVariable) or ('m2om' in scanVariable):
        tolerance = 2
        
        approved = False
        if 'Si111' in crystal:
            if (180 - tolerance <= scan_angleMin) and (scan_angleMax <= 180 + tolerance):
                approved = True
        
        elif 'Si311' in crystal:    
            if (0 - tolerance <= scan_angleMin) and (scan_angleMax <= 0 + tolerance):
                approved = True
                
        if not approved:
            print 'angle out of range'
            return
        
    ''' execution '''
    
    sics.execute('hset user/name '  + configModel.user_name)
    sics.execute('hset user/email ' + configModel.user_email)
    
    sics.execute('hset sample/name '        + configModel.sample_name)
    sics.execute('hset sample/description ' + configModel.sample_description)
    sics.execute('hset sample/thickness %g' % configModel.sample_thickness)
    
    sics.execute('hset experiment/bkgLevel %g'  % bkgLevel)
    sics.execute('hset experiment/empLevel %g'  % empLevel)
    
    sics.execute('hset instrument/detector/MainDeadTime %g'     % MainDeadTime)
    sics.execute('hset instrument/detector/TransDeadTime %g'    % TransDeadTime)
    sics.execute('hset instrument/detector/TransBackground %g'  % TransBackground)
    sics.execute('hset instrument/detector/TransmissionTube %i' % TransmissionTube)
    
    sics.execute('hset instrument/crystal/dOmega %g'      % dOmega)
    sics.execute('hset instrument/crystal/gDQv %g'        % gDQv)
    sics.execute('hset instrument/crystal/gDQh %g'        % gDQh)
    sics.execute('hset instrument/crystal/wavelength %g'  % wavelength)
    sics.execute('hset instrument/crystal/scan_variable ' + scanVariable);
    
    # slits
    def getSlitValues(gap, offset, a0, b0, aOpen, bOpen):
        
        if gap == 'fully opened':
            return (aOpen, bOpen)
        
        if gap == 'fully closed':
            gap    = -5.0
            offset =  0.0
        
        a = a0 + 0.5 * float(gap) + float(offset)
        b = b0 - 0.5 * float(gap) + float(offset)

        return (a, b)
    
    ss1vg = configModel.ss1vg
    ss1vo = configModel.ss1vo
    ss1hg = configModel.ss1hg
    ss1ho = configModel.ss1ho
    
    ss2vg = configModel.ss2vg
    ss2vo = configModel.ss2vo
    ss2hg = configModel.ss2hg
    ss2ho = configModel.ss2ho

    (ss1u, ss1d) = getSlitValues(ss1vg, ss1vo, ss1u0, ss1d0, 35.8, -38.8)
    (ss1r, ss1l) = getSlitValues(ss1hg, ss1ho, ss1r0, ss1l0, 57.0, -58.0)
    
    (ss2u, ss2d) = getSlitValues(ss2vg, ss2vo, ss2u0, ss2d0, 37.0, -39.5)
    (ss2r, ss2l) = getSlitValues(ss2hg, ss2ho, ss2r0, ss2l0, 35.0, -35.0)
    
    # apply slits
    sics.execute('run ss1u %.2f' % ss1u)
    sics.execute('run ss1d %.2f' % ss1d)
    sics.execute('run ss1r %.2f' % ss1r)
    sics.execute('run ss1l %.2f' % ss1l)
    
    sics.execute('run ss2u %.2f' % ss2u)
    sics.execute('run ss2d %.2f' % ss2d)
    sics.execute('run ss2r %.2f' % ss2r)
    sics.execute('run ss2l %.2f' % ss2l)
    
    # load sample positions
    sam_positions = str(configModel.sam_position)
    
    if (len(sam_positions) == 0) or (sam_positions == 'fixed'):
        samz_list = [0.0]
    else:
        samz_list = []
        
        pos2samz = {}
        pos2samz[1] =  33.5
        pos2samz[2] = 178.5
        pos2samz[3] = 323.5
        pos2samz[4] = 468.5
        pos2samz[5] = 613.5

        for range in filter(None, sam_positions.split(',')):
            rangeItems = range.split('-')
            if ('' in rangeItems) or (len(rangeItems) < 1) or (len(rangeItems) > 2):
                raise Exception('format in "Sample Position" is incorrect')
            
            if len(rangeItems) == 1:
                samz_list.append(pos2samz[int(rangeItems[0])])
            else:
                for i in xrange(int(rangeItems[0]), int(rangeItems[1])+1):
                    samz_list.append(pos2samz[i])

        if len(samz_list) == 0:
            samz_list = [0.0]

    for samz in samz_list:
    
        sics.execute('histmem stop')
        time.sleep(3)
        sics.execute('histmem mode time')
    
        if samz != 0.0:
            print 'run samz %.2f' % samz
            sics.execute('run samz %.2f' % samz)
            # sics.execute('prun samz 2' % samz) !!!
            time.sleep(1)

        sics.execute('newfile HISTOGRAM_XYT')
        #sics.execute('autosave 60') # 60 seconds
        time.sleep(1)
        
        sicsController = sics.getSicsController()
        
        print 'frames:', len(scan['angles'])
        for frame_index in xrange(len(scan['angles'])):
            angle   = scan['angles'  ][frame_index]
            preset  = scan['presets' ][frame_index]
            maxTime = scan['maxTimes'][frame_index]
            
            print 'run %s %.6f' % (scanVariable, angle)
            sics.execute('run %s %.6f' % (scanVariable, angle))
            time.sleep(10)
            while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                time.sleep(0.1)
            print 'run done'
            
            time.sleep(1)
            print 'histmem start'
            while True:
                if mode == 'count_roi':
                    sics.execute('histmem preset %i' % maxTime)
                else:
                    sics.execute('histmem preset %i' % preset)
                    
                time.sleep(5)
                
                sics.execute('histmem start')
                time.sleep(5)
                
                if mode == 'count_roi':
                    print 'count_roi'
                    
                    time.sleep(configModel.min_time)
                    
                    count_roi = 0
                    while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                        try:
                            count_roi = int(sicsext.runCommand('hmm configure num_events_filled_to_count_roi'))
                            print count_roi
                            
                            if count_roi > preset:
                                print 'reached desired count_roi'
                                sics.execute('histmem pause')
                                time.sleep(1)
                                break
                        except:
                            pass
                            
                        time.sleep(0.5)
                        
                    break
                
                else:
                    while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                        time.sleep(0.1)
        
                    valid = False
                    for i in xrange(10):
                        time.sleep(1)
                        detector_time = sics.getValue('/instrument/detector/time').getFloatData()
                        
                        valid = (detector_time >= preset - 1) or (detector_time >= preset * 0.90)
                        if valid:
                            break
                        
                    print 'detector_time:', detector_time
                    
                    if valid:
                        break
                    else:
                        print 'scan was invalid and needs to be repeated'
                
            #sics.execute('histmem stop')
            sics.execute('save %i' % frame_index)
            frame_index += 1
            print 'histmem done'
            
        sics.execute('newfile clear')
        #sics.execute('autosave 0') # disable autosave
        
        # Get output filename
        filenameController = sicsController.findDeviceController('datafilename')
        savedFilename = filenameController.getValue().getStringData()
        print 'saved:', savedFilename
    
    print 'done'
    print
  
def btnPlotSteps_clicked():
    scan = getScan()
    print 'range [%g, %g]' % (scan['angles'][0], scan['angles'][-1])
    
    try:
        for mask in Plot1.masks:
            Plot1.remove_mask(mask)
    except:
        pass
    
    if Plot1.get_dataset() is None:
        scan_angleMin = builtin_min(scan['angles'])
        scan_angleMax = builtin_max(scan['angles'])
        
        dummy = zeros(2)
        dummy.axes[0] = [scan_angleMin, scan_angleMax]
        
        Plot1.add_dataset(dummy)
    
    inclusive = True
    angles = scan['angles']
    for i in xrange(1, len(angles)):
        xL = angles[i-1]
        xH = angles[i  ]
                
        Plot1.add_mask_1d(xL, xH, '', inclusive)
        inclusive = not inclusive
        
    groups = scan['groups']
    for i in xrange(len(groups)):
        Plot1.add_mask_1d(groups[i], groups[i]+1e-12, str(i+1), True)


def btnPlot_clicked():
    
    Plot1.clear()
    Plot2.clear()
        
    fns = []
    for sds in __DATASOURCE__.getSelectedDatasets():    
        fns.append(sds.getLocation())
        
    if len(fns) != 1:
        print 'select one dataset'
        return
        
    path = fns[0]
    basename = os.path.basename(str(path))
    basename = basename[:basename.find('.nx.hdf')]
    
    ds = df[str(path)]
    ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm')
    #ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm_xy')
    ds.__iDictionary__.addEntry('time', 'entry1/instrument/detector/time')
    ds.__iDictionary__.addEntry('m1om', 'entry1/instrument/crystal/m1om')
    ds.__iDictionary__.addEntry('m1chi', 'entry1/instrument/crystal/m1chi')
    ds.__iDictionary__.addEntry('m1x', 'entry1/instrument/crystal/m1x')
    ds.__iDictionary__.addEntry('m2om', 'entry1/instrument/crystal/m2om')
    ds.__iDictionary__.addEntry('m2chi', 'entry1/instrument/crystal/m2chi')
    ds.__iDictionary__.addEntry('m2x', 'entry1/instrument/crystal/m2x')
    ds.__iDictionary__.addEntry('m2y', 'entry1/instrument/crystal/m2y')
    ds.__iDictionary__.addEntry('mdet', 'entry1/instrument/crystal/mdet')
    ds.__iDictionary__.addEntry('pmom', 'entry1/instrument/crystal/pmom')
    ds.__iDictionary__.addEntry('pmchi', 'entry1/instrument/crystal/pmchi')
    ds.__iDictionary__.addEntry('ss1u', 'entry1/instrument/slits/ss1u')
    ds.__iDictionary__.addEntry('ss1d', 'entry1/instrument/slits/ss1d')
    ds.__iDictionary__.addEntry('ss1r', 'entry1/instrument/slits/ss1r')
    ds.__iDictionary__.addEntry('ss1l', 'entry1/instrument/slits/ss1l')
    ds.__iDictionary__.addEntry('ss2u', 'entry1/instrument/slits/ss2u')
    ds.__iDictionary__.addEntry('ss2d', 'entry1/instrument/slits/ss2d')
    ds.__iDictionary__.addEntry('ss2r', 'entry1/instrument/slits/ss2r')
    ds.__iDictionary__.addEntry('ss2l', 'entry1/instrument/slits/ss2l')
    ds.__iDictionary__.addEntry('ss1vo', 'entry1/instrument/slits/ss1vo')
    ds.__iDictionary__.addEntry('ss1vg', 'entry1/instrument/slits/ss1vg')
    ds.__iDictionary__.addEntry('ss1ho', 'entry1/instrument/slits/ss1ho')
    ds.__iDictionary__.addEntry('ss1hg', 'entry1/instrument/slits/ss1hg')
    ds.__iDictionary__.addEntry('ss2vo', 'entry1/instrument/slits/ss2vo')
    ds.__iDictionary__.addEntry('ss2vg', 'entry1/instrument/slits/ss2vg')
    ds.__iDictionary__.addEntry('ss2ho', 'entry1/instrument/slits/ss2ho')
    ds.__iDictionary__.addEntry('ss2hg', 'entry1/instrument/slits/ss2hg')
        
    scanVariable = str(scan_variable_plot.value)
    scanVariable = scanVariable[:scanVariable.find(' ')]
    scanVariable = ds[scanVariable]
    
    sorting = scan_variable_sorting.value
    if sorting:
        info = sorted(enumerate(scanVariable), key=lambda item:item[1])
        scanVariable = [item[1] for item in info]
    
    shape = ds.shape
    if shape[0] <= 1:
        print 'Must have at least 2 scan positions'
        return
     
    n = shape[0]
    
    # tubes
    data = zeros(n)
    
    tids = []
    if combine_tube0.value:
        tids.append(0)
    if combine_tube1.value:
        tids.append(1)
    if combine_tube2.value:
        tids.append(2)
    if combine_tube3.value:
        tids.append(3)
    if combine_tube4.value:
        tids.append(4)
    if combine_tube6.value:
        tids.append(6)
        
    Plot1.clear()    
    if str(combine_mode.value) == 'individual':
        for tid in tids:
            if ds.hmm.ndim == 4:
                data[:] = ds.hmm[:, 0, :, tid].sum(0) # hmm
            else:
                data[:] = ds.hmm[:, :, tid].sum(0)  # hmm_xy
            
            if data.size == 1:
                data[0] = data[0] * 1.0 / ds.time
            else:
                data[:] = data[:] * 1.0 / ds.time
                if sorting:
                    data[:] = [data[item[0]] for item in info] # sorting
                
            data.var[:] = 0 # total_counts / (ds.time * ds.time)

            axis0 = data.axes[0]
            axis0[:] = scanVariable[:]
                        
            dataF = data.float_copy()
            dataF.title = 'Tube %i' % tid
            
            Plot1.add_dataset(dataF)
        
        Plot1.title = 'Count Rate (individual)'
            
    else:
        for tid in tids:
            if ds.hmm.ndim == 4:
                data[:] += ds.hmm[:, 0, :, tid].sum(0) # hmm
            else:
                data[:] += ds.hmm[:, :, tid].sum(0)  # hmm_xy
            
        if data.size == 1:
            data[0] = data[0] * 1.0 / ds.time
        else:
            data[:] = data[:] * 1.0 / ds.time
            if sorting:
                data[:] = [data[item[0]] for item in info] # sorting
            
        data.var[:] = 0 # total_counts / (ds.time * ds.time)
        
        axis0    = data.axes[0]
        axis0[:] = scanVariable[:]
        
        data.title ='Tubes ' + str(tids)
        
        Plot1.set_dataset(data)
        Plot1.title   = 'Count Rate (combined)'

    Plot1.title = Plot1.title + ' ' + basename
    
    if Plot1.ds is not None:
        Plot1.x_label = str(scan_variable_plot.value)
        Plot1.y_label = 'counts per sec'
    
    # transmission
    data = zeros(n)
    
    tids = []
    if check_tube9.value:
        tids.append(9)
    if check_tube10.value:
        tids.append(10)
        
    Plot2.clear()
    for tid in tids:
        if ds.hmm.ndim == 4:
            data[:] = ds.hmm[:, 0, :, tid].sum(0) # hmm
        else:
            data[:] = ds.hmm[:, :, tid].sum(0)  # hmm_xy
        
        if data.size == 1:
            data[0] = data[0] * 1.0 / ds.time
        else:
            data[:] = data[:] * 1.0 / ds.time
            if sorting:
                data[:] = [data[item[0]] for item in info] # sorting
            
        data.var[:] = 0 # total_counts / (ds.time * ds.time)

        axis0 = data.axes[0]
        axis0[:] = scanVariable[:]
                    
        dataF = data.float_copy()
        if tid == 9:
            dataF.title = 'Tube %i: Si (311)' % tid
        elif tid == 10:
            dataF.title = 'Tube %i: Si (111)' % tid
        else:
            dataF.title = 'Tube %i' % tid
        
        Plot2.add_dataset(dataF)
        Plot2.title   = 'Count Rate (individual) ' + basename
        
    if Plot2.ds is not None:
        Plot2.x_label = str(scan_variable_plot.value)
        Plot2.y_label = 'counts per sec'
        
    return True

def export_clicked():
    
    if not btnPlot_clicked():
        return
    
    path     = str(__DATASOURCE__.getSelectedDatasets()[0].getLocation())
    basename = os.path.basename(path)
    basename = basename[:basename.find('.nx.hdf')]

    p1 = (Plot1.ds is not None) and (len(Plot1.ds) >= 1)
    p2 = (Plot2.ds is not None) and (len(Plot2.ds) >= 1)

    if p1 or p2:
        f = open(__EXPORT_PATH__ + '/KKB%07d.csv' % df[path].id, 'w+')
        
        variable     = str(scan_variable_plot.value)
        variableName = variable[:variable.find(' ')]
        variableUnit = variable[(2+len(variableName)):-1]
        
        f.write(variableName)
        columns = 0
        
        dsRef = None
        
        if p1:
            dsRef = Plot1.ds[0]
            dsRefAngle = dsRef.axes[0]
            
            for ds in Plot1.ds:
                if len(ds) == len(dsRef): # to ignore Gauss fit
                    f.write(', %s_%s' % (basename, str(ds.title).replace(',', ';').replace(' ','')))
                    columns += 1

        if p2:
            if dsRef is None:
                dsRef = Plot2.ds[0]
                dsRefAngle = dsRef.axes[0]

            for ds in Plot2.ds:
                title = str(ds.title)
                
                f.write(',  %s_%s' % (basename, title[:title.find(':')].replace(' ','')))
                columns += 1
            
        f.write('\n')
        f.write(variableUnit)
        for i in xrange(columns):
            f.write(',c/s')
        f.write('\n')
        
        for i in xrange(len(dsRef)):
            f.write('%.7f' % dsRefAngle[i])
            if p1:
                for ds in Plot1.ds:
                    if len(ds) == len(dsRef): # to ignore Gauss fit
                        f.write(', %.5f' % ds[i])
            if p2:
                for ds in Plot2.ds:
                    f.write(', %.5f' % ds[i])
            f.write('\n')

        f.close()
        print 'finished output ' + f.name

def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
        
    print 'please press "Start Scan" in scan box'

def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()


## model

class ConfigurationModel:
    def __init__(self):
        self.scanVariable = str(scan_variable.value)
        self.scanVariable = self.scanVariable[:self.scanVariable.find(' ')]
        
        self.crystal      = str(crystal_name.value)
        self.mode         = str(scan_mode.value)
        
        self.scan = getScan()
        self.scan_reference = scan_reference.value
        
        self.logscale = logscale_position.value
        self.stepInfo = []
        for step in stepInfo:
            d = dict()
            for key in step.keys():
                d[key] = step[key].value
            self.stepInfo.append(d);

        self.user_name  = str(user_name.value)
        self.user_email = str(user_email.value)
        
        self.sample_name        = str(sample_name.value)
        self.sample_description = str(sample_description.value)
        self.sample_thickness   = float(sample_thickness.value)
        
        # vertical/horizontal pre-slit
        self.ss1vg = float(pss_ss1vg.value)
        self.ss1vo = float(pss_ss1vo.value)
        self.ss1hg = float(pss_ss1hg.value)
        self.ss1ho = float(pss_ss1ho.value)
        # vertical/horizontal post-slit
        self.ss2vg = float(pss_ss2vg.value)
        self.ss2vo = float(pss_ss2vo.value)
        self.ss2hg = float(pss_ss2hg.value)
        self.ss2ho = float(pss_ss2ho.value)
        
        # load sample positions
        self.sam_position = str(scan_sam_position.value)
        self.min_time     = int(scan_min_time.value)
        
    def apply(self):
        for option in scan_variable.options:
            if self.scanVariable == option[:option.find(' ')]:
                scan_variable.value = option

        crystal_name.value  = self.crystal
        scan_mode.value     = self.mode

        logscale_position.value = self.logscale 
        scan_reference.value    = self.scan_reference
        i = 0
        for step in self.stepInfo:
            for key in step.keys():
                stepInfo[i][key].value = step[key]
            setEnabled(i)
            i += 1
            
        setScanMode()

        user_name.value  = self.user_name
        user_email.value = self.user_email
        
        sample_name.value        = self.sample_name
        sample_description.value = self.sample_description
        sample_thickness.value   = self.sample_thickness
        
        # vertical/horizontal pre-slit
        pss_ss1vg.value = self.ss1vg
        pss_ss1vo.value = self.ss1vo
        pss_ss1hg.value = self.ss1hg
        pss_ss1ho.value = self.ss1ho
        # vertical/horizontal post-slit
        pss_ss2vg.value = self.ss2vg
        pss_ss2vo.value = self.ss2vo
        pss_ss2hg.value = self.ss2hg
        pss_ss2ho.value = self.ss2ho
        
        # load sample positions
        scan_sam_position.value = self.sam_position
        scan_min_time.value     = self.min_time
