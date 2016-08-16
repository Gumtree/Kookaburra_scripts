
__script__.title = 'KKB Measurement Script'
__script__.version = '1.0'

from gumpy.commons import sics
from org.gumtree.gumnix.sics.control import ServerStatus
from pickle import Pickler, Unpickler
import time

from math import log as ln
from math import exp, isnan, isinf, sin

from __builtin__ import max as builtin_max
from __builtin__ import min as builtin_min
from org.eclipse.swt.widgets import FileDialog
from org.eclipse.swt import SWT
from org.eclipse.swt.widgets import Display
from java.io import File
import time

SINGLE_TYPE = SWT.SINGLE
SAVE_TYPE = SWT.SAVE
MULTI_TYPE = SWT.MULTI

class __Display_Runnable__(Runnable):
    def __init__(self, type=SINGLE_TYPE, ext=['*.*']):
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
         
def open_file_dialog(type=SWT.SINGLE, ext=['*.*']):
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

# # templates

reference_templates_dict = {}
reference_templates_dict['Si111'] = 180.326
reference_templates_dict['Si311'] = 0.057

steps_templates_list = []

# steps_templates['Background'] = [
#    'time', 'logscale',
#    [20, 6.0e-5,  1200, 1200]]

# steps_templates['----------'] = [
#    'time', 'logscale',
#    [0, 0,  0, 0]]

steps_templates_list.append([
    'Si111: Logarithmic Overview Scan',
    'time',
    'logscale',
    [17, 1.20e-4, 1, 1200],
    [30, 2.0e-4, 20, 1200]])

steps_templates_list.append([
    'Si111: Logarithmic Scan (few features)',
    'ba',
    'logscale',
    [33, 6.0e-5, 1000, 1200],
    [33, 2.0e-4, 1000, 1200]])

steps_templates_list.append([
    'Si111: Logarithmic Scan (fine features)',
    'ba',
    'logscale',
    [33, 6.0e-5, 1000, 1200],
    [73, 8.0e-5, 1000, 1200]])

steps_templates_list.append([
    'Si111: Kinetic Scan 8 points',
    'time',
    'logscale',
    [ 0, 6.0e-5, 1, 1200],
    [1, 3.0e-3, 180, 1200],
    [7, 3.0e-3, 180, 1200]])

steps_templates_list.append([
    'Si111: Kinetic Scan 4 points',
    'time',
    'logscale',
    [ 0, 6.0e-5, 1, 1200],
    [1, 5.0e-3, 180, 1200],
    [3, 1.5e-2, 180, 1200]])

steps_templates_list.append([
    '----------',
    'time',
    'logscale',
    [0, 0, 0, 0]])

steps_templates_list.append([
    'Si311: Logarithmic Overview Scan',
    'time',
    'logscale',
    [17, 2.0e-5, 1, 1200],
    [30, 3.7e-5, 20, 1200]])

steps_templates_list.append([
    'Si311: Logarithmic Scan (few features, broadened peak)',
    'ba',
    'logscale',
    [80, 2e-5, 1000, 1200],
    [29, 1e-4, 1000, 1200]])

steps_templates_list.append([
    'Si311: Logarithmic Scan (fine features)',
    'ba',
    'logscale',
    [31, 2e-5, 1000, 1200],
    [60, 2.5e-5, 1000, 1200]])


# # export path

__EXPORT_PATH__ = 'V:/shared/KKB Logbook/Temp Plot Data Repository/'

if not os.path.exists(__EXPORT_PATH__):
    os.makedirs(__EXPORT_PATH__)
    
# # User Details

user_name = Par('string', 'Christine', options=['Christine', 'Lela'])
user_name.title = 'Name'

user_email = Par('string', 'cre@ansto.gov.au', options=['cre@ansto.gov.au', 'liliana.decampo@ansto.gov.au'])
user_email.title = 'EMail'

g0 = Group('User Details')
g0.numColumns = 2
g0.add(user_name, user_email)

# # Sample Details

sample_name = Par('string', 'UNKNOWN', options=['Empty Cell', 'Empty Beam'], command="sample_thickness.enabled = sample_name.value not in ['Empty Cell', 'Empty Beam']")
sample_name.title = 'Name'

sample_description = Par('string', 'UNKNOWN')
sample_description.title = 'Description'

sample_thickness = Par('string', '1', options=['0.01', '0.1', '1.0', '10.0'])
sample_thickness.title = 'Thickness (mm)'


g0 = Group('Sample  Details')
g0.numColumns = 2
g0.add(sample_name, sample_thickness, sample_description)


# Group('Sample Details').add(sample_name, sample_description, sample_thickness)


# # Crystal
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

    
g0 = Group('Crystal Info')
g0.numColumns = 2
g0.add(crystal_name)

# CRYSTAL END #############################################





# SLIT 1  ####################################################################### 

def updateOffset(gapBox, offsetBox):
    offsetBox.enabled = 'fully' not in gapBox.value
    
def getSlitGapAndOffset(aPath, a0, bPath, b0):
    try:
        a = sics.getValue(aPath).getFloatData()
        b = sics.getValue(bPath).getFloatData()
            
        gap = (a - a0 - (b - b0)) / 1.0
        offset = (a - a0 + (b - b0)) / 2.0
        
        return (gap, offset)
    except:
        return (float('nan'), float('nan'))

crystal = str(crystal_name.value)
if 'Si111' in crystal:
    ss1r0 = 28.35
    ss1l0 = 27.75

elif 'Si311' in crystal:
    ss1r0 = -9.16
    ss1l0 = -9.76
    
else:
    ss1r0 = float('nan')
    ss1l0 = float('nan')
    
ss1u0 = -8.04
ss1d0 = -7.30




