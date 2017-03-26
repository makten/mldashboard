from ucsmsdk import *
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.ucscoreutils import get_meta_info
from ucsmsdk.utils.ucsguilaunch import ucs_gui_launch
from ucsmsdk.mometa.comm.CommDateTime import CommDateTime
from ucsmsdk.utils.ucsbackup import backup_ucs, import_ucs_backup

# Connection
# handle = UcsHandle("192.168.202.137", "ucspe", "ucspe")


#Login
# handle.login()


def get_blades(handle):
    ## Get all blades from UCS
    compute_blade = handle.query_classid(class_id="computeBlade")
    blades = []

    blades = []
    for blade in compute_blade:  
        print(blade)  
        i = {      
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
                "oper_power": blade.oper_power,
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
                "vid": blade.vid
            }
        blades.append(i)

    
    handle.logout()
    
    return blades




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

