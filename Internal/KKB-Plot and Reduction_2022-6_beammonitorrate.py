


# Script control setup area
# script info
__script__.title = 'KKB Plot and Reduction 08.06.2022'
__script__.version = '2.0'



# 15.6.2017 Allow to reduce the detector range 
# 15.6. Throw out points below resolution
# 16.6. Tidy up run time to display in the reduction; tidy up display properties
# 11.7.2018 Start changing deadtime
# 12.7.2018 Implement Plot for monitoring Tube6 and Tube7
# June 2019 Add temperature and "raw" to name
# June 2019 Incorporate time dependance into batch reduce
# June 2019 Create batch mode overview file
# Sep 2020 Create proper putputformats also for batch reduce
# Feb 21 batch mode
# March 21 Use tube 6 as beam monitor - brute force
# December 21: can now use either tube6 or bm as monitor
# December 27: include new file with Tsas m2om0 I0 and Iwide in progress
# 2022 Jan 22: include export for batch file. To be copid onto DAV1 
# 2022 June 15: incorporate 


from math import sqrt, sin, exp
from datetime import datetime, timedelta
from bisect import bisect_left
from __builtin__ import max as builtin_max
from __builtin__ import min as builtin_min

# TO ADD A FORTH PLOT
try :
    Plot_START.close()
    Plot4.close()
except:
    pass
Plot_START =  plot()
Plot4 =  plot()



'''

    INPUT

'''



combine_tube0 = Par('bool', True)
combine_tube0.title = '  Tube 0'

combine_tube1 = Par('bool', True)
combine_tube1.title = '    Tube 1'

combine_tube2 = Par('bool', True)
combine_tube2.title = '    Tube 2'

combine_tube3 = Par('bool', True)
combine_tube3.title = '    Tube 3'

combine_tube4 = Par('bool', True)
combine_tube4.title = '    Tube 4'

use_beammonitor = Par('bool', False)
use_beammonitor.title = 'Use Beam Monitor'

defaultMCR = Par('float', '2000')
defaultMCR.title = 'Default MCR'

medianMCR = Par('string', '0')
medianMCR.title = 'Median MCR'
medianMCR.enabled = False

use_medianMCRPlot = Par('bool', False)
use_medianMCRPlot.title = 'Use Median MCR for plot'

use_tube6_monitor = Par('bool', False)
use_tube6_monitor.title = 'Use Tube6 Monitor'

defaultMCR_tube6 = Par('float', '4000')
defaultMCR_tube6.title = 'Default MCR tube6'

TWideMarker = Par('float', '2e-3')
TWideMarker.title = 'TWide Marker (1/A)'

convert2q = Par('bool', True)
convert2q.title = 'Convert to q'

negative_steps = Par('bool', False)
negative_steps.title = 'Negative Steps'

sort_scanvar = Par('bool', True)
sort_scanvar.title = 'Sort Scan Variable'

limit_lowq = Par('bool', True)
limit_lowq.title = 'Cut low q'

limit_lowq_number = Par('float', '1.8e-5')
limit_lowq_number.title = 'below Ang^-1'

remove_duplicate_points = Par('bool', True)
remove_duplicate_points.title = 'Remove Duplicate Points'

# FIXED construction site
fix_m2om0_int0 = Par('bool', False)
fix_m2om0_int0.title = 'Fix m2om 0-position and intensity'

m2om0_fixed = Par('float', '179.38')
m2om0_fixed.title = 'm2om (q=0)'

int0_fixed = Par('float', '33972.452')
int0_fixed.title = 'Intensity(q=0)'

fix_Iwide = Par('bool', False)
fix_Iwide.title = 'Fix Iwide'

Iwide_fixed = Par('float', '674.0')
Iwide_fixed.title = 'I(wide)'

# limit detector
limit_detector = Par('bool', False)
limit_detector.title = 'Limit detector'

detectorheight_start = Par('integer', '0')
detectorheight_start.title = 'Start'

detectorheight_end = Par('integer', '1023')
detectorheight_end.title = 'End'       

# SAMPLE INPUT
Thickness = Par('float', 'NaN')
Thickness.title = ''
Thickness.enabled = False
Thickness_Patching = Par('bool', False, command='Thickness.enabled = Thickness_Patching.value')
Thickness_Patching.title = ''
Thickness_FromFile = Par('float', 'NaN')
Thickness_FromFile.title = 'Sample Thickness (mm)'
Thickness_FromFile.enabled = False

SampleName = Par('string', 'patch?')
SampleName.title = ''
SampleName.enabled = False
SampleName_Patching = Par('bool', False, command='SampleName.enabled = SampleName_Patching.value')
SampleName_Patching.title = ''
SampleName_FromFile = Par('string', 'NaN')
SampleName_FromFile.title = 'Sample Name'
SampleName_FromFile.enabled = False

SampleDescr = Par('string', 'patch?')
SampleDescr.title = ''
SampleDescr.enabled = False
SampleDescr_Patching = Par('bool', False, command='SampleDescr.enabled = SampleDescr_Patching.value')
SampleDescr_Patching.title = ''
SampleDescr_FromFile = Par('string', 'NaN')
SampleDescr_FromFile.title = 'Sample Description'
SampleDescr_FromFile.enabled = False

SampleBkg = Par('float', 'NaN')
SampleBkg.title = ''
SampleBkg.enabled = False
SampleBkg_Patching = Par('bool', False, command='SampleBkg.enabled = SampleBkg_Patching.value')
SampleBkg_Patching.title = ''
SampleBkg_FromFile = Par('string', 'NaN')
SampleBkg_FromFile.title = 'Ambient Background'
SampleBkg_FromFile.enabled = False

samIgnorePts = Par('string', '')
samIgnorePts.title = 'Ignore Sample Data Points' 
samIgnorePts.colspan = 1

g2 = Group('SAMPLE')
g2.numColumns = 3
g2.add(SampleName_FromFile,SampleName_Patching,SampleName,
       SampleDescr_FromFile,SampleDescr_Patching,SampleDescr,
       Thickness_FromFile,Thickness_Patching,Thickness,      
       SampleBkg_FromFile,SampleBkg_Patching,SampleBkg,
       samIgnorePts)


# add 2018-07-11 Deadtime
DeadTime = Par('float', 'NaN')
DeadTime.title = ''
DeadTime.enabled = False
DeadTime_Patching = Par('bool', False, command='DeadTime.enabled = DeadTime_Patching.value')
DeadTime_Patching.title = ''
DeadTime_FromFile = Par('string', 'NaN')
DeadTime_FromFile.title = 'Deadtime'
DeadTime_FromFile.enabled = False
DeadTimeTypePara = Par('bool', True)
DeadTimeTypePara.title = 'Paralysable'
DeadTimeTypeNonPara = Par('bool', False)
DeadTimeTypeNonPara.title = 'Non-paralysable'

TemperatureVTE_setpoint = Par('bool', False)
TemperatureVTE_setpoint.title = 'Temperature VTE setpoint'
TemperatureVTE = Par('bool', False)
TemperatureVTE.title = 'Temperature VTE'
TemperatureLSC = Par('bool', False)
TemperatureLSC.title = 'Temperature LS-C'
TemperatureLSD = Par('bool', False)
TemperatureLSD.title = 'Temperature LS-D'

CreateBatchOverView_points = Par('bool', True)
CreateBatchOverView_points.title = 'Create Batch Overview Points'
CreateBatchOverView_points_file = Par('string', 'test.csv')
CreateBatchOverView_points_file.title = 'filename'

CreateBatchOverView_Tsas = Par('bool', True)
CreateBatchOverView_Tsas.title = 'Create Batch Overview Tsas'
CreateBatchOverView_Tsas_file = Par('string', 'test_Tsas.csv')
CreateBatchOverView_Tsas_file.title = 'filename'




def clearPlots():
    global Plot1
    global Plot2
    global Plot3
    global Plot_START
    global Plot4
    Plot1.clear()
    Plot2.clear() 
    Plot3.clear()
    Plot_START.clear()
    Plot4.clear()
    '''
    try :
       Plot_START.close()
    except:
       pass
    '''
    
def __run_script__(fns):
              
    datasets = __DATASOURCE__.getSelectedDatasets()
    for sds in datasets:
            ds = Dataset(str(sds.getLocation()))
            SampleName_FromFile.value   = str(ds['entry1/sample/name'             ])
            SampleDescr_FromFile.value  = str(ds['entry1/sample/description'      ])
            Thickness_FromFile.value    = float(ds['entry1/sample/thickness'        ])
            SampleBkg_FromFile.value    = float(ds['entry1/experiment/bkgLevel'     ])
            DeadTime_FromFile.value     = float(ds['entry1/instrument/detector/MainDeadTime'     ])
        
    dsFilePaths = [str(ds.getLocation()) for ds in __DATASOURCE__.getSelectedDatasets()]
        
    if len(dsFilePaths) == 0:
        print 'Warning: no Sample Scans were selected'
        return
        
    # get name of first sample file
    filename = os.path.basename(dsFilePaths[0])
    filename = filename[:filename.find('.nx.hdf')]
    
    path = 'V:/shared/KKB Logbook/Temp Plot Data Repository/'    
           
    ds = LoadNxHdf(dsFilePaths)
   
    ds.MeasurementTime()
    if sort_scanvar.value:
        ds.SortAngles()    
    ds = RemoveIgnoredRanges(ds, samIgnorePts.value)
    
    if convert2q.value:                       
       # under fix construction
        if fix_m2om0_int0.value:
            ds.PeakAng = m2om0_fixed.value
            ds.PeakVal = int0_fixed.value
            print 'Peak angle is fixed to ', m2om0_fixed.value
            print 'I(rock) is fixed to ', int0_fixed.value 
        else:
            ds.FindZeroAngle()      
            
        ds.DetermineQVals()  
        
        # under construction
        if fix_Iwide.value:
            print 'I(wide) is fixed to ', Iwide_fixed.value
            ds.TWideCtr = Iwide_fixed.value
        else:
            ds.FindTWideCtr()           
        
    else:
        ds.Qvals = copy(ds.Angle)
    
    
    if TemperatureVTE_setpoint.value:   
            ds.SaveRaw(path + filename + '_' + ds.SampleName + '_tempVTEsp_' + str(int(ds.TempvTE_sp)) + 'C-raw.dat')
            #ds.SaveRaw_Mantid(path + 'Mantid_' + filename + '_' + ds.SampleName + '_tempVTEsp_' + str(int(ds.TempvTE_sp)) + 'C-raw.dat')
    elif TemperatureVTE.value:
            ds.SaveRaw(path + filename + '_' + ds.SampleName + '_tempVTE_' + str(int(ds.TempvTE)) + 'C-raw.dat')
            #ds.SaveRaw_Mantid(path + 'Mantid_' + filename + '_' + ds.SampleName + '_tempVTE_' + str(int(ds.TempvTE)) + 'C-raw.dat')
    elif TemperatureLSC.value:
            ds.SaveRaw(path + filename + '_' + ds.SampleName + '_tempLSC_' + str(int(ds.TempLSC)) + 'C-raw.dat')
            #ds.SaveRaw_Mantid(path + 'Mantid_' + filename + '_' + ds.SampleName + '_tempLSC_' + str(int(ds.TempLSC)) + 'C-raw.dat')
    elif TemperatureLSD.value:
            ds.SaveRaw(path + filename + '_' + ds.SampleName + '_tempLSD_' + str(int(ds.TempLSD)) + 'C-raw.dat')
            #ds.SaveRaw_Mantid(path + 'Mantid_' + filename + '_' + ds.SampleName + '_tempLSD_' + str(int(ds.TempLSD)) + 'C-raw.dat')
    else:
        ds.SaveRaw(path + filename + '_' + ds.SampleName + '-raw.dat')
        #ds.SaveRaw(path + filename + '-raw.dat')
        #ds.SaveRaw_Mantid(path + 'Mantid_' + filename + '_' + ds.SampleName + '-raw.dat')
        #ds.SaveRaw(path + filename + '_raw.dat')
        
    
    # determine median beam-monitor count rate
    buffer = list(ds.MonCtr)
    buffer.sort()
    n = len(buffer)
    if n == 0:
        medianMCR.value = 'nan'
    elif n % 2 == 1:
        medianMCR.value = '%.0f' % (buffer[n/2])
    else:
        medianMCR.value = '%.0f' % ((buffer[n/2 - 1] + buffer[n/2]) / 2.0)
    
    PlotTransmissionDataset(Plot1, ds, filename + ': ' + ds.SampleName)   
    PlotMonitorDataset(Plot2, ds, filename + ': ' + ds.SampleName)
    PlotDataset_log(Plot3, ds, filename + ': ' + ds.SampleName)
    PlotDataset(Plot_START, ds, filename + ': ' + ds.SampleName)
    
    Plot3.add_y_marker(ds.SampleBkg, 6000, 'blue')    
    Plot_START.add_y_marker(ds.SampleBkg, 6000, 'blue')
    
    PlotTube67Dataset(Plot4, ds, 'tube6', filename + ': ' + ds.SampleName)