(ss1vg, ss1vo) = getSlitGapAndOffset('/instrument/slits/ss1u', ss1u0, '/instrument/slits/ss1d', ss1d0)
(ss1hg, ss1ho) = getSlitGapAndOffset('/instrument/slits/ss1r', ss1r0, '/instrument/slits/ss1l', ss1l0)

pss_ss1vg = Par('string', '%.1f' % ss1vg, options=['fully closed', '5', '10', '15', '20', '25', '30', '40', '50', 'fully opened'], command='updateOffset(pss_ss1vg, pss_ss1vo)')
pss_ss1vg.title = 'Vertical Gap (mm)'
# pss_ss1vg.colspan = 50

pss_ss1vo = Par('float', ss1vo)
pss_ss1vo.title = 'Vertical Offset (mm)'
# pss_ss1vo.colspan = 50

pss_ss1hg = Par('string', '%.1f' % ss1hg, options=['fully closed', '5', '10', '15', '20', '25', '30', '40', '50', 'fully opened'], command='updateOffset(pss_ss1hg, pss_ss1ho)')
pss_ss1hg.title = 'Horizontal Gap (mm)'
# pss_ss1hg.colspan = 50

pss_ss1ho = Par('float', ss1ho)
pss_ss1ho.title = 'Horizontal Offset (mm)'
# pss_ss1ho.colspan = 50

g0 = Group('Sample Slit Settings')
g0.numColumns = 2
g0.add(pss_ss1vg, pss_ss1vo, pss_ss1hg, pss_ss1ho)

# SLIT 1 END #######################################################################




## Scan parameters ##########################################################################################################

scan_variable = Par('string', 'm2om [deg]', options=[
    'pmom [deg]', 'pmchi [deg]', 'm1om [deg]', 'm1chi [deg]', 'm1x [mm]', 'm2om [deg]', 'm2chi [deg]', 'm2x [mm]', 'm2y [mm]', 'mdet [mm]',
    'ss1u [mm]', 'ss1d [mm]', 'ss1l [mm]', 'ss1r [mm]',
    'ss2u [mm]', 'ss2d [mm]', 'ss2l [mm]', 'ss2r [mm]',
    'ss1vg [mm]', 'ss1vo [mm]', 'ss1hg [mm]', 'ss1ho [mm]',
    'ss2vg [mm]', 'ss2vo [mm]', 'ss2hg [mm]', 'ss2ho [mm]'], command="scan_variable_plot.value = scan_variable.value")


scan_variable.title = 'Scan Variable'
scan_variable.colspan = 33

scan_reference = Par('float', '0.0')
scan_reference.title = 'Zero Angle'
scan_reference.colspan = 33

for key in reference_templates_dict.keys():
    if key in crystal_name.value:
        scan_reference.value = reference_templates_dict[key]

scan_mode = Par('string', 'ba', options=['ba', 'time'], command='setScanMode()')
scan_mode.title = 'Acquisition Mode'
scan_mode.colspan = 33

scan_min_time = Par('int', '5')
scan_min_time.title = 'Min Time (sec)'
scan_min_time.colspan = 33



scan_sam_position = Par('string', 'fixed', options=['fixed', '-----', '1', '2', '3', '4', '5', '-----', '1-16', '2-16', '3-16', '4-16', '5-16', '6-16', '7-16', '8-16', '9-16', '10-16', '11-16', '12-16', '13-16', '14-16', '15-16', '16-16', '-----', '1 top', '1 bottom', '2 top', '2 bottom', '3 top', '3 bottom', '4 top', '4 bottom', '5 top', '5 bottom', ])
scan_sam_position.title = 'Sample Position'
scan_sam_position.colspan = 33

logscale_position = Par('bool', True)
logscale_position.title = 'Logarithmic Steps'
logscale_position.colspan = 33

negative_steps = Par('bool', False)
negative_steps.title = 'Negative Steps'
negative_steps.colspan = 33

steps_label = Par('label', 'Please choose scan template or adjust steps manually:  ')
steps_label.colspan = 200

steps_templates = Par('string', '', options=[item[0] for item in steps_templates_list], command='setTemplate()')
steps_templates.title = 'Scan Template'
steps_templates.colspan = 100

# steps_space = Par('space', '')
# steps_space.colspan = 10



g0 = Group('Scan Parameters')
g0.numColumns = 100  # 9
g0.add(scan_variable, scan_mode, scan_reference, logscale_position, scan_min_time, scan_sam_position, negative_steps, steps_label, steps_templates)


stepInfo = []

for i in xrange(4):
    steps_e = Par('bool', True, command='setEnabled(%i)' % i)
    steps_e.title = '(%i)' % (i + 1)
    steps_e.colspan = 10
    steps_m = Par('int', 0, command='clearScanTemplateSelection()')
    steps_m.title = 'Number of steps'
    steps_m.colspan = 20
    steps_s = Par('float', 0, command='clearScanTemplateSelection()')
    steps_s.title = 'Step Size [deg]'
    steps_s.colspan = 20
    steps_p = Par('int', 0, command='clearScanTemplateSelection()')
    steps_p.title = 'Mode Preset'
    steps_p.colspan = 25
    steps_t = Par('int', 1200, command='clearScanTemplateSelection()')
    steps_t.title = 'Max Time'
    steps_t.colspan = 25
    
    stepInfo.append({'enabled': steps_e, 'dataPoints':steps_m, 'stepSize':steps_s, 'preset':steps_p, 'maxTime':steps_t})
    g0.add(steps_e, steps_m, steps_s, steps_p, steps_t)
    
def clearScanTemplateSelection():
    steps_templates.value = None

btnPlotSteps = Act('btnPlotSteps_clicked()', 'Plot Measurement Steps')  # 'compare measurement steps with previous scan')
btnPlotSteps.colspan = 50

