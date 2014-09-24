
__script__.title = 'HMM Tube Export'
__script__.version = '1.0'

from gumpy.nexus.fitting import Fitting, GAUSSIAN_FITTING

from math import exp, fabs


__FOLDER_PATH__ = 'V:/shared/KKB Logbook/Temp Plot Data Repository'

if not os.path.exists(__FOLDER_PATH__):
    os.makedirs(__FOLDER_PATH__)

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

g0 = Group('Select Tube(s) of Interest:')
g0.numColumns = 6
g0.add(combine_tube0, combine_tube1, combine_tube2, combine_tube3, combine_tube4, combine_tube6)

check_tube9 = Par('bool', False)
check_tube9.title = ' Tube 9: Si (311)'

check_tube10 = Par('bool', True)
check_tube10.title = '   Tube 10: Si (111)'
        
g1 = Group('Select Transmission Tube(s) of Interest:')
g1.numColumns = 2
g1.add(check_tube9, check_tube10)

scan_variable = Par('string', 'm2om [deg]', options = [
    'pmom [deg]', 'pmchi [deg]', 'm1om [deg]', 'm1chi [deg]', 'm1x [mm]', 'm2om [deg]', 'm2chi [deg]', 'm2x [mm]', 'm2y [mm]', 'mdet [mm]',
    'ss1u [mm]', 'ss1d [mm]', 'ss1l [mm]', 'ss1r [mm]',
    'ss2u [mm]', 'ss2d [mm]', 'ss2l [mm]', 'ss2r [mm]',
    'ss1hg [mm]', 'ss1ho [mm]', 'ss1vg [mm]', 'ss1vo [mm]',
    'ss2hg [mm]', 'ss2ho [mm]', 'ss2vg [mm]', 'ss2vo [mm]'])

scan_variable.title = 'Scan Variable'

combine_mode = Par('string', 'combined', options = ['individual', 'combined'])
combine_mode.title = 'Main Detector Tubes'
      
scan_variable_sorting = Par('bool', True)
scan_variable_sorting.title = 'Sort Scan Variable'

run_fitting = Par('bool', False)
run_fitting.title = 'Show Fitting Result'

Group('Settings').add(scan_variable, combine_mode, scan_variable_sorting, run_fitting)


# export to csv
export = Act('export_clicked()', 'Export to CSV')

def GetTubeCounts(hmm, tid):
    if hmm.ndim == 4:
        return hmm[:, 0, :, tid].sum(0) # hmm
    else:
        return hmm[:, :, tid].sum(0)    # hmm_xy
    
def TimeNormalization(counts, time):
    if counts.size == 1:
        counts[0] = counts[0] * 1.0 / time
    else:
        counts[:] = counts[:] * 1.0 / time
        
def AnngleSorting(counts, sortInfo):
    if counts.size > 1:
        counts[:] = [counts[item[0]] for item in sortInfo]

def DeadtimeCorrection(counts, deadTime, time):
    for i in xrange(len(counts)):
        
        # x1 = x0 - (x0 - y*e^cx0) / (1 - cx0)
        y = counts[i]
        x = y       # initial value
        
        dtt = deadTime / time[i]
        
        for j in xrange(4):
            x = x - (x - y*exp(dtt * x)) / (1 - dtt * x)
            
        counts[i] = x

        #tube[i] = tube[i] * (1 / (1.0 - tube[i] * deadTime / countTimes[i]))

