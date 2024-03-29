
# 2018-06-21 Scan Variable


__script__.title = 'KKB Overview'
__script__.version = '2.0'



__FOLDER_PATH__ = 'V:/shared/KKB Logbook/Temp Plot Data Repository/'

if not os.path.exists(__FOLDER_PATH__):
    os.makedirs(__FOLDER_PATH__)
    
#__savefile__ = 'overview'


SampleName_tick = Par('bool', True)
SampleName_tick.title = 'Sample Name'

SampleDescription_tick = Par('bool', False)
SampleDescription_tick.title = '    Sample Description'

SampleThickness_tick = Par('bool', True)
SampleThickness_tick.title = '    Sample Thickness'

SamplePosition_tick = Par('bool', True)
SamplePosition_tick.title = '    Sample Position'

g0 = Group('Sample:')
g0.numColumns = 6
g0.add(SampleName_tick,SampleDescription_tick,SampleThickness_tick,SamplePosition_tick)


NumberOfPoints_tick = Par('bool', True)
NumberOfPoints_tick.title = 'Number Of Points'

StartTime_tick = Par('bool', True)
StartTime_tick.title = '   StartTime'

EndTime_tick = Par('bool', True)
EndTime_tick.title = '   EndTime'

RunTime_tick = Par('bool', True)
RunTime_tick.title = '   Runtime'

WaveLength_tick = Par('bool', True)
WaveLength_tick.title = '   Wavelength'

ScanVariable_tick = Par('bool', False)
ScanVariable_tick.title = '   Scan Variable'

g0 = Group('Measurement:')
g0.numColumns = 4
g0.add(NumberOfPoints_tick, StartTime_tick, EndTime_tick, RunTime_tick, WaveLength_tick, ScanVariable_tick)

pmchi_tick = Par('bool', False)
pmchi_tick.title = 'pmchi'

pmom_tick = Par('bool', False)
pmom_tick.title = '  pmom'

bex_tick = Par('bool', False)
bex_tick.title = '  bex'

m1chi_tick = Par('bool', False)
m1chi_tick.title = '  m1chi'

m1x_tick = Par('bool', False)
m1x_tick.title = '  m1x'

m1om_tick = Par('bool', False)
m1om_tick.title = '  m1om'

m2chi_tick = Par('bool', False)
m2chi_tick.title = '  m2chi'

m2x_tick = Par('bool', False)
m2x_tick.title = '  m2x'

m2y_tick = Par('bool', False)
m2y_tick.title = '  m2y'

m2om_tick = Par('bool', False)
m2om_tick.title = '  m2om'

mdet_tick = Par('bool', False)
mdet_tick.title = '  mdet'
mdet_tick.colspan = 2

ss1vg_tick = Par('bool', False)
ss1vg_tick.title = '  ss1vg'

ss1hg_tick = Par('bool', False)
ss1hg_tick.title = '  ss1hg'

ss1vo_tick = Par('bool', False)
ss1vo_tick.title = '  ss1vo'

ss1ho_tick = Par('bool', False)
ss1ho_tick.title = '  ss1ho'

g0 = Group('Instrument Settings:')
g0.numColumns = 6
g0.add(pmchi_tick, pmom_tick, bex_tick, m1chi_tick, m1x_tick, m1om_tick,
       m2chi_tick, m2x_tick, m2y_tick, m2om_tick, mdet_tick,
       ss1vg_tick, ss1hg_tick, ss1vo_tick, ss1ho_tick)


tempSensorC_tick = Par('bool', False)
tempSensorC_tick.title = '  SensorC'

tempSensorD_tick = Par('bool', False)
tempSensorD_tick.title = '  SensorD'

tempvTE_sp_tick = Par('bool', False)
tempvTE_sp_tick.title = '  vTE setpoint'

tempvTE_sensor_tick = Par('bool', False)
tempvTE_sensor_tick.title = '  vTE sensor'



g0 = Group('Temp Settings:')
g0.numColumns = 3
g0.add(tempvTE_sp_tick,tempvTE_sensor_tick, tempSensorC_tick, tempSensorD_tick)




ReactorPower_tick = Par('bool', False)
ReactorPower_tick.title = '  Reactor Power'

CNSout_tick = Par('bool', False)
CNSout_tick.title = '  CNS out'