cnfg_save_btn = Act('saveConfiguration()', 'Save Single Scan Parameters')
cnfg_save_btn.colspan = 50

btnTimeEstimation = Act('runTimeEstimation()', 'Time Estimation with selected Data Set')
btnTimeEstimation.colspan = 50

txtTimeEstimation = Par('int', '0')
txtTimeEstimation.title = 'Time Estimation (min)'
txtTimeEstimation.enabled = False
txtTimeEstimation.colspan = 50

g0.add(btnPlotSteps, cnfg_save_btn, btnTimeEstimation, txtTimeEstimation)

def runTimeEstimation():
    
    if str(scan_mode.value) == 'time':
        scan = getScan()
        times = scan['presets']
        txtTimeEstimation.value = int((sum(times) + len(times) * 25) / 60.0) # 25 seconds for each move
        return

    fns = []
    for sds in __DATASOURCE__.getSelectedDatasets():    
        fns.append(sds.getLocation())
        
    if len(fns) != 1:
        print 'select one dataset'
        return
        
    ds = openDataset(fns[0])

    scanVariable = str(scan_variable.value)
    scanVariable = scanVariable[:scanVariable.find(' ')]
    scanVariable = ds[scanVariable]
    
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

    for tid in tids:
        if ds.hmm.ndim == 4:
            data[:] += ds.hmm[:, 0, :, tid].sum(0)  # hmm
        else:
            data[:] += ds.hmm[:, :, tid].sum(0)  # hmm_xy
        
    if data.size == 1:
        data[0] = data[0] * 1.0 / ds.time
    else:
        data[:] = data[:] * 1.0 / ds.time
        data[:] = [data[item[0]] for item in info]  # sorting
        
    # angle and count rate
    a0 = [float(angle) for angle in scanVariable]
    r0 = [float(rate) for rate in data[:]]
    
    # angle, counts, max time and min time
    model = ConfigurationModel()
    scan = model.scan
    tMin = model.min_time
    
    a1 = scan['angles']
    c1 = scan['presets']
    t1 = scan['maxTimes']
    
    total = 0.0
    for i in xrange(len(a1)):
        try:
            rate = sample(a0, r0, a1[i])
            time = c1[i] / rate
            
            if time < tMin:
                total += tMin
            elif time > t1[i]:
                total += t1[i]
            else:
                total += time
            
        except ValueError as e:
            if e.message == "OutOfRange":
                total += t1[i] # add max time
            else:
                raise
    
    txtTimeEstimation.value = int(total / 60.0)

def sample(x0, y0, x1):
    from __builtin__ import max, min
    
    if len(x0) != len(y0):
        raise Exception("len(x0) != len(y0)")

    x0_min = min(x0)
    x0_max = max(x0)

    if len(x0) < 2:
        raise Exception("len(x0) < 2")
    if x0_min >= x0_max:
        raise Exception("x0_min >= x0_max")
    
    if x1 < x0_min:
        raise ValueError("OutOfRange")
    if x0_max < x1:
        raise ValueError("OutOfRange")

    i0 = 0
    i1 = 1
    x0i0 = x0[i0]
    y0i0 = y0[i0]
    x0i1 = x0[i1]
    y0i1 = y0[i1]
    
    # in case first x values are equal
    while x0i0 == x0i1:
        i1 += 1
        x0i1 = x0[i1]
        y0i1 = y0[i1]

    # not iterable
    while x0i1 < x1:
        x0i0 = x0i1
        y0i0 = y0i1

        i1 += 1
        
        x0i1 = x0[i1]
        y0i1 = y0[i1]

    return y0i0 + (x1 - x0i0) * (y0i1 - y0i0) / (x0i1 - x0i0)

## Scan parameters END #########################################################################

## RUN ##############################################

cnfg_load_btn = Act('loadConfigurations()', 'Load Multiple Scan Parameters')

cnfg_lookup = dict()
cnfg_options = Par('string', '', options=[''], command="applyConfiguration()")
cnfg_options.title = 'Read'

start_scan = Act('startScan(ConfigurationModel())', '#############   Run Single Scan   #############')
cnfg_run_btn = Act('runConfigurations()', '#############   Run Multiple Scans   #############')

g0 = Group('Execute Scans')
g0.numColumns = 1
g0.add(start_scan, cnfg_load_btn, cnfg_options, cnfg_run_btn)

## Save/Load Configuration END############################################################################


def saveConfiguration():    
    file = open_file_dialog(type=SAVE_TYPE, ext=['*.kkb'])
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
        
        print 'saved'
        
    finally:
        fh.close()
    
def loadConfigurations():
    fileList = open_file_dialog(type=MULTI_TYPE, ext=['*.kkb'])
    if not fileList:
        return

    finalDict = dict()
    finalNames = []

    for path in fileList:
        fh = open(path, 'r')
        try:
            p = Unpickler(fh)
            if p.load() != 'KKB':
                print 'ERROR:', os.path.basename(path)
            else:
                model = ConfigurationModel()
                
                # set defaults
                model.negative = False  # old models may not have this attribute
                
                for att in dir(model):
                    att_value = getattr(model, att)
                    if (att.find('_') != 0) and ('instancemethod' not in str(type(att_value))):
                        if p.load() != att:
                            print 'FORMAT ERROR:', os.path.basename(path)
                            break
                            
                        setattr(model, att, p.load())
                else:
                    name = os.path.basename(path)
                    finalDict[name] = path
                    finalNames.append(name)
                    
        finally:
            fh.close()
            
    cnfg_lookup.clear()
    cnfg_lookup.update(finalDict)
    
    cnfg_options.options = finalNames
    time.sleep(0.5)
    cnfg_options.value = finalNames[0] if finalNames else ''
    
            
