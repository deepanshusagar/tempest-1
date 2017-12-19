import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler

#If you want to cleanup all test resources like vms, volumes, workloads then set
# following cleanup parameter value to True otherwise False
cleanup = True

# pre requisite paramter
pre_req = True

#Test results for reporting
PASS = "PASS"
FAIL = "FAIL"

#Id of workload type "parallel"
parallel="2ddd528d-c9b4-4d7e-8722-cc395140255a"

#Resources to use from file
#Please add your resources one on each line in files: tempest/tempest/vms_file, volumes_file, workloads_file
vms_from_file=False
volumes_from_file=False
workloads_from_file=False

#CLI configuration parameters
workload_type_id="f82ce76f-17fe-438b-aa37-7a023058e50d"
workload_name="clitest"
source_platform="openstack"
snapshot_name = "test2-snapshot"
snapshot_type_full = "full"
restore_name = "test-oneclick-restore"
selective_restore_name = "test-selective-restore"
restore_filename = "/opt/restore.json"
vm_license_filename = "test_licenses/tvault_license_10VM.txt"
capacity_license_filename = "test_licenses/tvault_license_100GB.txt"
compute_license_filename = "test_licenses/tvault_license_10compute.txt"
invalid_license_filename = "test_licenses/tvault_license_invalid.txt"
expired_license_filename = "test_licenses/tvault_license_expired.txt"

workload_modify_name = "test2-new"
workload_modify_description = "test2-new-description"
restore_type = "restore"
global_job_scheduler=False

tvault_ip = "192.168.1.116"
tvault_dbusername = "root"
tvault_dbpassword = "52T8FVYZJse"
tvault_dbname = "workloadmgr"

no_of_compute_nodes = 1

# Scheduler parameter
interval="1 hrs"
enabled='false'
retention_policy_type="Number of Snapshots to Keep"
retention_policy_value="3"
schedule_report_file="scheduleReport.txt"
sched=BlockingScheduler()
count=0
No_of_Backup=1

# test parameters
key_pair_name  = "tempest_test_key_pair"
instance_username = "ubuntu"
snapshot_restore_name = "Tempest Test Restore"
restored_instance_flavor = 2
security_group_id = "baaae013-75d5-4821-806c-2cb259c95fb4"
security_group_name = "test_security"
flavor_name = "test_flavor"
