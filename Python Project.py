#!/usr/bin/python3

import time

# Function to read file content
def read_file_content(file_path):
    with open(file_path, 'r') as file:	# Open the auth.log file in read-only mode and read its content
        content = file.readlines()		# Read all lines in the file
    return content

# 1. Log Parse auth.log: Extract command usage.

# This function parses the auth.log file to extract command usage details.
def parse_auth_log(file_path):
	content = read_file_content(file_path)
	for line in content:				# Process each line to extract the required information
            # Check if the line contains a sudo command execution
            if 'COMMAND=' in line and 'sudo' in line:
                parts = line.split(';') # Split the line into parts
                # Extract the timestamp, user, and command
                
                # 1.1. Include the Timestamp.
                timestamp_parts = parts[0].strip().split()[:3]
                timestamp = ' '.join(timestamp_parts)
                
                #1.2. Include the executing user.
                user = [part.split('=')[1].strip() for part in parts if 'USER=' in part][0]
                
                # 1.3. Include the command.
                command = [part.split('=')[1].strip() for part in parts if 'COMMAND=' in part][0]
                
                # Print the extracted details
                print(f'[#] Timestamp: {timestamp}, User: {user}, Command: {command}')

# 2. Log Parse auth.log: Monitor user authentication changes

# 2.1. Print details of newly added users, including the Timestamp
def monitor_new_users(file_path):
	content = read_file_content(file_path)
	for line in content:
			if 'new user' in line:
				parts = line.split(';') # Split the line into parts
                # Extract the timestamp, user
                
                # 1.1. Include the Timestamp.
				timestamp_parts = parts[0].strip().split()[:3]
				timestamp = ' '.join(timestamp_parts)
                
                #1.2. Include the New User.
				user = [part.split('=')[1].split(',')[0].strip() for part in parts if 'name=' in part][0]
				                
                # Print the extracted details
				print('[#] New user added:')
				print(f'[#] Timestamp: {timestamp}, New User: {user}')
				print(f'[#] Details:\n  {line}')
				time.sleep(2)

# 2.2. Print details of deleted users, including the Timestamp.				
def monitor_deleted_users(file_path):
	content = read_file_content(file_path)
	for line in content:
		if 'delete user' in line:
            # Extract the timestamp
			parts = line.split()  					# Split the line into parts
			timestamp_parts = parts[:3]  			# Get the first three parts
			timestamp = ' '.join(timestamp_parts)  	# Join them to form the timestamp

            # Extract the deleted user
			user_part = line.split("'")[1]  		# Get the part between single quotes

            # Print the extracted details
			print(f'[#] Timestamp: {timestamp}, Deleted User: {user_part}')
			print(f'[#] Details:\n {line}')
			time.sleep(2)

# 2.3. Print details of changing passwords, including the Timestamp.
def monitor_passwd_changes(file_path):
	content = read_file_content(file_path)
	for line in content:		
			if 'password changed for' in line:
            # Extract the timestamp
				parts = line.split()  
				timestamp_parts = parts[:3]  
				timestamp = ' '.join(timestamp_parts)  

            # Extract the user whose password was changed
				user_part = line.split('password changed for ')[1].strip().split()[0]

            # Print the extracted details
				print(f'[#] Timestamp: {timestamp}, Password Changed for User: {user_part}')
				print(f'[#] Details:\n {line}')
				time.sleep(2)

# 2.4. Print details of when users used the su command.	
def monitor_su(file_path):
	content = read_file_content(file_path)
	for line in content:
			if(
				'session opened for user' in line and			# to filter su session opened for user
				'server su' in line and
				'server sudo' not in line and
				'session closed for user' not in line
			):		
				# Extract the timestamp
				timestamp_parts = line.split()[:3]
				timestamp = ' '.join(timestamp_parts)				
				# Extract the user who opened the session
				user = line.split(' by ')[-1].split('(')[0].strip()				
				# Extract the command 
				command = line.split(': ')[-1].strip()
				# ~ print('[#] Su command used: ')
				print(f'[#] Timestamp: {timestamp}, User: {user}, Command: {command}')
				print(f'[#] Details: \n{line}\n')


# 2.5. Print details of users who used the sudo; include the command.
# 2.6. Print ALERT! If users failed to use the sudo command; include the command.			
def monitor_sudo_users(file_path):
	content = read_file_content(file_path)
	for line in content:
			if 'COMMAND=' in line:
				parts = line.split(';')
				# Extract the timestamp
				timestamp_parts = parts[0].strip().split()[:3]
				timestamp = ' '.join(timestamp_parts)
				# Extract the user who used SUDO
				user = [part.split('=')[1].strip() for part in parts if 'USER=' in part][0]
				# Extract the command
				command = [part.split('=')[1].strip() for part in parts if 'COMMAND=' in part][0]
				# Check if it's a failed sudo attempt
				if 'sudo' in line and 'incorrect password attempts' in line:
					print(f'[!] ALERT! Failed sudo attempt: \n Timestamp: {timestamp}, User: {user}, Command: {command}')
					print(f'Details: \n {line} \n')
				else:
					print(f'[#] Timestamp: {timestamp}, User: {user}, Command: {command}')
					print(f'Details: \n {line} \n')
				time.sleep(1)
				
# This is the main fuction.
def main():
	file_path='/home/kali/Desktop/Project/Project_4/auth.log'
	#Please change file path accordingly to where auth.log is stored
	
	print('\n [*] Parsing the auth.log file to extract command usage details.\n')
	time.sleep(2)
	
	parse_auth_log(file_path)							# Call the function with the path to your auth.log file
	time.sleep(2)
	
	print('\n [*] List of New Users \n')				# Call the function to list new users
	monitor_new_users(file_path)
	time.sleep(2)
	
	print('\n [*] List of Deleted Users \n')			# Call the function to list deleted users
	monitor_deleted_users(file_path)
	time.sleep(2)
	
	print('\n [*] List of Password Changes \n')			# Call the function to list password changes
	monitor_passwd_changes(file_path)
	time.sleep(2)
	
	print('\n [*] List of Attempted su Usage \n')		# Call the function to list attempted su usage
	monitor_su(file_path)
	time.sleep(2)
	
	print('\n [*] List of Attempted SUDO Commands \n')	# Call the function to list attempted sudo commands usage
	monitor_sudo_users(file_path)
	
	time.sleep(1)
	print('\n *********** END OF SCRIPT ***********')

# Executing the main function.	
# This conditional statement checks if the script is being run directly as the main programme.
if __name__ == '__main__':			
    main()


#################### END OF SCRIPT ########################


#part 2


# 2.1. Print details of newly added users
            # ~ if 'new user' in line:
                # ~ print(f'New user added: {line}')
            # ~ # 2.2. Print details of deleted users
            # ~ if 'delete user' in line:
                # ~ print(f'User deleted: {line}')
            # ~ # 2.3. Print details of changing passwords
            # ~ if 'password changed for' in line:
                # ~ print(f'Password changed: {line}')
            # ~ # 2.4. Print details of when users used the su command
            # ~ if 'session opened for user' in line:
                # ~ print(f'su command used: {line}')
            # ~ # 2.5. Print details of users who used the sudo; include the command
            # ~ # Already covered in the sudo command execution check
            # ~ # 2.6. Print ALERT! If users failed to use the sudo command; include the command
            # ~ if 'command not allowed' in line:
                # ~ print(f'ALERT! sudo failed: {line}')