def applyConfiguration():
    file = str(cnfg_options.value)
    if not file:
        return

    fh = open(cnfg_lookup[file], 'r')
    try:
        p = Unpickler(fh)
        if p.load() != 'KKB':
            print 'ERROR:', file
        else:
            model = ConfigurationModel()
            for att in dir(model):
                att_value = getattr(model, att)
                if (att.find('_') != 0) and ('instancemethod' not in str(type(att_value))):
                    if p.load() != att:
                        print 'FORMAT ERROR:', file
                        break
                        
                    setattr(model, att, p.load())
            else:
                # print 'read:', file
                model.apply()
    finally:
        fh.close()

def runConfigurations():    
    for file in cnfg_options.options:
        fh = open(cnfg_lookup[file], 'r')
        try:
            p = Unpickler(fh)
            if p.load() != 'KKB':
                print 'ERROR:', file
            else:
                model = ConfigurationModel()
                for att in dir(model):
                    att_value = getattr(model, att)
                    if (att.find('_') != 0) and ('instancemethod' not in str(type(att_value))):
                        if p.load() != att:
                            print 'FORMAT ERROR:', file
                            break
                            
                        setattr(model, att, p.load())
                else:
                    print 'run:', file
                    startScan(model)
        finally:
            fh.close()


# # Plot
tubes_label = Par('label', 'Main Detector:')
tubes_label.colspan = 1

combine_tube0 = Par('bool', True)
combine_tube0.title = ' Tube 0'
combine_tube0.colspan = 1

combine_tube1 = Par('bool', True)
combine_tube1.title = '   Tube 1'
combine_tube1.colspan = 1

combine_tube2 = Par('bool', True)
combine_tube2.title = '   Tube 2'
combine_tube2.colspan = 1

combine_tube3 = Par('bool', True)
combine_tube3.title = '   Tube 3'
combine_tube3.colspan = 1

combine_tube4 = Par('bool', True)
combine_tube4.title = '   Tube 4'
combine_tube4.colspan = 1

combine_tube6 = Par('bool', False)
combine_tube6.title = '   Tube 6'
combine_tube6.colspan = 1



combine_mode = Par('string', 'combined', options=['individual', 'combined'])
combine_mode.title = '  Mode'
combine_mode.colspan = 1





trans_tube_label = Par('label', 'Trans Detector: ')
trans_tube_label.colspan = 2

check_tube9 = Par('bool', True)
check_tube9.title = ' Tube 9: Si (311)'
check_tube9.colspan = 2

check_tube10 = Par('bool', False)
check_tube10.title = '   Tube 10: Si (111)'
check_tube10.colspan = 2

# steps_space = Par('space', '')
# steps_space.colspan = 12

scan_variable_plot = Par('string', 'm2om [deg]', options=[
    'pmom [deg]', 'pmchi [deg]', 'm1om [deg]', 'm1chi [deg]', 'm1x [mm]', 'm2om [deg]', 'm2chi [deg]', 'm2x [mm]', 'm2y [mm]', 'mdet [mm]',
    'ss1u [mm]', 'ss1d [mm]', 'ss1l [mm]', 'ss1r [mm]',
    'ss2u [mm]', 'ss2d [mm]', 'ss2l [mm]', 'ss2r [mm]',
    'ss1vg [mm]', 'ss1vo [mm]', 'ss1hg [mm]', 'ss1ho [mm]',
    'ss2vg [mm]', 'ss2vo [mm]', 'ss2hg [mm]', 'ss2ho [mm]'])

scan_variable_plot.title = 'Scan Variable'
scan_variable_plot.colspan = 1

scan_variable_sorting = Par('bool', True)
scan_variable_sorting.title = 'Sorting'
scan_variable_sorting.colspan = 1

btnPlot = Act('btnPlot_clicked()', 'Plot Selected Data Set')
btnPlot.colspan = 8

g0 = Group('Plotting')
g0.numColumns = 7
g0.add(tubes_label, combine_tube0, combine_tube1, combine_tube2, combine_tube3, combine_tube4, combine_tube6, combine_mode, trans_tube_label, check_tube9, check_tube10, scan_variable_plot, scan_variable_sorting, btnPlot)





# export to csv

# btnExport  = Act('export_clicked()', 'Export to CSV')


################################# SLIT 2 ##########################################################
ss2u0 = 0  # 2.00
ss2d0 = 0  # 1.40
ss2l0 = 0  # 5 0.50
ss2r0 = 0  # -2 -1.00

(ss2vg, ss2vo) = getSlitGapAndOffset('/instrument/slits/ss2u', ss2u0, '/instrument/slits/ss2d', ss2d0)
(ss2hg, ss2ho) = getSlitGapAndOffset('/instrument/slits/ss2r', ss2r0, '/instrument/slits/ss2l', ss2l0)

pss_ss2vg = Par('string', '%.1f' % ss2vg, options=pss_ss1vg.options, command='updateOffset(pss_ss2vg, pss_ss2vo)')
pss_ss2vg.title = 'Vertical Opening (mm)'

pss_ss2vo = Par('float', ss2vo)
pss_ss2vo.title = 'Vertical Offset (mm)'

pss_ss2hg = Par('string', '%.1f' % ss2hg, options=pss_ss1hg.options, command='updateOffset(pss_ss2hg, pss_ss2ho)')
pss_ss2hg.title = 'Horizontal Opening (mm)'

pss_ss2ho = Par('float', ss2ho)
pss_ss2ho.title = 'Horizontal Offset (mm)'

g0 = Group('Post-Sample Slit')
g0.numColumns = 2
g0.add(pss_ss2vg, pss_ss2vo, pss_ss2hg, pss_ss2ho)
################################# SLIT 2 END ##########################################################




