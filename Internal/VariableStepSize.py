
__script__.title = 'KKB Measurement Script'
__script__.version = '1.0'

from gumpy.commons import sics
from org.gumtree.gumnix.sics.control import ServerStatus
import time

from __builtin__ import max as builtin_max
from __builtin__ import min as builtin_min

## templates

reference_templates_dict = {}
reference_templates_dict['Si111'] = 179.622
reference_templates_dict['Si311'] =  -0.02270

steps_templates_dict = {}
steps_templates_dict['Comprehensive Scan for Si111'] = [
    'time',
    [33, 6e-5, 50000],
    [13, 1.2e-4, 1000],
    [15, 2.4e-4, 1000],
    [10, 6.0e-4, 1000],
    [10, 1.2e-3, 1000],
    [16, 2.4e-3, 1000],
    [60, 6.0e-3, 1000]]
steps_templates_dict['Find Primary Beam for Si111'] = [
    'time',
    [31, 0.00025, 1]]
steps_templates_dict['Find Primary Beam for Si311'] = [
    'time',
    [51, 0.00004, 1]]

steps_templates_dict['TEST for Si111'] = [
    'count_roi',
    [33, 1.3e-5, 50000],
    [13, 6.0e-5, 1000],
    [15, 1.2e-4, 1000],
    [10, 3.0e-4, 1000],
    [10, 6.0e-4, 1000],
    [16, 1.2e-3, 1000],
    [60, 3.0e-3, 1000]]
steps_templates_dict['Comprehensive Scan for Si311'] = [
    'count_roi',
    [21, 1.3e-5, 50000],
    [13, 6.0e-5, 1000],
    [15, 1.2e-4, 1000],
    [10, 3.0e-4, 1000],
    [10, 6.0e-4, 1000],
    [16, 1.2e-3, 1000],
    [60, 3.0e-3, 1000]]
steps_templates_dict['Fast Scan'] = [
    'count_roi',
    [33, 6e-5, 50000],
    [13, 1.2e-4, 1000],
    [15, 2.4e-4, 1000],
    [10, 6.0e-4, 1000],
    [10, 1.2e-3, 1000],
    [16, 2.4e-3, 1000],
    [60, 6.0e-3, 1000]]
steps_templates_dict['Si111 m2om scan'] = [
    'time',
    [31, 0.00025, 1]]
    
    
steps_templates_dict['Si111 m2chi scan'] = [
    'time',
    [31, 0.1, 1]]


## export path

__EXPORT_PATH__ = 'V:/shared/Hot Commissioning/Temp Plot Data Repository'

if not os.path.exists(__EXPORT_PATH__):
    os.makedirs(__EXPORT_PATH__)
    
## User

user_name = Par('string', 'Christine', options = ['Christine', 'Lela'])
user_name.title = 'Name'

user_email = Par('string', 'cre@ansto.gov.au', options = ['cre@ansto.gov.au', 'liliana.decampo@ansto.gov.au'])
user_email.title = 'EMail'

Group('User').add(user_name, user_email)

## sample

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
    
Group('Crystal').add(crystal_name, crystal_change)
    
## Scan

scan_variable = Par('string', 'm2om [deg]', options = [
    'pmom [deg]', 'pmchi [deg]', 'm1om [deg]', 'm1chi [deg]', 'm1x [mm]', 'm2om [deg]', 'm2chi [deg]', 'm2x [mm]', 'm2y [mm]', 'mdet [mm]',
    'ss1u [mm]', 'ss1d [mm]', 'ss1l [mm]', 'ss1r [mm]',
    'ss2u [mm]', 'ss2d [mm]', 'ss2l [mm]', 'ss2r [mm]'], command="scan_variable_plot.value = scan_variable.value")

scan_variable.title = 'Variable'

scan_reference = Par('float', '0.0')
scan_reference.title = 'Reference'

for key in reference_templates_dict.keys():
    if key in crystal_name.value:
        scan_reference.value = reference_templates_dict[key]
    