g0 = Group('Reactor:')
g0.numColumns = 3
g0.add(ReactorPower_tick, CNSout_tick)

BeamMonitor_tick = Par('bool', False)
BeamMonitor_tick.title = '  BM counts'

Tube6_tick = Par('bool', False)
Tube6_tick.title = '  Tube 6'

Tube7_tick = Par('bool', False)
Tube7_tick.title = '  Tube 7'

g0 = Group('Beam Monitor:')
g0.numColumns = 3
g0.add(BeamMonitor_tick, Tube6_tick, Tube7_tick)



export_tick = Par('bool', True)
export_tick.title = 'export'

exportfilename = Par('string', 'Overview')
exportfilename.title = 'Filename'

print_tick = Par('bool', False)
print_tick.title = 'print - not working yet'

g0 = Group('Show/Export Parameters:')
g0.numColumns = 2
g0.add(export_tick, exportfilename, print_tick)



###########################

def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    
    # check if a list of file names has been given
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
    else :
        pass

        f = open(__FOLDER_PATH__ + str(exportfilename.value) + '.csv', 'w+')
        
        i = 0 # so that header is only written once
        
        for fn in fns:
            # load dataset with each file name
            ds = df[fn]
            
            filename = os.path.basename(fn) # gets rid of the path
            filename = filename[:filename.find('.nx.hdf')] # gets rid of the hdf
            
            print filename
            
            header = []
            data = []
            header.append('filname')
            data.append(filename)
            
            
            
            if SampleName_tick.value:                
                ds.__iDictionary__.addEntry('SampleName', 'entry1/sample/name')
                #print 'ds.SampleName', str(ds.SampleName)
                name = str(ds.SampleName)
                data.append(name.replace(',' , '___'))
                header.append('SampleName')
            
            if SampleDescription_tick.value:                
                ds.__iDictionary__.addEntry('SampleDescription', 'entry1/sample/description')
                #print 'ds.SampleDescription', str(ds.SampleDescription)                
                des = str(ds.SampleDescription)
                data.append(des.replace(',' , '___'))
                header.append('SampleDecription')
                
            if SampleThickness_tick.value:                
                ds.__iDictionary__.addEntry('SampleThickness', 'entry1/sample/thickness')
                #print 'ds.SampleThickness', str(ds.SampleThickness)
                data.append(str(ds.SampleThickness))
                header.append('SampleThickness')
                
            if SamplePosition_tick.value:                
                ds.__iDictionary__.addEntry('SamplePosition', 'entry1/sample/samz')
                #print 'ds.SamplePosition', str(ds.SamplePosition[0])
                try:
                    data.append(str(ds.SamplePosition[0]))
                except:
                    data.append(str(ds.SamplePosition))
                header.append('SamplePosition')
                
            if NumberOfPoints_tick.value:                               
                ds.__iDictionary__.addEntry('NumberOfPoints', 'entry1/sample/samz')
                if print_tick.value:
                    try:
                        print 'NumberOfPoints', str(len(ds.NumberOfPoints))
                    except:
                        print 'NumberOfPoints == 1'
                try:                    
                    data.append(str(len(ds.NumberOfPoints)))
                except:
                    data.append('1')
                header.append('NumberOfPoints')
                
            if StartTime_tick.value:                
                ds.__iDictionary__.addEntry('StartTime', 'entry1/start_time')
                #print 'ds.StartTime', str(ds.StartTime)
                data.append(str(ds.StartTime[0]))
                header.append('StartTime')
                
                
            if EndTime_tick.value:                
                ds.__iDictionary__.addEntry('EndTime', 'entry1/end_time')
                #print 'ds.EndTime', str(ds.EndTime)
                try:                    
                    data.append(str(ds.EndTime[0]))
                except:
                    data.append(str(ds.EndTime))
                header.append('EndTime')
                
            if RunTime_tick.value:                
                ds.__iDictionary__.addEntry('TimeStamp', 'entry1/time_stamp')
                ds.__iDictionary__.addEntry('CountTimes', 'entry1/instrument/detector/time')
                try: 
                    TotalTime = ds.TimeStamp[-1] + ds.CountTimes[0]
                    h      = TotalTime // 3600
                    h_left = TotalTime % 3600
                    min    = h_left // 60
                    sec    = h_left % 60
                    TotalTime = "%02i:%02i:%02i" % (h, min, sec)        
                    data.append(TotalTime)
                    header.append('TotalTime')
                except:
                    pass
        
        
                
            if WaveLength_tick.value:                
                ds.__iDictionary__.addEntry('WaveLength', 'entry1/instrument/crystal/wavelength')
                #print 'ds.WaveLength', str(ds.WaveLength)
                data.append(str(ds.WaveLength))
                header.append('WaveLength')
                
            if ScanVariable_tick.value:                
                ds.__iDictionary__.addEntry('ScanVariable', 'entry1/instrument/crystal/scan_variable')
                #print 'ds.WaveLength', str(ds.WaveLength)
                data.append(str(ds.ScanVariable))
                header.append('ScanVariable')
                
                
                
                
                
            if pmchi_tick.value:                
                ds.__iDictionary__.addEntry('pmchi', 'entry1/instrument/crystal/pmchi')
                #print 'ds.pmchi', str(ds.pmchi[0])
                try:
                    data.append(str(ds.pmchi[0]))
                except:
                    data.append(str(ds.pmchi))
                header.append('pmchi')
                
            if pmom_tick.value:                
                ds.__iDictionary__.addEntry('pmom', 'entry1/instrument/crystal/pmom')
                #print 'ds.pmom', str(ds.pmom[0])
                try:
                    data.append(str(ds.pmom[0]))
                except:
                    data.append(str(ds.pmom))
                header.append('pmom')
                
            if bex_tick.value:                
                ds.__iDictionary__.addEntry('bex', 'entry1/instrument/crystal/bex')
                #print 'ds.bex', str(ds.bex[0])
                try:
                    data.append(str(ds.bex[0]))
                except:
                    data.append(str(ds.bex))
                header.append('bex')
                
            if m1chi_tick.value:                
                ds.__iDictionary__.addEntry('m1chi', 'entry1/instrument/crystal/m1chi')
                #print 'ds.m1chi', str(ds.m1chi[0])
                try:
                    data.append(str(ds.m1chi[0]))
                except:
                    data.append(str(ds.m1chi))                  
                header.append('m1chi')
                
            if m1x_tick.value:                
                ds.__iDictionary__.addEntry('m1x', 'entry1/instrument/crystal/m1x')
                #print 'ds.m1x', str(ds.m1x[0])
                try:
                    data.append(str(ds.m1x[0]))
                except:
                    data.append(str(ds.m1x))
                header.append('m1x')
                
            if m1om_tick.value:                
                ds.__iDictionary__.addEntry('m1om', 'entry1/instrument/crystal/m1om')
                #print 'ds.m1om', str(ds.m1om[0])
                try:
                    data.append(str(ds.m1om[0]))
                except:
                    data.append(str(ds.m1om))
                header.append('m1om')
                
            if m2chi_tick.value:                
                ds.__iDictionary__.addEntry('m2chi', 'entry1/instrument/crystal/m2chi')
                #print 'ds.m2chi', str(ds.m2chi[0])
                try:
                    data.append(str(ds.m2chi[0]))
                except:
                    data.append(str(ds.m2chi))
                header.append('m2chi')
                
            if m2x_tick.value:                
                ds.__iDictionary__.addEntry('m2x', 'entry1/instrument/crystal/m2x')
                #print 'ds.m2x', str(ds.m2x[0])
                try:
                    data.append(str(ds.m2x[0]))
                except:
                    data.append(str(ds.m2x))
                header.append('m2x')
                
            if m2y_tick.value:                
                ds.__iDictionary__.addEntry('m2y', 'entry1/instrument/crystal/m2y')
                #print 'ds.m2y', str(ds.m2y[0])
                try:
                    data.append(str(ds.m2chi[0]))
                except:
                    data.append(str(ds.m2chi))
                header.append('m2y')
                
            if m2om_tick.value:                
                ds.__iDictionary__.addEntry('m2om', 'entry1/instrument/crystal/m2om')
                #print 'ds.m2om', str(ds.m2om[0])
                try:
                    data.append(str(ds.m2om[0]))
                except:
                    data.append(str(ds.m2om))
                header.append('m2om')
                
            if mdet_tick.value:                
                ds.__iDictionary__.addEntry('mdet', 'entry1/instrument/crystal/mdet')
                #print 'ds.mdet', str(ds.mdet[0])
                try:
                    data.append(str(ds.mdet[0]))
                except:
                    data.append(str(ds.mdet))
                header.append('mdet')
                
            if ss1vg_tick.value:                
                ds.__iDictionary__.addEntry('ss1vg', 'entry1/instrument/slits/gaps/ss1vg')
                #print 'ds.ss1vg', str(ds.ss1vg[0])
                try:
                    data.append(str(ds.ss1vg[0]))
                except:
                    data.append(str(ds.ss1vg))
                header.append('ss1vg')
                
            if ss1hg_tick.value:                
                ds.__iDictionary__.addEntry('ss1hg', 'entry1/instrument/slits/gaps/ss1hg')
                #print 'ds.ss1hg', str(ds.ss1hg[0])
                try:
                    data.append(str(ds.ss1hg[0]))
                except:
                    data.append(str(ds.ss1hg))
                header.append('ss1hg')
                
            if ss1vo_tick.value:                
                ds.__iDictionary__.addEntry('ss1vo', 'entry1/instrument/slits/gaps/ss1vo')
                #print 'ds.ss1vo', str(ds.ss1vo[0])
                try:
                    data.append(str(ds.ss1vo[0]))
                except:
                    data.append(str(ds.ss1vo))
                header.append('ss1vo')
                
            if ss1ho_tick.value:                
                ds.__iDictionary__.addEntry('ss1ho', 'entry1/instrument/slits/gaps/ss1ho')
                try:
                    data.append(str(ds.ss1ho[0]))
                except:
                    data.append(str(ds.ss1ho))
                header.append('ss1ho')
                
                
            if tempSensorC_tick.value:                
                ds.__iDictionary__.addEntry('sensorC', 'entry1/sample/tc3/sensor/sensorValueC')
                #print ds.sensorC
                try:
                    sensorC0 = float(ds.sensorC[0])-273.15
                    data.append(str(sensorC0))
                except:
                    data.append(str(ds.sensorC[0]))
                header.append('sensorC')
                
            if tempSensorD_tick.value:                
                ds.__iDictionary__.addEntry('sensorD', 'entry1/sample/tc3/sensor/sensorValueD')
                try:
                    sensorD0 = float(ds.sensorD[0])-273.15
                    data.append(str(sensorD0))
                except:
                    data.append(str(ds.sensorD[0]))
                header.append('sensorD')
                
            if tempvTE_sp_tick.value:                
                ds.__iDictionary__.addEntry('vTE_setpoint', 'entry1/sample/tc2/Loop1/vSP')
                #print 'ds.ss1ho', str(ds.ss1ho[0])
                try:
                    data.append(str(ds.vTE_setpoint[0]))
                    header.append('vTE_setpoint')
                except:
                    pass

            if tempvTE_sensor_tick.value:                
                ds.__iDictionary__.addEntry('vTE_sensor', 'entry1/sample/tc2/Loop1/sensor')
                #print 'ds.ss1ho', str(ds.ss1ho[0])
                try:
                    data.append(str(ds.vTE_sensor[0]))
                    header.append('vTE_sensor')
                except:
                    pass
            
            
            if ReactorPower_tick.value:                
                ds.__iDictionary__.addEntry('ReactorPower', 'entry1/instrument/source/power')
                #print 'ds.ss1ho', str(ds.ss1ho[0])
                try:
                    data.append(str(ds.ReactorPower[0]))
                except:
                    data.append(str(ds.ReactorPower))
                header.append('ReactorPower')
                
                
            if CNSout_tick.value:                
                ds.__iDictionary__.addEntry('CNS_out', 'entry1/instrument/source/cns_out')
                #print 'ds.ss1ho', str(ds.ss1ho[0])
                try:
                    data.append(str(ds.CNS_out[0]))
                except:
                    data.append(str(ds.CNS_out))
                header.append('CNS_out')
            
            
                
                
            if BeamMonitor_tick.value:                
                ds.__iDictionary__.addEntry('BM_Counts', 'entry1/monitor/bm1_counts')
                ds.__iDictionary__.addEntry('BM_Time', 'entry1/monitor/bm1_time')
                #print 'ds.ss1ho', str(ds.ss1ho[0])
                try:
                    data.append(str(ds.BM_Counts[0]))
                    data.append(str(ds.BM_Time[0]))
                    BM_Rate = float(ds.BM_Counts[0])/float(ds.BM_Time[0])
                    data.append(str(BM_Rate))
                except:
                    data.append(str(ds.BM_Counts))
                    data.append(str(ds.BM_Time))
                    BM_Rate = float(ds.BM_Counts)/float(ds.BM_Time)
                    data.append(str(BM_Rate))
                    
                header.append('BM_Counts')
                header.append('BM_Time')
                header.append('BM_Rate')
                
                
            if (Tube6_tick.value) or (Tube7_tick.value):  # probably this does not work if there is only one value
                ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm')                              
                ds.__iDictionary__.addEntry('Det_Time', 'entry1/instrument/detector/time')
                
                if (Tube6_tick.value):
                    Tube6_Counts=[]
                    if ds.hmm.ndim == 4:
                        Tube6_Counts[:] = ds.hmm[:, 0, :, 6].sum(0) # hmm
                        Tube6_Counts1 = Tube6_Counts[0]
                    else:
                        Tube6_Counts[:] = ds.hmm[:, :, 6].sum(0)    # hmm_xy 
                        Tube6_Counts1 = Tube6_Counts[0]
                        #Tube6_Counts1 = Tube6_Counts[:].sum(0)
                    try:
                        Det_Time1 = ds.Det_Time[0]
                    except:
                        Det_Time1 = ds.Det_Time
               
                
                    print Tube6_Counts1
                    print Det_Time1
                        
                    
                    data.append(str(Tube6_Counts1))
                    data.append(str(Det_Time1))
                    Tube6_Rate = float(Tube6_Counts1)/float(Det_Time1)
                    data.append(str(Tube6_Rate))
                    
                header.append('Tube6_Counts')
                header.append('Tube6_Time')
                header.append('Tube6_Rate')
                
                if (Tube7_tick.value):
                    Tube7_Counts=[]
                    if ds.hmm.ndim == 4:
                        Tube7_Counts[:] = ds.hmm[:, 0, :, 7].sum(0) # hmm
                        Tube7_Counts1 = Tube7_Counts[0]
                    else:
                        Tube7_Counts[:] = ds.hmm[:, :, 7].sum(0)    # hmm_xy 
                        Tube7_Counts1 = Tube7_Counts[0]
                        #Tube6_Counts1 = Tube6_Counts[:].sum(0)
                    try:
                        Det_Time1 = ds.Det_Time[0]
                    except:
                        Det_Time1 = ds.Det_Time
               
                
                    print Tube7_Counts1
                    print Det_Time1
                        
                    
                    data.append(str(Tube7_Counts1))
                    data.append(str(Det_Time1))
                    Tube7_Rate = float(Tube7_Counts1)/float(Det_Time1)
                    data.append(str(Tube7_Rate))
                    
                header.append('Tube7_Counts')
                header.append('Tube7_Time')
                header.append('Tube7_Rate')
                
                
           
            
            
                
            
                
            print ''

            
            if i == 0:
                for h in range(len(header)):                  
                    f.write(header[h])
                    f.write(',') 
                f.write('\n')    
            i = 1          
            
            for h in range(len(data)):           
                f.write(data[h])
                f.write(',')
            f.write('\n')

            
            
        f.close()
        print 'finished output ' + f.name               
                

            
   
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()

# not used yet:    
def MeasurementTime(self):   
        
        TotalTime = self.TimeStamp[-1] + self.CountTimes[0] # first point is detector time for the first point
        
        h      = TotalTime // 3600
        
        h      = TotalTime // 3600
        h_left = TotalTime % 3600
        min    = h_left // 60
        sec    = h_left % 60
        
        self.TotalTime_form = "%02i:%02i:%02i" % (h, min, sec)

        
        print 'Total Run Time: ' + self.TotalTime_form + ' [h:min:sec]'          
        print ''
        
        for i in xrange(len(self.TimeStamp)-1):
            self.ActualTime[i+1] = self.TimeStamp[i+1]-self.TimeStamp[i]
    
