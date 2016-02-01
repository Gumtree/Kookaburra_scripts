# Script control setup area
# script info
__script__.title = 'KKB TOF'
__script__.version = '1.0'


# Use below example to create parameters.
# The type can be string, int, float, bool, file.

#directory = 'C:/temp/' 
directory = 'V:/shared/KKB Logbook/Temp Plot Data Repository/KKB_TOF/' 


# INFO ################################################
det_info1 = Par('label', 'Detector Height: 0 - 255')
det_info2 = Par('label', 'Detector Tubes: 0 - 15')
det_info3 = Par('label', 'Time Bins: 0 - 255')

g0 = Group('Info')
g0.numColumns = 2 #9
g0.add(det_info1,det_info2,det_info3)

# INPUT ################################################################
# DETECTOR AREA FOR PLOT 1 

empty = Par('label', '')
 
scanvariable_number = Par('int', 0, command = 'scanvariable_number_changed()')
scanvariable_number.title = 'Scanvariable point number'
def scanvariable_number_changed():
    print 'Scanvariable change to ' + str(scanvariable_number.value)
scanvariable_FromFile = Par('string', 'NaN')
scanvariable_FromFile.title = 'of'
scanvariable_FromFile.enabled = False

timebin_start = Par('int', 0, command = 'timebin_start_changed()')
timebin_start.title = 'Time bin from '
def timebin_start_changed():
    print 'Time bin from ' + str(timebin_start.value)
timebin_end = Par('int', 255, command = 'timebin_end_changed()')
timebin_end.title = 'to '
def timebin_end_changed():
    print 'Time bin to ' + str(timebin_end.value)
timebins_FromFile = Par('string', 'NaN')
timebins_FromFile.title = 'of'
timebins_FromFile.enabled = False

detheight_start = Par('int', 0, command = 'detheight_start_changed()')
detheight_start.title = 'Detector tube height from '
def detheight_start_changed(): 
    print 'Detector tube height from ' + str(detheight_start.value)
detheight_end = Par('int', 255, command = 'detheight_end_changed()')
detheight_end.title = 'to '
def detheight_end_changed():
    print 'Detector tube height to ' + str(detheight_end.value)
detheight_FromFile = Par('string', 'NaN')
detheight_FromFile.title = 'of'
detheight_FromFile.enabled = False

dettube_start = Par('int', 0, command = 'dettube_start_changed()')
dettube_start.title = 'Detector tube number from '
def dettube_start_changed():
    print 'Detector tube number from ' + str(dettube_start.value)
dettube_end = Par('int', 15, command = 'dettube_end_changed()')
dettube_end.title = 'to '
def dettube_end_changed():
    print 'Detector tube number to ' + str(dettube_end.value)    
dettube_FromFile = Par('string', 'NaN')
dettube_FromFile.title = 'of'
dettube_FromFile.enabled = False

TwoD_export = Par('bool', False)
TwoD_export.title = 'Export 2D image?'
TOF_export = Par('bool', False)
TOF_export.title = 'TOF?'

g1 = Group('Choose Detector Area For Plot1 and Plot2 (red)')
g1.numColumns = 3 #9
g1.add(scanvariable_number,scanvariable_FromFile,empty,empty,
       timebin_start, timebin_end,timebins_FromFile,
       detheight_start, detheight_end,detheight_FromFile,
       dettube_start, dettube_end,dettube_FromFile,
       TwoD_export,TOF_export)



# DETECTOR AREA TO INTEGRATE PROFILES
timebin_int_start = Par('int', 0, command = 'timebin_int_start_changed()')
timebin_int_start.title = 'Time bin from '
def timebin_int_start_changed():
    print 'Time bin from ' + str(timebin_int_start.value)
timebin_int_end = Par('int', 255, command = 'timebin_int_end_changed()')
timebin_int_end.title = 'to '
def timebin_int_end_changed():
    print 'Time bin to ' + str(timebin_int_end.value)
    
scanvariable_int_start = Par('int', 0, command = 'scanvariable_int_start_changed()')
scanvariable_int_start.title = 'ScanVariable from '
def scanvariable_int_start_changed():
    print 'ScanVariable from ' + str(scanvariable_int_start.value)
scanvariable_int_end = Par('int', 0, command = 'scanvariable_int_end_changed()')
scanvariable_int_end.title = 'to '
def scanvariable_int_end_changed():
    print 'ScanVariable to ' + str(scanvariable_int_end.value)

