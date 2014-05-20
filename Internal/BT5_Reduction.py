# Script control setup area
# script info
__script__.title = 'KKB Reduction'
__script__.version = '1.0'

'''

    INPUT

'''

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
        
Group('Select Tube(s) of Interest:').add(combine_tube0, combine_tube1, combine_tube2, combine_tube3, combine_tube4)


Wavelength = Par('float', '4.74', options=['2.37', '4.74'])
Wavelength.title = 'Wavelength (A)' 

Thickness = Par('float', '10')
Thickness.title = 'Sample Thickness (mm)' 

MainDeadTime = Par('float', '4e-5')
MainDeadTime.title = 'Main Dead Time'

TransDeadTime = Par('float', '1.26e-5')
TransDeadTime.title = 'Trans Dead Time'

empLevel = Par('float', '0.76')
empLevel.title = 'EMP Level'

bkgLevel = Par('float', '0.62')
bkgLevel.title = 'BKG Level'

defaultMCR = Par('float', '1.0e6')
defaultMCR.title = 'Default MCR'

TWideMarker = Par('float', '3e-3')
TWideMarker.title = 'TWide Marker (1/A)'

dOmega = Par('float', '7.1e-7')
dOmega.title = 'dOmega'

gDQv = Par('float', '0.117')
gDQv.title = 'Q divergence (1/A)'

Group('Parameters').add(Wavelength, Thickness, MainDeadTime, TransDeadTime, empLevel, bkgLevel, defaultMCR, TWideMarker, dOmega, gDQv)

# empty measurement

empFiles = Par('string', '')
empFiles.title = 'Files' 
empFilesTakeBtn = Act('empFilesTake()', 'take from selection')

Group('Empty Scans').add(empFiles, empFilesTakeBtn)

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

'''

    REDUCTION

'''

from math import sqrt, sin
from datetime import datetime
from bisect import bisect_left

from __builtin__ import max as builtin_max
from __builtin__ import min as builtin_min


def DeadtimeCorrection(value, deadTime, countTime):
    return value / (1.0 - value * deadTime / countTime)

def interp(q, Q, I):
    
    def helper(q, Q, I, k):
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

             
class ReductionDataset:

    def __init__(self, path):
        
        print 'loading:', path
                
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

    def Convert2Countrate(self, normalizeToMCR):
        ctTimes = self.CountTimes
        
        for i in xrange(len(ctTimes)):
            ctTime = self.CountTimes[i]
                   
            self.DetCts[i]     = self.DetCts[i]    / ctTime
            self.ErrDetCts[i]  = self.ErrDetCts[i] / ctTime
            self.MonCts[i]     = self.MonCts[i]    / ctTime
            self.TransCts[i]   = self.TransCts[i]  / ctTime
            self.CountTimes[i] = 1.0

        if normalizeToMCR:
            mcr = defaultMCR.value
            for i in xrange(len(self.Angle)):
                f = mcr / self.MonCts[i]
                
                self.DetCts[i]    = self.DetCts[i]    * f
                self.ErrDetCts[i] = self.ErrDetCts[i] * f

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
        deg2QConv  = 5.55e-5 # TBD
        self.Qvals = [deg2QConv * (angle - self.PeakAng) for angle in self.Angle]

    def FindTWideCts(self):
        level = 2.0 # TBD
        i0 = bisect_left(self.Angle, level);
        if i0 == len(self.Angle):
            print "You don't have data past 2 degrees - so Twide may not be reliable"
            i0 = builtin_max(0, len(self.Angle) - 5)
        
        sumTransCts = 0
        sumMonCts   = 0
        for i in xrange(i0, len(self.Qvals)):
            sumTransCts += self.TransCts[i]
            sumMonCts   += self.MonCts[i]

        self.TWideCts = sumTransCts / sumMonCts
        
        print "TWide: ", self.TWideCts
        return self.TWideCts

    def CorrectData(self, emp):
        self.Emp = emp
        
        domega = dOmega.value
        
        samRock = self.PeakVal
        samWide = self.TWideCts

        empRock = emp.PeakVal
        empWide = emp.TWideCts

        self.TransRock  = samRock / empRock
        self.TransWide  = samWide / empWide

        # absolute scaling factor
        scale = 1.0 / (self.TransWide * self.Thick * domega * emp.PeakVal)

        maxq = emp.Qvals[-1]
        for i in xrange(len(self.Qvals)):
            wq = self.Qvals[i]
            if wq < maxq:
                tempI   = interp(wq, emp.Qvals, emp.DetCts)
                tempErr = interp(wq, emp.Qvals, emp.ErrDetCts)
            else:
                tempI   = self.empLevel
                tempErr = 0

            self.DetCts[i]    = (self.DetCts[i] - self.bkgLevel) - self.TransRock * (tempI - self.bkgLevel)
            
            
            # self.DetCts[i]    = self.DetCts[i] - self.TransRock * tempI - (1 - self.TransRock) * self.bkgLevel
            
            self.ErrDetCts[i] = sqrt(self.ErrDetCts[i]**2 + (self.TransRock * tempErr)**2)

            self.DetCts[i]    *= scale
            self.ErrDetCts[i] *= scale

    def Save(self, path):
        LE = '\n'
        with open(path, 'w') as fp:
            fp.write("COR FILES: " + self.Filename.replace(';',',') + LE)
            fp.write("CREATED: " + datetime.now().strftime("%a, %d %b %Y at %H:%M:%S") + LE)
            fp.write("LABEL: " + self.Label + LE)
            fp.write("EMP FILES: " + self.Emp.Filename.replace(';',',') + LE)
            fp.write("Ds = %g cm ; Twide = %g ; Trock = %g" % (self.Thick, self.TransWide, self.TransRock) + LE)
            fp.write("SAM PEAK ANGLE: %g ; EMP PEAK ANGLE: %g" % (self.PeakAng, self.Emp.PeakAng) + LE)
            fp.write("EMP LEVEL: %g ; BKG LEVEL: %g" % (self.empLevel, self.Emp.bkgLevel) + LE)

            # divergence, in terms of Q (1/A) 
            gdqv = gDQv.value

            for i in xrange(len(self.Qvals)):
                fp.write("%15.6g %15.6g %15.6g %15.6g %15.6g %15.6g" % (self.Qvals[i], self.DetCts[i], self.ErrDetCts[i], -gdqv, -gdqv, -gdqv) + LE)

