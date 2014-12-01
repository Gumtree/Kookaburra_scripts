# Script control setup area
# script info
__script__.title = 'KKB Reduction'
__script__.version = '1.0'

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
        
g0 = Group('Select Tube(s) of Interest:')
g0.numColumns = 5
g0.add(combine_tube0, combine_tube1, combine_tube2, combine_tube3, combine_tube4)


Wavelength = Par('float', '4.74')
Wavelength.title = 'Wavelength, 4.74 or 2.37 (A)' 
Wavelength.enabled = False
Wavelength_Patching = Par('bool', False, command='Wavelength.enabled = Wavelength_Patching.value')
Wavelength_Patching.title = ''
Wavelength_FromFile = Par('float', 'NaN')
Wavelength_FromFile.title = ''
Wavelength_FromFile.enabled = False

Thickness = Par('float', '1')
Thickness.title = 'Sample Thickness (mm)'
Thickness.enabled = False
Thickness_Patching = Par('bool', False, command='Thickness.enabled = Thickness_Patching.value')
Thickness_Patching.title = ''
Thickness_FromFile = Par('float', 'NaN')
Thickness_FromFile.title = ''
Thickness_FromFile.enabled = False

MainDeadTime = Par('float', '1.08e-6')
MainDeadTime.title = 'Main Dead Time (s)'
MainDeadTime.enabled = False
MainDeadTime_Patching = Par('bool', False, command='MainDeadTime.enabled = MainDeadTime_Patching.value')
MainDeadTime_Patching.title = ''
MainDeadTime_FromFile = Par('float', 'NaN')
MainDeadTime_FromFile.title = ''
MainDeadTime_FromFile.enabled = False

TransDeadTime = Par('float', '1.08e-6')
TransDeadTime.title = 'Trans Dead Time (s)'
TransDeadTime.enabled = False
TransDeadTime_Patching = Par('bool', False, command='TransDeadTime.enabled = TransDeadTime_Patching.value')
TransDeadTime_Patching.title = ''
TransDeadTime_FromFile = Par('float', 'NaN')
TransDeadTime_FromFile.title = ''
TransDeadTime_FromFile.enabled = False

bkgLevel = Par('float', '38.5')
bkgLevel.title = 'Normalised BKG Level'
bkgLevel.enabled = False
bkgLevel_Patching = Par('bool', False, command='bkgLevel.enabled = bkgLevel_Patching.value')
bkgLevel_Patching.title = ''
bkgLevel_FromFile = Par('float', 'NaN')
bkgLevel_FromFile.title = ''
bkgLevel_FromFile.enabled = False

TransBkg = Par('float', '75')
TransBkg.title = 'Trans BKG Level'
TransBkg.enabled = False
TransBkg_Patching = Par('bool', False, command='TransBkg.enabled = TransBkg_Patching.value')
TransBkg_Patching.title = ''
TransBkg_FromFile = Par('float', 'NaN')
TransBkg_FromFile.title = ''
TransBkg_FromFile.enabled = False

dOmega = Par('float', '2.3e-6')
dOmega.title = 'dOmega (ster)'
dOmega.enabled = False
dOmega_Patching = Par('bool', False, command='dOmega.enabled = dOmega_Patching.value')
dOmega_Patching.title = ''
dOmega_FromFile = Par('float', 'NaN')
dOmega_FromFile.title = ''
dOmega_FromFile.enabled = False

gDQv = Par('float', '0.0586')
gDQv.title = 'Vertical Q Divergence (1/A)'
gDQv.enabled = False
gDQv_Patching = Par('bool', False, command='gDQv.enabled = gDQv_Patching.value')
gDQv_Patching.title = ''
gDQv_FromFile = Par('float', 'NaN')
gDQv_FromFile.title = ''
gDQv_FromFile.enabled = False

bm1rate = Par('float', '52.0')
bm1rate.title = 'bm1 Count Rate (counts/s)'
bm1rate.enabled = False
bm1rate_Patching = Par('bool', False, command='bm1rate.enabled = bm1rate_Patching.value')
bm1rate_Patching.title = ''

parametersShowBtn = Act('parametersShow()', 'Show Parameters')