detheight_int_start = Par('int', 0, command = 'detheight_int_start_changed()')
detheight_int_start.title = 'Detector tube height from '
def detheight_int_start_changed():
    print 'Detector tube height from ' + str(detheight_int_start.value)
detheight_int_end = Par('int', 255, command = 'detheight_int_end_changed()')
detheight_int_end.title = 'to '
def detheight_int_end_changed():
    print 'Detector tube height to ' + str(detheight_int_end.value)

dettube_int_start = Par('int', 0, command = 'dettube_int_start_changed()')
dettube_int_start.title = 'Detector tube number from '
def dettube_int_start_changed():
    print 'Detector tube number from ' + str(dettube_int_start.value)
dettube_int_end = Par('int', 15, command = 'dettube_int_end_changed()')
dettube_int_end.title = 'to '
def dettube_int_end_changed():
    print 'Detector tube number to ' + str(dettube_int_end.value)

integration_mode = Par('string', 'ScanVariable', options = ['ScanVariable', 'Time of Flight', 'Tube Height', 'Tube Number'])
integration_mode.title = 'Profile along '

m2om = Par('bool', False)
m2om.title = 'm2om?'   

g3 = Group('Choose Parameters for Profile in Plot3')
g3.numColumns = 3
g3.add(scanvariable_int_start, scanvariable_int_end,scanvariable_FromFile,
       timebin_int_start, timebin_int_end,timebins_FromFile,
       detheight_int_start, detheight_int_end,detheight_FromFile,
       dettube_int_start, dettube_int_end,dettube_FromFile,
       integration_mode,m2om)

