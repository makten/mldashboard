from ucsmsdk import *
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.ucscoreutils import get_meta_info
from ucsmsdk.utils.ucsguilaunch import ucs_gui_launch
from ucsmsdk.mometa.comm.CommDateTime import CommDateTime
from ucsmsdk.utils.ucsbackup import backup_ucs, import_ucs_backup
import json



handle = None


def getUcsInfo(handle):
    """ 
        Get General UCS Information 
    """
    
    info = handle.query_classid(class_id='TopSystem')
    for ucs in info:
        ucs_info = {
            'address': ucs.address,
            'status': ucs.status,
            'name': ucs.name,
            'mode': ucs.mode,
            'owner': ucs.owner,
            'site': ucs.site,
            'system_up_time': ucs.system_up_time,            
        }

    return ucs_info


def get_chassis(handle):
    # Get all EquipmentChassis

    chassis = handle.query_classid(class_id="EquipmentChassis")

    chasses = []
    for chas in chassis:        
        x = {
            "name": chas.rn,
            "dn": chas.dn,
            "rn": chas.rn,
            "power": chas.power,
            "model": chas.model,
            "status": chas.oper_state,
            "operability": chas.operability,
            "id": chas.id,
            "serial": chas.serial,
            "part_number": chas.part_number
        }
        chasses.append(x) 

    handle.logout()
    return chasses

def getChassisStats(handle, dn):
    
    flt_str = '(dn, "sys/'+ str(dn) +'")'
    chas_stats = handle.query_classid(class_id='EquipmentChassisStats', filter_str=flt_str)

    chassis_stats = {
        # 'dn': chas_stats.dn,
        'input_power': 123343,
        'input_power_avg': 744,
        'input_power_max': 238,
        'input_power_min': 250,
        'output_power': 250,
    }

    return chassis_stats



def get_blades(handle):
    ## Get all blades from UCS    

    compute_blade = handle.query_classid(class_id="computeBlade")
    
    blades = []
    for bid, blade in enumerate(compute_blade):  
        
        flt_str = '(dn, "'+ str(blade.dn) +'/.*")'
        # stats = get_cpuStats(flt_str)
        cpu_stats = []
        for cpu in handle.query_classid(class_id="ProcessorEnvStats", filter_str=flt_str):            
            
            cp = {
                "child_action": cpu.child_action,
                "dn": cpu.dn,                
                "input_current": cpu.input_current,
                "input_current_avg": cpu.input_current_avg,
                "input_current_max": cpu.input_current,
                "input_current_min": cpu.input_current,
                "intervals": cpu.intervals,
                "rn": cpu.rn,
                "sacl": cpu.sacl,
                "suspect": cpu.suspect,
                "temperature": cpu.temperature,
                "temperature_avg": cpu.temperature_avg,
                "temperature_max": cpu.temperature_max,
                "temperature_min": cpu.temperature_min,
                "thresholded": cpu.thresholded,
                "time_collected": cpu.time_collected,
                "update": cpu.update,
                
            }
            cpu_stats.append(cp)
            
                     
        i = {       "cpu_stats": cpu_stats, 
                    "equipment": 'Chassis '+blade.chassis_id,
                    "num_cpu_cores": blade.num_of_cores_enabled,
                    "enabled_cpu_cores": blade.num_of_cores_enabled,
                    "adaptors": blade.num_of_adaptors,
                    "NICs": blade.num_of_eth_host_ifs,            
                    "admin_power": blade.admin_power,
                    "admin_state": blade.admin_state,
                    "availability": blade.availability,
                    "available_memory": blade.available_memory,
                    "chassis_id": blade.chassis_id,
                    "check_point": blade.check_point,
                    "child_action": blade.child_action,
                    "conn_path": blade.conn_path,
                    "conn_status": blade.conn_status,
                    "descr": blade.descr,
                    "dn": blade.dn,
                    "int_id": blade.int_id,
                    "memory_speed": blade.memory_speed,
                    "model": blade.model,
                    "name": blade.name,
                    "num_of_adaptors": blade.num_of_adaptors,
                    "num_of_cores": blade.num_of_cores,
                    "num_of_cores_enabled": blade.num_of_cores_enabled,
                    "num_of_cpus": blade.num_of_cpus,
                    "num_of_eth_host_ifs": blade.num_of_eth_host_ifs,
                    "num_of_fc_host_ifs": blade.num_of_fc_host_ifs,
                    "num_of_threads": blade.num_of_threads,
                    "power": blade.oper_power,
                    "oper_state": blade.oper_state,
                    "operability": blade.operability,
                    "original_uuid": blade.original_uuid,
                    "part_number": blade.part_number,
                    "policy_level": blade.policy_level,
                    "policy_owner": blade.policy_owner,
                    "presence": blade.presence,
                    "rn": blade.rn,
                    "serial": blade.serial,
                    "server_id": blade.server_id,
                    "slot_id": blade.slot_id,
                    "status": blade.status,
                    "total_memory": blade.total_memory,
                    "uuid": blade.uuid,
                    "vendor": blade.vendor,
                    "vid": blade.vid,
                    "assocState": blade.association
                }

        blades.append(i)
    
    
    handle.logout()
    
    return blades


