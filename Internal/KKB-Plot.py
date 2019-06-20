__script__.title = 'HMM Tube Export'
__script__.version = '1.0'

#from gumpy.nexus.fitting import Fitting, GAUSSIAN_FITTING

# 2019-06-16 Add sample temp for batch file mode

from math import exp, fabs, sin, sqrt


__FOLDER_PATH__ = 'V:/shared/KKB Logbook/Temp Plot Data Repository'
#__FOLDER_PATH__ = 'C:/temp'


if not os.path.exists(__FOLDER_PATH__):
    os.makedirs(__FOLDER_PATH__)


'''
INPUT
'''


combine_mode = Par('string', 'combined', options = ['individual', 'combined'])
combine_mode.title = 'Mode:'

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

combine_tube7 = Par('bool', False)
combine_tube7.title = '   Tube 7'


g0 = Group('Main Detector')
g0.numColumns = 10
g0.add(combine_mode,
       combine_tube0, combine_tube1, combine_tube2, 
       combine_tube3, combine_tube4, combine_tube6, combine_tube7)

check_tube9 = Par('bool', False)
check_tube9.title = ' Tube 9: Si (311)'

check_tube10 = Par('bool', True)
check_tube10.title = '   Tube 10: Si (111)'

g1 = Group('Transmission Detector')
g1.numColumns = 2
g1.add(check_tube9,check_tube10)


scan_variable = Par('string', 'm2om [deg]', options = [
    'pmom [deg]', 'pmchi [deg]', 
    'm1om [deg]', 'm1chi [deg]', 'm1x [mm]', 
    'm2om [deg]', 'm2chi [deg]', 'm2x [mm]', 'm2y [mm]', 
    'mdet [mm]','samz [mm]', 'samx [mm]', 'apsel [mm]',
    'ss1u [mm]', 'ss1d [mm]', 'ss1l [mm]', 'ss1r [mm]',
    'ss2u [mm]', 'ss2d [mm]', 'ss2l [mm]', 'ss2r [mm]',
    'ss1hg [mm]', 'ss1ho [mm]', 'ss1vg [mm]', 'ss1vo [mm]',
    'ss2hg [mm]', 'ss2ho [mm]', 'ss2vg [mm]', 'ss2vo [mm]', 
    'index'])

scan_variable.title = 'Scan Variable'
      
scan_variable_sorting = Par('bool', True)
scan_variable_sorting.title = 'Sort Scan Variable'

convert2q = Par('bool', False)
convert2q.title = 'Convert to q'

use_beammonitor = Par('bool', False)
use_beammonitor.title = 'Use Beam Monitor'

g2 = Group('Plot & Export Settings')
g2.numColumns = 2
g2.add(scan_variable,scan_variable_sorting,use_beammonitor,convert2q)



# export to csv
export = Act('export_clicked()', 'Plot And Export to CSV')




def GetTubeCounts(hmm, tid):
    if hmm.ndim == 4:
        return hmm[:, 0, :, tid].sum(0) # hmm
        
    else:
        
        return hmm[:, :, tid].sum(0)    # hmm_xy    
      
def TimeNormalization(counts, time, countrate):    
    #print counts.size
    
    if counts.size == 1:
        countrate [0] = counts[0] * 1.0 / time
    else:
        countrate [:] = counts[:] * 1.0 / time
        
def AngleSorting(counts, sortInfo):
    if counts.size > 1:
        counts[:] = [counts[item[0]] for item in sortInfo]

def DeadtimeCorrection(counts, deadTime, time, counts_dt_corrected):
    
    for i in xrange(len(counts)):
        
        # x1 = x0 - (x0 - y*e^cx0) / (1 - cx0)
        t = time[i]
        y = counts[i]
        x = y       # initial value
        
        if t > 0.5: 
            dtt = deadTime / time[i]
            
            for j in xrange(4):
                x = x - (x - y*exp(dtt * x)) / (1 - dtt * x)
                
            counts_dt_corrected[i] = x
            
        else:
            counts_dt_corrected[i] = 0
     
    #print counts.storage
    #print counts_dt_corrected.storage
     
     
    #return counts_dt_corrected

        #tube[i] = tube[i] * (1 / (1.0 - tube[i] * deadTime / countTimes[i]))
'''
def FindZeroAngle(scanvariable,data,peakangle):
        # find peak
        x = scanvariable
        y = data
        i = y.index(builtin_max(y))

        dy = slopeAt(y, i)
        if dy < 0.0:
            aX = x[i-1]
            bX = x[i  ]
            
            aY = slopeAt(y, i-1)
            bY = dy
        else:
            aX = x[i  ]
            bX = x[i+1]
            
            aY = dy
            bY = slopeAt(y, i+1)
            
        PeakAng = (aY*bX - aX*bY) / (aY - bY)
        PeakVal = y[i];
        
        print "PeakAng:", self.PeakAng
'''

