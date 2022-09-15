# MIT License

# Copyright (c) 2022 Duke University. All rights reserved.

# See LICENSE for license information
import subprocess
import argparse
import time
ETH_BYTES = "rx_vport_rdma_unicast_bytes"
ETH_PACKETS = "rx_vport_rdma_unicast_packets"

def ParseResult(results):
	val = {
		ETH_BYTES : 0.0,
		ETH_PACKETS : 0.0
	}
	for r in results:
		if ETH_BYTES in r:
			val[ETH_BYTES] = float(r.split(' ')[-1])
		if ETH_PACKETS in r:
			val[ETH_PACKETS] = float(r.split(' ')[-1])
	return val

def killall():
	try:
		subprocess.check_output("killall RdmaEngine", shell=True)
	except Exception as e:
		pass
	try:
		subprocess.check_output("killall RdmaCtrlTest", shell=True)
	except Exception as e:
		pass
	try:
		subprocess.check_output("killall ib_write_bw", shell=True)
	except Exception as e:
		pass
	try:
		subprocess.check_output("killall ib_read_bw", shell=True)
	except Exception as e:
		pass
	try:
		subprocess.check_output("killall ib_send_bw",shell=True)
	except Exception as e:
		pass
	try:
		subprocess.check_output("killall ib_atomic_bw", shell=True)
	except Exception as e:
		pass
	
		

def main():
	parser = argparse.ArgumentParser(description="Rdma Monitor")
	parser.add_argument("--action", action="store", default="monitor")
	parser.add_argument("--interface", action="store", help="The ethernet interface")
	parser.add_argument("--count", action="store", type=int, help="Number of seconds to monitor")
	args = parser.parse_args()
	if args.action == "monitor":
		intf = args.interface 
		cmd = "ethtool -S {}".format(intf)
		old_time = time.time_ns()
		results = subprocess.check_output(cmd, shell=True).decode().split('\n')
		old_val = ParseResult(results)
		time.sleep(args.count)
		new_time = time.time_ns()
		results = subprocess.check_output(cmd, shell=True).decode().split('\n')
		new_val = ParseResult(results)
		bitrate = (new_val[ETH_BYTES] - old_val[ETH_BYTES]) * 8.0 / (new_time - old_time) # ->K->M->G, ->us->ms->s
		pktrate = (new_val[ETH_PACKETS] - old_val[ETH_PACKETS]) * 1000.0 / (new_time - old_time) # ->K->M, ->us->ms->s
		print ("{}:{}".format(ETH_BYTES, bitrate))
		print ("{}:{}".format(ETH_PACKETS, pktrate))
	elif args.action == "kill":
		killall()
		

if __name__ == "__main__":
	main()