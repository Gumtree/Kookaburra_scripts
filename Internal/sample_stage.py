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


                      

class KKB06cells_som(AbstractSampleStage):
    ## 28.11.2018 LdC
    name = "KKB 6 Cells Tumbler som"
    in_service = True
    index_samz_pairs = [('1', -12.8),
                        ('2', 92.4),
                        ('3', 197.6),
                        ('4', 302.8), 
                        ('5', 408.0), 
                        ('6', 513.2),                      
                        ]

class KKB05cells_som(AbstractSampleStage):
    # updated 12.2.2022 29mm aperture aligned by eye
    name = "KKB 5 Cells som"
    in_service = False
    index_samz_pairs = [
                        ('1', -25.5), 
                        ('2', 120.0), 
                        ('3', 265.0), 
                        ('4', 411.0),
                        ('5', 556.0),
                        ]   

class KKB16Cells_som(AbstractSampleStage):
    name = "KKB 16 Cells som"
    in_service = False
    index_samz_pairs = [
                        ('1-16', -23.5),
                        ('2-16', 16.5),
                        ('3-16', 56.5),
                        ('4-16', 96.5),
                        ('5-16', 136.5),
                        ('6-16', 176.5),
                        ('7-16', 216.5),
                        ('8-16', 256.5),
                        ('9-16', 296.5),
                        ('10-16', 336.5),
                        ('11-16', 376.5),
                        ('12-16', 416.5),
                        ('13-16', 456.5),
                        ('14-16', 496.5),
                        ('15-16', 536.5),
                        ('16-16', 576.5),
                        ] # 16.4.22 8mm cadmium
    
class KKB_Tom_pressurecell(AbstractSampleStage):
    ## 28.11.2018 LdC
    name = "High Pressure cell"
    in_service = False
    index_samz_pairs = [('Cell in', 163.5),
                        ('Cell out', 70)                     
                        ]
    
'''    
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
                           
    
    
class KKB05Roundcells_12mm_som(AbstractSampleStage):
    name = "KKB 5 Round Cells 12mm aperture som"
    in_service = False
    index_samz_pairs = [
                        ('1', -23.4),
                        ('2', 122.1), 
                        ('3', 267.6), 
                        ('4', 413.1),
                        ('5', 558.6),
                        ]
    
#   commented out 27.10.2020
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
    

    