def setTemplate():
    try:
        matches = [item for item in steps_templates_list if item[0] == steps_templates.value]
        if len(matches) != 1:
            steps_templates.value = None
            return
        
        template = matches[0]
        
        # ignore '----'
        if template[0][0] == '-':
            steps_templates.value = None
            return
        
        scan_mode.value = template[1]
        if template[2] == 'logscale':
            logscale_position.value = True
        elif template[2] == 'linear':
            logscale_position.value = False
            
        # by default templates measure in positive direction
        negative_steps.value = False

        setScanMode()
        
        headers = 3
        for i in xrange(len(template) - headers):
            templateItem = template[i + headers]
            stepInfoItem = stepInfo[i]
            
            stepInfoItem['enabled'   ].value = True
            stepInfoItem['dataPoints'].enabled = True
            stepInfoItem['dataPoints'].value = templateItem[0]
            stepInfoItem['stepSize'  ].enabled = True
            stepInfoItem['stepSize'  ].value = templateItem[1]
            stepInfoItem['preset'    ].enabled = True
            stepInfoItem['preset'    ].value = templateItem[2]
            stepInfoItem['maxTime'   ].enabled = scan_min_time.enabled
            stepInfoItem['maxTime'   ].value = templateItem[3]
            
        for i in xrange(len(template) - headers, len(stepInfo)):
            stepInfoItem = stepInfo[i]
                        
            stepInfoItem['enabled'   ].value = False
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
            stepInfoItem['maxTime'].enabled = stepInfoItem['enabled'].value

def setEnabled(index):
    steps_templates.value = None
    
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
    angle = angle_ref
    logscale = False  # first data points are always on a linear scale
    
    negative = bool(negative_steps.value)
    
    for stepInfoItem in stepInfo:
        if stepInfoItem['enabled'].value:
            dataPoints = stepInfoItem['dataPoints'].value
            stepSize = stepInfoItem['stepSize'  ].value
            preset = stepInfoItem['preset'    ].value
            maxTime = stepInfoItem['maxTime'   ].value
            
            if (dataPoints > 0) and (stepSize <= 0.0):
                raise Exception('step sizes have to be positive')
            
            if first:
                angle -= ((dataPoints - 1) / 2.0) * stepSize;
                
            elif len(scan['angles']) != 0:
                angle += stepSize
                
            scan['angles'  ].append(angle)
            scan['presets' ].append(preset)
            scan['maxTimes'].append(maxTime)
            
            scan['groups'].append(angle)
            for i in xrange(1, dataPoints):
                if logscale:
                    a0 = ln(angle - angle_ref - stepSize)
                    a1 = ln(angle - angle_ref)                    
                    a2 = a1 + (a1 - a0);
                    
                    if not isnan(a2) and not isinf(a2):
                        stepSize = angle_ref + exp(a2) - angle
                    
                angle += stepSize

                scan['angles'  ].append(angle)
                scan['presets' ].append(preset)
                scan['maxTimes'].append(maxTime)

        first = False
        logscale = bool(logscale_position.value)

    if negative:
        # negate angles with reference to zero angle
        scan['angles'] = [angle_ref - (angle - angle_ref) for angle in scan['angles']]
                
    return scan

def startScan(configModel):
    
    ''' setup '''
    
    scanVariable = configModel.scanVariable
    crystal = configModel.crystal
    mode = configModel.mode

    
    MainDeadTime = 1.08E-6
    TransDeadTime = 1.08E-6
        
    if 'Si111' in crystal:
        empLevel = 0.3
        bkgLevel = 0.21
        dOmega = 2.3E-6
        gDQv = 0.0586
        gDQh = 0
        
        wavelength = 4.74
        TransmissionTube = 10
        TransBackground = 0  # counts per second
    
    elif 'Si311' in crystal:
        empLevel = 0.34
        bkgLevel = 0.21
        dOmega = 4.6E-7
        gDQv = 0.117
        gDQh = 0
        
        wavelength = 2.37
        TransmissionTube = 9
        TransBackground = 0  # counts per second
        
    else:
        print 'selected crystal is invalid'
        return
    
    ''' angles '''
    
    scan = configModel.scan
    
    scan_angleMin = builtin_min(scan['angles'])
    scan_angleMax = builtin_max(scan['angles'])
    
    if ('m1om' in scanVariable) or ('m2om' in scanVariable):
        tolerance = 6
        
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
    
    sics.execute('hset user/name ' + configModel.user_name)
    sics.execute('hset user/email ' + configModel.user_email)
    
    sics.execute('hset sample/name ' + configModel.sample_name)
    sics.execute('hset sample/description ' + configModel.sample_description)
    sics.execute('hset sample/thickness %g' % configModel.sample_thickness)
    
    sics.execute('hset experiment/bkgLevel %g' % bkgLevel)
    sics.execute('hset experiment/empLevel %g' % empLevel)
    
    sics.execute('hset instrument/detector/MainDeadTime %g' % MainDeadTime)
    sics.execute('hset instrument/detector/TransDeadTime %g' % TransDeadTime)
    sics.execute('hset instrument/detector/TransBackground %g' % TransBackground)
    sics.execute('hset instrument/detector/TransmissionTube %i' % TransmissionTube)
    
    sics.execute('hset instrument/crystal/dOmega %g' % dOmega)
    sics.execute('hset instrument/crystal/gDQv %g' % gDQv)
    sics.execute('hset instrument/crystal/gDQh %g' % gDQh)
    sics.execute('hset instrument/crystal/wavelength %g' % wavelength)
    sics.execute('hset instrument/crystal/scan_variable ' + scanVariable);
    
    sicsController = sics.getSicsController()
        
    # slits
    def getSlitValues(gap, offset, a0, b0, aOpen, bOpen):
        
        if gap == 'fully opened':
            return (aOpen, bOpen)
        
        if gap == 'fully closed':
            gap = -5.0
            offset = 0.0
        
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
    run = {}
    run['ss1u'] = ss1u
    run['ss1d'] = ss1d
    run['ss1r'] = ss1r
    run['ss1l'] = ss1l
    
    run['ss2u'] = ss2u
    run['ss2d'] = ss2d
    run['ss2r'] = ss2r
    run['ss2l'] = ss2l