#########################################################################################
# EMPTY SAMPLE COMPARTMENT

empFiles = Par('string', '')
empFiles.title = 'Files' 
empFilesTakeBtn = Act('empFilesTake()', 'Select As Empty Sample Container')

empIgnorePts = Par('string', '')
empIgnorePts.title = 'Ignore Data Points' 

empLevel = Par('float', '0')
empLevel.title = 'Empty Level'
empLevel_Error = Par('float', '0')
empLevel_Error.title = ' Actual Error'
empLevel_Error.enabled = False
empLevel_tailpoints = Par('int', '5')
empLevel_tailpoints.title = 'Tail Points'

g3 = Group('EMPTY SAMPLE CONTAINER')
g3.numColumns = 2
g3.add(empFiles, empFilesTakeBtn,empIgnorePts,  empLevel, 
        empLevel_tailpoints,empLevel_Error)


def empFilesTake():
    fns = None
    for sds in __DATASOURCE__.getSelectedDatasets():
        basename = os.path.basename(str(sds.getLocation()))
        basename = basename[:basename.find('.nx.hdf')]

        if fns is None:
            fns = basename
        else:
            fns += ', ' + basename
            
    if fns is None:
        empFiles.value = ''
    else:
        empFiles.value = fns
    
    tailpoints = int(empLevel_tailpoints.value)
    if tailpoints < 1:
        print 'tail point needs to be greater than 0'
        return
    
    # find empty files
    emFileList = filter(None, str(empFiles.value).split(','))
    for i in xrange(0, len(emFileList)):
        emFileList[i] = emFileList[i].strip()

    emFilePaths = []
    if len(emFileList) != 0:
        for emFile in emFileList:
            found = False
            
            for ds in __DATASOURCE__.getDatasetList():
                dsLocation = str(ds.getLocation())
                if emFile in dsLocation:
                    if not found:
                        emFilePaths.append(dsLocation)
                        found = True
                    else:
                        print 'Warning: "%s" has multiple matches' % emFile
                        break
                    
            if not found:
                print 'Warning: "%s" was not found' % emFile
          
    if len(emFilePaths) == 0:
        print 'Warning: no Empty Scans were selected'
        return
  
    em = LoadNxHdf(emFilePaths)                           
    em.SortAngles()    
    em = RemoveIgnoredRanges(em, empIgnorePts.value)
    
    
    
    if bool(negative_steps.value):
        empLevel.value = sum(em.DetCtr[:tailpoints]) / tailpoints
        empLevel_Error.value = sum(em.ErrDetCtr[:tailpoints]) / tailpoints 
    else:
        empLevel.value = sum(em.DetCtr[-tailpoints:]) / tailpoints
        empLevel_Error.value = sum(em.ErrDetCtr[-tailpoints:]) / tailpoints 
    
    
    
    em.FindZeroAngle()
    em.DetermineQVals()
    em.MeasurementTime()
    
    filename = os.path.basename(emFilePaths[0])
    filename = filename[:filename.find('.nx.hdf')]
    path = 'V:/shared/KKB Logbook/Temp Plot Data Repository/'

    em.SaveRaw(path + filename + '-empty.dat')
    
    global Plot_START
    global Plot4
    
    #print dir(em)
    PlotDataset(Plot_START, em, 'EMPTY: ' + filename)
    PlotDataset_log(Plot3, em, 'EMPTY: ' + filename)   
    for i in xrange(tailpoints):
        x = em.Qvals[-i-1]
        y = em.DetCtr[-i-1]
        Plot_START.add_marker(x, y, 'red')
        Plot3.add_marker(x, y, 'red')
        
    # ADD IGNORED RANGE
    
    Plot3.add_y_marker(empLevel.value, 6000, 'red')    
    Plot_START.add_y_marker(empLevel.value, 6000, 'red')
    
    PlotTransmissionDataset(Plot1, em, 'EMPTY: ' + filename)
    
    PlotMonitorDataset(Plot2, em, 'EMPTY: ' + filename)

steps_label = Par('label', '')
steps_label.colspan = 2
steps_label = Par('label', '')
steps_label.colspan = 2


clearPlotsBtn = Act('clearPlots()', '*** CLEAR ALL PLOTS ***')


steps_label = Par('label', '')
steps_label.colspan = 2

######################################################################################

reduceStitchedFilesBtn = Act('reduceStitchedFiles()', '*** REDUCE SINGLE (STITCHED) FILES ***')        
reduceStitchedFilesBtn.colspan = 1

def reduceStitchedFiles():
    
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    global Plot_START
    global Plot4
    
    
    Plot1.clear()
    Plot2.clear() 
    Plot3.clear() 
    Plot_START.clear()
    Plot4.clear() 
       
    # find empty files
    emFileList = filter(None, str(empFiles.value).split(','))
    for i in xrange(0, len(emFileList)):
        emFileList[i] = emFileList[i].strip()

    emFilePaths = []
    if len(emFileList) != 0:
        for emFile in emFileList:
            found = False
            
            for ds in __DATASOURCE__.getDatasetList():
                dsLocation = str(ds.getLocation())
                if emFile in dsLocation:
                    if not found:
                        emFilePaths.append(dsLocation)
                        found = True
                    else:
                        print 'Warning: "%s" has multiple matches' % emFile
                        break
                    
            if not found:
                print 'Warning: "%s" was not found' % emFile
                
    if len(emFilePaths) == 0:
        print ''
        print 'WARNING: Please select an empty sample container'
        return

    # find sample files    
    dsFilePaths = [str(ds.getLocation()) for ds in __DATASOURCE__.getSelectedDatasets()]
        
    if len(dsFilePaths) == 0:
        print 'Warning: no Sample Scans were selected'
        return

    # reduction
        
    # get name of first sample file
    filename = os.path.basename(dsFilePaths[0])
    filename = filename[:filename.find('.nx.hdf')]
    
    path = 'V:/shared/KKB Logbook/Temp Plot Data Repository/'          
        
    datasets = __DATASOURCE__.getSelectedDatasets()
    for sds in datasets:
        ds = Dataset(str(sds.getLocation()))
        SampleName_FromFile.value   = str(ds['entry1/sample/name'             ])
        SampleDescr_FromFile.value  = str(ds['entry1/sample/description'      ])
        Thickness_FromFile.value    = float(ds['entry1/sample/thickness'        ])
        SampleBkg_FromFile.value    = float(ds['entry1/experiment/bkgLevel'     ])         
    
    print ''    
    print '*** REDUCTION ****'
    print ''
    print '*** SAMPLE:', ', '.join(dsFilePaths)
    ds = LoadNxHdf(dsFilePaths)  
    ds.MeasurementTime()
    
    if ds.ScanVariablename == 'm2om':
        pass
    else:
        raise Exception ("This is not an m2om scan")
    if convert2q.value:
        pass
    else:
        raise Exception("Please tick 'Convert to q'")
    
    ds.SortAngles()    
    ds = RemoveIgnoredRanges(ds, samIgnorePts.value)                          
        
    # under fix construction
    if fix_m2om0_int0.value:
        ds.PeakAng = m2om0_fixed.value
        ds.PeakVal = int0_fixed.value
        print 'Peak angle is fixed to ', m2om0_fixed.value
        print 'I(rock) is fixed to ', int0_fixed.value 
    else:
        ds.FindZeroAngle()      
        
    ds.DetermineQVals()  
    
    # under construction
    if fix_Iwide.value:
        print 'I(wide) is fixed to ', Iwide_fixed.value
        ds.TWideCtr = Iwide_fixed.value
    else:
        ds.FindTWideCtr()
     
    PlotDataset(Plot_START, ds, 'SAM: '+ filename)
    PlotTransmissionDataset(Plot1, ds, 'SAM: '+ filename)
    PlotMonitorDataset(Plot2, ds, 'SAM: '+ filename)
    PlotDataset_log(Plot3, ds, 'SAM: '+ filename)      
    
    print ''
    print '*** EMPTY: ', ', '.join(emFilePaths)
    em = LoadNxHdf(emFilePaths)
    em.MeasurementTime()
    
    if em.ScanVariablename == 'm2om':
        pass
    else:
        raise Exception ("This is not an m2om scan")
    if convert2q.value:
        pass
    else:
        raise Exception("Please tick 'Convert to q'")
    
    em.SortAngles()
    em = RemoveIgnoredRanges(em, empIgnorePts.value)
    em.FindZeroAngle()
    em.DetermineQVals()
    em.FindTWideCtr()    
    
    PlotDataset(Plot_START, em, 'EMPTY')
    PlotTransmissionDataset(Plot1, em, 'EMPTY')
    PlotMonitorDataset(Plot2, em, 'EMPTY')
    PlotDataset_log(Plot3, em, 'EMPTY')
    Plot3.add_y_marker(em.empLevel, 6000, 'green')
    Plot_START.add_y_marker(em.empLevel, 6000, 'green')
    Plot3.add_y_marker(em.SampleBkg, 6000, 'blue')
    Plot_START.add_y_marker(em.SampleBkg, 6000, 'blue')
    
    # correction
    ds.CorrectData(em)
    
    
    
    q_cut = False # to cut the low q-values
    
    if limit_lowq.value:
        q_cut = True
        ds.Qvals_cut = []
        ds.DetCtr_cut = []
        ds.ErrDetCtr_cut = []

        for i in xrange(len(ds.Qvals)):                    
            if ds.Qvals[i] > limit_lowq_number.value:              
                ds.Qvals_cut.append(ds.Qvals[i])
                ds.DetCtr_cut.append(ds.DetCtr[i])
                ds.ErrDetCtr_cut.append(ds.ErrDetCtr[i])
                
        if TemperatureVTE_setpoint.value:   
                ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '_tempVTEsp_' + str(int(ds.TempvTE_sp)) + 'C-abs_cut.dat')
                #ds.SaveAbs_cut_Mantid( path + 'Mantid_' + filename + '_' + ds.SampleName + '_tempVTEsp_' + str(int(ds.TempvTE_sp)) + '-abs_cut.dat')
        elif TemperatureVTE.value:
                ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '_tempVTE_' + str(int(ds.TempvTE)) + 'C-abs_cut.dat')
                #ds.SaveAbs_cut_Mantid( path + 'Mantid_' + filename + '_' + ds.SampleName + '_tempVTE_' + str(int(ds.TempvTE)) + '-abs_cut.dat')
        elif TemperatureLSC.value:
                ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '_tempLSC_' + str(int(ds.TempLSC)) + 'C-abs_cut.dat')
                #ds.SaveAbs_cut_Mantid( path + 'Mantid_' + filename + '_' + ds.SampleName + '_tempLSC_' + str(int(ds.TempLSC)) + '-abs_cut.dat')
        elif TemperatureLSD.value:
                ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '_tempLSD_' + str(int(ds.TempLSD)) + 'C-abs_cut.dat')
                #ds.SaveAbs_cut_Mantid( path + 'Mantid_' + filename + '_' + ds.SampleName + '_tempLSD_' + str(int(ds.TempLSD)) + '-abs_cut.dat')
        else:
            ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '-abs_cut.dat')
            #ds.SaveAbs_cut_Mantid( path + 'Mantid_' + filename + '_' + ds.SampleName + '-abs_cut.dat')   
        

    if TemperatureVTE_setpoint.value:   
            ds.SaveAbs(path + filename + '_' + ds.SampleName + '_tempVTEsp_' + str(int(ds.TempvTE_sp)) + 'C-abs.dat')
    elif TemperatureVTE.value:
            ds.SaveAbs(path + filename + '_' + ds.SampleName + '_tempVTE_' + str(int(ds.TempvTE)) + 'C-abs.dat')
    elif TemperatureLSC.value:
            ds.SaveAbs(path + filename + '_' + ds.SampleName + '_tempLSC_' + str(int(ds.TempLSC)) + 'C-abs.dat')
    elif TemperatureLSD.value:
            ds.SaveAbs(path + filename + '_' + ds.SampleName + '_tempLSD_' + str(int(ds.TempLSD)) + 'C-abs.dat')
    else:
        ds.SaveAbs(path + filename + '_' + ds.SampleName + '-abs.dat')

    
    PlotDataset_log(Plot3, ds, 'ABS', q_cut)
    PlotDataset(Plot_START, ds, 'ABS', q_cut)    
    Plot3.x_range = [1.6e-5, 0.02]
    
    