g1 = Group('Parameter Patching')
g1.numColumns = 3
g1.add(Wavelength_Patching,
       Wavelength,
       Wavelength_FromFile,
       Thickness_Patching,
       Thickness,
       Thickness_FromFile,
       MainDeadTime_Patching,
       MainDeadTime,
       MainDeadTime_FromFile,
       TransDeadTime_Patching,
       TransDeadTime,
       TransDeadTime_FromFile,
       bkgLevel_Patching,
       bkgLevel,
       bkgLevel_FromFile,
       TransBkg_Patching,
       TransBkg,
       TransBkg_FromFile,
       dOmega_Patching,
       dOmega,
       dOmega_FromFile,
       gDQv_Patching,
       gDQv,
       gDQv_FromFile,
       bm1rate_Patching,
       bm1rate,
       parametersShowBtn)

def parametersShow():
    def TryGet(ds, pathList):
        for path in pathList:
            try:
                return ds[path]
            except AttributeError:
                pass
        
        return float('NaN')
        
    datasets = __DATASOURCE__.getSelectedDatasets()
    if len(datasets) == 1:
        for sds in datasets:
            ds = Dataset(str(sds.getLocation()))
            Wavelength_FromFile.value = TryGet(ds, ['entry1/instrument/crystal/wavelength'])
            Thickness_FromFile.value  = TryGet(ds, ['entry1/sample/thickness'             ])
            
            MainDeadTime_FromFile.value  = TryGet(ds, ['entry1/instrument/detector/MainDeadTime' ])
            TransDeadTime_FromFile.value = TryGet(ds, ['entry1/instrument/detector/TransDeadTime'])
            
            bkgLevel_FromFile.value = TryGet(ds, ['entry1/experiment/bkgLevel'])
            TransBkg_FromFile.value = TryGet(ds, ['entry1/instrument/detector/TransBackground'])
            dOmega_FromFile.value   = TryGet(ds, ['entry1/experiment/dOmega', 'entry1/instrument/crystal/dOmega'])
            gDQv_FromFile.value     = TryGet(ds, ['entry1/experiment/gDQv'  , 'entry1/instrument/crystal/gDQv'  ])

    else:
        print 'please select one file'

defaultMCR = Par('float', '5000')
defaultMCR.title = 'Default MCR'

TWideMarker = Par('float', '3e-3')
TWideMarker.title = 'TWide Marker (1/A)'

samIgnorePts = Par('string', '')
samIgnorePts.title = 'Ignore Sample Data Points' 

Group('Reduction Parameters').add(defaultMCR, TWideMarker, samIgnorePts)


# empty measurement

empFiles = Par('string', '')
empFiles.title = 'Files' 
empFilesTakeBtn = Act('empFilesTake()', 'Take From Selection')

empIgnorePts = Par('string', '')
empIgnorePts.title = 'Ignore Data Points' 

empLevel = Par('float', '0')
empLevel.title = 'Empty Level'
empLevel_SampleCount = Par('int', '10')
empLevel_SampleCount.title = 'Tail Points'
empLevelCalcBtn = Act('empLevelCalc()', 'Determine Empty Level')

Group('Empty Scans').add(empFiles, empFilesTakeBtn, empIgnorePts, empLevel, empLevel_SampleCount, empLevelCalcBtn)

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
        
def empLevelCalc():
    
    sampleCount = int(empLevel_SampleCount.value)
    if sampleCount < 1:
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

    empLevel.value = sum(em.DetCts[-sampleCount:]) / sampleCount


# plot range
    
plotXMin = Par('float', '3e-5')
plotXMax = Par('float', '0.02')
plotYMin = Par('float', '100')
plotYMax = Par('float', '1e7')

plotXMin.title = '                                 x min'
plotXMax.title = 'x max'
plotYMin.title = 'y min'
plotYMax.title = 'y max'

plotXLog = Par('bool', True)
plotYLog = Par('bool', True)

plotXLog.title = 'x log'
plotYLog.title = 'y log'

Group('Plot Range').add(plotXMin, plotXMax, plotYMin, plotYMax, plotXLog, plotYLog)

# determine background level

bkgLevelGetFiles = Par('string', '')
bkgLevelGetFiles.title = 'File'
bkgLevelGetFilesTakeBtn = Act('bkgFilesTake()', 'Take From Selection')

bkgLevelGetIgnorePts = Par('string', '')
bkgLevelGetIgnorePts.title = 'Ignore Data Points' 

bkgLevelGetMcr = Par('string', '')
bkgLevelGetMcr.title = 'MCR'
bkgLevelGetMcr.enabled = False