steps_templates = Par('string', '', options = sorted(steps_templates_dict.keys()), command='SetTemplate()')
steps_templates.title = 'Template'

scan_mode = Par('string', 'count_roi', options = ['count_roi', 'time'])
scan_mode.title = 'Mode'

crystal = str(crystal_name.value)
crystal = crystal[:crystal.find(' ')]
for key in steps_templates_dict.keys():
    if ('Find Primary Beam' in key) and (crystal in key):
        steps_templates.value = key
        break

start_scan = Act('startScan()', 'start scan')

Group('Scan').add(scan_variable, scan_reference, steps_templates, scan_mode, start_scan)

## Measurement Steps

g0 = Group('Measurement Steps')
g0.numColumns = 4

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
    
    stepInfo.append({'enabled': steps_e, 'dataPoints':steps_m, 'stepSize':steps_s, 'preset':steps_p})
    g0.add(steps_e, steps_m, steps_s, steps_p)
    
btnPlotSteps = Act('btnPlotSteps_clicked()', 'Plot Measurement Steps') #'compare measurement steps with previous scan')

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
    'ss2u [mm]', 'ss2d [mm]', 'ss2l [mm]', 'ss2r [mm]'])

scan_variable_plot.title = 'Scan Variable'

combine_mode = Par('string', 'individual', options = ['individual', 'combined'])
combine_mode.title = 'Mode'
      
scan_variable_sorting = Par('bool', True)
scan_variable_sorting.title = 'Sorting'

#check_fitting = Par('bool', False)
#check_fitting.title = 'Fitting'

Group('Plotting - Settings').add(scan_variable_plot, combine_mode, scan_variable_sorting)

# export to csv
btnPlot    = Act('btnPlot_clicked()', 'Plot selected Dataset')
btnExport  = Act('export_clicked()', 'Export to CSV')

def SetTemplate():
    try:
        template = steps_templates_dict[steps_templates.value]
        
        scan_mode.value = template[0]
        
        for i in xrange(len(template) - 1):
            templateItem = template[i + 1]
            stepInfoItem = stepInfo[i]
                
            stepInfoItem['enabled'   ].value   = True
            stepInfoItem['dataPoints'].enabled = True
            stepInfoItem['dataPoints'].value   = templateItem[0]
            stepInfoItem['stepSize'  ].enabled = True
            stepInfoItem['stepSize'  ].value   = templateItem[1]
            stepInfoItem['preset'    ].enabled = True
            stepInfoItem['preset'    ].value   = templateItem[2]
            
        for i in xrange(len(template) - 1, len(stepInfo)):
            stepInfoItem = stepInfo[i]
                        
            stepInfoItem['enabled'   ].value   = False
            stepInfoItem['dataPoints'].enabled = False
            stepInfoItem['stepSize'  ].enabled = False
            stepInfoItem['preset'    ].enabled = False
            
    except:
        pass
    
SetTemplate()

def setEnabled(index):
    stepItem = stepInfo[index]
    value = stepItem['enabled'].value
    stepItem['dataPoints'].enabled = value
    stepItem['stepSize'  ].enabled = value
    stepItem['preset'    ].enabled = value


def getScan():
    
    scan = { 'angles': [], 'presets': [], 'groups': [] }
    
    first = True
    angle = scan_reference.value
    for stepInfoItem in stepInfo:
        if stepInfoItem['enabled'].value :
            dataPoints = stepInfoItem['dataPoints'].value
            stepSize   = stepInfoItem['stepSize'  ].value
            preset     = stepInfoItem['preset'    ].value
            
            if first:
                angle -= ((dataPoints-1)/2.0) * stepSize;
                scan['angles' ].append(angle)
                scan['presets'].append(preset)
                
            elif len(scan['angles']) == 0:
                scan['angles' ].append(angle)
                scan['presets'].append(preset)
                
            else:
                angle += stepSize
                scan['angles' ].append(angle)
                scan['presets'].append(preset)
            
            scan['groups'].append(angle)
            for i in xrange(1, dataPoints):
                angle += stepSize
                scan['angles' ].append(angle)
                scan['presets'].append(preset)

        first = False
        
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