#############################################################################
# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
    
    # check if a list of file names has been given
    
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
    else :
        for fn in fns:
            # load dataset with each file name
            ds = df[fn]

            filename = os.path.basename(fn) # gets rid of the path
            filename = filename[:filename.find('.nx.hdf')] # gets rid of the hdf
            filename = filename.replace('000','')
        
            
            scanvariable_FromFile.value  = ds.shape[0]            
            #det = ds[0] # to get rid of first nonsense number -> takes first element in list(list(list(list))))            
            
            ds.__iDictionary__.addEntry('m2om', 'entry1/instrument/crystal/m2om')
 
            
            det = ds[scanvariable_number.value]            
            det.axes[0] = range(det.shape[0]) # so that all axes are integers
            det.axes[1] = range(det.shape[1]) #
            det.axes[2] = range(det.shape[2]) #         
            
            timebins_FromFile.value  = det.shape[0] #
            detheight_FromFile.value  = det.shape[1]#
            dettube_FromFile.value  = det.shape[2]  #
            
            det_roi = det[:,
                       detheight_start.value:detheight_end.value+1,
                       dettube_start.value:dettube_end.value+1] # #!!! limit detector to ROI
           
            det_roi_tof_1D = det_roi[:, :, :].sum(0) # sum to one axis (axis [0] = time of flight)
            
            det_roi_tof_1D.axes.title = 'time_bin'
            det_roi_tof_1D.title = 'intensity'
           
            Plot2.set_dataset(det_roi_tof_1D)
            Plot2.add_x_marker(timebin_start.value, 50, 'red')
            Plot2.add_x_marker(timebin_end.value, 50, 'red')
            Plot2.title = 'TOF spectrum of detector image above'
            Plot2.x_label = str(det_roi_tof_1D.axes.title) #'time bin'
           
           
            if TOF_export.value: 
               export_ascii_1D(det_roi_tof_1D, directory + 'TOF_' + filename +
                         '_SCANVAR_'+ str(scanvariable_number.value) + 
                         '_TIME_'+ str(timebin_start.value) + 'to' + str(timebin_end.value) +
                         '_TUBES_'+ str(dettube_start.value) + 'to' + str(dettube_end.value) +
                         '_HEIGHT_'+ str(detheight_start.value) + 'to' + str(detheight_end.value)+ '.txt')           
            
            det_roi_time = det_roi[timebin_start.value:timebin_end.value+1]
            det_roi_timebin = det_roi_time.intg(0)        
            #det_roi_timebin.axes[0].title = 'tube_height' 
            #det_roi_timebin.axes[1].title = 'tube_number'
            Plot1.set_dataset(det_roi_timebin)
            Plot1.title = filename + ': Detector image from time bin ' + str(timebin_start.value) + ' to ' + str(timebin_end.value)
            Plot1.x_label = 'tube_number'
            Plot1.y_label = 'tube_height'
            
            if TwoD_export.value:
                export_ascii_2D(det_roi_timebin, directory + '2D_' + filename +
                         '_SCANVAR_'+ str(scanvariable_number.value) +
                         '_TIME_'+ str(timebin_start.value) + 'to' + str(timebin_end.value) +
                         '_HEIGHT_'+ str(detheight_start.value) + 'to' + str(detheight_end.value) +
                         '_TUBE_'+ str(dettube_start.value) + 'to' + str(dettube_end.value)+ '.txt')
                print ''
                print 'Detector image is exported'

            # integrate TOF profile        
            det_roi_profile = det[:,
                       detheight_int_start.value:detheight_int_end.value+1,
                       dettube_int_start.value:dettube_int_end.value+1]
            det_roi_profile_timebin = det_roi_profile[timebin_start.value:timebin_end.value+1,:,:]
            
            Plot1.add_x_marker(dettube_int_start.value, 50, 'red')
            Plot1.add_x_marker(dettube_int_end.value, 50, 'red')
            Plot1.add_y_marker(detheight_int_start.value, 50, 'red')
            Plot1.add_y_marker(detheight_int_end.value, 50, 'red')
            
            
            # TODO: catch errors when above limits

            intpatch = ds[scanvariable_int_start.value:scanvariable_int_end.value+1,
                          timebin_int_start.value:timebin_int_end.value+1,
                          detheight_int_start.value:detheight_int_end.value+1,
                          dettube_int_start.value:dettube_int_end.value+1] 
            
            
            if m2om.value:
               intpatch.axes[0] = ds.m2om[scanvariable_int_start.value:scanvariable_int_end.value+1] 
            intpatch.axes[1] = range(intpatch.shape[1]) #
            intpatch.axes[2] = range(intpatch.shape[2]) #
            intpatch.axes[3] = range(intpatch.shape[3])
            
            
            if str(integration_mode.value) == 'ScanVariable':                
                det_roi_profile_1D = intpatch[:, :, :,:].sum(0)
                det_roi_profile_1D.axes.title = 'scanvariable'
                det_roi_profile_1D.title = 'intensity'
                
                Plot3.set_dataset(det_roi_profile_1D)
                Plot3.title = 'SCANVARIABLE. Scanvariable: ' + str(scanvariable_int_start.value) + 'to' + str(scanvariable_int_end.value) +'. Time bin: ' + str(timebin_int_start.value) + 'to' + str(timebin_int_end.value) + '. Tube Height: ' + str(detheight_int_start.value) + 'to' + str(detheight_int_end.value) + '. Tube: '+ str(dettube_start.value)+ 'to' + str(dettube_end.value)                  
                Plot3.x_label = str(det_roi_profile_1D.axes.title) # 'tube number'# WHY IS THAT NECESSARY?                
                
                export_ascii_1D(det_roi_profile_1D, directory + filename + '_SCANVARIABLE_' +
                   '_scanvar_'+ str(scanvariable_int_start.value) + 'to' + str(scanvariable_int_end.value) +
                   '_tof_'+ str(timebin_int_start.value) + 'to' + str(timebin_int_end.value) +
                   '_tubes_'+ str(dettube_int_start.value) + 'to' + str(dettube_int_end.value) +
                   '_height_'+ str(detheight_int_start.value) + 'to' + str(detheight_int_end.value)+ '.txt')
            
            if str(integration_mode.value) == 'Time of Flight':                                
                det_roi_profile_1D = intpatch[:, :, :, :].sum(1)             
                det_roi_profile_1D.axes.title = 'time bin'
                det_roi_profile_1D.title = 'intensity'
                
                Plot3.set_dataset(det_roi_profile_1D)
                Plot3.title = 'TOF. Scanvariable: ' + str(scanvariable_int_start.value) + 'to' + str(scanvariable_int_end.value) +'. Time bin: ' + str(timebin_int_start.value) + 'to' + str(timebin_int_end.value) + '. Tube Height: ' + str(detheight_int_start.value) + 'to' + str(detheight_int_end.value) + '. Tube: '+ str(dettube_start.value)+ 'to' + str(dettube_end.value)                  
                Plot3.x_label = str(det_roi_profile_1D.axes.title) # 'tube number'# WHY IS THAT NECESSARY?                
                
                export_ascii_1D(det_roi_profile_1D, directory + filename + '_TOF_' +
                   '_scanvar_'+ str(scanvariable_int_start.value) + 'to' + str(scanvariable_int_end.value) +
                   '_tof_'+ str(timebin_int_start.value) + 'to' + str(timebin_int_end.value) +
                   '_tubes_'+ str(dettube_int_start.value) + 'to' + str(dettube_int_end.value) +
                   '_height_'+ str(detheight_int_start.value) + 'to' + str(detheight_int_end.value)+ '.txt')
  
             
            if str(integration_mode.value) == 'Tube Height':                                
                det_roi_profile_1D = intpatch[:, :, :, :].sum(2)             
                det_roi_profile_1D.axes.title = 'tube_height'
                det_roi_profile_1D.title = 'intensity'
                
                Plot3.set_dataset(det_roi_profile_1D)
                Plot3.title = 'TUBE HEIGHT. Scanvariable: ' + str(scanvariable_int_start.value) + 'to' + str(scanvariable_int_end.value) +'. Time bin: ' + str(timebin_int_start.value) + 'to' + str(timebin_int_end.value) + '. Tube Height: ' + str(detheight_int_start.value) + 'to' + str(detheight_int_end.value) + '. Tube: '+ str(dettube_start.value)+ 'to' + str(dettube_end.value)                  
                Plot3.x_label = str(det_roi_profile_1D.axes.title) # 'tube number'# WHY IS THAT NECESSARY?                
                
                export_ascii_1D(det_roi_profile_1D, directory + filename + '_TUBEHEIGHT_' +
                   '_scanvar_'+ str(scanvariable_int_start.value) + 'to' + str(scanvariable_int_end.value) +
                   '_tof_'+ str(timebin_int_start.value) + 'to' + str(timebin_int_end.value) +
                   '_tubes_'+ str(dettube_int_start.value) + 'to' + str(dettube_int_end.value) +
                   '_height_'+ str(detheight_int_start.value) + 'to' + str(detheight_int_end.value)+ '.txt')
                
            if str(integration_mode.value) == 'Tube Number':                
                det_roi_profile_1D = intpatch[:, :, :, :].sum(3)
                det_roi_profile_1D.axes.title = 'tube_number'
                det_roi_profile_1D.title = 'intensity'
                
                Plot3.set_dataset(det_roi_profile_1D)
                Plot3.title = 'TUBE NUMBER. Scanvariable: ' + str(scanvariable_int_start.value) + 'to' + str(scanvariable_int_end.value) +'. Time bin: ' + str(timebin_int_start.value) + 'to' + str(timebin_int_end.value) + '. Tube Height: ' + str(detheight_int_start.value) + 'to' + str(detheight_int_end.value) + '. Tube: '+ str(dettube_start.value)+ 'to' + str(dettube_end.value)                  
                Plot3.x_label = str(det_roi_profile_1D.axes.title) # 'tube number'# WHY IS THAT NECESSARY?                
                
                export_ascii_1D(det_roi_profile_1D, directory + filename + '_TUBENUMBER_' +
                   '_scanvar_'+ str(scanvariable_int_start.value) + 'to' + str(scanvariable_int_end.value) +
                   '_tof_'+ str(timebin_int_start.value) + 'to' + str(timebin_int_end.value) +
                   '_tubes_'+ str(dettube_int_start.value) + 'to' + str(dettube_int_end.value) +
                   '_height_'+ str(detheight_int_start.value) + 'to' + str(detheight_int_end.value)+ '.txt')
            
           
            print ''
            print 'Detector profile is exported'    
    
 
   
def export_ascii_1D(ds, path):
    f = open(path, 'w')    
    x = str(ds.axes[0].title)
    y = str(ds.title)       
    f.write("%s    %s" % (x, y) + '\n')
    for i in xrange(len(ds)):
       f.write("%5f %15g" % (ds.axes[0][i], ds.storage[i]) + '\n')            
    f.close()   
                    
def export_ascii_2D(ds, path, delimiter = ' '):
    if ds.ndim != 2:
        raise Exception, 'wrong dimension, should be 2 instead of ' + str(ds.ndim)
    f = open(path, 'w')
    try:
        for i in xrange(len(ds)) : # note that this also gets rid of the brackets
            it = ds[i].item_iter()
            while it.has_next():
                f.write(str(it.next()) + delimiter)
            f.write('\n')
    finally:
        if f != None:
            f.close()                

    
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
