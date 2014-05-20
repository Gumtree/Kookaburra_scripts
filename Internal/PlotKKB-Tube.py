from gumpy.nexus.fitting import Fitting, GAUSSIAN_FITTING

import math

# Script control setup area
# script info
__script__.title = 'HMM Tube Export'
__script__.version = '1.0'

__FOLDER_PATH__ = 'D:/users/kookaburra/Hot Commissioning/Temp Plot Data Repository'

if not os.path.exists(__FOLDER_PATH__):
    os.makedirs(__FOLDER_PATH__)

combine_tube0 = Par('bool', True)
combine_tube0.title = '     - Tube 0'

combine_tube1 = Par('bool', True)
combine_tube1.title = '     - Tube 1'

combine_tube2 = Par('bool', True)
combine_tube2.title = '     - Tube 2'

combine_tube3 = Par('bool', True)
combine_tube3.title = '     - Tube 3'

combine_tube4 = Par('bool', True)
combine_tube4.title = '     - Tube 4'

combine_mode = Par('string', 'individual', options = ['individual', 'combined'])
combine_mode.title = 'Mode'

check_fitting = Par('bool', False)
check_fitting.title = 'Fitting'
        
Group('Select Tube(s) of Interest:').add(combine_tube0, combine_tube1, combine_tube2, combine_tube3, combine_tube4, combine_mode, check_fitting)

check_tube9 = Par('bool', False)
check_tube9.title = '     - Tube 9: Si (311)'

check_tube10 = Par('bool', False)
check_tube10.title = '     - Tube 10: Si (111)'
        
Group('Select Transmission Tube(s) of Interest:').add(check_tube9, check_tube10)

# export to csv
export = Act('export_clicked()', 'Export to CSV')

def proc_fn(path):
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
    
    scanVariable = ds.m2om
    
    shape = ds.shape
    if shape[0] <= 1:
        print 'Must have at least 2 scan positions'
        return
     
    n = shape[0]
    
    data = zeros(n)
    data.title = 'Detector Counts'

    # transmission
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
        Plot2.title   = 'Count Rate (individual)'
        
    if Plot2.ds is not None:
        Plot2.x_label = 'angle in deg'
        Plot2.y_label = 'counts per sec'
    
    # tubes
    
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
                
            data.var[:] = 0 # total_counts / (ds.time * ds.time)

            axis0 = data.axes[0]
            axis0[:] = scanVariable[:]
                        
            dataF = data.float_copy()
            dataF.title = 'Tube %i' % tid
            
            Plot1.add_dataset(dataF)
            Plot1.title   = 'Count Rate (individual)'
            
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
            
        data.var[:] = 0 # total_counts / (ds.time * ds.time)
        
        axis0    = data.axes[0]
        axis0[:] = scanVariable[:]
        
        data.title ='Tubes ' + str(tids)
        
        Plot1.set_dataset(data)
        Plot1.title   = 'Count Rate (combined)'
    
    if Plot1.ds is not None:
        Plot1.x_label = 'angle in deg'
        Plot1.y_label = 'counts per sec'
    
    # fitting
    if check_fitting.value and (Plot1.ds is not None) and (len(Plot1.ds) == 1):
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
        fitting.set_param('sigma', math.fabs(0.0015 / 2.35482))
        fitting.set_histogram(ds0, xMax - 0.0015, xMax + 0.0015)
        
        for i in xrange(5):
            fit = fitting.fit()
        
        fit.var[:] = 0
        fit.title  = 'Gauss (center: %.7f)' % fitting.params['mean']
        Plot1.add_dataset(fit)
        print 'center: %.7f' % fitting.params['mean']

def export_clicked():
    
    Plot1.clear()
    Plot2.clear()
    
    fns = []
    for sds in __DATASOURCE__.getSelectedDatasets():
        fns.append(sds.getLocation())
    __run_script__(fns)

    p1 = (Plot1.ds is not None) and (len(Plot1.ds) >= 1)
    p2 = (Plot2.ds is not None) and (len(Plot2.ds) >= 1)

    if p1 or p2:        
        f = open(__FOLDER_PATH__ + '/KBB%07d.csv' % df[str(fns[0])].id, 'w+')
        f.write('Angle')
        
        dsRef = None
        
        if p1:
            dsRef = Plot1.ds[0]
            dsRefAngle = dsRef.axes[0]
            
            for ds in Plot1.ds:
                if len(ds) == len(dsRef): # to ignore Gauss fit
                    f.write(', %s' % str(ds.title).replace(',', ';'))
                    
        if p2:
            if dsRef is None:
                dsRef = Plot2.ds[0]
                dsRefAngle = dsRef.axes[0]

            for ds in Plot2.ds:
                f.write(', %s' % str(ds.title).replace(',', ';'))
            
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