#    sics.multiDrive(run)
    dc = 'drive'
    for key in run:
        dc += ' ' + key + ' ' + str(run[key])

    sics.execute(dc)
    
    time.sleep(5)
    while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
        time.sleep(0.1)
    
    '''
    sics.execute('run ss1u %.2f' % ss1u)
    sics.execute('run ss1d %.2f' % ss1d)
    sics.execute('run ss1r %.2f' % ss1r)
    sics.execute('run ss1l %.2f' % ss1l)
    
    sics.execute('run ss2u %.2f' % ss2u)
    sics.execute('run ss2d %.2f' % ss2d)
    sics.execute('run ss2r %.2f' % ss2r)
    sics.execute('run ss2l %.2f' % ss2l)
    '''
    
    # load sample positions
    sam_positions = str(configModel.sam_position)
    
    if (len(sam_positions) == 0) or (sam_positions == 'fixed'):
        samz_list = [None]
    else:
        samz_list = []
        
        pos2samz = {}
        
        '''
        # Quokka Sample tumbler Dec 2015
        pos2samz['1'] = 202.6
        pos2samz['2'] = 262.5
        pos2samz['3'] = 322.7
        pos2samz['4'] = 382.7
        pos2samz['5'] = 442.6       
        '''
        
        
        # KKB new 1mm CELLS WITH PERMANENT ORIGINAL (NEW) 30mm APERTURE
        # need metal spacer beneath them
        pos2samz['1'] = 32    
        pos2samz['2'] = 177   
        pos2samz['3'] = 321.5 
        pos2samz['4'] = 468 
        pos2samz['5'] = 612.5  
        
        '''
        # Original centre of sample compartment
        pos2samz['1'] =  35.5 #33.5
        pos2samz['2'] = 181.0 #178.5
        pos2samz['3'] = 326.0 #323.5
        pos2samz['4'] = 472.5 #468.5
        pos2samz['5'] = 617.0 #613.5
        '''
        '''
        # KKB new 10mm and 0.5mm CELLS WITH PERMANENT ORIGINAL (NEW) 30mm APERTURE
        # NO metal spacer!
        pos2samz['1'] = 34   
        pos2samz['2'] = 179   
        pos2samz['3'] = 323.5 
        pos2samz['4'] = 470 
        pos2samz['5'] = 614.5 
        '''
        
        '''
        # QUOKKA CELLS WITH PERMANENT ORIGINAL (NEW) 15mm APERTURE
        # this is right in the middle with 1mm gap on each side 
        # December 2015
        pos2samz['1'] = 30.0
        pos2samz['2'] = 176.0
        pos2samz['3'] = 320.0 # CHECK TROUBLESOME
        pos2samz['4'] = 467.0
        pos2samz['5'] = 612.0
        '''
        pos2samz['1-16'] = 28.1
        pos2samz['2-16'] = 68.6
        pos2samz['3-16'] = 108.6
        pos2samz['4-16'] = 149.2
        pos2samz['5-16'] = 189.0
        pos2samz['6-16'] = 228.9
        pos2samz['7-16'] = 268.8
        pos2samz['8-16'] = 309.1
        pos2samz['9-16'] = 349.4
        pos2samz['10-16'] = 389.2
        pos2samz['11-16'] = 429.4
        pos2samz['12-16'] = 469.5
        pos2samz['13-16'] = 509.3
        pos2samz['14-16'] = 549.6
        pos2samz['15-16'] = 589.5
        pos2samz['16-16'] = 630.0
        
        pos2samz['1 top'   ] = 17.4
        pos2samz['1 bottom'] = 77.7
        pos2samz['2 top'   ] = 163.5
        pos2samz['2 bottom'] = 223.1
        pos2samz['3 top'   ] = 308.0
        pos2samz['3 bottom'] = 368.1
        pos2samz['4 top'   ] = 454.1
        pos2samz['4 bottom'] = 513.6
        pos2samz['5 top'   ] = 598.2
        pos2samz['5 bottom'] = 658.0

        samz_list.append(pos2samz[sam_positions])

        '''
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
            
        '''

    for samz in samz_list:
    
        sics.execute('histmem stop')
        time.sleep(3)
        if mode == 'ba':
            sics.execute('histmem mode unlimited')
            sics.execute('histmem ba enable')
        else:
            sics.execute('histmem mode time')
            sics.execute('histmem ba disable')

        if samz is not None:
            print 'run samz %.2f' % samz
            sics.execute('run samz %.2f' % samz)
            # sics.execute('prun samz 2' % samz) !!!
            time.sleep(1)
            while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                time.sleep(0.1)

        sics.execute('newfile HISTOGRAM_XYT')
        # sics.execute('autosave 60') # 60 seconds
        time.sleep(1)
        
        # start/stop hmm
        if mode == 'count_roi':
            sics.execute('histmem preset 1')
            time.sleep(1)
            sics.execute('histmem start')
            time.sleep(5)
            while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                time.sleep(0.1)
            sics.execute('histmem stop')
        
        print 'frames:', len(scan['angles'])
        
        count_rate_history = []
        
        for frame_index in xrange(len(scan['angles'])):
            angle = scan['angles'  ][frame_index]
            preset = scan['presets' ][frame_index]
            maxTime = scan['maxTimes'][frame_index]
            
            print 'drive %s %.6f' % (scanVariable, angle)
            
            # sics.drive(scanVariable, float(angle))
            sics.execute('drive %s %.6f' % (scanVariable, angle))
            time.sleep(10)
            while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                time.sleep(0.1)
           
            print 'drive done'
            
            time.sleep(1)
            
            if mode == 'ba':
                sics.execute('histmem ba roi roi')
                sics.execute('histmem ba monitor %i' % 1)
                sics.execute('histmem ba mintime %i' % configModel.min_time)
                sics.execute('histmem ba maxtime %i' % maxTime)
                sics.execute('histmem ba maxdetcount %i' % preset)
                sics.execute('histmem ba maxbmcount -1')
                sics.execute('histmem ba undermintime ba_maxdetcount')

                print 'histmem start'
                sics.execute('histmem start block')
                
                time0 = time.time()
                while sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                    if time.time() - time0 > 15.0:
                        print 'WARNING: HM may not have started counting. Gumtree will save anyway.'
                        break 
                    else:
                        time.sleep(0.1)

                time0 = time.time()
                while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                    time.sleep(0.1)
                        
                print 'time counted (estimate):', float(time.time() - time0)
                
            else:
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
                                # print count_roi
                                
                                if count_roi > preset:
                                    print count_roi
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
                
            # sics.execute('histmem stop')
            sics.execute('save %i' % frame_index)
            frame_index += 1
            print 'histmem done'
            
            #check if in background
            try:
                roi_counts = float(sics.get_raw_value('hmm configure num_events_filled_to_count_roi'))
                roi_time = sics.getValue('/instrument/detector/time').getFloatData()
                roi_rate = roi_counts / roi_time
                
                print 'measured count rate:', roi_rate
                count_rate_history.append(roi_rate)
                
                bkg_frames = 3 # change back to 5
                bkg_range  = bkgLevel + 0.05

                if (len(count_rate_history) >= bkg_frames) and (builtin_max(count_rate_history[-bkg_frames:]) < bkg_range):
                    print 'background reached'
                    print 'scan completed (early exit)'
                    break
                    
            except:
                pass
            
        sics.execute('newfile clear')
        # sics.execute('autosave 0') # disable autosave
        
        # Get output filename
        filenameController = sicsController.findDeviceController('datafilename')
        savedFilename = filenameController.getValue().getStringData()
        print 'saved:', savedFilename
    
    
    sics.execute('histmem ba disable')
    
    print 'done'
    print

  