def proc_fn(path):
    
    #global ds
    #global dataF
    
    MainDeadTime = 1.08e-6
    
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
    ds.__iDictionary__.addEntry('ss1hg', 'entry1/instrument/slits/gaps/ss1hg')
    ds.__iDictionary__.addEntry('ss1ho', 'entry1/instrument/slits/gaps/ss1ho')
    ds.__iDictionary__.addEntry('ss1vg', 'entry1/instrument/slits/gaps/ss1vg')
    ds.__iDictionary__.addEntry('ss1vo', 'entry1/instrument/slits/gaps/ss1vo')
    ds.__iDictionary__.addEntry('ss2hg', 'entry1/instrument/slits/gaps/ss2hg')
    ds.__iDictionary__.addEntry('ss2ho', 'entry1/instrument/slits/gaps/ss2ho')
    ds.__iDictionary__.addEntry('ss2vg', 'entry1/instrument/slits/gaps/ss2vg')
    ds.__iDictionary__.addEntry('ss2vo', 'entry1/instrument/slits/gaps/ss2vo')
    
    scanVariable = str(scan_variable.value)
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
            data[:] = GetTubeCounts(ds.hmm, tid)
                            
            TimeNormalization(data, ds.time)
            if sorting:
                AnngleSorting(data, info)
                
            data.var[:] = 0 # total_counts / (ds.time * ds.time)

            axis0 = data.axes[0]
            axis0[:] = scanVariable[:]
                        
            dataF = data.float_copy()
            dataF.title = 'Tube %i' % tid
            
            Plot1.add_dataset(dataF)
        
        Plot1.title = 'Count Rate (individual) ' + basename
            
    else:
        for tid in tids:
            data[:] += GetTubeCounts(ds.hmm, tid)
            
        TimeNormalization(data, ds.time)
        if sorting:
            AnngleSorting(data, info)
            
        data.var[:] = 0 # total_counts / (ds.time * ds.time)
        
        axis0    = data.axes[0]
        axis0[:] = scanVariable[:]
        
        data.title ='Tubes ' + str(tids)
        
        Plot1.set_dataset(data)
        Plot1.title = 'Count Rate (combined) ' + basename
    
    if Plot1.ds is not None:
        Plot1.x_label = str(scan_variable.value)
        Plot1.y_label = 'counts per sec'
    
    # dead-time corrected / fitted
    Plot2.clear()
    
    data = zeros(n)
    for tid in tids:
        data[:] += GetTubeCounts(ds.hmm, tid)
        
    DeadtimeCorrection(data, MainDeadTime, ds.time)
    TimeNormalization(data, ds.time)
    if sorting:
        AnngleSorting(data, info)
        
    data.var[:] = 0 # total_counts / (ds.time * ds.time)
    
    axis0    = data.axes[0]
    axis0[:] = scanVariable[:]
    
    data.title ='Tubes ' + str(tids)
    
    Plot2.set_dataset(data)
    Plot2.title = 'Deadtime corrected (combined) ' + basename
    
    if Plot2.ds is not None:
        Plot2.x_label = str(scan_variable.value)
        Plot2.y_label = 'counts per sec'

    # transmission
    data = zeros(n)
    
    tids = []
    if check_tube9.value:
        tids.append(9)
    if check_tube10.value:
        tids.append(10)
        
    Plot3.clear()
    for tid in tids:
        data[:] = GetTubeCounts(ds.hmm, tid)
            
        TimeNormalization(data, ds.time)
        if sorting:
            AnngleSorting(data, info)

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
        
        Plot3.add_dataset(dataF)
        Plot3.title   = 'Count Rate (individual) ' + basename
        
    if Plot3.ds is not None:
        Plot3.x_label = str(scan_variable.value)
        Plot3.y_label = 'counts per sec'
        
    # fitting
    '''
    if run_fitting.value and (Plot1.ds is not None) and (len(Plot1.ds) == 1):
        ds0 = Plot1.ds[0]
        
        nan = float('nan')
        
        # parameter estimation
        xMax = 0
        yMax = 0
        for i in xrange(len(ds0)):
            if yMax < ds0[i]:
                xMax = ds0.axes[0][i]
                yMax = ds0[i]
        
        fitting = Fitting(GAUSSIAN_FITTING)
        fitting.set_param('mean', xMax)
        fitting.set_param('sigma', fabs(0.0015 / 2.35482))
        fitting.set_histogram(ds0, xMax - 0.1, xMax + 0.1)
        #fitting.set_histogram(ds0, xMax - 0.0015, xMax + 0.0015)
        
        for i in xrange(5):
            fit = fitting.fit()
        
        fit.var[:] = 0
        fit.title  = 'Gauss (center: %.7f)' % fitting.params['mean']
        Plot1.add_dataset(fit)
        print 'center: %.7f' % fitting.params['mean']
    '''

def export_clicked():
    
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
    
    basename = ''
    
    fns = []
    for sds in __DATASOURCE__.getSelectedDatasets():
        basename = os.path.basename(str(sds.getLocation()))
        basename = basename[:basename.find('.nx.hdf')]
    
        fns.append(sds.getLocation())
        
    __run_script__(fns)

    p1 = (Plot1.ds is not None) and (len(Plot1.ds) >= 1)
    p2 = (Plot2.ds is not None) and (len(Plot2.ds) >= 1)
    p3 = (Plot3.ds is not None) and (len(Plot3.ds) >= 1)

    if p1 or p3:
        f = open(__FOLDER_PATH__ + '/KKB%07d.csv' % df[str(fns[0])].id, 'w+')
        
        variable     = str(scan_variable.value)
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
                if len(ds) == len(dsRef): # to ignore Gauss fit
                    title = str(ds.title) # select "[0;1;2;3;4]"
                    f.write(', %s_DeadtimeCorrected%s' % (basename, title[title.find('['):].replace(',', ';').replace(' ','')))
                    columns += 1
                    
        if p3:
            if dsRef is None:
                dsRef = Plot3.ds[0]
                dsRefAngle = dsRef.axes[0]

            for ds in Plot3.ds:
                title = str(ds.title) # select "Tube9" or "Tube10"
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
                    if len(ds) == len(dsRef): # to ignore Gauss fit
                        f.write(', %.5f' % ds[i])
            if p3:
                for ds in Plot3.ds:
                    f.write(', %.5f' % ds[i])
            f.write('\n')

        f.close()
        print 'finished output ' + f.name


# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    
    # check if a list of file names has been given
    if (fns is not None) and (len(fns) == 1):
        df.datasets.clear()
        proc_fn(fns[0])
    else:
        print 'select one dataset'


def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