######################################################################################

reduceBatchFilesBtn = Act('reduceBatchFiles()', '*** REDUCE BATCH FILES ***')        
reduceBatchFilesBtn.colspan = 1

def reduceBatchFiles():

    # find empty files
    emFileList = filter(None, str(empFiles.value).split(','))
    for i in xrange(0, len(emFileList)):
        emFileList[i] = emFileList[i].strip()

    emFilePaths = []
    if len(emFileList) != 0:
        for emFile in emFileList:
            found = False
            
            for ds in __DATASOURCE__.getDatasetList():
                dsLocation = str(ds.getLocation())
                if emFile in dsLocation:
                    if not found:
                        emFilePaths.append(dsLocation)
                        found = True
                    else:
                        print 'Warning: "%s" has multiple matches' % emFile
                        break
                    
            if not found:
                print 'Warning: "%s" was not found' % emFile
                
    if len(emFilePaths) == 0:
        print ''
        print 'WARNING: Please select an empty sample container'
        return

    print 'empty: ', ', '.join(emFilePaths)
    em = LoadNxHdf(emFilePaths)
    
    if em.ScanVariablename == 'm2om':
        pass
    else:
        raise Exception ("This is not an m2om scan")
    
    if convert2q.value:
        pass
    else:
        raise Exception("Please tick 'Convert to q'")
    
    em.SortAngles()
    em = RemoveIgnoredRanges(em, empIgnorePts.value)
    em.FindZeroAngle()
    em.DetermineQVals()
    em.FindTWideCtr()    

    # find sample files    
    dsFilePaths = [str(ds.getLocation()) for ds in __DATASOURCE__.getSelectedDatasets()]
        
    if len(dsFilePaths) == 0:
        print 'Warning: no Sample Scans were selected'
        return

    # reduction
    path = 'V:/shared/KKB Logbook/Temp Plot Data Repository/'   
    
    # for overview file December 2021
    
    file_names = []
    sample_names = []
    file_start_times = []
    summary_all = []
    summary_all_Tsas = []
    earliest_time = datetime.strptime('2100-01-01 00:00:00','%Y-%m-%d %H:%M:%S') #set this to some time in the future             
            
    
    for dsFilePath in dsFilePaths:
        # get name of sample file
        filename = os.path.basename(dsFilePath)
        filename = filename[:filename.find('.nx.hdf')]

        ds = LoadNxHdf([dsFilePath])  
        
        if ds.ScanVariablename == 'm2om':
            pass
        else:
            raise Exception ("This is not an m2om scan")
        
        if convert2q.value:
            pass
        else:
            raise Exception("Please tick 'Convert to q'")
        
        ds.SortAngles()    
        ds = RemoveIgnoredRanges(ds, samIgnorePts.value)
              
        # under fix construction
        if fix_m2om0_int0.value:
            ds.PeakAng = m2om0_fixed.value
            ds.PeakVal = int0_fixed.value
            print 'Peak angle is fixed to ', m2om0_fixed.value
            print 'I(rock) is fixed to ', int0_fixed.value 
        else:
            ds.FindZeroAngle()      
            
        ds.DetermineQVals()  
        
        # under construction
        if fix_Iwide.value:
            print 'I(wide) is fixed to ', Iwide_fixed.value
            ds.TWideCtr = Iwide_fixed.value
        else:
            ds.FindTWideCtr()

        # correction
        ds.CorrectData(em)
    
        q_cut = False # to cut the low q-values
    
        if limit_lowq.value:
            q_cut = True
            ds.Qvals_cut = []
            ds.DetCtr_cut = []
            ds.ErrDetCtr_cut = []
    
            for i in xrange(len(ds.Qvals)):                    
                if ds.Qvals[i] > limit_lowq_number.value:              
                    ds.Qvals_cut.append(ds.Qvals[i])
                    ds.DetCtr_cut.append(ds.DetCtr[i])
                    ds.ErrDetCtr_cut.append(ds.ErrDetCtr[i])
                    
            if TemperatureVTE_setpoint.value:   
                    ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '_tempVTEsp_' + str(int(ds.TempvTE_sp)) + 'C-abs_cut.dat')
            elif TemperatureVTE.value:
                    ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '_tempVTE_' + str(int(ds.TempvTE)) + 'C-abs_cut.dat')
            elif TemperatureLSC.value:
                    ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '_tempLSC_' + str(int(ds.TempLSC)) + 'C-abs_cut.dat')
            elif TemperatureLSD.value:
                    ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '_tempLSD_' + str(int(ds.TempLSD)) + 'C-abs_cut.dat')
            else:
                ds.SaveAbs_cut(path + filename + '_' + ds.SampleName + '-abs_cut.dat') 
                #ds.SaveAbs_cut_Mantid( path + 'Mantid_' + filename + '_' + ds.SampleName + '-abs_cut.dat')  
        

        if TemperatureVTE_setpoint.value:   
                ds.SaveAbs(path + filename + '_' + ds.SampleName + '_tempVTEsp_' + str(int(ds.TempvTE_sp)) + 'C-abs.dat')
        elif TemperatureVTE.value:
                ds.SaveAbs(path + filename + '_' + ds.SampleName + '_tempVTE_' + str(int(ds.TempvTE)) + 'C-abs.dat')
        elif TemperatureLSC.value:
                ds.SaveAbs(path + filename + '_' + ds.SampleName + '_tempLSC_' + str(int(ds.TempLSC)) + 'C-abs.dat')
        elif TemperatureLSD.value:
                ds.SaveAbs(path + filename + '_' + ds.SampleName + '_tempLSD_' + str(int(ds.TempLSD)) + 'C-abs.dat')
        else:
            ds.SaveAbs(path + filename + '_' + ds.SampleName + '-abs.dat') 
              
        
        # for batch overview file
        
        file_names.append(filename)
        sample_names.append(ds.SampleName)
        
        filetime = datetime.strptime(ds.start_time,'%Y-%m-%d %H:%M:%S')
        
        if filetime < earliest_time :  #set earliest_time to the earliest file start_time
                earliest_time = filetime 
        file_start_times.append(filetime)        

        if CreateBatchOverView_points.value:
            
            summary_i = [] #14.1.2017 Add to get an overview for files with few q-values
            
            for i in range(len(ds.Qvals)):
                data_point = []
                data_point.append(ds.TimeStamp[i])
                data_point.append(ds.Qvals[i])
                data_point.append(ds.DetCtr[i])
                data_point.append(ds.ErrDetCtr[i])
                if TemperatureVTE_setpoint.value:
                    data_point.append(ds.TempvTE_sp_all[i])
                if TemperatureVTE.value:
                    data_point.append(ds.TempvTE_all[i])
                if TemperatureLSC.value:
                    data_point.append(ds.TempLSC_all[i]-273.15)
                if TemperatureLSD.value:
                    data_point.append(ds.TempLSD_all[i]-273.15)             

                summary_i.append(data_point)
            
            summary_all.append(summary_i)
            
            #print 'summary_all',summary_all

        if CreateBatchOverView_Tsas.value:
            
            summary_i_Tsas = []
            summary_i_Tsas.append(ds.sz)
            summary_i_Tsas.append(ds.PeakAng)
            summary_i_Tsas.append(ds.PeakVal)
            summary_i_Tsas.append(ds.TransRock)
            summary_i_Tsas.append(ds.TransWide)
            summary_i_Tsas.append(ds.TransRock/ds.TransWide)
            summary_i_Tsas.append(ds.TotalTime_form)
            
            summary_all_Tsas.append(summary_i_Tsas)
            
            #print 'summary_all_Tsas',summary_all_Tsas
            
               
    
    if CreateBatchOverView_points.value:
        filename_out = CreateBatchOverView_points_file.value
        
        header = ["filename", "sample name", "start_time", "time_stamp [s]", "delta_time [s]", "q [A^-1]", "Int [cm^-1]", "dI [cm^-1]"]
        
        if TemperatureVTE_setpoint.value:
            header.append("VTE_SP [C]")
        if TemperatureVTE_setpoint.value:
            header.append("VTE [C]")
        if TemperatureLSC.value:
            header.append("LSC [C]")
        if TemperatureLSD.value:
            header.append("LSD [C]")
    
        LE = '\n'
        with open(path + filename_out, 'w') as fp:
            for i in range(len(header)):
                fp.write(header[i] + ',')
            fp.write(LE)
            
            for j in range(len(dsFilePaths)):
                delta_time = file_start_times[j] - earliest_time
                
                for i in range(len(summary_all[j])):                
                    fp.write(file_names[j] +',')
                    fp.write(sample_names[j] +',')
                    fp.write(str(file_start_times[j]) +',')
                    fp.write(str(summary_all[j][i][0])+',') # q-value
                    
                    
                    td= (delta_time+ timedelta(seconds=summary_all[j][i][0]))
                    t_secs = td.seconds + td.days * 24 * 3600
                    fp.write(str(t_secs) +',') # time                    
                    fp.write(str(summary_all[j][i][1])+',') # q-value
                    fp.write(str(summary_all[j][i][2])+',') # this is I
                    fp.write(str(summary_all[j][i][3])) # this is dI
                    for k in range(4,len(data_point)):
                        fp.write(',' + str(summary_all[j][i][k])) # temperatures if ticked
                    fp.write(LE)
    
    
            
            
                            
    if CreateBatchOverView_Tsas.value:
        filename_out = CreateBatchOverView_Tsas_file.value
        
        header = ["filename","sample name", "start_time", "sample pos",  "m2om_0 [cm^-1]", "I_0 [cm^-1]", 'Trock', 'Twide', 'Tsas', 'Run_time'," delta_time [s]"]
        
        LE = '\n'
        with open(path + filename_out, 'w') as fp:
            
            for i in range(len(header)):
                fp.write(header[i] + ',')
            fp.write(LE)
            
            for j in range(len(dsFilePaths)):
                delta_time = file_start_times[j] - earliest_time
                
                fp.write(file_names[j] +',')
                fp.write(sample_names[j] +',')
        
                
                fp.write(str(file_start_times[j]) +',')
                fp.write(str(summary_all_Tsas[j][0]) +',') # this is sample pos
                fp.write(str(summary_all_Tsas[j][1]) +',') # this is PeakAng
                fp.write(str(summary_all_Tsas[j][2]) +',') # this is PeakVal
                fp.write(str(summary_all_Tsas[j][3]) +',') # this is Trock
                fp.write(str(summary_all_Tsas[j][4]) +',') # this is Twide
                fp.write(str(summary_all_Tsas[j][5]) +',') # this is Twide
                fp.write(str(summary_all_Tsas[j][6]) +',') # this is Tsas
                fp.write(str(delta_time))
                fp.write(LE)
        
        

