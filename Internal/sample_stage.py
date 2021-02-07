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
    
class KKB06cells_Shroud_Mark_plus9(AbstractSampleStage):
    ## 28.11.2018 LdC
    name = "KKB 6 Cells Tumbler Shroud MARK plus9"
    in_service = False
    index_samz_pairs = [('4', 364.9), 
                        ('5', 470.1),                       
                        ('6', 575.3),
                        ]
                                                                 
class KKB06cells_Shroud_Shane(AbstractSampleStage):
    ## 28.11.2018 LdC
    name = "KKB 6 Cells Tumbler Shroud Shane"
    in_service = False
    index_samz_pairs = [
                        ('2', 145.5), ('2_bottom(-16)', 161.5),
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
                        ('rotating gradient 370.0', 370.0),
                        ('4Bed', 364.4),
                        ('5Bed', 469.6)                       
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
    
class SANS_Demountable_12mmAperture(AbstractSampleStage): #27.10.2020 with apsel=3, and samx -6
    name = "SANS Demountable 5 Cells"
    in_service = False
    index_samz_pairs = [
                        ('1', 31.0),
                        ('2', 175.5),
                        ('3', 321.5), # CHECK TROUBLESOME
                        ('4', 467.5),
                        ('5', 613.0),
                        ]
'''   commented out 27.10.2020
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
 '''  
    
# changed from above with 10mm old Cd aperture. apselnum 1, samx -5.5. Note that this is very sensitive
# to any movement of the aperture    
    
class SANS_Hellma_10mmAperture(AbstractSampleStage):
    name = "SANS Hellma 5 Cells"
    in_service = False
    index_samz_pairs = [
                        ('1', 40.0),
                        ('2', 185.5),
                        ('3', 331.0),
                        ('4', 476.5),
                        ('5', 622.0),
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
    
class KKB16Cells_12mm(AbstractSampleStage):
    name = "KKB 16 Cells 12mm aperture"
    in_service = False
    index_samz_pairs = [
                        ('1-16', 27.7),
                        ('2-16', 67.7),
                        ('3-16', 107.7),
                        ('4-16', 147.7),
                        ('5-16', 187.7),
                        ('6-16', 227.7),
                        ('7-16', 267.7),
                        ('8-16', 307.7),
                        ('9-16', 347.7),
                        ('10-16', 387.7),
                        ('11-16', 427.7),
                        ('12-16', 467.7),
                        ('13-16', 507.7),
                        ('14-16', 547.7),
                        ('15-16', 587.7),
                        ('16-16', 627.7),
                        ] # 11.9.20 20mm cadmium on sample, 12mm aperture on aperture slider
    
class KKB16Cells_10mm(AbstractSampleStage):
    name = "KKB 16 Cells 10mm aperture"
    in_service = False
    index_samz_pairs = [
                        ('1-16', 36.3),
                        ('2-16', 76.3),
                        ('3-16', 116.3),
                        ('4-16', 156.3),
                        ('5-16', 196.3),
                        ('6-16', 236.3),
                        ('7-16', 276.3),
                        ('8-16', 316.3),
                        ('9-16', 356.3),
                        ('10-16', 396.3),
                        ('11-16', 436.3),
                        ('12-16', 476.3),
                        ('13-16', 516.3),
                        ('14-16', 556.3),
                        ('15-16', 596.3),
                        ('16-16', 636.3),
                        ] # 29.9.20 12mm cadmium on sample, 10mm aperture on aperture slider
    
    
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

