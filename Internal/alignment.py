import inspect
from java.lang import System
import time
import math
from gumpy.nexus.fitting import Fitting, GAUSSIAN_FITTING
from gumpy.commons import sics
from Internal import sicsext
from java.lang import Double

# Script control setup area
# script info
__script__.title = 'Device Alignment'
__script__.version = ''

G1 = Group('Scan on device')
device_name = Par('string', 'dummy_motor', options = sicsext.getDrivables(), command = 'update_axis_name()')
device_name.title = 'Device'
scan_start = Par('float', 179.619)
scan_start.title = 'Start'
scan_stop = Par('float', 179.624)
scan_stop.title = 'Stop'

#number_of_points = Par('int', 0)

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

scan_mode = Par('string', 'time', options = ['time', 'count'])
scan_mode.title = 'Scan Mode'
scan_preset = Par('int', 0)
scan_preset.title = 'Scan Preset'

act_scan_device = Act('scan_device()', 'Scan on Device')
act_scan_device.independent = True
def scan_device():
    aname = device_name.value
    try:
        if DEBUGGING :
            aname = 'dummy_motor'
    except:
        pass
    
    axis_name.value = aname
    slog('runscan ' + str(device_name.value) + ' ' + str(scan_start.value) + ' ' + str(scan_stop.value) \
                    + ' ' + str(sc_count.value) + ' ' + str(scan_mode.value) + ' ' + str(scan_preset.value))
    
    sicsext.runscan(device_name.value, scan_start.value, scan_stop.value, sc_count.value, 
                    scan_mode.value, scan_preset.value, load_experiment_data, True, \
                    'HISTOGRAM_XY')
    time.sleep(2)
    peak_pos.value = float('NaN')
    FWHM.value = float('NaN')
    if auto_fit.value :
        fit_curve()
    
def update_axis_name():
    axis_name.value = device_name.value
        
G1.add(device_name, scan_start, scan_stop, sc_enabled, sc_count, sw_enabled, sw_width, scan_mode, scan_preset, act_scan_device)

G2 = Group('Plot 1')
data_name = Par('string', 'first_5_tubes', \
               options = ['first_5_tubes',
                          'tube_9',
                          'tube_10',
                          'total_counts', 
                          'bm1_counts', 
                          'bm2_counts'], 
                command = 'change_data_name()')
show_individuals = Par('bool', True)
show_individuals.enabled = True
normalise = Par('bool', True)
axis_name = Par('string', '')
axis_name.enabled = True
fix_axis = Par('bool', False)
auto_fit = Par('bool', False)
fit_min = Par('float', 'NaN')
fit_max = Par('float', 'NaN')
peak_pos = Par('float', 'NaN')
FWHM = Par('float', 'NaN')
fact = Act('fit_curve()', 'Fit Again')
fact.independent = True
#offset_done = Par('bool', False)
#act3 = Act('offset_s2()', 'Set Device Zero Offset')
G2.add(data_name, show_individuals, normalise, axis_name, fix_axis, auto_fit, fit_min, fit_max, peak_pos, FWHM, fact)

G3 = Group('Plot 2')
allow_duplication = Par('bool', False)
act2 = Act('import_to_plot2()', text = 'Import Data Files to Plot2')
act2.independent = True
to_remove = Par('string', '', options=[])
act3 = Act('remove_curve()', 'Remove selected curve')
act3.independent = True
plot2_fit_min = Par('float', 'NaN')
plot2_fit_max = Par('float', 'NaN')
plot2_act1 = Act('plot2_fit_curve()', 'Gaussian Fit Plot2')
plot2_act1.independent = True
plot2_peak_pos = Par('float', 'NaN')
plot2_FWHM = Par('float', 'NaN')
act_reset = Act('reset_fitting_plot2()', 'Remove Fitting')
act_reset.independent = True
act_remove_all = Act('remove_all_curves()', 'Remove All Curves')
act_remove_all.independent = True
G3.add(allow_duplication, act2, to_remove, act3, plot2_fit_min, plot2_fit_max, 
       plot2_act1, plot2_peak_pos, plot2_FWHM, act_reset, act_remove_all)

def change_data_name():
    dn = str(data_name.value)
    if dn == 'first_5_tubes':
        show_individuals.enabled = True
    else:
        show_individuals.enabled = False
    
def scan(dname, start, stop, np, mode, preset):
    device_name.value = dname
    scan_start.value = start
    scan_stop.value = stop
    number_of_points.value = np
    scan_mode.value = mode
    scan_preset.value = preset
    axis_name.value = dname
    scan_device()
    
