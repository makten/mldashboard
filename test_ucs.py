from ucsmsdk import *
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.mometa.processor import ProcessorErrorStats, ProcessorEnvStats
from ucsmsdk.ucscoreutils import get_meta_info
from ucsmsdk.utils.ucsguilaunch import ucs_gui_launch
from ucsmsdk.mometa.comm.CommDateTime import CommDateTime
from ucsmsdk.utils.ucsbackup import backup_ucs, import_ucs_backup
from ucsmsdk.mometa.equipment import EquipmentChassisStats
import json

# Connection
handle = UcsHandle("192.168.202.168", "ucspe", "ucspe")

#Login
handle.login()



## ----- Get ComputeMbTempStats ----
# comp_temp = handle.query_classid(class_id='ComputeMbTempStats')

# for temp in comp_temp:
#     print(temp)


##-----Switch stats Status --
sw_envs = handle.query_classid(class_id='ComputeRackUnit')
print(len(sw_envs))
for sw in sw_envs:
    print(sw.dn)

# flt_str = '(dn, "sys/chassis-5")'
# chas_stats = handle.query_classid(class_id='EquipmentChassis', filter_str=flt_str)
# print(len(chas_stats))

# for c in chas_stats:
#     print(c)

# for sw in sw_envs:
#     print(sw)

# print(handle.session_id, handle.cookie, handle.ip, handle.domains)


eq = handle.query_classid(class_id="EquipmentCapModSpec")

for i in eq:
    print(i)


##----Switch System status -----
# sw_sys_stats = handle.query_classid(class_id='SwSystemStats')

# for sw in sw_sys_stats:
#     print(sw)





# sp = LsServer(parent_mo_or_dn="org-root", name="sp_demo")
# handle.add_mo(sp)

# handle.commit()


# chassis = handle.query_classid(class_id="computeBlade")

# for chas in chassis:
#     print(chas)

fault = handle.query_dn("sys/switch-A/fault-F1465")
event = handle.query_dn("sys/switch-A")

# flt = '(dn, "org-root/ls-FirstVMEver.*")'
# chassis = handle.query_classid(class_id="FaultAckFaultsMeta")
# print(chassis)
# for c in chassis:
#     print('-----')

# for c in chassis:
#     print(c)

chasses = []


compute_blade = handle.query_classid(class_id="computeBlade")
# for blade in compute_blade:
        # print(blade)


# for chas in chassis:    
#     x = dict(chas.__dict__)
#     # print(x['config_state'])
#     chasses.append(json.dumps(str(x)))

    # print(s)

    # i = {
    #     "dn": chas.dn,
    #     ""
    # }

# print(chasses[0])

# compute_blade = handle.query_classid(class_id="")
# x = []
# for blade in compute_blade:  
#     print(blade)
    
#     i = {      
#             "admin_power": blade.admin_power,
#             "admin_state": blade.admin_state,
#             "availability": blade.availability,
#             "available_memory": blade.available_memory,
#             "chassis_id": blade.chassis_id,
#             "check_point": blade.check_point,
#             "child_action": blade.child_action,
#             "conn_path": blade.conn_path,
#             "conn_status": blade.conn_status,
#             "descr": blade.descr,
#             "dn": blade.dn,
#             "int_id": blade.int_id,
#             "memory_speed": blade.memory_speed,
#             "model": blade.model,
#             "name": blade.name,
#             "num_of_adaptors": blade.num_of_adaptors,
#             "num_of_cores": blade.num_of_cores,
#             "num_of_cores_enabled": blade.num_of_cores_enabled,
#             "num_of_cpus": blade.num_of_cpus,
#             "num_of_eth_host_ifs": blade.num_of_eth_host_ifs,
#             "num_of_fc_host_ifs": blade.num_of_fc_host_ifs,
#             "num_of_threads": blade.num_of_threads,
#             "oper_power": blade.oper_power,
#             "oper_state": blade.oper_state,
#             "operability": blade.operability,
#             "original_uuid": blade.original_uuid,
#             "part_number": blade.part_number,
#             "policy_level": blade.policy_level,
#             "policy_owner": blade.policy_owner,
#             "presence": blade.presence,
#             "rn": blade.rn,
#             "serial": blade.serial,
#             "server_id": blade.server_id,
#             "slot_id": blade.slot_id,
#             "status": blade.status,
#             "total_memory": blade.total_memory,
#             "uuid": blade.uuid,
#             "vendor": blade.vendor,
#             "vid": blade.vid
#         }
#     x.append(i)