def proc_fn(path):
    
    basename = os.path.basename(str(path))
    basename = basename[:basename.find('.nx.hdf')]
    
    ds = df[str(path)]
    ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm')
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
    ds.__iDictionary__.addEntry('samz', 'entry1/sample/samz')
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
    ds.__iDictionary__.addEntry('bm1_counts', 'entry1/monitor/bm1_counts')
    ds.__iDictionary__.addEntry('bm1_time', 'entry1/monitor/bm1_time')
    ds.__iDictionary__.addEntry('samplename', 'entry1/sample/name')
    ds.__iDictionary__.addEntry('sampledescription', 'entry1/sample/description')
    ds.__iDictionary__.addEntry('MainDeadTime', 'entry1/instrument/detector/MainDeadTime')
    ds.__iDictionary__.addEntry('TransDeadTime', 'entry1/instrument/detector/TransDeadTime')
    try:
        ds.__iDictionary__.addEntry('LS_C', 'entry1/sample/tc3/sensor/sensorValueC')
    except:
        pass
     
    for i in xrange(len(ds.time)):        
        if ds.time[i] < 0.5:
            ds.time[i] = float('inf')
    print ''
    print 'Sample Temperature:', float(ds.LS_C[0])-273.15
    
    scanVariable = str(scan_variable.value)
    
    if scanVariable =='index':
        scanVariable = range(len(ds.m2om))
        
    else:
        scanVariable = scanVariable[:scanVariable.find(' ')]
        scanVariable = ds[scanVariable]
    
    
    samplename = str(ds.samplename) 
    sampledescription = str(ds.sampledescription) 
  
    sorting = scan_variable_sorting.value # use sorting? true or false
  
    beammonitor = use_beammonitor.value # use beam monitor? true or false
    
    if sorting:
        info = sorted(enumerate(scanVariable), key=lambda item:item[1])
        scanVariable = [item[1] for item in info]
    
    
    shape = ds.shape
   
    if shape[0] <= 1:
        print 'Must have at least 2 scan positions'
        return
     
    n = shape[0]

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
        tids.append(6) # this just says how many tubes to combine
    if combine_tube7.value:
        tids.append(7)
    
    
  # START PLOTTING  
    
    
    # MAIN PLOT
        
    Plot1.clear()  
    
    # tubes
    data_counts = zeros(n)
      
    if str(combine_mode.value) == 'individual':
        
        #print "doesn't work yet"
        
        for tid in tids:
            data_counts[:] = GetTubeCounts(ds.hmm, tid)
            
            data = copy(data_counts)                
            TimeNormalization(data_counts, ds.time, data)
            if sorting:
                AngleSorting(data, info)
            
            axis0 = data.axes[0]
            axis0[:] = scanVariable[:]
            data.title = 'Tube' + str(tid)
            Plot1.add_dataset(data)
      
        Plot1.title = 'Count Rate (individual) ' + basename
         
    
    
    else:
        for tid in tids:
            data_counts[:] += GetTubeCounts(ds.hmm, tid)        
        
        for i in range (len(data_counts)):
            data_counts.var[i]=sqrt(data_counts[i])
      
        data_counts.axes[0] = scanVariable[:]
        data_counts.title = 'counts'       
        
        
        data = copy(data_counts) # syntax doesnt seem to make sense but works
        data.title ='data'     
        
        TimeNormalization(data_counts, ds.time, data) # error propagation not correct
        
        if sorting:
            AngleSorting(data, info) # error propagation not correct

        Plot1.set_dataset(data)
        Plot1.set_mouse_follower_precision(6,2,2)       
        Plot1.title = basename + ',  Sample: ' + samplename + '; ' + sampledescription
          
        
        
        ################################################################################
        # deadtime correction
    
        data_counts_dt = copy(data_counts)
        data_counts_dt.title = 'data_counts_dt'
        data_dt = copy(data_counts)
        data_dt.title = 'data_dt'

        DeadtimeCorrection(data_counts, ds.MainDeadTime, ds.time, data_counts_dt)              
        TimeNormalization(data_counts_dt, ds.time, data_dt)
        
        if sorting:
            AngleSorting(data_dt, info)         
        
        Plot1.add_dataset(data_dt)

        
        ################################################################################
        # beam monitor normalisation
        
        data_dt_bm = copy(data_dt)
        data_dt_bm.title = 'data_dt_bm'
        
        if beammonitor:
            data_dt_bm *= ds.bm1_time/ds.bm1_counts * 13000
            Plot1.add_dataset(data_dt_bm)
              
        
        ################################################################################
        
    if Plot1.ds is not None:
        Plot1.x_label = str(scan_variable.value)
        Plot1.y_label = 'counts per sec'     
    
    # beam monitor ################################################################
    Plot2.clear()
    
    beammonitorrate = copy(data_counts)
    beammonitorrate.title ='bm_rate'
    beammonitorrate [:] = ds.bm1_counts [:] / ds.bm1_time [:]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    Plot2.set_dataset(beammonitorrate)
    Plot2.set_mouse_follower_precision(6,2,2)
    Plot2.title = 'Beam Monitor ' #+ basename + ': ' + samplename
    
    if Plot2.ds is not None:
        Plot2.x_label = str(scan_variable.value)
        Plot2.y_label = 'counts per sec'
    
    
    # transmission tube ################################################################ 
    Plot3.clear()
    counts_trans = copy(data_counts)
    
    tids = []
    if check_tube9.value:
        tids.append(9)
    if check_tube10.value:
        tids.append(10)

    for tid in tids:
        counts_trans[:] = GetTubeCounts(ds.hmm, tid)
        
        data_trans = copy(counts_trans)   
        data_trans.title = 'transmission'
        data_trans.var[:] = 0 # total_counts / (ds.time * ds.time)
        TimeNormalization(counts_trans, ds.time, data_trans)

        if sorting:
            AngleSorting(data_trans, info)

        if tid == 9:
            data_trans.title = 'Tube %i: Si (311)' % tid
        elif tid == 10:
            data_trans.title = 'Tube %i: Si (111)' % tid
        else:
            data_trans.title = 'Tube %i' % tid
        
        
        Plot3.add_dataset(data_trans)
        Plot3.set_mouse_follower_precision(6,2,2)
        Plot3.title   = 'Transmission detector ' #+ basename + ': ' + samplename
        
    if Plot3.ds is not None:
        Plot3.x_label = str(scan_variable.value)
        Plot3.y_label = 'counts per sec'
    
     # FINAL PLOT
 
    if convert2q.value:


        ds0 = Plot1.ds[0] ## takes first dataset in plot 1
        xMax = 0
        yMax = 0
        
        #Plot1.clear()
        
        for i in xrange(len(ds0)):
            if yMax<ds0[i]:
                xMax = ds0.axes[0][i]
                yMax = ds0[i]
   
        peakangle = xMax
        f = 4*3.1415/4.74 # 4pi/lambda    
        q = [(f*sin((x-peakangle)*3.1415/360)) for x in scanVariable]
        data.axes[0] = q[:] 
 
        if str(combine_mode.value) == 'combined':
            data_dt.axes[0] = q[:]
            data_dt_bm.axes[0] = q[:]
            Plot1.set_dataset(data)
            Plot1.add_dataset(data_dt)
            Plot1.add_dataset(data_dt_bm)
        
            
        if str(combine_mode.value) == 'individual':
            
            
            print 'q-conversion does not work with individual tubes yet'

        
        Plot1.set_mouse_follower_precision(6,2,2)
        
        Plot1.x_label = 'q [1/A]'
        Plot1.y_label = 'counts per sec'
        Plot1.title = basename + ',  Sample: ' + samplename + '; ' + sampledescription
        
        Plot1.set_log_x_on(True)
        Plot1.set_log_y_on(True)
        Plot1.set_marker_on(True)    
    
        plotXMax = Par('float', '0.02')
        Plot1.x_range = [1e-6,plotXMax.value]
    
    print '     '
    print 'sample name: ' + samplename
    print 'description: ' + sampledescription
    print '     '


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

    if p1:
        
        f = open(__FOLDER_PATH__ + '/KKB%07d.csv' % df[str(fns[0])].id, 'w+')
        
        variable     = str(scan_variable.value)
        variableName = variable[:variable.find(' ')]
        variableUnit = variable[(2+len(variableName)):-1]
        sample = Plot1.title
        
        f.write(variableName)
        columns = 0
        
        dsRef = None
        
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
                    #title = str(ds.title) # select "[0;1;2;3;4]"
                    #f.write(', %s_DeadtimeCorrected%s' % (basename, title[title.find('['):].replace(',', ';').replace(' ','')))
                    f.write(', %s_%s' % (basename, str(ds.title).replace(',', ';').replace(' ','')))
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
        
        
        f.write(sample)
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
    #global Plot4
    
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
    #global Plot4
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
    #Plot4.clear()