def btnPlotSteps_clicked():
    scan = getScan()
    # print 'zero angle:'
    # print scan_reference.value    
    print ''
    print 'scan variable range [%f, %f]' % (scan['angles'][0], scan['angles'][-1])   
    print ''
    
    #Plot1.clear()
    #Plot2.clear()
        
    
    scan_angleMin = builtin_min(scan['angles'])
    scan_angleMax = builtin_max(scan['angles'])
    
    if scan_angleMin == 0 and scan_angleMax == 0:
        print 'please select a scan template'
        return
    
    if scan_angleMin == scan_angleMax:
        print 'the min angle and max angle can not be the same'
        return
    
    dummy = zeros(2)
    dummy.axes[0] = [scan_angleMin, scan_angleMax]
    
    print [scan_angleMin, scan_angleMax]
    
    Plot1.add_dataset(dummy)
    Plot1.title = 'Preview'
    Plot1.x_label = 'm2om'
    Plot1.y_label = 'counts per sec'
    # Plot1.x_range = [scan_angleMin,scan_angleMax]
    
    inclusive = True
    angles = scan['angles']
    
    for i in xrange(1, len(angles)):
        xL = angles[i - 1]
        xH = angles[i  ]
                
        Plot1.add_mask_1d(xL, xH, '', inclusive)
        inclusive = not inclusive
        
    groups = scan['groups']
    for i in xrange(len(groups)):
        Plot1.add_mask_1d(groups[i], groups[i] + 1e-12, str(i + 1), True)
    
    
    # convert to q PLOT 2
    crystal = str(crystal_name.value)
    if 'Si111' in crystal:
        wavelength = 4.74
    
    elif 'Si311' in crystal:
        wavelength = 2.37
        
    else:
        wavelength = float('nan')

    q = convert2q(angles, scan_reference.value, wavelength)

    scan_angleMin = builtin_min(q)
    scan_angleMax = builtin_max(q)
    
    if isnan(scan_angleMin) or isnan(scan_angleMax):
        print 'please check the wavelength'
        return
    
    if scan_angleMin == scan_angleMax:
        print 'the min q and max q can not be the same'
        return

    dummy = zeros(2)
    dummy.axes[0] = [scan_angleMin, scan_angleMax]
    
    Plot2.add_dataset(dummy)
    Plot2.title = 'Preview'
    Plot2.x_label = 'q [1/A]'
    Plot2.y_label = 'counts per sec'

    Plot2.set_log_x_on(True)
    Plot2.set_log_y_on(True)
          
    Plot2.x_range = [1e-6, q[-1]]
        
    for i in xrange(1, len(q)):
        xL = q[i - 1]
        xH = q[i  ]
                
        Plot2.add_mask_1d(xL, xH, '', inclusive)
        inclusive = not inclusive
        
    groups = scan['groups']
    for i in xrange(len(groups)):
        Plot2.add_mask_1d(groups[i], groups[i] + 1e-12, str(i + 1), True)  
    
    # print "angles"
    # print angles       
    # print q
    print ''
    print 'scan q-range [%f, %f]' % (q[0], q[-1])
    print ''
    
def openDataset(path):
    
    ds = df[str(path)]
    ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm')
    # ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm_xy')
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
    ds.__iDictionary__.addEntry('samplename', 'entry1/sample/name')
    ds.__iDictionary__.addEntry('wavelength', 'entry1/instrument/crystal/wavelength')
    ds.__iDictionary__.addEntry('TimeStamp', 'entry1/time_stamp')

    return ds
 