bkgLevelGetLevel = Par('string', '')
bkgLevelGetLevel.title = 'BKG Level'
bkgLevelGetLevel.enabled = False

bkgLevelGetNLevel = Par('string', '')
bkgLevelGetNLevel.title = 'Normalised BKG Level'
bkgLevelGetNLevel.enabled = False

bkgLevelGetCalcBtn = Act('bkgLevelGet()', 'Determine BKG Level')

Group('Background Level').add(bkgLevelGetFiles, bkgLevelGetFilesTakeBtn, bkgLevelGetIgnorePts, bkgLevelGetMcr, bkgLevelGetLevel, bkgLevelGetNLevel, bkgLevelGetCalcBtn)

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
        bkgLevelGetFiles.value = ''
    else:
        bkgLevelGetFiles.value = fns
        
def bkgLevelGet():
    
    # find bkg files
    bkgFileList = filter(None, str(bkgLevelGetFiles.value).split(','))
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
        print 'Warning: no Empty Scans were selected'
        return
    
    if len(bkgFilePaths) > 1:
        print 'Warning: more than one background file is not support (yet)'
        return
    
    ds = Dataset(str(bkgFilePaths[0]))
    
    # get times
    ctTimes      = list(ds['entry1/instrument/detector/time'])
    mainDeadTime = TryGet(ds, ['entry1/instrument/detector/MainDeadTime'], MainDeadTime.value, MainDeadTime_Patching.value)
    
    
    bkgLevelGetMcr
    
    
    # sum selected tubes
    data = zeros(len(ctTimes))
    for tid in [0, 1, 2, 3, 4]:
        if ds.hmm.ndim == 4:
            data[:] += ds.hmm[:, 0, :, tid].sum(0) # hmm
        else:
            data[:] += ds.hmm[:, :, tid].sum(0)    # hmm_xy    
        
    DeadtimeCorrection(data, mainDeadTime, ctTimes)

    detCts = list(data)
    monCts = list(ds.bm1_counts)
    
    indices = GetToKeepFilter(len(ctTimes), bkgLevelGetIgnorePts.value)
    if indices is not None:
        ctTimes = [ctTimes[i] for i in indices]
        detCts  = [detCts[i]  for i in indices]
        monCts  = [monCts[i]  for i in indices]
    
    # for average
    mcrS = 0.0 
    rawS = 0.0
    nrmS = 0.0
    
    dMCR = defaultMCR.value
    for i in xrange(len(ctTimes)):
        ctTime = ctTimes[i]
               
        detCts[i] = detCts[i] / ctTime
        
        if not bm1rate_Patching.value:
            monCts[i] = monCts[i] / ctTime
        else:
            monCts[i] = float(bm1rate.value)
        
        mcrS += monCts[i]
        rawS += detCts[i]

        detCts[i] = detCts[i] * dMCR / monCts[i]
        
        nrmS += detCts[i]
        
    if len(ctTimes) > 0:
        invN = 1.0 / len(ctTimes)
    else:
        invN = 0.0
        
    mcrS *= invN
    rawS *= invN
    nrmS *= invN

    bkgLevelGetMcr.value    = mcrS
    bkgLevelGetLevel.value  = rawS
    bkgLevelGetNLevel.value = nrmS


'''

    REDUCTION

'''

from math import sqrt, sin, exp
from datetime import datetime
from bisect import bisect_left

#from __builtin__ import max
#from __builtin__ import min
from __builtin__ import max as builtin_max
from __builtin__ import min as builtin_min

'''
def DeadtimeCorrection(value, deadTime, countTime):
    return value / (1.0 - value * deadTime / countTime)
'''
def DeadtimeCorrection(counts, deadTime, countTimes):
    # x1 = x0 - (x0 - y*e^cx0) / (1 - cx0)
        
    for i in xrange(len(counts)):
        dtt = deadTime / countTimes[i]
        
        y = counts[i]
        x = y       # initial value
        
        # 4 iterations
        for j in xrange(4):
            x = x - (x - y*exp(dtt * x)) / (1 - dtt * x)
            
        counts[i] = x

        #tube[i] = tube[i] * (1 / (1.0 - tube[i] * deadTime / countTimes[i]))

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

def slopeAt(list, i):
    L = 0
    H = len(list) - 1

    yL = list[builtin_max(L, i - 1)]
    yH = list[builtin_min(H, i + 1)]

    return yH - yL

