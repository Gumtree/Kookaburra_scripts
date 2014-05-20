from gumpy.nexus.fitting import Fitting, GAUSSIAN_FITTING

# Script control setup area
# script info
__script__.title = 'HMM Tube Export'
__script__.version = '1.0'

__FOLDER_PATH__ = 'D:/users/kookaburra/Hot Commissioning/Temp Plot Data Repository'

if not os.path.exists(__FOLDER_PATH__):
    os.makedirs(__FOLDER_PATH__)


G1 = Group('Select Tube(s) of Interest:')
combine_tube9 = Par('bool', True)
combine_tube9.title = '     - Tube 9'

combine_tube1 = Par('bool', True)
combine_tube1.title = '     - Tube 1'

combine_tube2 = Par('bool', True)
combine_tube2.title = '     - Tube 2'

combine_tube3 = Par('bool', True)
combine_tube3.title = '     - Tube 3'

combine_tube4 = Par('bool', True)
combine_tube4.title = '     - Tube 4'
        
G1.add(combine_tube9, combine_tube1, combine_tube2, combine_tube3, combine_tube4)

combine_mode = Par('string', 'individual', options = ['individual', 'combined'])
combine_mode.title = 'Mode'

# export to csv
export = Act('export_clicked()', 'Export to CSV') 

def proc_fn(path):
    ds = df[str(path)]
    ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm')
    #ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm_xy')
    ds.__iDictionary__.addEntry('time', 'entry1/instrument/detector/time')
    ds.__iDictionary__.addEntry('m1om', 'entry1/instrument/crystal/m1om')
    ds.__iDictionary__.addEntry('m2om', 'entry1/instrument/crystal/m2om')
    
    scanVariable = ds.m2om
    
    shape = ds.shape
    if shape[0] <= 1:
        print 'Must have at least 2 scan positions'
        return
     
    n = shape[0]
    
    data = zeros(n)
    data.title = 'Detector Counts'
    
    tids = []
    if combine_tube9.value:
        tids.append(9)
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
        for tid in tids: # or xrange(10, 11): or xrange(5):
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

    Plot1.x_label = 'angle in deg'
    Plot1.y_label = 'counts per sec'
    
    if (Plot1.ds is not None) and (len(Plot1.ds) == 1):
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
    
    fns = []
    for sds in __DATASOURCE__.getSelectedDatasets():
        fns.append(sds.getLocation())
    __run_script__(fns)

    if (Plot1.ds is not None) and (len(Plot1.ds) >= 1):        
        f = open(__FOLDER_PATH__ + '/KBB%07d.csv' % df[str(fns[0])].id, 'w+')
        
        dds = Plot1.ds;
        f.write('Angle')
        for ds in dds:
            f.write(', %s' % str(ds.title))
        f.write('\n')
        
        dsRef = Plot1.ds[0]
        for i in xrange(len(dsRef)):
            f.write('%.7f' % dsRef.axes[0][i])
            for ds in dds:
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