def btnPlot_clicked():
    
    #Plot1.clear()
    #Plot2.clear()
        
    fns = []
    for sds in __DATASOURCE__.getSelectedDatasets():    
        fns.append(sds.getLocation())
        
    if len(fns) != 1:
        print 'select one dataset'
        return
        
    path = fns[0]
    basename = os.path.basename(str(path))
    basename = basename[:basename.find('.nx.hdf')]
    
    ds = openDataset(path)
    
    scanVariable = str(scan_variable.value)
    scanVariable = scanVariable[:scanVariable.find(' ')]
    scanVariable = ds[scanVariable]
    samplename = str(ds.samplename)
    
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
                data[:] = ds.hmm[:, 0, :, tid].sum(0)  # hmm
            else:
                data[:] = ds.hmm[:, :, tid].sum(0)  # hmm_xy
            
            if data.size == 1:
                data[0] = data[0] * 1.0 / ds.time
            else:
                data[:] = data[:] * 1.0 / ds.time
                if sorting:
                    data[:] = [data[item[0]] for item in info]  # sorting
                
            data.var[:] = 0  # total_counts / (ds.time * ds.time)

            axis0 = data.axes[0]
            axis0[:] = scanVariable[:]
                        
            # dataF = data.float_copy()
            # dataF.title = 'Tube %i' % tid
            
            # Plot1.add_dataset(dataF)
        
        Plot1.title = 'Count Rate (individual)'
            
    else:
        for tid in tids:
            if ds.hmm.ndim == 4:
                data[:] += ds.hmm[:, 0, :, tid].sum(0)  # hmm
            else:
                data[:] += ds.hmm[:, :, tid].sum(0)  # hmm_xy
            
        if data.size == 1:
            data[0] = data[0] * 1.0 / ds.time
        else:
            data[:] = data[:] * 1.0 / ds.time
            if sorting:
                data[:] = [data[item[0]] for item in info]  # sorting
            
        data.var[:] = 0  # total_counts / (ds.time * ds.time)
        
        axis0 = data.axes[0]
        axis0[:] = scanVariable[:]
        
        data.title = 'Tubes ' + str(tids)
        
        
        Plot1.set_dataset(data)
        Plot1.set_mouse_follower_precision(6, 2, 2)
        Plot1.title = basename + ' (combined):  ' + samplename

    # Plot1.title = Plot1.title + ' ' + basename
    
    if Plot1.ds is not None:
        Plot1.x_label = str(scan_variable_plot.value)
        Plot1.y_label = 'counts per sec'

    
    Plot2.clear()
    
    ds0 = Plot1.ds[0]  # # don't understand how this works
    xMax = 0
    yMax = 0
    for i in xrange(len(ds0)):
        if yMax < ds0[i]:
            xMax = ds0.axes[0][i]
            yMax = ds0[i]
   
    peakangle = xMax
    q = convert2q(scanVariable, peakangle, ds.wavelength)
        
    data.axes[0] = q[:]
    Plot2.set_dataset(data)
    Plot2.set_mouse_follower_precision(6, 2, 2)
        
    Plot2.x_label = 'q [1/A]'
    Plot2.y_label = 'counts per sec'
    # Plot1.title = 'Main Detector ' + basename + ': ' + samplename
    # Plot2.title = 'Sample: ' + samplename + '; ' + sampledescription
    Plot2.title = basename + ' (combined): ' + samplename
        
    Plot2.set_log_x_on(True)
    Plot2.set_log_y_on(True)
        
    Plot2.set_marker_on(True)      
    plotXMax = Par('float', q[-1])
    Plot2.x_range = [1e-6, plotXMax.value]
    
        
def convert2q(angles, reference, wavelength):
    if wavelength is list:
        wavelength = wavelength[0]
        
    wavelength = float(wavelength)
    
    deg2rad = 3.14159265359 / 180
    f = 4 * 3.14159265359 / wavelength

    if bool(negative_steps.value):
        f *= -1.0
        
    q = [(f * sin(deg2rad * (angle - reference) / 2)) for angle in angles]
    
    return q
 
def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
        
    print 'please press "Run Single Scan" or "Run Multiple Scans"'

def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()


# # model

class ConfigurationModel:
    def __init__(self):
        self.scanVariable = str(scan_variable.value)
        self.scanVariable = self.scanVariable[:self.scanVariable.find(' ')]
        
        self.crystal = str(crystal_name.value)
        self.mode = str(scan_mode.value)
        
        self.scan = getScan()
        self.scan_reference = scan_reference.value
        
        self.logscale = bool(logscale_position.value)
        self.negative = bool(negative_steps.value)
        self.stepInfo = []
        for step in stepInfo:
            d = dict()
            for key in step.keys():
                d[key] = step[key].value
            self.stepInfo.append(d);

        self.user_name = str(user_name.value)
        self.user_email = str(user_email.value)
        
        self.sample_name = str(sample_name.value)
        self.sample_description = str(sample_description.value)
        self.sample_thickness = float(sample_thickness.value)
        
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
        self.min_time = int(scan_min_time.value)
        
    def apply(self):
        for option in scan_variable.options:
            if self.scanVariable == option[:option.find(' ')]:
                scan_variable.value = option

        crystal_name.value = self.crystal
        scan_mode.value = self.mode

        logscale_position.value = self.logscale
        negative_steps.value = self.negative
        scan_reference.value = self.scan_reference
        i = 0
        for step in self.stepInfo:
            for key in step.keys():
                stepInfo[i][key].value = step[key]
            setEnabled(i)
            i += 1
            
        setScanMode()

        user_name.value = self.user_name
        user_email.value = self.user_email
        
        sample_name.value = self.sample_name
        sample_description.value = self.sample_description
        sample_thickness.value = self.sample_thickness
        
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
        scan_min_time.value = self.min_time