def TryGet(ds, pathList, default, forceDefault=False):
    if forceDefault:
        return default
    
    for path in pathList:
        try:
            return ds[path]
        except AttributeError:
            pass
        
    return default

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
        start = int(rangeItems[0]) - 1
        
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

def RemoveIgnoredRanges(ds, ignorePtsStr):
    indices = GetToKeepFilter(len(ds.Angle), ignorePtsStr)
    if indices is not None:
        ds.KeepOnly(indices)
        
    return ds
        
class ReductionDataset:
            
    def __init__(self, path):
        
        print 'loading:', path
        
        ds = Dataset(path) # df[path] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # in case of 4d data
        ds.__iDictionary__.addEntry('hmm', 'entry1/data/hmm')
        
        self.Filename   = os.path.basename(path)
        self.FileDate   = str(ds.start_time)
        self.Label      = str(ds.experiment_title)
        
        self.CountTimes = list(ds['entry1/instrument/detector/time'])
        self.Angle      = list(ds['entry1/instrument/crystal/m2om'])
            
        self.DetCts     = []
        self.ErrDetCts  = []
        self.MonCts     = []
        self.TransCts   = []
        
        # parameters
        
        self.Wavelength = TryGet(ds, ['entry1/instrument/crystal/wavelength'], Wavelength.value, Wavelength_Patching.value)
        self.Thick      = TryGet(ds, ['entry1/sample/thickness'             ], Thickness.value , Thickness_Patching.value ) / 10.0 # mm to cm
        
        self.MainDeadTime  = TryGet(ds, ['entry1/instrument/detector/MainDeadTime' ], MainDeadTime.value , MainDeadTime_Patching.value )
        self.TransDeadTime = TryGet(ds, ['entry1/instrument/detector/TransDeadTime'], TransDeadTime.value, TransDeadTime_Patching.value)
        
        self.transBkgLevel = TryGet(ds, ['entry1/instrument/detector/TransBackground'], TransBkg.value, TransBkg_Patching.value)
            
        self.empLevel = empLevel.value
        self.bkgLevel = TryGet(ds, ['entry1/experiment/bkgLevel'], bkgLevel.value, bkgLevel_Patching.value)
        self.dOmega   = TryGet(ds, ['entry1/experiment/dOmega', 'entry1/instrument/crystal/dOmega'], dOmega.value  , dOmega_Patching.value  )
        self.gDQv     = TryGet(ds, ['entry1/experiment/gDQv'  , 'entry1/instrument/crystal/gDQv'  ], gDQv.value    , gDQv_Patching.value    )
        
        self.defaultMCR  = defaultMCR.value
        self.TWideMarker = TWideMarker.value
        
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
        for tid in tids:
            if ds.hmm.ndim == 4:
                data[:] += ds.hmm[:, 0, :, tid].sum(0) # hmm
            else:
                data[:] += ds.hmm[:, :, tid].sum(0)    # hmm_xy
                
        DeadtimeCorrection(data, self.MainDeadTime, self.CountTimes)

        self.DetCts    = list(data)
        self.ErrDetCts = [sqrt(cts) for cts in self.DetCts]
        
        if not bm1rate_Patching.value:
            self.MonCts = list(ds.bm1_counts)
        else:
            self.MonCts = [bm1rate.value * time for time in self.CountTimes]

        # transmission counts
        if abs(self.Wavelength - 4.74) < 0.01:
            tid = 10
        elif abs(self.Wavelength - 2.37) < 0.01:
            tid = 9
        else:
            raise Exception('unsupported wavelength')
            
        if ds.hmm.ndim == 4:
            data[:] = ds.hmm[:, 0, :, tid].sum(0) # hmm
        else:
            data[:] = ds.hmm[:, :, tid].sum(0)    # hmm_xy
            
        DeadtimeCorrection(data, self.TransDeadTime, self.CountTimes)
        
        # subtraction of transmission background
        self.TransCts = [cts - self.transBkgLevel for cts in data]

        
        '''
        self.Filename  = ''
        self.FileDate  = ''
        self.CountTime = 0
        self.Thick     = 0.10 # cm TBD

        self.Angle     = []
        self.DetCts    = []
        self.ErrDetCts = []
        self.MonCts    = []
        self.TransCts  = []

        # TBD
        self.MainDeadTime  = 4e-5
        self.TransDeadTime = 1.26e-5
        
        # TBD
        self.empLevel = 0.76
        self.bkgLevel = 0.62
        
        with open(path, 'r') as fp:

            # read header
            items = fp.readline().split()
            self.Filename  = items[0].strip("'")
            self.FileDate  = (items[1] + ' ' + items[2] + ' ' + items[3] + ' ' + items[4]).strip("'")
            self.CountTime = float(items[6]) * float(items[7])
            fp.readline() # skip line 2
            self.Label = fp.readline().strip()

            # skip next 10 lines
            for i in xrange(10):
                fp.readline()

            line = fp.readline()
            while len(line) != 0:
                # first line
                items = line.split()
                line  = fp.readline()
                # read angle
                self.Angle.append(float(items[0]))

                # second line
                items = line.split(',')
                line  = fp.readline()
                # monitor
                self.MonCts.append(float(items[0]))
                # deadtime correction
                v2 = DeadtimeCorrection(float(items[1]), self.MainDeadTime, self.CountTime)
                v3 = DeadtimeCorrection(float(items[2]), self.MainDeadTime, self.CountTime)
                v5 = DeadtimeCorrection(float(items[4]), self.MainDeadTime, self.CountTime)
                v6 = DeadtimeCorrection(float(items[5]), self.MainDeadTime, self.CountTime)
                v7 = DeadtimeCorrection(float(items[6]), self.MainDeadTime, self.CountTime)

                self.DetCts.append(v2 + v3 + v5 + v6 + v7)
                self.TransCts.append(DeadtimeCorrection(float(items[3]), self.TransDeadTime, self.CountTime))
                self.ErrDetCts.append(sqrt(self.DetCts[-1]))
                
            self.CountTimes = [self.CountTime] * len(self.Angle)
        '''

    def Convert2Countrate(self):
        ctTimes = self.CountTimes
        
        for i in xrange(len(ctTimes)):
            ctTime = ctTimes[i]
                   
            self.DetCts[i]     = self.DetCts[i]    / ctTime
            self.ErrDetCts[i]  = self.ErrDetCts[i] / ctTime
            self.MonCts[i]     = self.MonCts[i]    / ctTime
            self.TransCts[i]   = self.TransCts[i]  / ctTime
            self.CountTimes[i] = 1.0

        mcr = self.defaultMCR
        for i in xrange(len(self.Angle)):
            f = mcr / self.MonCts[i]
            
            self.DetCts[i]    = self.DetCts[i]    * f
            self.ErrDetCts[i] = self.ErrDetCts[i] * f
            self.TransCts[i]  = self.TransCts[i]  * f

    def Append(self, other):
        self.Filename  += ';' + other.Filename
        self.Angle     += other.Angle
        self.DetCts    += other.DetCts
        self.ErrDetCts += other.ErrDetCts
        self.MonCts    += other.MonCts
        self.TransCts  += other.TransCts

    def SortAngles(self):
        info = sorted(enumerate(self.Angle), key=lambda item:item[1])
        
        self.Angle     = [item[1]                 for item in info]
        self.DetCts    = [self.DetCts   [item[0]] for item in info]
        self.ErrDetCts = [self.ErrDetCts[item[0]] for item in info]
        self.MonCts    = [self.MonCts   [item[0]] for item in info]
        self.TransCts  = [self.TransCts [item[0]] for item in info]
        
    def KeepOnly(self, toKeep):
        self.Angle     = [self.Angle[i]     for i in toKeep]
        self.DetCts    = [self.DetCts[i]    for i in toKeep]
        self.ErrDetCts = [self.ErrDetCts[i] for i in toKeep]
        self.MonCts    = [self.MonCts[i]    for i in toKeep]
        self.TransCts  = [self.TransCts[i]  for i in toKeep]

    def FindZeroAngle(self):
        # find peak
        x = self.Angle
        y = self.DetCts
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
            
        self.PeakAng = (aY*bX - aX*bY) / (aY - bY)
        self.PeakVal = y[i];
        
        print "PeakAng:", self.PeakAng
        print "PeakVal:", self.PeakVal
        return self.PeakAng

    def DetermineQVals(self):
        deg2rad = 3.14159265359 / 180
        f = 4 * 3.14159265359 / self.Wavelength
        
        #self.Qvals = [f * sin((angle - self.PeakAng) / 2) for angle in self.Angle]
        self.Qvals = [f * sin(deg2rad * (angle - self.PeakAng) / 2) for angle in self.Angle]
        
        # Christine demands to leave this here (16/10/2014)
        #deg2QConv  = 5.55e-5 # TBD
        #self.Qvals = [deg2QConv * (angle - self.PeakAng) for angle in self.Angle]

    def FindTWideCts(self):
        '''
        level = 2.0 # TBD
        i0 = bisect_left(self.Angle, level);
        if i0 == len(self.Angle):
            print "You don't have data past 2 degrees - so Twide may not be reliable"
            i0 = max(0, len(self.Angle) - 5)
        '''
        level = self.TWideMarker
        i0 = bisect_left(self.Qvals, level);
        if i0 == len(self.Qvals):
            print "You don't have data past %f (1/A) - so TWide may not be reliable" % level
            i0 = builtin_max(0, len(self.Qvals) - 5)
        
        sumTransCts = 0
        sumMonCts   = 0
        for i in xrange(i0, len(self.Qvals)):
            sumTransCts += self.TransCts[i]
            sumMonCts   += self.MonCts[i]

        self.TWideCts = sumTransCts / sumMonCts
        
        print "IWide: ", self.TWideCts
        return self.TWideCts

    def CorrectData(self, emp):
        self.Emp = emp
        
        dOmega = self.dOmega
        
        samRock = self.PeakVal
        samWide = self.TWideCts

        empRock = emp.PeakVal
        empWide = emp.TWideCts

        self.TransRock  = samRock / empRock
        self.TransWide  = samWide / empWide
        
        print "Trock:       %.4g" % (self.TransRock)
        print "Twide:       %.4g" % (self.TransWide)
        print "Trock/Twide: %.4g" % (self.TransRock / self.TransWide)

        # absolute scaling factor
        print 'self.Thick', self.Thick
        print 'dOmega', dOmega
        print 'emp.PeakVal', emp.PeakVal
        
        scale = 1.0 / (self.TransWide * self.Thick * dOmega * emp.PeakVal)
        scale_lela = (self.TransWide * self.Thick * dOmega) #lela
        
        
        # lela: CHECK: this emp.PeakVal should be the one of the empty CELL???
        
        print 'scale', scale # lela
        print 'scale_lela', scale_lela # lela


        
        
        maxq = emp.Qvals[-1]
        for i in xrange(len(self.Qvals)):
            wq = self.Qvals[i]
            if wq < maxq:
                tempI   = interp(wq, emp.Qvals, emp.DetCts)
                tempErr = interp(wq, emp.Qvals, emp.ErrDetCts)
            else:
                tempI   = self.empLevel
                tempErr = 0
                
            detCts = self.DetCts[i] - self.bkgLevel
            empCts = tempI          - self.bkgLevel

            self.DetCts[i]    = detCts - self.TransRock * empCts
            self.ErrDetCts[i] = sqrt(self.ErrDetCts[i]**2 + (self.TransRock * tempErr)**2)

            self.DetCts[i]    *= scale
            self.ErrDetCts[i] *= scale

    def Save(self, path):
        LE = '\n'
        with open(path, 'w') as fp:
            fp.write("COR FILES: " + self.Filename.replace(';',',') + LE)
            fp.write("CREATED: " + datetime.now().strftime("%a, %d %b %Y at %H:%M:%S") + LE)
            fp.write("LABEL: " + self.Label + LE)
            try:
                fp.write("EMP FILES: " + self.Emp.Filename.replace(';',',') + LE)
                fp.write("Ds = %g cm ; Twide = %g ; Trock = %g ; Trock = %g" % (self.Thick, self.TransWide, self.TransRock, self.TransRock / self.TransWide) + LE) #lela
                fp.write("SAM PEAK ANGLE: %g ; EMP PEAK ANGLE: %g" % (self.PeakAng, self.Emp.PeakAng) + LE)
                fp.write("EMP LEVEL: %g ; BKG LEVEL: %g" % (self.empLevel, self.Emp.bkgLevel) + LE)
            except:
                fp.write("SAM PEAK ANGLE: %g" % self.PeakAng + LE)
                fp.write("EMP LEVEL: %g" % self.empLevel + LE)

            # divergence, in terms of Q (1/A) 
            gdqv = self.gDQv

            preQ = float('nan')
            for i in xrange(len(self.Qvals)):
                newQ = self.Qvals[i]
                if preQ != newQ:
                    fp.write("%15.6g %15.6g %15.6g %15.6g %15.6g %15.6g" % (newQ, self.DetCts[i], self.ErrDetCts[i], -gdqv, -gdqv, -gdqv) + LE)
                    preQ = newQ

