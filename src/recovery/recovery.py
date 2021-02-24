import sys, os
from pwn import *
import time
import json
from swpag_client import Team
import subprocess

# ---need to be modified---
docker_compose = '/opt/ictf/services/docker-compose.yml'

backup_map = {
	1: '~/backup/backup/backup',
	2: '~/backup/flaskids/*',
	3: '~/backup/sampleak/sampleak',
	4: '~/backup/saywhat/*'
}

original_file_path_map = {
	1: '/opt/ictf/services/backup/ro/backup',
	2: '/opt/ictf/services/flaskids/ro',
	3: '/opt/ictf/services/sampleak/ro/sampleak'
	4: '/opt/ictf/services/saywhat/ro'
}

# --------------------------
def recover_service(backup_file_path, original_file_path):
	# down
	down_cmd = ['sudo', 'docker-compose', '-f', docker_compose, 'stop']
	up_cmd = ['sudo', 'docker-compose', '-f', docker_compose, 'start', '-d']
	p_down = subprocess.Popen(down_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	outs, errs = p_down.communicate()
	print(outs)

	# copy backup file back to the original path 
	os.system('cp ' + backup_file_path + ' ' + original_file_path)
	# # change permission
	# os.system('chmod 750 ' + original_file_path)
	# # change ownership
	# os.system('chown <user>:<group> ' + original_file_path)

	# up
	p_up = subprocess.Popen(up_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	outs1, errs1 = p_up.communicate()
	print(outs1)

def get_service_ids(team):
	service_ids = []
	services = team.get_service_list()
	
	for service in services:
		service_ids.append(service['service_id'])

	return service_ids


if __name__ == '__main__':

	# insert information: game_url, team_token, team_id
	game_url = "http://34.211.129.130"
	team_token = "WOfdkzdhsZEIlPEIai49"
	team_id = "9"

	#create team object
	team = Team(game_url, team_token)

	game_status = team.get_game_status()
	service_ids = get_service_ids(team)

	while True:

		for id in service_ids:
			id_string = str(id)
			service_state = game_status['service_states'][team_id][id_string]['service_state']
			message = "TeamId: " + team_id + ", service_id: " + id_string + ", state: " + service_state
			print(message)
			# service_state can be "untested", "up", "down"
			if service_state == "down":
				print("Need recovery")
				backup_file_path = backup_map.get(id)
				original_file_path = original_file_path_map.get(id)
				recover_service(backup_file_path, original_file_path)

		time.sleep(30)
