import sys
import os
sys.path.append(os.getcwd())
from tempest.api.workloadmgr import base
from tempest import config
from tempest import test
from oslo_log import log as logging
from tempest import tvaultconf
from tempest import reporting
import time
from tempest import command_argument_string
from tempest.util import cli_parser
from tempest.util import query_data

LOG = logging.getLogger(__name__)
CONF = config.CONF

class WorkloadTest(base.BaseWorkloadmgrTest):

    credentials = ['primary']

    @classmethod
    def setup_clients(cls):
        super(WorkloadTest, cls).setup_clients()
        cls.client = cls.os.wlm_client
	reporting.add_test_script(str(__name__))

    @test.attr(type='smoke')
    @test.idempotent_id('9fe07175-912e-49a5-a629-5f52eeada4c9')
    def test_tvault1294_delete_snapshot(self):
	try:
	    #Prerequisites
            self.created = False
            self.workload_instances = []
            self.volume_snapshots = []
        
            #Launch instance
            self.vm_id = self.create_vm()
            LOG.debug("VM ID: " + str(self.vm_id))

            #Create volume
            self.volume_id = self.create_volume(tvaultconf.volume_size,tvaultconf.volume_type)
            LOG.debug("Volume ID: " + str(self.volume_id))
        
            #Attach volume to the instance
            self.attach_volume(self.volume_id, self.vm_id)
            LOG.debug("Volume attached")

            #Create workload
            self.workload_instances.append(self.vm_id)
            self.wid = self.workload_create(self.workload_instances, tvaultconf.parallel, workload_name=tvaultconf.workload_name)
            LOG.debug("Workload ID: " + str(self.wid))
            time.sleep(5)
        
            #Create snapshot
            self.snapshot_id = self.workload_snapshot(self.wid, True, tvaultconf.snapshot_name, snapshot_cleanup=False)
            LOG.debug("Snapshot ID: " + str(self.snapshot_id))
        
            wc = self.wait_for_snapshot_tobe_available(self.wid,self.snapshot_id)
            if (str(wc) == "available"):
                LOG.debug("Workload snapshot successfully completed")
                self.created = True
            else:
                if (str(wc) == "error"):
                    pass
            if (self.created == False):
                raise Exception ("Workload snapshot did not get created")
        
            #Delete snapshot using CLI command
            rc = cli_parser.cli_returncode(command_argument_string.snapshot_delete + self.snapshot_id)
            if rc != 0:
	        reporting.add_test_step("Execute snapshot-delete command", tvaultconf.FAIL)
                raise Exception("Command did not execute correctly")
            else:
    	        reporting.add_test_step("Execute snapshot-delete command", tvaultconf.PASS)
                LOG.debug("Command executed correctly")
            time.sleep(5)
            wc = query_data.get_workload_snapshot_delete_status(tvaultconf.snapshot_name,tvaultconf.snapshot_type_full, self.snapshot_id)
            LOG.debug("Snapshot Delete status: " + str(wc))
            if (str(wc) == "1"):
    	        reporting.add_test_step("Verification", tvaultconf.PASS)
                LOG.debug("Workload snapshot successfully deleted")
            else:
   	        reporting.add_test_step("Verification", tvaultconf.FAIL)
                raise Exception ("Snapshot did not get deleted")
        
            #Cleanup
            #Delete volume
            self.volume_snapshots = self.get_available_volume_snapshots()
            self.delete_volume_snapshots(self.volume_snapshots)
	    reporting.test_case_to_write()

        except Exception as e:
            LOG.error("Exception: " + str(e))
            reporting.set_test_script_status(tvaultconf.FAIL)
            reporting.test_case_to_write()