def LoadNxHdf(filePaths):
    result = None
    for file in filePaths:
        tmp = ReductionDataset(file)
        tmp.Convert2Countrate()

        if result is None:
            result = tmp
        else:
            result.Append(tmp)
            
    return result

def LoadBT5(path, files):
    result = None
    for file in files:
        tmp = ReductionDataset(path + file)
        tmp.Convert2Countrate()

        if result is None:
            result = tmp
        else:
            result.Append(tmp)
            
    return result

def PlotDataset(plot, ds, title):
    data = zeros(len(ds.Qvals))
    data[:]     = ds.DetCts
    data.var[:] = ds.ErrDetCts
    data.title  = title
    axis0       = data.axes[0]
    axis0[:]    = ds.Qvals
    
    plot.add_dataset(data)
    
def PlotTransmissionDataset(plot, ds, title):
    data = zeros(len(ds.Qvals))
    data[:]     = ds.TransCts
    data.var[:] = 0
    data.title  = title
    axis0       = data.axes[0]
    axis0[:]    = ds.Qvals
    
    plot.add_dataset(data)
    
def PlotMonitorDataset(plot, ds, title):
    data = zeros(len(ds.Qvals))
    data[:]     = ds.MonCts
    data.var[:] = 0
    data.title  = title
    axis0       = data.axes[0]
    axis0[:]    = ds.Qvals
    
    plot.add_dataset(data)


# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    
    Plot1.clear()
    Plot2.clear() #lela
    Plot3.clear() #lela
    
    
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
    
    #ds = LoadBT5(path, ['CRc8a001.bt5', 'CRc8a002.bt5', 'CRc8a003.bt5', 'CRc8a004.bt5', 'CRc8a005.bt5', 'CRc8a006.bt5', 'CRc8a007.bt5'])
    #em = LoadBT5(path, ['CRemp001.bt5', 'CRemp002.bt5', 'CRemp003.bt5', 'CRemp004.bt5', 'CRemp005.bt5', 'CRemp006.bt5', 'CRemp007.bt5'] )

    print 'sample:', ', '.join(dsFilePaths)
    ds = LoadNxHdf(dsFilePaths)    
    ds.SortAngles()    
    ds = RemoveIgnoredRanges(ds, samIgnorePts.value)
    ds.FindZeroAngle()
    ds.DetermineQVals()
    ds.FindTWideCts()

    ds.Save(path + filename + '-sam.txt')
    PlotDataset(Plot1, ds, 'SAM')
    
    print 'empty: ', ', '.join(emFilePaths) 
    em = LoadNxHdf(emFilePaths)
    em.SortAngles()
    em = RemoveIgnoredRanges(em, empIgnorePts.value)
    em.FindZeroAngle()
    em.DetermineQVals()
    em.FindTWideCts()
    
    em.Save(path + filename + '-emp.txt')
    PlotDataset(Plot1, em, 'EMP')
    
    # correction
    ds.CorrectData(em)
    
    ds.Save(path + filename + '-cor.txt')
    PlotDataset(Plot1, ds, 'Cor')
        
    Plot1.title   = 'Main detector' #lela
    Plot1.x_label = 'q (1/Angstrom)'
    Plot1.y_label = 'intensity (counts/sec)'
    
    Plot1.set_log_x_on(plotXLog.value)
    Plot1.set_log_y_on(plotYLog.value)
    
    Plot1.x_range = [plotXMin.value, plotXMax.value]
    Plot1.y_range = [plotYMin.value, plotYMax.value]
    
    # plot 2
    Plot2.clear()
    PlotTransmissionDataset(Plot2, ds, 'SAM')
    PlotTransmissionDataset(Plot2, em, 'EMP')
    
    Plot2.title   = 'Transmission Detector' #lela
    Plot2.x_label = 'q (1/Angstrom)'
    Plot2.y_label = 'intensity (counts/sec)'
        
    # plot 3
    Plot3.clear()
    PlotMonitorDataset(Plot3, ds, 'SAM')
    PlotMonitorDataset(Plot3, em, 'EMP')

    Plot3.title   = 'Monitor Counts'
    Plot3.x_label = 'q (1/Angstrom)'
    Plot3.y_label = 'intensity (counts/sec)'

def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