# Empty Space
steps_label = Par('label', '')
steps_label.colspan = 2
steps_label = Par('label', '')
steps_label.colspan = 2
steps_label = Par('label', '')
steps_label.colspan = 2
steps_label = Par('label', '')
steps_label.colspan = 2
steps_label = Par('label', '')
steps_label.colspan = 2
steps_label = Par('label', '')


# OPTIONAL: AMBIENT BACKGROUND ########################################################
bkgFiles = Par('string', '')
bkgFiles.title = 'Files' 
bkgFilesTakeBtn = Act('bkgFilesTake()', 'Select As Ambient Background')

bkgIgnorePts = Par('string', '')
bkgIgnorePts.title = 'Ignore Data Points' 

bkgLevel = Par('float', '0.2')
bkgLevel.title = 'Background Level'
bkgLevel.enabled = False
bkgLevel_Error = Par('float', '0')
bkgLevel_Error.title = ' Actual Error'
bkgLevel_Error.enabled = False
bkgLevel_space = Par('label', '')
bkgLevel_space.colspan = 2

g4 = Group('Optional: Determine Ambient Background')
g4.numColumns = 2
g4.add(bkgFiles, bkgFilesTakeBtn, bkgIgnorePts, 
       bkgLevel, bkgLevel_space,bkgLevel_Error)

#steps_label.colspan = 200

def bkgFilesTake():
    fns = None
    for sds in __DATASOURCE__.getSelectedDatasets():
        basename = os.path.basename(str(sds.getLocation()))
        basename = basename[:basename.find('.nx.hdf')]

        if fns is None:
            fns = basename
        else:
            fns += ', ' + basename
            
    if fns is None:
        bkgFiles.value = ''
    else:
        bkgFiles.value = fns
    # find background files
    bkgFileList = filter(None, str(bkgFiles.value).split(','))
    for i in xrange(0, len(bkgFileList)):
        bkgFileList[i] = bkgFileList[i].strip()

    bkgFilePaths = []
    if len(bkgFileList) != 0:
        for bkgFile in bkgFileList:
            found = False
            
            for ds in __DATASOURCE__.getDatasetList():
                dsLocation = str(ds.getLocation())
                if bkgFile in dsLocation:
                    if not found:
                        bkgFilePaths.append(dsLocation)
                        found = True
                    else:
                        print 'Warning: "%s" has multiple matches' % bkgFile
                        break
                    
            if not found:
                print 'Warning: "%s" was not found' % bkgFile
                
    if len(bkgFilePaths) == 0:
        print 'Warning: no Background Scans were selected'
        return
    
    filename = os.path.basename(bkgFilePaths[0])
    
    print 'filname:', filename
    
    bkg = LoadNxHdf(bkgFilePaths)
    bkg.SortAngles()
    bkg = RemoveIgnoredRanges(bkg, bkgIgnorePts.value)
    
    bkgLevel.value = sum(bkg.DetCtr)/len(bkg.Angle)
    bkgLevel_Error.value = sum(bkg.ErrDetCtr)/len(bkg.Angle)
    
    bkg.FindZeroAngle()
    bkg.DetermineQVals()
    
    global Plot_START
    global Plot4

    PlotDataset(Plot_START, bkg, 'Determine background: ' + filename)
    PlotDataset_log(Plot3, bkg, 'Determine background: ' + filename)
    
    Plot_START.add_y_marker(bkgLevel.value, 600, 'green')
    Plot3.add_y_marker(bkgLevel.value, 600, 'green')
       
    PlotTransmissionDataset(Plot1, bkg, 'Determine background: ' + filename)
    PlotMonitorDataset(Plot2, bkg, 'Determine background: ' + filename)    




    
    
g0 = Group('Advanced Settings - Select Tube(s) of Interest:')
g0.numColumns = 5
g0.add(combine_tube0, combine_tube1, combine_tube2, combine_tube3, combine_tube4)

g2 = Group('Advanced Settings - Limit Detector Area')
g2.numColumns = 3
g2.add(limit_detector,detectorheight_start,detectorheight_end)

g1 = Group('Advanced Settings - Beam Monitor')
g1.numColumns = 2
g1.add(use_beammonitor, defaultMCR, use_tube6_monitor,defaultMCR_tube6,medianMCR,use_medianMCRPlot)

g3 = Group('Advanced Settings - Cut Low Q Values')
g3.numColumns = 3
g3.add(limit_lowq, limit_lowq_number, remove_duplicate_points)

g4 = Group('Advanced Settings')
g4.numColumns = 4
g4.add(convert2q, sort_scanvar, negative_steps, TWideMarker)

g5 = Group('Advanced Settings - Fix m2om and Intensity - under construction')
g5.numColumns = 3
g5.add(fix_m2om0_int0, m2om0_fixed, int0_fixed, fix_Iwide, Iwide_fixed)

g6 = Group('Advanced Settings - DEADTIME in testing')
g6.numColumns = 3
g6.add(DeadTime_FromFile,DeadTime_Patching,DeadTime,
       DeadTimeTypePara, DeadTimeTypeNonPara)   

g7 = Group('Advanced Settings Temperature')
g7.numColumns = 2
g7.add(TemperatureVTE_setpoint,TemperatureVTE,
       TemperatureLSC, TemperatureLSD)

g8 = Group('Advanced Settings Batch File')
g8.numColumns = 2
g8.add(CreateBatchOverView_points,CreateBatchOverView_points_file,CreateBatchOverView_Tsas,CreateBatchOverView_Tsas_file)


def LoadNxHdf(filePaths):

    result = None
    for file in filePaths:
        tmp = ReductionDataset(file)

        if result is None:
            result = tmp
        else:
            result.Append(tmp)
            
    return result

    result = None
    for file in files:
        tmp = ReductionDataset(path + file)

        if result is None:
            result = tmp
        else:
            result.Append(tmp)
            
    return result

