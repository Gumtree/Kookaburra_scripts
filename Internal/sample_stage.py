import sys, inspect
from collections import OrderedDict

class StagePool():
    def __init__(self):
        self.stages = []
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if issubclass(obj, AbstractSampleStage) \
                    and not obj is AbstractSampleStage:
                    self.stages.append(obj())
    
    def get_stages(self):
        return self.stages

    def get_stage_in_service(self):
        for stage in self.stages:
            if stage.is_in_service():
                return stage
        return None
    
    def get_stage_names(self):
        names = []
        for stage in self.stages:
            names.append(stage.get_name())
        return names
    
    def get_stage_by_name(self, name):
        for stage in self.stages:
            if stage.get_name() == name:
                return stage
        return None
    
def check_declarations():
    num_stages = 0
    num_in_service = 0
    try:
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if issubclass(obj, AbstractSampleStage) \
                    and not obj is AbstractSampleStage:
                    stage = obj()
                    num_stages += 1
                    if stage.get_name() is None or stage.get_name() == 'Abstract stage':
                        raise 'please declare a proper name for ' + name
                    if stage.is_in_service():
                        num_in_service += 1
                    if stage.get_size() == 0:
                        raise 'wrong stage size, check your declaration of ' + name
                    if len(stage.get_sample_indexes()) == 0:
                        raise 'wrong stage declaration of ' + name
    except Exception, e:
        return [False, str(e)]
    if num_stages == 0:
        return [False, 'no valid stage declaration, please check sample_stage.py']
    if num_in_service != 1:
        return [False, 'please declare only one stage in service, got ' + str(num_in_service)]
    return [True, None]
    
class AbstractSampleStage():
    
    index_samz_pairs = []
    name = 'Abstract stage'
    in_service = False
    
    def get_name(self):
        return self.name
    
    def is_in_service(self):
        return self.in_service
    
    def get_size(self):
        return len(self.index_samz_pairs)
    
    def get_sample_indexes(self):
        keys = []
        for pair in self.index_samz_pairs:
            keys.append(pair[0])
        return keys
            
    def get_samz(self, index):
        for pair in self.index_samz_pairs:
            if str(index) == pair[0]:
                return pair[1]
        raise 'index not found in stage: ' + str(index)
    
# QUOKKA CELLS WITH PERMANENT ORIGINAL (NEW) 15mm APERTURE
# this is right in the middle with 1mm gap on each side 
# December 2015
class Quokka5Cells15mmAperture(AbstractSampleStage):
    name = "QKK 5 Cells"
    in_service = False
    index_samz_pairs = [
                        ('1', 37.0),
                        ('2', 183.0),
                        ('3', 327.0), # CHECK TROUBLESOME
                        ('4', 474.0),
                        ('5', 619.0),
                        ]

class KKB16Cells(AbstractSampleStage):
    name = "KKB 16 Cells"
    in_service = True
    index_samz_pairs = [
                        ('1-16', 31.1),
                        ('2-16', 71.6),
                        ('3-16', 111.6),
                        ('4-16', 152.2),
                        ('5-16', 192.0),
                        ('6-16', 231.9),
                        ('7-16', 271.8),
                        ('8-16', 312.1),
                        ('9-16', 352.4),
                        ('10-16', 392.2),
                        ('11-16', 432.4),
                        ('12-16', 472.5),
                        ('13-16', 512.3),
                        ('14-16', 552.6),
                        ('15-16', 592.5),
                        ('16-16', 633.0),
                        ]
    
class KKB10Cells(AbstractSampleStage):
    name = "KKB 10 Cells"
    in_service = False
    index_samz_pairs = [
                        ('1 top'   , 17.4),
                        ('1 bottom', 77.7),
                        ('2 top'   , 163.5),
                        ('2 bottom', 223.1),
                        ('3 top'   , 308.0),
                        ('3 bottom', 368.1),
                        ('4 top'   , 454.1),
                        ('4 bottom', 513.6),
                        ('5 top'   , 598.2),
                        ('5 bottom', 658.0),
                        ]
