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


class KKB06cells(AbstractSampleStage):
    name = "KKB 6 Cells Tumbler"
    in_service = False
    index_samz_pairs = [
                        ('1', 59.5),
                        ('2', 164.8), 
                        ('3', 270.1), 
                        ('4', 375.3), 
                        ('5', 480.5),
                        ('6', 585.7),                       
                        ]
    
'''    
class KKB06cells_Shroud(AbstractSampleStage):
    name = "KKB 6 Cells Tumbler Shroud"
    in_service = True
    index_samz_pairs = [('1', 42.3),
                        ('2', 147.5), 
                        ('3', 252.7), 
                        ('4', 357.9), 
                        ('5', 463.1),
                        ('6', 568.3),                       
                        ]
'''                        
                        
                        
class KKB06cells_Shroud(AbstractSampleStage):
    ## 28.11.2018 LdC
    name = "KKB 6 Cells Tumbler Shroud"
    in_service = True
    index_samz_pairs = [('1', 40.3),
                        ('2', 145.5), 
                        ('3', 250.7), 
                        ('4', 355.9), 
                        ('5', 461.1),
                        ('6', 566.3),                       
                        ]
                        
                        
                       
                        
                        #('1', 39.8),
                        #('2', 145.0), 
                        #('3', 250.2), 
                        #('4', 355.4), 
                        #('5', 460.6),
                        #('6', 565.8),                       
                        #]
                        
                        
class KKB06cells_Shroud_Shane(AbstractSampleStage):
    ## 28.11.2018 LdC
    name = "KKB 6 Cells Tumbler Shroud Shane"
    in_service = False
    index_samz_pairs = [
                        ('2', 145.5), 
                        ('3L', 250.7),
                        ('3B', 268.5),
                        ('3M-8', 261.5),
                        ('3M', 253.5),
                        ('3T', 238.5), 
                        ('4', 355.9),
                        ('4B', 373.7),
                        ('4M', 358.7),
                        ('4T', 343.7), 
                        ('5L', 461.1),
                        ('5B', 478.9),
                        ('5M', 463.9),
                        ('5T', 448.9),
                        ('6', 566.3),
                        ('sedimented 261.5', 261.5),
                        ('rotating middle 355.9', 355.9),
                        ('rotating gradient 370.0', 370.0)                       
                        ]
                           
    
class KKB05Roundcells(AbstractSampleStage):
    name = "KKB 5 Round Cells"
    in_service = False
    index_samz_pairs = [
                        ('1', 32), 
                        ('2', 177.5), 
                        ('3', 323), 
                        ('4', 468.5),
                        ('5', 614),
                        ]
    
class KKB05cells(AbstractSampleStage):
    # updated 18.6.2019 with new aperture
    name = "KKB 5 Cells"
    in_service = False
    index_samz_pairs = [
                        ('1', 31.5), 
                        ('2', 177), 
                        ('3', 322), 
                        ('4', 468),
                        ('5', 613),
                        ]






class SANS_Demountable_12mmAperture(AbstractSampleStage): #after apsel and samx JM
    name = "SANS Demountable 5 Cells"
    in_service = False
    index_samz_pairs = [
                        ('1', 31.0),
                        ('2', 175.5),
                        ('3', 321.5), # CHECK TROUBLESOME
                        ('4', 467.5),
                        ('5', 613.0),
                        ]
    
class SANS_Hellma_10mmAperture(AbstractSampleStage):
    name = "SANS Hellma 5 Cells"
    in_service = False
    index_samz_pairs = [
                        ('1', 35.0),
                        ('2', 180.5),
                        ('3', 326.0),
                        ('4', 471.5),
                        ('5', 617.0),
                        ]

class Quokka5Cells15mmAperture(AbstractSampleStage):
    name = "QKK 5 Cells old"
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
    in_service = False
    index_samz_pairs = [
                        ('1-16', 33.1),
                        ('2-16', 73.6),
                        ('3-16', 113.6),
                        ('4-16', 154.2),
                        ('5-16', 194.0),
                        ('6-16', 233.9),
                        ('7-16', 273.8),
                        ('8-16', 314.1),
                        ('9-16', 354.4),
                        ('10-16', 394.2),
                        ('11-16', 434.4),
                        ('12-16', 474.5),
                        ('13-16', 514.3),
                        ('14-16', 554.6),
                        ('15-16', 594.5),
                        ('16-16', 635.0),
                        ] # 28.7.2017 with 5x5mm aperture on slider and sample
    
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