def startScan():
    
    ''' setup '''
    
    scanVariable = str(scan_variable.value)
    scanVariable = scanVariable[:scanVariable.find(' ')]
    crystal      = str(crystal_name.value)
    mode         = str(scan_mode.value)

    empLevel = 0.76
    bkgLevel = 0.98757
    dOmega = 4.6E-6
    gDQv = 0.0586
    #gDQh = 0
    
    MainDeadTime = 2.78E-6
    TransDeadTime = 3.15E-5
    
    ''' angles '''
    
    scan = getScan()
    
    scan_angleMin = builtin_min(scan['angles'])
    scan_angleMax = builtin_max(scan['angles'])
    
    if ('m1om' in scanVariable) or ('m2om' in scanVariable):
        crystal   = str(crystal_name.value)
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
    
    sics.execute('hset user/name '  + str(user_name.value))
    sics.execute('hset user/email ' + str(user_email.value))
    
    sics.execute('hset sample/name '        + str(sample_name.value))
    sics.execute('hset sample/description ' + str(sample_description.value))
    sics.execute('hset sample/thickness %f' % float(sample_thickness.value))
    
    sics.execute('hset experiment/bkgLevel %f'  % bkgLevel)
    sics.execute('hset experiment/empLevel %f'  % empLevel)
    sics.execute('hset experiment/dOmega %f'    % dOmega)
    sics.execute('hset experiment/gDQv %f'      % gDQv)
    #sics.execute('hset experiment/gDQh %f'      % gDQh)
    
    sics.execute('hset instrument/detector/MainDeadTime %f'  % MainDeadTime)
    sics.execute('hset instrument/detector/TransDeadTime %f' % TransDeadTime)
    
    if 'Si111' in crystal:
        sics.execute('hset instrument/crystal/wavelength 4.74')
        sics.execute('hset instrument/detector/TransmissionTube 10')
    
    elif 'Si311' in crystal:
        sics.execute('hset instrument/crystal/wavelength 2.37')
        sics.execute('hset instrument/detector/TransmissionTube 9')
        
    else:
        print 'selected crystal is invalid'
        sics.execute('hset instrument/crystal/wavelength 0')
        sics.execute('hset instrument/detector/TransmissionTube -1')
        return

    sics.execute('histmem stop')
    time.sleep(3)
    sics.execute('histmem mode %s' % mode)
    sics.execute('newfile HISTOGRAM_XYT')
    time.sleep(1)
    
    sicsController = sics.getSicsController()
    
    list_x = []
    list_y = []
    for frame_index in xrange(len(scan['angles'])):
        angle  = scan['angles' ][frame_index]
        preset = scan['presets'][frame_index]
        
        print 'run %s %.5f' % (scanVariable, angle)
        sics.execute('run %s %f' % (scanVariable, angle))
        #sics.drive(scanVariable, angle)
        time.sleep(10)
        while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
            time.sleep(0.1)
        print 'run done'
        
        time.sleep(1)
        print 'histmem start'
        while True:
            sics.execute('histmem preset %i ' % preset)
            time.sleep(5)
            
            sics.execute('histmem start')
            time.sleep(5)
            
            while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                time.sleep(0.1)
    
            if mode == 'count_roi':
                break
            else:
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
                
        total_counts = sics.getValue('/instrument/detector/total_counts').getFloatData()
        print 'total_counts:', total_counts
        
        list_x.append(angle)
        list_y.append(total_counts)
        
    sics.execute('

')
    
    # Get output filename
    filenameController = sicsController.findDeviceController('datafilename')
    savedFilename = filenameController.getValue().getStringData()
    print 'saved:', savedFilename
    
    print 'done'
    print
  
def btnPlotSteps_clicked():
    scan = getScan()
    print 'range [%f, %f]' % (scan['angles'][0], scan['angles'][-1])
    
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
        
    print 'please press "start scan" in scan box'

def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