# print(json.dumps(x[0]))
# print(fault)
# print(event)

# flt_str = '(dn, "sys/chassis-3/blade-1") and (severity, "minor")'
# flt_str = '(dn, "sys/chassis-.*/blade-1/.*")'

# fs = handle.query_classid(class_id="faultInst", filter_str=flt_str)
# e = handle.query_classid(class_id="EquipmentChassisStats")
# print(e)
# for i in e:
#     print(i)


# envs = []
# for stat in e:    
#     x = {
#         "dn" : stat.dn,
#         "input_current": stat.input_current,
#         "input_current_avg": stat.input_current_avg,
#         "input_current_max": stat.input_current_max,
#         "input_current_min": stat.input_current_min,
#         "intervals": stat.intervals,
#         "rn": stat.rn,
#         "status": stat.status,
#         "suspect": stat.suspect,
#         "temperature": stat.temperature,
#         "temperature_avg": stat.temperature_avg,
#         "temperature_max": stat.temperature_max,
#         "temperature_min": stat.temperature_min,
#         "thresholded": stat.thresholded,
#         "time_collected": stat.time_collected,
#         "update": stat.update
#         }
#     envs.append(x)
# print(envs[0])
# f = handle.q
# uery_classid(class_id="faultInst", filter_str=flt_str)


# for i, fl in enumerate(e):
#     x = json.dumps(fl[i])
#     print(x)
#     print(fl)


# for flt in fs:
#     print(flt)

# for b in x[0].faultInst:
#     print(b)


# blade = handle.query_dn('sys/chassis-3/blade-1')



# for blade_child_object in blade_by_dn_children:
#        print(blade_child_object)

handle.logout()

# class_meta = get_meta_info("FabricVlan")

# print(class_meta)

##-- Time Zone Update ----##
# timezone_mo = handle.query_dn("sys/svc-ext/datetime-svc")
# timezone_mo.timezone = 'Europe/Amsterdam'
# handle.set_mo(timezone_mo)
# handle.commit()
# timezone_mo = handle.query_dn("sys/svc-ext/datetime-svc")
# print(timezone_mo)


## -- backup and restore
# backup_ucs(handle,"config-all","C:\\ucs_scripts","config-all.xml")
# import_ucs_backup(handle,"C:|\ucs_scripts","config-all.xml",True)


## -- 
# compute_blade = handle.query_classid(class_id="computeBlade")

# for c in handle.query_classid("EquipmentChassis", filter_str="(dn, 'sys/chassis-6')"):
#     print(c)

# print(chassis)

# for chassis in handle.query_classid(class_id="EquipmentChassis"):    
#     print(chassis)

# print(len(compute_blade))
# print(compute_blade[1].dn, compute_blade[1].serial)
# for x in compute_blade:
#     print(x.total_memory, x.num_of_cpus)















# for chassis in handle.query_classid(class_id="equipmentFanStats"):    
#     print(chassis)
#     for chassis_child in handle.query_children(in_mo=chassis):
#         print(chassis, chassis_child)
        
        # if chassis_child.get_class_id() == 'ComputeBlade':
        #     for blade_part in handle.query_children(in_mo=chassis_child):               
                
                # if blade_part.get_class_id() == "BiosUnit":
                    # for bios_part in handle.query_children(in_mo=blade_part):
                    #     if bios_part.get_class_id() == 'FirmwareRunning':
                    #         print(chassis_child, bios_part.version