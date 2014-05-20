# Script control setup area
# script info
__script__.title = 'Find Peak Angle'
__script__.version = '1.0'

# Use below example to create parameters.
# The type can be string, int, float, bool, file.

ui_min = Par('string', 'm2om')
ui_min.title = 'Motor'

ui_min = Par('float', 179.619)
ui_min.title = 'Min'
ui_max = Par('float', 179.624)
ui_max.title = 'Max'

# step count
sc_enabled = Par('bool', True, command = 'set_sc_enabled()')
sc_enabled.title = 'Enable'
sc_count = Par('int', 31)
sc_count.title = 'Data Points'

# step width
sw_enabled = Par('bool', False, command = 'set_sw_enabled()')
sw_enabled.title = 'Enable'
sw_width = Par('float', 0.0001)
sw_width.title = 'Step Width'
sw_width.enabled = False

def set_sc_enabled():
    enabled = sc_enabled.value
    
    sc_count.enabled = enabled    
    sw_enabled.value = not enabled
    sw_width.enabled = not enabled

def set_sw_enabled():
    enabled = sw_enabled.value
    
    sw_width.enabled = enabled    
    sc_enabled.value = not enabled
    sc_count.enabled = not enabled

# Use below example to create a button
ui_runscan = Act('runscan()', 'Run Scan') 
def runscan():
    pass




'''
    dss = __DATASOURCE__.getSelectedDatasets()
    df.datasets.clear()
    for ds in dss:
        proc_fn(ds.getLocation())
'''


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
    
    if ind_tube.value:
        Plot1.clear()
        for tid in xrange(5): # or xrange(10, 11): or xrange(5):
            if ds.hmm.ndim == 4:
                total_counts = ds.hmm[:, 0, :, tid].sum(0) # hmm
            else:
                total_counts = ds.hmm[:, :, tid].sum(0)  # hmm_xy
            
            if data.size == 1:
                data[0] = total_counts * 1.0 / ds.time
            else :
                data[:]     = total_counts * 1.0 / ds.time
            data.var[:] = 0 # total_counts / (ds.time * ds.time)
#            for i in xrange(n):
#                data[i] = sum(ds.hmm[i, :, tid])[0] # only tube at 2 (starting from 0)
                #data[i] = sum(sum(ds.hmm[i, 0, :, 4])) # only tube at 2 (starting from 0)
                #data[i] = sum(sum(ds.hmm[i, 0, :, 0:5])) # detectors from 0 to 4
                #data[i] = sum(sum(ds.hmm[i, :, 0:5])) # detectors from 0 to 4
            
            axis0 = data.axes[0]
            axis0[:] = scanVariable[:]
            
            data.title = 'Tube ' + str(tid)
            Plot1.add_dataset(data.float_copy())
            Plot1.x_label = 'scan points'
            Plot1.y_label = 'counts'
            
            # export to csv
            f = open(__FOLDER_PATH__ + '/KBB%(fid)07d_%(tid)d.csv' 
                     % {'fid':ds.id, 'tid':tid}, 'w+')
            for i in xrange(n):
                f.write('%.5f, %.5f\n' % (axis0[i], data[i]))
            f.close()
            print 'finished output ' + f.name
    else:
        
        ctb = str(comb_tube.value)
        if ctb.__contains__(','):
            
            items = ctb.split(',')
            for item in items:
                tid   = int(item)
                if ds.hmm.ndim == 4:
                    data[:] += ds.hmm[:, 0, :, tid].sum(0) # hmm
                else:
                    data[:] += ds.hmm[:, :, tid].sum(0)  # hmm_xy
                
            if data.size == 1:
                data[0] = data[0] / ds.time
            else:
                data[:] = data[:] / ds.time
                
            data.var[:] = 0 # total_counts / (ds.time * ds.time)
            
            axis0    = data.axes[0]
            axis0[:] = scanVariable[:]
            
            Plot1.set_dataset(data)
            Plot1.x_label = 'scan points'
            Plot1.y_label = 'counts'
            
            ctb_fname = ctb.replace(',','_').replace(' ', '')
            # export to csv
            f = open(__FOLDER_PATH__ + '/KBB%(fid)07d_%(tid)s.csv' 
                     % {'fid':ds.id, 'tid':ctb_fname}, 'w+')
            for i in xrange(n):
                f.write('%.5f, %.5f\n' % (axis0[i], data[i]))
            f.close()
            print 'finished output ' + f.name
             

    
   
# Use below example to create a new Plot
# Plot4 = Plot(title = 'new plot')

# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3


def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