def get_rackcomputes(handle):
    r_units = handle.query_classid(class_id='ComputeRackUnit')
    pass




def get_cpuStats(flt_str = None):
    
    cpu_stats = []
    for cpu in handle.query_classid(class_id="ProcessorEnvStats", filter_str=flt_str):            
            
            cp = {
                "child_action": cpu.child_action,
                "dn": cpu.dn,
                "input_current": cpu.input_current,
                "input_current_avg": cpu.input_current_avg,
                "input_current_max": cpu.input_current,
                "input_current_min": cpu.input_current,
                "intervals": cpu.intervals,
                "rn": cpu.rn,
                "sacl": cpu.sacl,
                "suspect": cpu.suspect,
                "temperature": cpu.temperature,
                "temperature_avg": cpu.temperature_avg,
                "temperature_max": cpu.temperature_max,
                "temperature_min": cpu.temperature_min,
                "thresholded": cpu.thresholded,
                "time_collected": cpu.time_collected,
                "update": cpu.update,
                
            }
            cpu_stats.append(cp)
    return cpu_stats
            

def get_bladestats(handle, dn):
    # Get all EquipmentChassis

    stats = handle.query_classid(class_id="EquipmentChassisSt")

    chasses = []
    for chas in stats:
        x = {
            "dn": chas.dn,
            "rn": chas.rn,
            "power": chas.power,
            "oper_state": chas.oper_state,
            "operability": chas.operability,
            "id": chas.id,
            "serial": chas.serial,
            "part_number": chas.part_number

        }
        
        chasses.append(x) 

    handle.logout()
    return chasses





def get_bladefaults(handle, chs, bld):
    # Get all EquipmentChassis
    
    flt_str = '(dn, "sys/chassis-3/' + bld + '/fault-.*")'    
    flts = fs = handle.query_classid(class_id="faultInst", filter_str=flt_str)

    faults = []
    for fl in flts:        
        x = {
            'code': fl.code,
            'cause': fl.cause,
            'created': fl.created,
            'descr': fl.descr,
            'severity': fl.severity,
            'rule': fl.rule,
            'status': fl.status,
            'type': fl.type
        }

        faults.append(x) 

    handle.logout()
    return faults


def get_cpustats(handle, chs, bld):   
    flt_str = '(dn, "sys/chassis-3/' + bld + '/fault-.*")' 
    fs = handle.query_classid(class_id="faultInst", filter_str=flt_str)
    stats = handle.query_classid(class_id="processorEnvStats", filter_str=flt_str)
    envs = []
    for stat in stats:
        x = {
            "dn" : stat.dn,
            "input_current": stat.input_current,
            "input_current_avg": stat.input_current_avg,
            "input_current_max": stat.input_current_max,
            "input_current_min": stat.input_current_min,
            "intervals": stat.intervals,
            "rn": stat.rn,
            "status": stat.status,
            "suspect": stat.suspect,
            "temperature": stat.temperature,
            "temperature_avg": stat.temperature_avg,
            "temperature_max": stat.temperature_max,
            "temperature_min": stat.temperature_min,
            "thresholded": stat.thresholded,
            "time_collected": stat.time_collected,
            "update": stat.update
        }
    envs.append(x)
    
    return envs

def domain_serials(handle):
    """
    This function will query all of the models and serial numbers from the ucs domain
    Args:
        handle (UcsHandle)
    
    Returns:
        Dictionary of dn, model, and serial for chassis, interconnects, and blades
    Raises:
        None
    Example:
        domain_serials(handle)
    """
    
    query_dict = {}
    query_dict['chassis'] = {}
    query_dict['fi'] = {}
    query_dict['blade'] = {}

    query_data = handle.query_classids('orgOrg', 'EquipmentChassis', 'NetworkElement', 'ComputeBlade')

    for chassis in query_data['EquipmentChassis']:
        query_dict['chassis'][chassis.dn] = {}
        query_dict['chassis'][chassis.dn]['model'] = chassis.model
        query_dict['chassis'][chassis.dn]['serial'] = chassis.serial

    for fi in query_data['NetworkElement']:
        query_dict['fi'][fi.dn] = {}
        query_dict['fi'][fi.dn]['model'] = fi.model
        query_dict['fi'][fi.dn]['serial'] = fi.serial

    for blade in query_data['ComputeBlade']:
        query_dict['blade'][blade.dn] = {}
        query_dict['blade'][blade.dn]['model'] = blade.model
        query_dict['blade'][blade.dn]['serial'] = blade.serial

    return query_dict



# flt_str = '(dn, "sys/chassis-3/blade-1") and (severity, "minor")'
# flt_str = '(dn, "sys/chassis-3/blade-1")'

# fs = handle.query_classid(class_id="faultInst", filter_str=flt_str)
# e = handle.query_classid(class_id="processorEnvStats", filter_str=flt_str)
# f = handle.query_classid(class_id="faultInst", filter_str=flt_str)


# for i, fl in enumerate(e):
#     x = json.dumps(fl[i])
#     print(x)
#     print(fl)


# for flt in fs:
#     print(flt)

# for b in x[0].faultInst:
#     print(b)