class ReductionDataset:
            
    def __init__(self, path):
        
        print ' '
        print 'loading file number:', path
        print ' '
        
        ds = Dataset(path) # df[path]
        # in case of 4d data
        ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm')
       
        self.Filename   = os.path.basename(path)
            
        self.CountTimes    = list(ds['entry1/instrument/detector/time'])
        self.Bex           = list(ds['entry1/instrument/crystal/bex'])
        self.MonCts        = list(ds['entry1/monitor/bm1_counts'])
        self.MonCountTimes = list(ds['entry1/monitor/time']) 
        self.MonCountRate = list(ds['entry1/monitor/bm1_event_rate'])  # new 15/06/2022   
        self.ScanVariablename  = str(ds['entry1/instrument/crystal/scan_variable'])
        self.ScanVariable = list(ds['entry1/instrument/crystal/' + self.ScanVariablename])        
        
        self.Angle = copy(self.ScanVariable)
        
        if self.ScanVariablename == 'm2om':
            pass
        else:
            if convert2q.value:
                raise Exception ("Please Untick 'Convert to q'")
                    
        self.DetCts     = [] # more difficult readout
        self.ErrDetCts  = [] # calculated
        self.TransCts   = [] # more difficult readout   
        
        # read parameters from file
     
        self.Wavelength    = float(ds['entry1/instrument/crystal/wavelength'])         
        self.TransDeadTime = float(ds['entry1/instrument/detector/TransDeadTime'])
        self.dOmega        = float(ds['entry1/instrument/crystal/dOmega'])      
        self.gDQv          = float(ds['entry1/instrument/crystal/gDQv'])
        self.ScanVariable  = str(ds['entry1/instrument/crystal/scan_variable'])
        self.TimeStamp     = list(ds['entry1/time_stamp'])
        self.start_time    = str(ds['entry1/start_time'])
        
        
        if TemperatureVTE_setpoint.value:   
            self.TempvTE_sp       = float(ds['entry1/sample/tc2/Loop1/setpoint'][0])
            self.TempvTE_sp_all   = list(ds['entry1/sample/tc2/Loop1/setpoint'])
        if TemperatureVTE.value:
            self.TempvTE          = float(ds['entry1/sample/tc2/Loop1/sensor'][0])
            self.TempvTE_all      = list(ds['entry1/sample/tc2/Loop1/sensor'])
        if TemperatureLSC.value:
            self.TempLSC          = float(ds['entry1/sample/tc3/sensor/sensorValueC'][0])-273.15
            self.TempLSC_all      = list(ds['entry1/sample/tc3/sensor/sensorValueC']) 
        if TemperatureLSD.value:
            self.TempLSD          = float(ds['entry1/sample/tc3/sensor/sensorValueD'][0])-273.15
            self.TempLSD_all      = list(ds['entry1/sample/tc3/sensor/sensorValueD'])
           
        # read parameters from file and possibly patch               
        self.Thick         = TryGet(ds, ['entry1/sample/thickness'                   ], Thickness.value , Thickness_Patching.value ) / 10.0 # mm to cm            
        self.SampleName    = TryGet(ds, ['entry1/sample/name'                        ], SampleName.value , SampleName_Patching.value )
        self.SampleDescr   = TryGet(ds, ['entry1/sample/description'                 ], SampleDescr.value , SampleDescr_Patching.value )
        self.SampleBkg     = TryGet(ds, ['entry1/experiment/bkgLevel'                ], SampleBkg.value , SampleBkg_Patching.value )
        self.MainDeadTime  = TryGet(ds, ['entry1/instrument/detector/MainDeadTime' ], DeadTime.value , DeadTime_Patching.value)
        #self.Magnet   = float(ds, ['entry1/data/BO1SO1'              ], Magnet.value)   
        
        self.empLevel = empLevel.value
        self.empLevel_Error = empLevel_Error.value
        
        self.defaultMCR = defaultMCR.value
        self.defaultMCR_tube6 = defaultMCR_tube6.value
        self.TWideMarker = TWideMarker.value
        self.ActualTime = range(len(self.Angle))
        self.widepoints = 0
        
        start_time         = str(ds['entry1/start_time'])
        print 'start time: ', start_time
        
        sample_z = list(ds['entry1/sample/samz'])
        self.sz = sample_z[0]
        
        # Check on actual sample positions
       
        print 'Sample Z: ', str(self.sz)
        '''
        if not ((sz >= 30 and sz <= 38) or 
                (sz >=176 and sz <=184) or 
                (sz >=321 and sz <= 328) or
                (sz >=467 and sz <= 475) or 
                (sz >=612 and sz <= 620)):  
            print 'Sample Z: ', str(sz)
            print ''
            print ''
            print 'WARNING SAMZ'
            print ''
            print ''
            print ''
        '''
  
        # tube ids
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

        # sum selected tubes
        data = zeros(len(self.Angle))
        data6 = zeros(len(self.Angle))
        data7 = zeros(len(self.Angle))
        
        
        for tid in tids:
            if ds.hmm.ndim == 4:
                #data[:] += ds.hmm[:, 0, :, tid].sum(0) # hmm 15.6.2017
                #print 'test'               
                
                if limit_detector.value:
                    #print 'limit_detector'
                    y0 = int(detectorheight_start.value)
                    yN = int(detectorheight_end.value) + 1 # python end range is exclusive
                                       
                    data[:] += ds.hmm[:, 0, y0:yN, tid].sum(0) # hmm
                    
                    data6[:] = ds.hmm[:, 0, y0:yN, 6].sum(0) # hmm to monitor flux/background
                    data7[:] = ds.hmm[:, 0, y0:yN, 7].sum(0) # hmm to monitor flux/background
                
                else: 
                    #print 'NOT limit_detector'
                    data[:] += ds.hmm[:, 0, :, tid].sum(0) # hmm
                    
                    data6[:] = ds.hmm[:, 0, :, 6].sum(0) # hmm
                    data7[:] = ds.hmm[:, 0, :, 7].sum(0) # hmm
                    

            else:
                data[:] += ds.hmm[:, :, tid].sum(0)    # hmm_xy  
                
                data6[:] += ds.hmm[:, :, 6].sum(0) # hmm
                data7[:] += ds.hmm[:, :, 7].sum(0) # hmm     
                                
        #2018-07-10. Note that det correction wrong if the detector is limiting high countrates
        if DeadTimeTypePara.value and DeadTimeTypeNonPara.value:
            print 'Please choose only one deadtime correction'    
        elif DeadTimeTypePara.value:                     
            DeadtimeCorrection(data, self.MainDeadTime, self.CountTimes)
            self.DetCts    = list(data)
            self.ErrDetCts = [sqrt(cts) for cts in self.DetCts]
            #DeadtimeCorrection(data6, self.MainDeadTime, self.CountTimes)
            #self.Tube6Cts    = list(data6)
            #DeadtimeCorrection(data7, self.MainDeadTime, self.CountTimes)
            #self.Tube7Cts    = list(data7)
        elif DeadTimeTypeNonPara.value:
            DeadtimeCorrection_NonPara(data, self.MainDeadTime, self.CountTimes)        
            self.DetCts    = list(data)
            self.ErrDetCts = [sqrt(cts) for cts in self.DetCts]
            #DeadtimeCorrection_NonPara(data6, self.MainDeadTime, self.CountTimes)
            #self.Tube6Cts    = list(data6)
            #DeadtimeCorrection_NonPara(data7, self.MainDeadTime, self.CountTimes)
            #self.Tube7Cts    = list(data7)
        else:
            print 'no deadtime correction'
            self.DetCts    = list(data)
            self.ErrDetCts = [sqrt(cts) for cts in self.DetCts]
            
        self.Tube6Cts    = list(data6) # note that tube6 and tube7 are not considered for dt correction
        self.Tube7Cts    = list(data7)
        
        # transmission counts
        if abs(self.Wavelength - 4.74) < 0.01:
            tid = 10
            #print 'long wavelength'
        elif abs(self.Wavelength - 2.37) < 0.01:
            tid = 9
            #print 'short wavelength'
        else:
            raise Exception('unsupported wavelength')
            
        # read in for transmission detector
        if ds.hmm.ndim == 4:   
            data[:] = ds.hmm[:, 0, :, tid].sum(0) # hmm
        else:
            data[:] = ds.hmm[:, :, tid].sum(0)    # hmm_xy                    
        DeadtimeCorrection(data, self.TransDeadTime, self.CountTimes)
        self.TransCts  = list(data) 
        
        
        # CONVERT TO COUNTRATES
        self.DetCtr     = range(len(self.DetCts))
        self.ErrDetCtr  = range(len(self.DetCts))
        self.TransCtr   = range(len(self.DetCts))
        self.MonCtr     = range(len(self.DetCts))
        
        self.Tube6Ctr   = range(len(self.DetCts))
        self.Tube7Ctr   = range(len(self.DetCts))
                
        
        ctTimes = self.CountTimes
        
        # to ignore all the 0 times in the detector       
        
        for i in xrange(len(self.DetCts)):    
            if ctTimes[i] < 0.01:                        
                print 'Please Ignore Data Point MainCountTimes: ', i+1
                print ''
                ctTimes[i] = ctTimes[i] + 100.0
                        
        for i in xrange(len(ctTimes)):
            ctTime = ctTimes[i]                  
            self.DetCtr[i]     = self.DetCts[i]    / ctTime
            self.ErrDetCtr[i]  = self.ErrDetCts[i] / ctTime
            self.TransCtr[i]   = self.TransCts[i]  / ctTime
            
            self.Tube6Ctr[i]  = self.Tube6Cts[i] / ctTime
            self.Tube7Ctr[i]  = self.Tube7Cts[i]  / ctTime          
    
        
        # this is all for the beam monitor
        '''
        ctTimes = self.MonCountTimes
        
        for i in xrange(len(ctTimes)):
            if ctTimes[i] < 0.1:                        
                #print 'Please Ignore Data Point MonCountTimes: ', i+1
                #print ''
                ctTimes[i] = ctTimes[i] + 100.0
            ctTime = ctTimes[i]
            self.MonCtr[i]     = self.MonCts[i]  / ctTime
         '''  
        
        self.MonCtr = self.MonCountRate # 15/06/2022 New feature from hdf file
        
        
        
        # TAKE ACCOUNT OF BEAMMONITOR       
        if use_beammonitor.value:         
           mcr = self.defaultMCR
           for i in xrange(len(self.Angle)):
               if self.MonCtr[i] <0.0001: #to fix the 0-divison problem
                   self.MonCtr[i] = 1000
               
               #f = mcr / self.MonCtr[i]
               f = mcr / self.MonCtr[i] # brutal cheat
            
               self.DetCtr[i]    = self.DetCtr[i]    * f
               self.ErrDetCtr[i] = self.ErrDetCtr[i] * f
               self.TransCtr[i]  = self.TransCtr[i]  * f
               
        if use_tube6_monitor.value:
            mcr_tube6 = self.defaultMCR_tube6
            for i in xrange(len(self.Angle)):
               if self.Tube6Ctr[i] <0.0001: #to fix the 0-divison problem
                   self.Tube6Ctr[i] = 1000
               
               #f = mcr / self.MonCtr[i]
               f = mcr_tube6 / self.Tube6Ctr[i] # brutal cheat
            
               self.DetCtr[i]    = self.DetCtr[i]    * f
               self.ErrDetCtr[i] = self.ErrDetCtr[i] * f
               self.TransCtr[i]  = self.TransCtr[i]  * f               
            
        # check on numbers written into beam monitor
        #for i in xrange(len(self.Angle)):
        #    print self.Tube6Cts[i],self.CountTimes[i],self.Tube6Ctr[i]
        #    
        #for i in xrange(len(self.Angle)):  
        #    print self.MonCts[i],self.MonCountTimes[i],self.MonCtr[i]    



  

                
     # CALCULATE TIME OF THE MEASUREMENT
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
        
    def SortAngles(self):
        info = sorted(enumerate(self.Angle), key=lambda item:item[1])
        
        self.Angle      = [item[1]                 for item in info]
        self.DetCtr     = [self.DetCtr    [item[0]] for item in info]
        self.ErrDetCtr  = [self.ErrDetCtr [item[0]] for item in info]
        self.MonCtr     = [self.MonCtr    [item[0]] for item in info]
        self.TransCtr   = [self.TransCtr  [item[0]] for item in info]
        self.CountTimes = [self.CountTimes[item[0]] for item in info]
        self.Bex        = [self.Bex       [item[0]] for item in info]
        self.TimeStamp  = [self.TimeStamp [item[0]] for item in info]
        self.ActualTime = [self.ActualTime[item[0]] for item in info]       
        self.Tube6Ctr   = [self.Tube6Ctr  [item[0]] for item in info]
        self.Tube7Ctr   = [self.Tube7Ctr  [item[0]] for item in info]
        # should include temperatures
    
    def Append(self, other): # CHECK MISSING COUNTRATE? CHECK CHECK CHECK!!!
        self.Filename   += ';' + other.Filename
        self.Angle      += other.Angle
        self.Bex        += other.Bex
        self.DetCtr     += other.DetCtr
        self.ErrDetCtr  += other.ErrDetCtr
        self.MonCtr     += other.MonCtr
        self.TransCtr   += other.TransCtr
        self.CountTimes += other.CountTimes
        self.TimeStamp  += other.TimeStamp
        self.ActualTime += other.ActualTime
        self.Tube6Ctr   += other.Tube6Ctr
        self.Tube7Ctr   += other.Tube7Ctr
        # should include temperatures
        
    def KeepOnly(self, toKeep):
        self.Angle      = [self.Angle[i]      for i in toKeep]
        self.DetCtr     = [self.DetCtr[i]     for i in toKeep]
        self.ErrDetCtr  = [self.ErrDetCtr[i]  for i in toKeep]
        self.MonCtr     = [self.MonCtr[i]     for i in toKeep]
        self.TransCtr   = [self.TransCtr[i]   for i in toKeep]
        self.CountTimes = [self.CountTimes[i] for i in toKeep]
        self.Bex        = [self.Bex[i]        for i in toKeep]
        self.TimeStamp  = [self.TimeStamp[i]  for i in toKeep]
        self.ActualTime = [self.ActualTime[i] for i in toKeep]
        self.Tube6Ctr   = [self.Tube6Ctr[i]   for i in toKeep]
        self.Tube7Ctr   = [self.Tube7Ctr[i]   for i in toKeep]
        # should include temperatures
 
    def FindZeroAngle(self):
        from __builtin__ import max, min, sorted
        
        # input
        x = self.Angle
        y = self.DetCtr

        # limits
        y_max = max(y)
        
        y_low = 0.01 * y_max # find suitable x range
        x_min = max(x)
        x_max = min(x)
        for xi, yi in zip(x, y):
            if yi > y_low:
                if x_min > xi:
                    x_min = xi
                if x_max < xi:
                    x_max = xi

        # sampling
        x_sam = self.linspace(x_min, x_max, num=500)
        y_sam = self.sample(x, y, x_sam)
        
        # normalized cross-correlation
        y_cnv = self.normxcorr(y_sam, y_sam)
        x_cnv = self.linspace(x_min, x_max, num=len(y_cnv))
                    
        # find suitable maximum of y_cnv
        yLevel = 0.5 * y_max
                    
        maxima = self.localmaxima(x_cnv, y_cnv)
        maxima = [m for m in maxima if m[1] > 0.0]                    # ignore negative matches
        maxima = [m for m in maxima if self.sample(x, y, m[0]) > yLevel]   # only consider high y values
        maxima = sorted(maxima, key=lambda m: m[1], reverse=True)     # best fit first
        
        if not maxima:
            self.PeakAng = x[y.index(y_max)]
            self.PeakVal = y_max
        
        else:
            x_cnv_max, y_cnv_max, i_cnv_max = maxima[0]
            self.PeakAng = self.maximumX(x_cnv, y_cnv, i_cnv_max)
            self.PeakVal = y_max
        
        print "Peak Angle:", self.PeakAng
        print "I(rock):", self.PeakVal
        return self.PeakAng

    def linspace(self, start, stop, num):
        r = [0.0] * num
        
        nom = stop - start
        den = num - 1
        for i in xrange(num):
            r[i] = start + (i * nom) / den
        return r
    
    def sample(self, x0, y0, x1):
        from __builtin__ import max, min
        
        if len(x0) != len(y0):
            raise Exception("len(x0) != len(y0)")

        x0_min = min(x0)
        x0_max = max(x0)

        if isinstance(x1, list):
            x1_min = min(x1)
            x1_max = max(x1)
        else:
            x1_min = x1
            x1_max = x1
    
        if len(x0) < 2:
            raise Exception("len(x0) < 2")
        if x0_min >= x0_max:
            raise Exception("x0_min >= x0_max")
        if x1_min < x0_min:
            raise Exception("x1_min < x0_min")
        if x0_max < x1_max:
            raise Exception("x0_max < x1_max")

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

        try:
            _ = iter(x1)
        except TypeError:
            # not iterable
            while x0i1 < x1:
                x0i0 = x0i1
                y0i0 = y0i1
    
                i1 += 1
                
                x0i1 = x0[i1]
                y0i1 = y0[i1]
    
            return y0i0 + (x1 - x0i0) * (y0i1 - y0i0) / (x0i1 - x0i0)
            
        else:
            # iterable
            y1 = [0.0] * len(x1)
            for j in xrange(len(x1)):
                x1j = x1[j]
                
                while x0i1 < x1j:
                    x0i0 = x0i1
                    y0i0 = y0i1
    
                    i1 += 1
                    
                    x0i1 = x0[i1]
                    y0i1 = y0[i1]

                y1[j] = y0i0 + (x1j - x0i0) * (y0i1 - y0i0) / (x0i1 - x0i0)
    
            return y1
        
    def fwhm(self, x, y, i):
    
        def helper(i, yLevel, J):
            x1 = x[i]
            y1 = y[i]
            
            xRef = x1
    
            for j in J:
                x0 = x1
                y0 = y1
                x1 = x[j]
                y1 = y[j]
                
                if y1 <= yLevel:
                    return (x0 + (x1 - x0) * (yLevel - y0) / (y1 - y0)) - (xRef)
    
            return None

        yLevel = 0.5 * y[i] # half maximum
    
        n = len(y)
        rhs = helper(i, yLevel, xrange(i + 1,  n, +1)) # right hand side
        lhs = helper(i, yLevel, xrange(i - 1, -1, -1)) # left hand side
    
        if rhs is None:
            if lhs is None:
                return np.max(x) - np.min(x)
            else:
                return 2 * lhs
        else:
            if lhs is None:
                return 2 * rhs
            else:
                return lhs + rhs
            
    def normxcorr(self, s, k):
        from __builtin__ import abs
        
        sLen = len(s)
        kLen = len(k)
        cLen = sLen + kLen - 1
    
        c = [0.0] * cLen
        
        for i in xrange(cLen):
            j0 = i - (kLen - 1) if i >= kLen - 1 else 0
            jN = i + 1 if i < sLen - 1 else sLen
    
            s1Sum = 0.0
            s2Sum = 0.0
    
            k1Sum = 0.0
            k2Sum = 0.0
    
            skSum = 0.0
    
            n = jN - j0
            for j in xrange(j0, jN):
                sVal = s[j    ]
                kVal = k[i - j]
    
                s1Sum += sVal
                s2Sum += sVal * sVal
                
                k1Sum += kVal
                k2Sum += kVal * kVal
    
                skSum += sVal * kVal
    
            nom  = skSum - s1Sum * k1Sum / n
            denS = s2Sum - s1Sum * s1Sum / n
            denk = k2Sum - k1Sum * k1Sum / n
            den  = sqrt(denS * denk)
    
            if den > 1e-5 * abs(nom):
                c[i] = nom / den
    
        return c
    
    def localmaxima(self, x, y):
        if len(x) != len(y):
            raise Exception("len(x) != len(y)")
        if len(x) < 3:
            raise Exception("len(x) < 3")
        
        # return list of tuples (x, y, i)
        result = []
    
        y1 = y[0]
        y2 = y[1]
        for i2 in xrange(2, len(y)):
            y0 = y1
            y1 = y2
            y2 = y[i2]
    
            if (y0 < y1) and (y1 > y2):
                result.append((x[i2 - 1], y1, i2 - 1))
            
        return result
    
    def maximumX(self, x, y, i):
                
        x0 = x[i - 1]
        x1 = x[i    ]
        x2 = x[i + 1]
        
        y0 = y[i - 1]
        y1 = y[i    ]
        y2 = y[i + 1]
        
        y10 = y1 - y0
        y20 = y2 - y0
        
        return -0.5 * ((x2*x2 - x0*x0)*y10 - (x1*x1 - x0*x0)*y20) / ((x1 - x0)*y20 - (x2 - x0)*y10)

    def DetermineQVals(self):
        deg2rad = 3.14159265359 / 180
        f = 4 * 3.14159265359 / self.Wavelength
        
        if bool(negative_steps.value):
            f *= -1.0
            
        self.Qvals = [f * sin(deg2rad * (angle - self.PeakAng) / 2) for angle in self.Angle]
        
        if bool(negative_steps.value):
            self.Angle.reverse()
            self.Qvals.reverse()
            self.DetCtr.reverse()
            self.ErrDetCtr.reverse()
            self.MonCtr.reverse()
            self.TransCtr.reverse()
            self.CountTimes.reverse()
            self.Bex.reverse()
            self.TimeStamp.reverse()
            self.ActualTime.reverse()
            self.Tube6Ctr.reverse()
            self.Tube7Ctr.reverse()

    def FindTWideCtr(self):

        level = self.TWideMarker
        i0 = bisect_left(self.Qvals, level);
        
        if i0 == len(self.Qvals):
            i0 = builtin_max(0, len(self.Qvals) - 5)
  
        sumTransCtr = 0
        points = 0
              
        for i in xrange(i0, len(self.Qvals)):
            sumTransCtr += self.TransCtr[i]
            points = points+1

        self.TWideCtr = sumTransCtr / points
        self.widepoints = points
        print "I(Wide): ", self.TWideCtr, ", ", points,'points used'
        
        
        if self.Qvals[i0] < level:
            print ''
            print "WARNING: You don't have data past %f (1/A) - so TWide may not be reliable" % level
            print ''
 
                                           
    def CorrectData(self, emp):
        self.Emp = emp
        
        dOmega = self.dOmega
        
        samRock = self.PeakVal # note: this might have been fixed
        samWide = self.TWideCtr # note: see above

        empRock = emp.PeakVal
        empWide = emp.TWideCtr

        self.TransRock  = samRock / empRock
        self.TransWide  = samWide / empWide
        
        print '  '
        print "T(rock):       %.4g" % (self.TransRock)
        print "T(wide):       %.4g" % (self.TransWide)
        print "T(sas) = Trock/Twide: %.4g" % (self.TransRock / self.TransWide)
        print '  '
        
        self.MeasurementTime()
        
        scale = 1.0 / (self.TransWide * self.Thick * dOmega * emp.PeakVal)                
        #print 'scale:' , scale   
             
        maxq = emp.Qvals[-1]
        for i in xrange(len(self.Qvals)):
            wq = self.Qvals[i]
            if wq < maxq:
                tempI   = interp(wq, emp.Qvals, emp.DetCtr)
                tempErr = interp(wq, emp.Qvals, emp.ErrDetCtr)
            else:
                tempI   = self.empLevel
                tempErr = emp.empLevel_Error # USE THIS!!!
                #tempErr = 0
                #tempErr = 0 ### MISSING NEEDS TO BE CHANGED!!!
 
            detCtr = self.DetCtr[i] - self.SampleBkg #- 0.15 # if we forgot the shielding
            empCtr = tempI          - self.SampleBkg

            self.DetCtr[i]    = detCtr - self.TransRock * empCtr
            self.ErrDetCtr[i] = sqrt(self.ErrDetCtr[i]**2 + (self.TransRock * tempErr)**2)
            
            
            self.DetCtr[i]    *= scale
            self.ErrDetCtr[i] *= scale
                                       

    def SaveAbs(self, path, q_cut = False):
            
        LE = '\n'
        with open(path, 'w') as fp:
            fp.write("CREATED: " + datetime.now().strftime("%a, %d %b %Y at %H:%M:%S") + LE) 
            fp.write("SAMPLE: " + self.SampleName + '; ' + self.SampleDescr + '; Thickness [cm]: %g' % (self.Thick) + LE)
            fp.write("SAMPLE: " + self.SampleName + '; ' + self.SampleDescr + '; Thickness [cm]: %g' % (self.Thick) + LE)
            fp.write("FILES: " + self.Filename.replace(';',',') + LE)

            gdqv = self.gDQv
            
            doublepoints = 0
            doublepointsi = []
                
            if remove_duplicate_points.value:
                preQ = float('nan')
                for i in xrange(len(self.Qvals)):
                    newQ = self.Qvals[i]                
                    if preQ == newQ:
                        doublepoints +=1
                        doublepointsi.append(i)                
                    if preQ != newQ:
                        fp.write("%15.6g %15.3f %15.3f %15.6g %15.6g %15.6g" % (newQ, self.DetCtr[i], self.ErrDetCtr[i], -gdqv, -gdqv, -gdqv) + LE)                      
                        preQ = newQ
            else:
                for i in xrange(len(self.Qvals)):
                    fp.write("%15.6g %15.3f %15.3f %15.6g %15.6g %15.6g" % (self.Qvals[i], self.DetCtr[i], self.ErrDetCtr[i], -gdqv, -gdqv, -gdqv) + LE)
            
            fp.write("AMBIENT BACKGROUND: %g" % self.SampleBkg + LE)
            fp.write("EMP LEVEL: %g " % (self.empLevel) + LE) 
            fp.write("EMP FILES: " + self.Emp.Filename.replace(';',',') + "; EMP LEVEL: %.4g " % self.empLevel + LE)
            fp.write("Trock = %.4f; Twide = %.4f; Tsas = %.4f" % (self.TransRock, self.TransWide, self.TransRock / self.TransWide) + LE)
            fp.write("SAM PEAK ANGLE: %.5f ; EMP PEAK ANGLE: %.5f" % (self.PeakAng, self.Emp.PeakAng) + LE)
        
        print ('Info: removed %i duplicate points in the full file: ' % doublepoints) + str(doublepointsi)

    def SaveAbs_cut(self, path):
            
        LE = '\n'
        with open(path, 'w') as fp:
            fp.write("CREATED: " + datetime.now().strftime("%a, %d %b %Y at %H:%M:%S") + LE) 
            fp.write("SAMPLE: " + self.SampleName + '; ' + self.SampleDescr + '; Thickness [cm]: %g' % (self.Thick) + LE)        
            fp.write("FILES: " + self.Filename.replace(';',',') + LE)
            
            gdqv = self.gDQv
            
            
            doublepoints = 0
            doublepointsi = []
            
            if remove_duplicate_points.value:                         
                preQ = float('nan')
                for i in xrange(len(self.Qvals_cut)):
                    newQ = self.Qvals_cut[i]                
                    if preQ == newQ:
                        doublepoints +=1
                        doublepointsi.append(i)                
                    if preQ != newQ:
                        fp.write("%15.6g %15.3f %15.3f %15.6g %15.6g %15.6g" % (newQ, self.DetCtr_cut[i], self.ErrDetCtr_cut[i], -gdqv, -gdqv, -gdqv) + LE)                      
                        preQ = newQ
            else:
                for i in xrange(len(self.Qvals_cut)):
                    fp.write("%15.6g %15.3f %15.3f %15.6g %15.6g %15.6g" % (self.Qvals_cut[i], self.DetCtr_cut[i], self.ErrDetCtr_cut[i], -gdqv, -gdqv, -gdqv) + LE)
            
            fp.write("AMBIENT BACKGROUND: %g" % self.SampleBkg + LE)
            fp.write("EMP LEVEL: %g " % (self.empLevel) + LE) 
            fp.write("EMP FILES: " + self.Emp.Filename.replace(';',',') + "; EMP LEVEL: %.4g " % self.empLevel + LE)
            fp.write("Trock = %.4f; Twide = %.4f; Tsas = %.4f" % (self.TransRock, self.TransWide, self.TransRock / self.TransWide) + LE)
            fp.write("SAM PEAK ANGLE: %.5f ; EMP PEAK ANGLE: %.5f" % (self.PeakAng, self.Emp.PeakAng) + LE)
        
        print ('Info: removed %i duplicate points in the cut file: ' % doublepoints) + str(doublepointsi)

    def SaveAbs_cut_Mantid(self, path):
            
        LE = '\n'
        with open(path, 'w') as fp:
            #fp.write("CREATED: " + datetime.now().strftime("%a, %d %b %Y at %H:%M:%S") + LE) 
            #fp.write("SAMPLE: " + self.SampleName + '; ' + self.SampleDescr + '; Thickness [cm]: %g' % (self.Thick) + LE)        
            #fp.write("FILES: " + self.Filename.replace(';',',') + LE)
            
            gdqv = self.gDQv
            
            
            doublepoints = 0
            doublepointsi = []
            
            if remove_duplicate_points.value:                         
                preQ = float('nan')
                for i in xrange(len(self.Qvals_cut)):
                    newQ = self.Qvals_cut[i]                
                    if preQ == newQ:
                        doublepoints +=1
                        doublepointsi.append(i)                
                    if preQ != newQ:
                        fp.write("%15.6g, %15.3f, %15.3f" % (newQ, self.DetCtr_cut[i], self.ErrDetCtr_cut[i]) + LE)                      
                        preQ = newQ
            else:
                for i in xrange(len(self.Qvals_cut)):
                    fp.write("%15.6g, %15.3f, %15.3f" % (self.Qvals_cut[i], self.DetCtr_cut[i], self.ErrDetCtr_cut[i]) + LE)
            
            #fp.write("AMBIENT BACKGROUND: %g" % self.SampleBkg + LE)
            #fp.write("EMP LEVEL: %g " % (self.empLevel) + LE) 
            #fp.write("EMP FILES: " + self.Emp.Filename.replace(';',',') + "; EMP LEVEL: %.4g " % self.empLevel + LE)
            #fp.write("Trock = %.4f; Twide = %.4f; Tsas = %.4f" % (self.TransRock, self.TransWide, self.TransRock / self.TransWide) + LE)
            #fp.write("SAM PEAK ANGLE: %.5f ; EMP PEAK ANGLE: %.5f" % (self.PeakAng, self.Emp.PeakAng) + LE)
        
        print ('Info: removed %i duplicate points in the cut file: ' % doublepoints) + str(doublepointsi)

                                       
    def SaveRaw(self, path):
        LE = '\n'
        with open(path, 'w') as fp:        
            if convert2q.value:
                fp.write('%15s' % 'q')
            else:
                fp.write('%15s' % self.ScanVariablename)
            fp.write('%15s' % self.Filename.replace('.nx.hdf','')) 
            fp.write('%15s' % 'y_error') 
            fp.write('%15s' % 'data_trans')
            fp.write('%15s' % 'beam_monitor')
            if convert2q.value:
                fp.write('%15s' % 'm2om')
            fp.write('%15s' % 'det_time')
            fp.write('%15s' % 'actual_time')
            fp.write('%15s' % 'diff_time')
            fp.write('\n')
            
            
            if convert2q.value:
                fp.write('%15s' % '[1/A]')
            else:
                fp.write('%15s' % '[]')
            fp.write('%15s' % '[c/s]') 
            fp.write('%15s' % '[c/s]') 
            fp.write('%15s' % '[c/s]')
            fp.write('%15s' % '[c/s]')
            if convert2q.value:
                fp.write('%15s' % '[deg]')
            fp.write('%15s' % '[s]')
            fp.write('%15s' % '[s]')
            fp.write('\n')

            
            
            for i in xrange(len(self.Qvals)):
                fp.write("%15.8g %15.3f %15.3f" % (self.Qvals[i], self.DetCtr[i], self.ErrDetCtr[i]))
                fp.write("%15.3f %15.3f" % (self.TransCtr[i], self.MonCtr[i]))
                if convert2q.value:
                    fp.write("%15f" % (self.Angle[i]))
                fp.write("%15f %15f %15f" % (self.CountTimes[i],self.ActualTime[i], self.ActualTime[i] - self.CountTimes[i]))
                fp.write('\n')
            
            fp.write("FILES: " + self.Filename.replace('.nx.hdf','') + ';  ' + LE)         
            fp.write("CREATED: " + datetime.now().strftime("%a, %d %b %Y at %H:%M:%S") + LE)
            fp.write("SAMPLE: " + self.SampleName + LE)
            fp.write("SAMPLE_DESCRIPTION: " + self.SampleDescr + LE) 
            fp.write("SAMPLE_THICKNESS [cm]: %g" % self.Thick + LE)
            fp.write("AMBIENT_BACKGROUND [c/s]: %g" % self.SampleBkg + LE)
            try:
               fp.write("PEAK_ANGLE [deg]: %.5f" % self.PeakAng + LE)
            except:
                pass   
            fp.write("TOTAL_TIME [h:min:sec]: " + self.TotalTime_form + LE)
                
    def SaveRaw_Mantid(self, path):
        LE = '\n'
        with open(path, 'w') as fp:        
            if convert2q.value:
                fp.write('%15s'',' % 'q')
            else:
                fp.write('%15s' % self.ScanVariablename)
            fp.write('%15s'',' % self.Filename.replace('.nx.hdf','')) 
            fp.write('%15s' % 'y_error') 
            #fp.write('%15s' % 'data_trans')
            #fp.write('%15s' % 'beam_monitor')
            #if convert2q.value:
            #    fp.write('%15s' % 'm2om')
            #fp.write('%15s' % 'det_time')
            #fp.write('%15s' % 'actual_time')
            #fp.write('%15s' % 'diff_time')
            fp.write('\n')
            
            
            if convert2q.value:
                fp.write('%15s'',' % '[1/A]')
            else:
                fp.write('%15s' % '[],')
            fp.write('%15s'',' % '[c/s]') 
            fp.write('%15s' % '[c/s]') 
            #fp.write('%15s' % '[c/s],')
            #fp.write('%15s' % '[c/s],')
            #if convert2q.value:
            #    fp.write('%15s' % '[deg]')
            #fp.write('%15s' % '[s]')
            #fp.write('%15s' % '[s]')
            fp.write('\n')

            
            
            for i in xrange(len(self.Qvals)):
                fp.write("%15.8g, %15.3f, %15.3f" % (self.Qvals[i], self.DetCtr[i], self.ErrDetCtr[i]))
                
                #fp.write("%15.3f %15.3f" % (self.TransCtr[i], self.MonCtr[i]))
                #if convert2q.value:
                #    fp.write("%15f" % (self.Angle[i]))
                #fp.write("%15f %15f %15f" % (self.CountTimes[i],self.ActualTime[i], self.ActualTime[i] - self.CountTimes[i]))
                fp.write('\n')
            
            #fp.write("FILES: " + self.Filename.replace('.nx.hdf','') + ';  ' + LE)         
            #fp.write("CREATED: " + datetime.now().strftime("%a, %d %b %Y at %H:%M:%S") + LE)
            #fp.write("SAMPLE: " + self.SampleName + LE)
            #fp.write("SAMPLE_DESCRIPTION: " + self.SampleDescr + LE) 
            #fp.write("SAMPLE_THICKNESS [cm]: %g" % self.Thick + LE)
            #fp.write("AMBIENT_BACKGROUND [c/s]: %g" % self.SampleBkg + LE)
            #try:
            #   fp.write("PEAK_ANGLE [deg]: %.5f" % self.PeakAng + LE)
            #except:
            #    pass   
            #fp.write("TOTAL_TIME [h:min:sec]: " + self.TotalTime_form + LE)            
                