#def fit_curve():
#    __std_fit_curve__()

def fit_curve():
    global Plot1
    ds = Plot1.ds
    if len(ds) == 0:
        log('Error: no curve to fit in Plot1.\n')
        return
    for d in ds:
        if d.title == 'fitting':
            Plot1.remove_dataset(d)
    d0 = ds[0]
    fitting = Fitting(GAUSSIAN_FITTING)
    try:
        fitting.set_histogram(d0, fit_min.value, fit_max.value)
        val = peak_pos.value
        if val == val:
            fitting.set_param('mean', val)
        val = FWHM.value
        if val == val:
            fitting.set_param('sigma', math.fabs(val / 2.35482))
        res = fitting.fit()
        res.var[:] = 0
        res.title = 'fitting'
        Plot1.add_dataset(res)
        Plot1.pv.getPlot().setCurveMarkerVisible(Plot1.__get_NXseries__(res), False)
        mean = fitting.params['mean']
        mean_err = fitting.errors['mean']
        FWHM.value = 2.35482 * math.fabs(fitting.params['sigma'])
        FWHM_err = 5.54518 * math.fabs(fitting.errors['sigma'])
        log('POS_OF_PEAK=' + str(mean) + ' +/- ' + str(mean_err))
        log('FWHM=' + str(FWHM.value) + ' +/- ' + str(FWHM_err))
        log('Chi2 = ' + str(fitting.fitter.getQuality()))
        peak_pos.value = fitting.mean
#        print fitting.params
    except:
#        traceback.print_exc(file = sys.stdout)
        log('can not fit\n')


# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
#    __std_run_script__(fns)
    __std_run_script__(fns)

def load_experiment_data(fullname = None):
    if fullname == None:
        basename = sicsext.getBaseFilename()
        fullname = str(System.getProperty('sics.data.path') + '/' + basename)
    df.datasets.clear()
    ds = df[fullname]
    dname = str(data_name.value)
    if dname == 'first_5_tubes':
        if ds.ndim == 4:
            data = ds[:,:,:,0:5].sum(0)
        elif ds.ndim == 3:
            data = ds[:,:,0:5].sum(0)
        elif ds.ndim == 2:
            data = ds[:,0:5].sum(0)
        else:
            raise Exception('invalid data dimension: {}'.format(ds.ndim))
    elif dname == 'tube_9':
        if ds.ndim == 4:
            data = ds[:,:,:,9].sum(0)
        elif ds.ndim == 3:
            data = ds[:,:,9].sum(0)
        elif ds.ndim == 2:
            data = ds[:,9].sum(0)
        else:
            raise Exception('invalid data dimension: {}'.format(ds.ndim))
    elif dname == 'tube_10':
        if ds.ndim == 4:
            data = ds[:,:,:,10].sum(0)
        elif ds.ndim == 3:
            data = ds[:,:,10].sum(0)
        elif ds.ndim == 2:
            data = ds[:,10].sum(0)
        else:
            raise Exception('invalid data dimension: {}'.format(ds.ndim))
    else:
        data = SimpleData(ds[dname])
#    data = ds[str(data_name.value)]
    if axis_name.value.strip() == '':
        axis = ds.axes[0]
        axis_name.value = axis.name
#        axis = ds.get_metadata(str(axis_name.value))
    else:
        if fix_axis.value:
            axis = SimpleData(ds[str(axis_name.value)])
        else:
            axis = ds.axes[0]
            axis_name.value = axis.name
    if not hasattr(axis, '__len__'):
        axis = SimpleData([axis], title = (axis_name.value))
    if data.size > axis.size:
        data = data[:axis.size]
    if normalise.value :
        if dname == 'bm1_counts':
            tname = 'bm1_time'
        elif dname == 'bm2_counts':
            tname = 'bm2_time'
        else:
            tname = 'detector_time'
        norm = ds[tname]
        if norm != None and hasattr(norm, '__len__'):
            avg = norm.sum() / len(norm)
            niter = norm.item_iter()
            if niter.next() <= 0:
                niter.set_curr(1)