def LoadNxHdf(filePaths):
    result = None
    for file in filePaths:
        tmp = ReductionDataset(file)
        tmp.Convert2Countrate(normalizeToMCR=True)

        if result is None:
            result = tmp
        else:
            result.Append(tmp)
            
    return result

def LoadBT5(path, files):
    result = None
    for file in files:
        tmp = ReductionDataset(path + file)
        tmp.Convert2Countrate(normalizeToMCR=True)

        if result is None:
            result = tmp
        else:
            result.Append(tmp)
            
    return result

def PlotReducedDataset(ds, title):
    data = zeros(len(ds.Qvals))
    data[:]     = ds.DetCts
    data.var[:] = ds.ErrDetCts
    data.title  = title
    axis0       = data.axes[0]
    axis0[:]    = ds.Qvals
    
    global Plot1
    Plot1.add_dataset(data)


# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    
    Plot1.clear()

    # reduction
        
    path = 'D:/Users/kookaburra/Desktop/David/Kookaburra/'
    
    ds = LoadBT5(path, ['CRc8a001.bt5', 'CRc8a002.bt5', 'CRc8a003.bt5', 'CRc8a004.bt5', 'CRc8a005.bt5', 'CRc8a006.bt5', 'CRc8a007.bt5'])
    em = LoadBT5(path, ['CRemp001.bt5', 'CRemp002.bt5', 'CRemp003.bt5', 'CRemp004.bt5', 'CRemp005.bt5', 'CRemp006.bt5', 'CRemp007.bt5'] )
    
    ds.SortAngles()
    ds.FindZeroAngle()
    ds.DetermineQVals()
    ds.FindTWideCts()
    
    PlotReducedDataset(ds, 'SAM')
    
    em.SortAngles()
    em.FindZeroAngle()
    em.DetermineQVals()
    em.FindTWideCts()
        
    PlotReducedDataset(em, 'EMP')
    
    ds.CorrectData(em)
    ds.Save(r'D:\Users\kookaburra\Desktop\David\test.txt')

    PlotReducedDataset(ds, 'Cor')


def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