def DeadtimeCorrection(counts, deadTime, countTimes):
    # x1 = x0 - (x0 - y*e^cx0) / (1 - cx0)
        
    #print 'paralysable', deadTime
    for i in xrange(len(counts)):
        if countTimes[i] == 0:
            counts[i] = 0
            
        else:
            dtt = deadTime / countTimes[i]
            
            y = counts[i]
            x = y       # initial value
            
            # 4 iterations
            for j in xrange(4):
                x = x - (x - y*exp(dtt * x)) / (1 - dtt * x)
                
            counts[i] = x
    
            #tube[i] = tube[i] * (1 / (1.0 - tube[i] * deadTime / countTimes[i]))        


# 2018-07-10
def DeadtimeCorrection_NonPara(counts, deadTime, countTimes):
    
    print 'non-paralysable', deadTime
    for i in xrange(len(counts)):
        if countTimes[i] == 0:
            counts[i] = 0
            
        else:
            counts[i] = counts[i] * (1 / (1.0 - counts[i] * deadTime / countTimes[i]))        
            
#end

def TryGet(ds, pathList, default, forceDefault=False):
    if forceDefault:
        return default
    
    for path in pathList:
        try:
            return ds[path]
        except AttributeError:
            pass
        
    return default

def slopeAt(list, i):
    L = 0
    H = len(list) - 1

    yL = list[builtin_max(L, i - 1)]
    yH = list[builtin_min(H, i + 1)]

    return yH - yL