#            data = data / norm * avg
            data = data / norm

    ds2 = Dataset(data, axes=[axis])
    ds2.title = ds.id
    ds2.location = fullname
    fit_min.value = axis.min()
    fit_max.value = axis.max()
    Plot1.set_dataset(ds2)
    if dname == 'first_5_tubes' and show_individuals.value:
        for i in xrange(5):
            if ds.ndim == 4:
                di = ds[:,:,:,i].sum(0)
                if normalise.value :
                    tname = 'detector_time'
                    norm = ds[tname]
                    if norm != None and hasattr(norm, '__len__'):
                        avg = norm.sum() / len(norm)
                        niter = norm.item_iter()
                        if niter.next() <= 0:
                            niter.set_curr(1)
#                        di = di / norm * avg
                        di = di / norm
                di2 = Dataset(di, axes=[axis])
                di2.title = 'tube {}'.format(i)
                Plot1.add_dataset(di2)
    Plot1.x_label = axis_name.value
    Plot1.y_label = str(data_name.value)
    Plot1.title = str(data_name.value) + ' vs ' + axis_name.value
    Plot1.pv.getPlot().setMarkerEnabled(True)

def import_to_plot2():
    global Plot2
    dss = __DATASOURCE__.getSelectedDatasets()
    for dinfo in dss:
        loc = dinfo.getLocation()
        ds = df[str(loc)]
        if not allow_duplication.value:
            did = str(ds.id)
            if to_remove.options.__contains__(did):
                for item in reversed(Plot2.ds) :
                    if item.title == did :
                        Plot2.remove_dataset(item)
                        rlist = copy(to_remove.options)
                        rlist.remove(did)
                        to_remove.options = rlist
                        break
        dname = str(data_name.value)
        if dname == 'first_5_tubes':
            if ds.ndim == 4:
                data = ds[:,:,:,0:5].sum(0)
            elif ds.ndim == 3:
                data = ds[:,:,0:5].sum(0)
            elif ds.ndim == 2:
                data = ds[:,0:5].sum(0)
            else:
                raise Exception('invalid data dimension: {}'.format(ds.ndim))
        elif dname == 'tube_9':
            if ds.ndim == 4:
                data = ds[:,:,:,9].sum(0)
            elif ds.ndim == 3:
                data = ds[:,:,9].sum(0)
            elif ds.ndim == 2:
                data = ds[:,9].sum(0)
            else:
                raise Exception('invalid data dimension: {}'.format(ds.ndim))
        elif dname == 'tube_10':
            if ds.ndim == 4:
                data = ds[:,:,:,10].sum(0)
            elif ds.ndim == 3:
                data = ds[:,:,10].sum(0)
            elif ds.ndim == 2:
                data = ds[:,10].sum(0)
            else:
                raise Exception('invalid data dimension: {}'.format(ds.ndim))
        else:
            data = SimpleData(ds[dname])
    #    data = ds[str(data_name.value)]
        if normalise.value :
            if dname == 'bm1_counts':
                tname = 'bm1_time'
            elif dname == 'bm2_counts':
                tname = 'bm2_time'
            else:
                tname = 'detector_time'
            norm = ds[tname]
            if norm != None and hasattr(norm, '__len__'):
                avg = norm.sum() / len(norm)
                niter = norm.item_iter()
                if niter.next() <= 0:
                    niter.set_curr(1)
#                data = data / norm * avg
                data = data / norm
        if axis_name.value:
            print axis_name.value
            axis = SimpleData(ds[str(axis_name.value)])
        else :
            axis_name.value = ds.axes[0].name
            axis = SimpleData(ds[str(axis_name.value)])
        if data.size > axis.size:
            data = data[:axis.size]
        ds2 = Dataset(data, axes=[axis])
        ds2.title = ds.id
        Plot2.add_dataset(ds2)
        Plot2.x_label = axis_name.value
        Plot2.y_label = dname
        Plot2.title = 'Overlay'
        rlist = copy(to_remove.options)
        rlist.append(str(ds2.title))
        to_remove.options = rlist

def remove_curve():
    global Plot2
    if Plot2.ds is None :
        return
    if to_remove.value is None or to_remove.value == '':
        return
    for item in Plot2.ds :
        if item.title == to_remove.value :
            Plot2.remove_dataset(item)
            rlist = copy(to_remove.options)
            rlist.remove(to_remove.value)
            to_remove.options = rlist
            break

def remove_peak():
    global Plot3
    ds = Plot3.ds
    if ds is None or len(ds) == 0:
        log('Warning: no data in Plot3.\n')
        return
    if peak_at.value is None or peak_at.value == '':
        log('Warning: please select the index of the peak to remove.\n')
        return
    ds0 = ds[0]
    idx = int(peak_at.value)
    if ds0.size == 1 and idx == 0:
        Plot3.clear()
        peak_at.options = []
    else:
        nds = delete(ds0, idx)
        Plot3.set_dataset(nds)
        rlist = []
        for i in xrange(nds.size):
            rlist.append(str(i))
        peak_at.options = rlist
    log('peak ' + str(idx) + ' is removed.\n')

