def __run_script__(fns):
    
    from gumpy.commons import sics
    from org.gumtree.gumnix.sics.control import ServerStatus
    import time
    
    '''
    
        helpers
        
    '''
    
    def InitLinearSteps(scan, measurements, step_size, preset):
        angle = -((measurements-1)/2.0) * step_size;
        scan['angles'].append(angle)
        scan['presets'].append(preset)
        
        for i in xrange(1, measurements):
            angle += step_size
            scan['angles'].append(angle)
            scan['presets'].append(preset)
        
        
    def AppendLinearSteps(scan, measurements, step_size, preset):
        angle = scan['angles'][-1]
        for i in xrange(0, measurements):
            angle += step_size
            scan['angles'].append(angle)
            scan['presets'].append(preset)
    
    
    '''
    
        setup
    
    '''
    
    user_name  = 'cre'
    user_email = 'cre@ansto.gov.au'
    
    mode = 'count_roi' # 'count_roi' or 'time'
    scan_variable = 'm2om'
    
    sample_name      = 'Adelaide quartz slice t=1mm'
    sample_thickness = 0.1 # mm
    
    crystal = 'Si111' # wavelength: 4.74 Angstrom
    #crystal = 'Si311' # wavelength: 2.37 Angstrom
    
    empLevel = 0.76
    bkgLevel = 0.98757
    dOmega = 2.3E-6
    gDQv = 0.0586
    #gDQh = 0
    
    MainDeadTime = 4.0E-5
    TransDeadTime = 1.26E-5
    
    angle_ref =  179.6221528 # 180.0
    
    scan = { 'angles': [], 'presets': [] }
    InitLinearSteps(  scan, measurements=33, step_size=6e-5, preset=50000 ) # angle_ref - (steps/2)*step_size
    AppendLinearSteps(scan, measurements=13, step_size=1.2e-4, preset=1000)
    AppendLinearSteps(scan, measurements=15, step_size=2.4e-4, preset=1000)
    AppendLinearSteps(scan, measurements=10, step_size=6.0e-4, preset=1000)
    AppendLinearSteps(scan, measurements=10, step_size=1.2e-3, preset=1000)
    AppendLinearSteps(scan, measurements=16, step_size=2.4e-3, preset=1000)
    AppendLinearSteps(scan, measurements=60, step_size=6.0e-3, preset=1000)
    
    
    '''
    
        execution
    
    '''
    
    sics.execute('hset user/name '  + user_name)
    sics.execute('hset user/email ' + user_email)
    
    sics.execute('hset sample/name '        + sample_name)
    sics.execute('hset sample/thickness %f' % sample_thickness)
    
    sics.execute('hset experiment/bkgLevel %f'  % bkgLevel)
    sics.execute('hset experiment/empLevel %f'  % empLevel)
    sics.execute('hset experiment/dOmega %f'    % dOmega)
    sics.execute('hset experiment/gDQv %f'      % gDQv)
    #sics.execute('hset experiment/gDQh %f'      % gDQh)
    
    sics.execute('hset instrument/detector/MainDeadTime %f'  % MainDeadTime)
    sics.execute('hset instrument/detector/TransDeadTime %f' % TransDeadTime)
    
    if crystal == 'Si111':
        sics.execute('hset instrument/crystal/wavelength 4.74')
        sics.execute('hset instrument/detector/TransmissionTube 10')
    
    elif crystal == 'Si311':
        sics.execute('hset instrument/crystal/wavelength 2.37')
        sics.execute('hset instrument/detector/TransmissionTube 9')
        
    else:
        print 'selected crystal is invalid'
        sics.execute('hset instrument/crystal/wavelength 0')
        sics.execute('hset instrument/detector/TransmissionTube -1')

    sics.execute('histmem stop')
    time.sleep(3)
    sics.execute('histmem mode %s' % mode)
    sics.execute('newfile HISTOGRAM_XYT')
    time.sleep(1)
    
    sicsController = sics.getSicsController()
    
    list_x = []
    list_y = []
    for frame_index in xrange(len(scan['angles'])):
        angle  = scan['angles'][frame_index]
        preset = scan['presets'][frame_index]
        
        print 'run %s %.5f' % (scan_variable, angle_ref + angle)
        sics.execute('run %s %f' % (scan_variable, angle_ref + angle))
        #sics.drive(scan_variable, angle_ref + angle)
        time.sleep(10)
        while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
            time.sleep(0.1)
        print 'run done'
        
        time.sleep(1)
        print 'histmem start'
        while True:
            sics.execute('histmem preset %i ' % preset)
            sics.execute('histmem start')
            
            time.sleep(5)
            while not sicsController.getServerStatus().equals(ServerStatus.EAGER_TO_EXECUTE):
                time.sleep(0.1)
    
            if mode == 'count_roi':
                break
            else:
                for i in xrange(10):
                    time.sleep(1)
                    detector_time = sics.getValue('/instrument/detector/time').getFloatData()
                    if detector_time >= preset - 1:
                        break
                    
                print 'detector_time:', detector_time
                if detector_time >= preset * 0.90:
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
        
    sics.execute('newfile clear')
    
    # Get output filename
    filenameController = sicsController.findDeviceController('datafilename')
    savedFilename = filenameController.getValue().getStringData()
    print 'saved:', savedFilename
    
    print 'done'
    print