def interp(q, Q, I):
    
    def helper(q, Q, I, k):
        if Q[k - 1] == Q[k]:
            return (I[k - 1] + I[k]) / 2
        else:
            return I[k] + (I[k - 1] - I[k]) / (Q[k - 1] - Q[k]) * (q - Q[k])

    if q <= Q[1]:
        return helper(q, Q, I, 1)
    elif q >= Q[-2]:
        return helper(q, Q, I, -1)
    else:
        return helper(q, Q, I, bisect_left(Q, q))

def RemoveIgnoredRanges(ds, ignorePtsStr):
    indices = GetToKeepFilter(len(ds.Angle), ignorePtsStr)
    if indices is not None:
        ds.KeepOnly(indices)        
    return ds

def GetToKeepFilter(maxCount, ignorePtsStr):
    ignoredRanges = filter(None, str(ignorePtsStr).split(','))
    if len(ignoredRanges) < 1:
        return None
    
    toKeep = range(0, maxCount)
    for ignoredRange in ignoredRanges:
        rangeItems = ignoredRange.split('-')
        if ('' in rangeItems) or (len(rangeItems) < 1) or (len(rangeItems) > 2):
            raise Exception('format in "ignore data points" is incorrect')
        
        # from 1 based to 0 based
        start = int(rangeItems[0]) #- 1
        
        if len(rangeItems) == 1:
            end = start + 1
        elif rangeItems[1]== '*':
            end = maxCount
        else:
            end = float(rangeItems[1])
        
        for point in xrange(start, end):
            if point in toKeep:
                toKeep.remove(point)
                
    return toKeep