def plot2_fit_curve():
    global Plot2
    ds = Plot2.ds
    if len(ds) == 0:
        log('Error: no curve to fit in Plot2.\n')
        return
    for d in ds:
        if d.title == 'fitting':
            Plot2.remove_dataset(d)
    if len(ds) == 1:
        sds = ds[0]
    else:
        sds = Plot2.get_selected_dataset()
        if sds is None :
            open_error('Please select a curve to fit. Right click on the plot to focus on a curve. Or use CTRL + Mouse Click on a curve to select one.')
            return
    fitting = Fitting(GAUSSIAN_FITTING)
    try:
        fitting.set_histogram(sds, plot2_fit_min.value, plot2_fit_max.value)
        val = plot2_peak_pos.value
        if val == val:
            fitting.set_param('mean', val)
        val = plot2_FWHM.value
        if val == val:
            fitting.set_param('sigma', math.fabs(val / 2.35482))
        res = fitting.fit()
        res.var[:] = 0
        res.title = 'fitting'
        Plot2.add_dataset(res)
        Plot2.pv.getPlot().setCurveMarkerVisible(Plot2.__get_NXseries__(res), False)
        mean = fitting.params['mean']
        log('POS_OF_PEAK=' + str(mean))
        log('FWHM=' + str(2.35482 * math.fabs(fitting.params['sigma'])))
        log('Chi2 = ' + str(fitting.fitter.getQuality()))
        plot2_peak_pos.value = fitting.mean
        plot2_FWHM.value = 2.35482 * math.fabs(fitting.params['sigma'])
#        print fitting.params
    except:
#        traceback.print_exc(file = sys.stdout)
        log('can not fit\n')

def reset_fitting_plot2():
    global Plot2
    ds = Plot2.ds
    if len(ds) == 0:
        return
    for d in ds:
        if d.title == 'fitting':
            Plot2.remove_dataset(d)
    plot2_peak_pos.value = Double.NaN
    plot2_FWHM.value = Double.NaN


def remove_all_curves():
    global Plot2
    Plot2.clear()
    plot2_fit_min.value = Double.NaN
    plot2_fit_max.value = Double.NaN
    plot2_peak_pos.value = Double.NaN
    plot2_FWHM.value = Double.NaN
    to_remove.options = []
    

def __dataset_added__(fns = None):
    pass
    
def __std_run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    # check if a list of file names has been given
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
    else :
        for fn in fns:
            # load dataset with each file name
#            ds = Plot1.ds
#            if ds != None and len(ds) > 0:
#                if ds[0].location == fn:
#                    return
            df.datasets.clear()
            load_experiment_data(fn)
#            ds = df[fn]
#            axis_name.value = ds.axes[0].name
#            dname = str(data_name.value)
#            if dname == 'total_counts':
##                data = ds.sum(0)
#                data = ds[dname]
#            else:
#                data = ds[dname]
#            if normalise.value :
#                if dname == 'bm1_counts':
#                    tname = 'bm1_time'
#                elif dname == 'bm2_counts':
#                    tname = 'bm2_time'
#                else:
#                    tname = 'detector_time'
#                norm = ds[tname]
#                if norm != None and hasattr(norm, '__len__'):
#                    avg = norm.sum() / len(norm)
#                    niter = norm.item_iter()
#                    if niter.next() <= 0:
#                        niter.set_curr(1)
#                    data = data / norm * avg
#        
#            axis = ds.get_metadata(str(axis_name.value))
#            if not hasattr(axis, '__len__'):
#                axis = SimpleData([axis], title = (axis_name.value))
#            ds2 = Dataset(data, axes=[axis])
#            ds2.title = ds.id
#            ds2.location = fn
#            fit_min.value = axis.min()
#            fit_max.value = axis.max()
#            Plot1.set_dataset(ds2)
#            Plot1.x_label = axis_name.value
#            Plot1.y_label = dname
#            Plot1.title = dname + ' vs ' + axis_name.value
#            Plot1.pv.getPlot().setMarkerEnabled(True)
#            peak_pos.value = float('NaN')
#            FWHM.value = float('NaN')
#            if auto_fit.value :
#                fit_curve()
            
def auto_run():
    pass

def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