def PlotDataset(plot, ds, title, q_cut = False):
    data = zeros(len(ds.Qvals))
    data[:]     = ds.DetCtr
    data.var[:] = Array(ds.ErrDetCtr) ** 2 # nice way of cheating for now
    data.title  = title
    axis0       = data.axes[0]
    axis0[:]    = ds.Qvals
    
    plot.add_dataset(data)
    
    if q_cut:
        data_cut = Dataset(ds.DetCtr_cut, var = ds.ErrDetCtr_cut*100, 
                           axes = [ds.Qvals_cut])             
        plot.add_dataset(data_cut)
        
        x = ds.Qvals_cut[0]
        y = ds.DetCtr_cut[0]
        plot.add_marker(x, y, 'red')
        
    plot.title    = 'Main Detector'
    plot.x_label = str(ds.ScanVariablename)
    if convert2q.value:
        plot.x_label = 'q (1/Angstrom)'
    plot.y_label = 'intensity (counts/sec)'
    plot.set_mouse_follower_precision(6,2,2)
    plot.set_log_y_on(True)
    plot.y_range = [0.1, data.max()]
    
    
    # under construction

def PlotDataset_log(plot, ds, title, q_cut = False):
    data = zeros(len(ds.Qvals))
    data[:]     = ds.DetCtr
    data.err    = ds.ErrDetCtr # there should be an [:] but needs to be fixed in Gumtree
    data.title  = title
    axis0       = data.axes[0]
    axis0[:]    = ds.Qvals
  
    plot.add_dataset(data)
    if q_cut:
        data_cut = Dataset(ds.DetCtr_cut, var = ds.ErrDetCtr_cut*100, 
                           axes = [ds.Qvals_cut])             
        plot.add_dataset(data_cut)
        
        x = ds.Qvals_cut[0]
        y = ds.DetCtr_cut[0]
        plot.add_marker(x, y, 'red')
        
    plot.title    = 'Main Detector'
    plot.x_label = str(ds.ScanVariablename)
    if convert2q.value:
        plot.x_label = 'q (1/Angstrom)'
    plot.y_label = 'intensity (counts/sec)'
    plot.set_mouse_follower_precision(6,2,2)
    plot.set_log_x_on(True)
    plot.set_log_y_on(True)
    plot.x_range = [1e-7, 0.05]
    plot.y_range = [0.1, data.max()]
#    plot.y_min = 0.1
    
def PlotTransmissionDataset(plot, ds, title):

    data = zeros(len(ds.Qvals))
    data[:]     = ds.TransCtr
    data.var[:] = 0
    data.title  = title
    axis0       = data.axes[0]
    axis0[:]    = ds.Qvals
    
    plot.add_dataset(data)
    plot.title = 'Transmission Detector'
    plot.x_label = str(ds.ScanVariablename)
    if convert2q.value:
        plot.x_label = 'q (1/Angstrom)'
    plot.y_label = 'intensity (counts/sec)'
    plot.set_mouse_follower_precision(6,2,2)
    
    for i in xrange(ds.widepoints):
        x = ds.Qvals[-i-1]
        y = ds.TransCtr[-i-1]
        plot.add_marker(x, y, 'red')
        plot.add_marker(x, y, 'red')
            
       
def PlotMonitorDataset(plot, ds, title):
    data = zeros(len(ds.Qvals))
    if use_medianMCRPlot.value: 
        data[:]     = Array(ds.MonCtr)/ds.defaultMCR
    else:
        data[:]     = ds.MonCtr
    data.var[:] = 0
    data.title  = title
    axis0       = data.axes[0]
    axis0[:]    = ds.Qvals
    
    plot.add_dataset(data)
    plot.title = 'Beam Monitor'
    plot.x_label = str(ds.ScanVariablename)
    if convert2q.value:
        plot.x_label = 'q (1/Angstrom)'
    plot.y_label = 'intensity (counts/sec)'
    plot.set_mouse_follower_precision(6,2,2)
    
def PlotTube67Dataset(plot, ds, tube, title):
    data = zeros(len(ds.Qvals))
    if tube == 'tube6':
        #data[:]     = ds.Tube6Ctr[:]
        if use_medianMCRPlot.value:            
            data[:]     = Array(ds.Tube6Ctr)/547
        else:
            data[:]     = ds.Tube6Ctr[:]
        data.var[:] = 0
        data.title  = title + 'tube6'
        axis0       = data.axes[0]
        axis0[:]    = ds.Qvals
    if tube == 'tube7':
        #data[:]     = ds.Tube7Ctr[:]
        if use_medianMCRPlot.value:
            data[:]     = Array(ds.Tube7Ctr)/155
        else:
            data[:]     = ds.Tube7Ctr[:]
        data.var[:] = 0
        data.title  = title + 'tube7'
        axis0       = data.axes[0]
        axis0[:]    = ds.Qvals
                
    
    plot.add_dataset(data)
    
    plot.title = 'Monitor flux/Background'
    plot.x_label = str(ds.ScanVariablename)
    if convert2q.value:
        plot.x_label = 'q (1/Angstrom)'
    plot.y_label = 'intensity (counts/sec)'
    plot.set_mouse_follower_precision(6,2,2)
