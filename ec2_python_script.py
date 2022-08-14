"""
PYTHON PORTFOLIO PROJECT
Joshua Zavala
New Apprenticeship
AWS Cloud Practitioner Project
26.05.2022

OBJECTIVE
1. Prompt the user for an EC2 instance name
2. Check your AWS account if the name already exists (Hint: Check the values of EC2 instances tagged with the key 'Name')
  a. If returns true, notify the user and prompt for the instance name again
  b. If returns false
    i. Create a t3.micro EC2 instance
   ii. Add a security group to permit SSH into the virtual machine
  iii. Check status of the instance every 10 seconds
      1. While the EC2 instance is in the pending state, notify the user it is still pending.
      2. When the EC2 instance reaches the running state, notify the user it is running and just waiting on the health checks
3. Exit the script
"""

########### IMPORTS ###########
import boto3
import getpass
import os
import time

########### FUNCTIONS #########
# user is greeted on program start with this introduction message
def greetings ():
	formatting ()
	print ("""EC2 CREATION SCRIPT
This script will create an Amazon Web Services EC2 Instance based on your input.

  GREETINGS:
  Welcome to the EC2 Creation Script!
  
  NOTES:
  To quit the program, use one of these methods.
  QUIT METHOD 1: At any input section, enter \"q\" and press \"Enter\" to exit.
  QUIT METHOD 2: At any time during the script, press key combination \"Ctrl + c\" to exit.
  
  This program uses two methods to login to AWS and you will need your AWS-CLI login credentials for both.
  LOGIN METHOD 1: AWS Session - Input your credentials every time this program runs due to it being a temporary session. 
  LOGIN METHOD 2: AWS Local - you will have to set your AWS-CLI credentials using the command \"aws configure\" in the terminal before running this script.
  
  *If option 1 is chosen and when prompted to enter your AWS-CLI login credentials, it is recommended to copy and paste them in then clear the clipboard after.""")

# user chooses which login method to use then sends the result to login ()
def login_choice ():
	formatting ()
	time.sleep (1)
	print ("CHOOSE LOGIN METHOD")
	print ("Enter \"s\" to use temporary AWS Session login or \"l\" to use an AWS Local default login session.")
	time.sleep (1)
	
	while True:
		# gets user input
		user_choice = input ("\n  LOGIN METHOD: ")
		# checks user input for "q" key then if found exits the program
		quit (user_choice)
		
		# tries to convert a single character string into an integer and if it fails it throws an exception
		try:
			user_choice = user_choice.lower ()
			if user_choice == "s":
				print (action_approved () + " AWS Session login will be used for EC2 creation.")
				return True
			elif user_choice == "l":
				print (action_approved () + " AWS Local login will be used for EC2 creation.")
				return False
			# if any other choice not 1 or 2 the user will be asked to try again.
			else:
				print (action_denied () + " \"" + user_choice + "\" is not a valid option.\n" + solution () + " option.")
				continue
		# if try cannot change the case to lower case then the user will be asked to try again
		except:
			print (action_denied (), user_choice, "is not a valid option.\n" + solution () + " option.")
			continue

# user credential handling based on login method and then sending user choice into a function to create the instance based on the aws session used
def login (login_method):
	time.sleep (1)
	print ("\n  --- LOGGING IN")
	
	stop = False
	while stop == False:
		if login_method == True:
			print ("  Enter your AWS-CLI credentials to login. The Secret Access Key is hidden on entry.")
			time.sleep (1)
			public_key = input ("\n  Enter your AWS Access Key Id: ")
			quit (public_key)
			
			private_key = getpass.getpass ("  Enter your AWS Secret Access Key: ")
			quit (private_key)
			
			session = boto3.Session (
				aws_access_key_id = public_key,
				aws_secret_access_key = private_key
			)
			
			stop = True
			checking ()
			print (action_approved () + " Login complete.")
			return session
			
		else:
			print ("  AWS-CLI locally configured credentials will be used to login.")
			time.sleep (1)
			
			stop = True
			print ("\n  --- USING DEFAULT CREDENTIALS")
			time.sleep (1)
			print (action_approved () + " Login complete.")
			return True

# start of instance creation with declaring an ec2 resource then calling name_instance ()
def declare_instance (login_type):
	formatting ()
	time.sleep (1)
	print ("CREATING THE INSTANCE")
	print ("This section will create an EC2 instance based on user input or N. Virginia region defaults")
	time.sleep (1)
	
	print ("\n  STEP 1: DECLARE THE INSTANCE\n  An EC2 resource will be delcared based on user login method in order to create an EC2 instance.")
	time.sleep (1)
	region = default_input ()
	if login_type == True:
		# declaring the instance resource based on default login session
		ec2 = boto3.resource ("ec2", region_name = region [1])
		print ("\n  --- DECLARING INSTANCE")
		time.sleep (1)
		print (action_approved () + " Instance declared using local credentials.")
		return ec2
	else:
		# declaring the instance resource based on user login session
		ec2 = login_type.resource ("ec2", region_name = region [1])
		print ("\n  --- DECLARING INSTANCE")
		time.sleep (1)
		print (action_approved () + " Instance declared using session credentials.")
		return ec2

# naming the instance and then calling check_name () to check the names availability then calls create_settings () to create it
def name_instance (ec2):
	time.sleep (1)
	print ("\n  STEP 2: NAME THE INSTANCE")
	print ("  Choose a name for the instance.")
	time.sleep (1)
	
	stop = False
	while stop == False:
		ec2_name = input ("\n  EC2 instance name: ")
		quit (ec2_name)
		
		if check_name (ec2_name, ec2) == True:
			continue
		else:
			return ec2_name

# checks the name of the instance for availability then sends either True or False back to name_instance ()
def check_name (ec2_name, ec2):
	checking ()
	
	instances = ec2.instances.all ()
	count = 0
	try:
		for instance in instances:
			if instance.tags [0]["Value"] == ec2_name:
				count = count + 1
	except:
		print ("\n  DEV ERROR MESSAGE: check the check_name () function for errors.\n")

	if count == 0:
		print (action_approved () + " Instance Name \"" + ec2_name + "\" is available for use.")
		return False
	else:
		print (action_denied () + " Instance Name \"" + ec2_name + "\" is already in use.\n" + solution () + " name.")
		return True

# creates the settings for the instance and then calls create_instance () with the settings declared
def create_settings (ec2_name, ec2):
	time.sleep (1)
	print ("\n  STEP 3: CONFIGURE THE INSTANCE SETTINGS")
	print ("  This will create the instance from user input or from default settings for US-East-1, N. Virginia.")
	time.sleep (1)
	
	stop = False
	while stop == False:
		user_in = input ("\n  Enter \"y\" to use default settings or \"n\" to enter your own: ")
		quit (user_in)
		
		checking ()
		user_in = user_in.lower ()
		if user_in == "y":
			print (action_approved () + "  The instance will use default settings.")
			stop = True
			
			# calls default_input () to get the list of default settings
			ec2_settings = default_input ()
			time.sleep (1)
			print ("\n  --- DEFAULT SETTINGS TO USE:")
			time.sleep (1)
			for default in ec2_settings:
				print ("  " + default)
			
			return ec2_settings
			
		elif user_in == "n":
			print (action_approved () + " The instance will use user defined settings.")
			stop = True
			
			# calls user_input () to get the list of user defined settings
			ec2_settings = user_input ()
			time.sleep (1)
			print ("\n  --- USER SETTINGS TO USE:")
			time.sleep (1)
			for user in ec2_settings:
				print ("  " + user)
			
			return ec2_settings
			
		else:
			print (action_denied () + " \"" + user_in + "\" is not a valid option.\n" + solution () + " option")
			continue

# default settings used for the ec2 creation
def default_input ():
	default_ami_id = "ami-0022f774911c1d690"           # 0 Amazon Linux 2 Kernel 5.10 AMI 2.0.20220426.0 x86_64 HVM gp2
	default_aws_region = "us-east-1"                   # 1 us-east-1, N. Virginia
	default_instance_type = "t2.micro"                 # 2 t2.micro
	default_subnet_id = "subnet-0e73890a8e6d3b463"     # 3 us-east-1a
	default_vpc_id = "vpc-044300ed69506ff0d"           # 4 us-east-1 default vpc
	
	default_settings = [default_ami_id, default_aws_region, default_instance_type, default_subnet_id, default_vpc_id]
	# makes sure all entries are lower case
	default_settings = lower_case (default_settings)
	
	return default_settings

# user defined settings used for the ec2 creation
def user_input ():
	time.sleep (1)
	print ("\n  --- ENTERING USER SETTINGS")
	print ("  Enter your desired settings for the EC2 Instance.")
	time.sleep (1)
	
	print ("\n  AMI ID format: ami-0032a704412c1e271")
	user_ami_id = input ("  AMI ID: ")
	quit (user_ami_id)
	user_ami_id = user_input_to_default (user_ami_id, 0)
	time.sleep (1)
	
	print ("\n  AWS Region format: us-east-2")
	user_aws_region = input ("  AWS Region: ")
	quit (user_aws_region)
	user_aws_region = user_input_to_default (user_aws_region, 1)
	time.sleep (1)
	
	print ("\n  Instance Type format: t2.micro")
	user_instance_type = input ("  Instance Type: ")
	quit (user_instance_type)
	user_instance_type = user_input_to_default (user_instance_type, 2)
	time.sleep (1)
	
	print ("\n  Subnet ID format: subnet-0e8a400b8o6w2m142")
	user_subnet_id = input ("  Subnet ID: ")
	quit (user_subnet_id)
	user_subnet_id = user_input_to_default (user_subnet_id, 3)
	time.sleep (1)
	
	print ("\n  VPC ID format: vpc-022300at17206eh8d")
	user_vpc_id = input ("  VPC ID: ")
	quit (user_vpc_id)
	user_vpc_id = user_input_to_default (user_vpc_id, 4)
	
	user_settings = [user_ami_id, user_aws_region, user_instance_type, user_subnet_id, user_vpc_id]
	# makes sure all entries are lower case
	user_settings = lower_case (user_settings)
	
	return user_settings
	
# if user does not want to change defaults on some settings then they don't have to enter anything and just press the "Enter" key
def user_input_to_default (user_input_to_default_setting, user_input_to_default_number):
	user_input_settings = default_input ()
	
	if user_input_to_default_setting == "":
		# checks the ami input section and returns default ami
		if user_input_to_default_number == 0:
			return user_input_settings [0]
		
		# checks the region input section and returns default region
		if user_input_to_default_number == 1:
			return user_input_settings [1]
			
		# checks the type input section and returns default type
		if user_input_to_default_number == 2:
			return user_input_settings [2]
		
		# checks the subnet input section and returns default subnet 
		if user_input_to_default_number == 3:
			return user_input_settings [3]
		
		# checks the vpc input section and returns default vpc
		if user_input_to_default_number == 4:
			return user_input_settings [4]
		
	else:
		return user_input_to_default_setting

# allows the user to either create a new key pair and saves it in the home directory or to either use an existing key pair
def choose_key (ec2):
	time.sleep (1)
	print ("\n  --- STEP A: CHOOSE SSH KEY METHOD")
	print ("  Choose to create a new ssh key pair or use an existing one.")
	time.sleep (1)
	
	stop = False
	while stop == False:
		user_input = input ("\n  Would you like to create a new key pair? Enter \"y\" or \"n\": ")
		quit (user_input)
		
		if user_input == "y":
			checking ()
			print (action_approved () + "  SSH key pair will be created.")
			time.sleep (1)
			
			key_name = input ("\n  Enter the name of your new key pair: ")
			quit (key_name)
			
			if key_name [-4:] == ".pem":
				key_name = key_name [:-4]
			
			ssh_keys = ec2.create_key_pair (
				KeyName = key_name,
				TagSpecifications = [
					{
						"ResourceType": "key-pair",
						"Tags": [
							{
								"Key": "Name",
								"Value": key_name
							},
						]
					},
				]
			)
			create_key_file (key_name, ssh_keys)
			stop = True
			return key_name
			
		elif user_input == "n":
			checking ()
			print (action_approved () + "  Existing key pair will be used.")
			
			key_name = input ("\n  Enter the name of your existing key pair: ")
			quit (key_name)
			
			if key_name [-4:] == ".pem":
				key_name = key_name [:-4]
			
			checking ()
			print (action_approved () +  "\"" + key_name + ".pem\" is set as your key pair to use.")
			stop = True
			
			return key_name
			
		else:
			print (action_denied () + "\"" + user_input + "\" is not an option.\n" + solution () + " option.\n")
			continue

# this function will save your private access key for ssh login to the home directory in linux
def create_key_file (key_name, ssh_keys):
	time.sleep (1)
	print ("\n  --- SAVING SSH KEY")
	print ("  Saving the new ssh key to the home directory.")
	time.sleep (1)
	
	checking ()
	print (action_approved () + "\"" + key_name + ".pem\" will be saved in the home directory.")

	key_file_name = key_name + ".pem"
	key_private_key = ssh_keys.key_material
	key_file = open (key_file_name, "w")
	key_file.write (key_private_key)
	key_file.close ()

# creates a security group to use for the ec2 instance and returns it to create_instance ()
def create_security_group (ec2, ec2_vpc_id):
	time.sleep (1)
	print ("\n  --- STEP B: CREATE SECURITY GROUP")
	print ("  Creates a security group to allow ssh traffic")
	time.sleep (1)
	
	security_group_name = input ("\n  Enter a name for your Security Group: ")
	quit (security_group_name)
	time.sleep (1)
	
	group_name = input ("  Enter a description for your Security Group: ")
	quit (group_name)
	
	checking ()
	print (action_approved () + "\"" + security_group_name + "\" security group is set.")
	
	security_group = ec2.create_security_group (
		Description = "Allow inbound SSH traffic",
		GroupName = group_name,
		VpcId = ec2_vpc_id,
		TagSpecifications = [
			{
				"ResourceType": "security-group",
				"Tags": [
					{
						"Key": "Name",
						"Value": security_group_name
					},
				]
			},
		],
	)
	security_group.authorize_ingress (
		CidrIp = "0.0.0.0/0",
		FromPort = 22,
		ToPort = 22,
		IpProtocol = "tcp",
	)
	
	return security_group.id

# This function creates the instance and then calls check_instances () to check the state of the instance
def create_instance (ec2_name, ec2_settings, ec2):
	time.sleep (1)
	print ("\n  STEP 4: CREATE THE INSTANCE")
	print ("  Creating the instance with user settings.")
	time.sleep (1)
	
	instances = ec2.create_instances (
		MinCount = 1,
		MaxCount = 1,
		ImageId = ec2_settings [0],
		InstanceType = ec2_settings [2],
		# calls choose_key () function to create a new ssh key pair or use an existing one
		KeyName = choose_key (ec2),
		SecurityGroupIds = [
			create_security_group (ec2, ec2_settings [4]),
		],
		SubnetId = ec2_settings [3],
		TagSpecifications = [
			{
				"ResourceType": "instance",
				"Tags": [
					{
						"Key": "Name",
						"Value": ec2_name
					},
				]
			},
		]
	)
	check_instances (instances)

# checks the state of the instance to make
def check_instances (instances):
	time.sleep (1)
	print ("\n  --- FINAL STEP: CHECK INSTANCE STATE")
	print ("  This section is checking the state of the instance and will notify every 10 seconds until it is running.")
	time.sleep (1)
	
	checking ()
	for instance in instances:
	
		stop = False
		while stop == False:
			instance.reload ()
			state = instance.state ["Code"]
			
			if state == 48:
				print ("  \"" + instance.tags [0]["Value"] + "\" instance is terminated.")
				stop = True
				
			elif state == 16:
				print ("  \"" + instance.tags [0]["Value"] + "\" instance is running. Status Checks Initializing.")
				stop = True
				
			elif state == 0:
				print ("  \"" + instance.tags [0]["Value"] + "\" instance is pending.")
				
				then = int (time.strftime ("%s", time.localtime ())) + 10
				quit = False
				while quit == False:
					timer = int (time.strftime ("%s", time.localtime ()))
					instance.reload ()
					state = instance.state ["Code"]
					if timer == then:
						print ("  \"" + instance.tags [0]["Value"] + "\" instance is still pending.")
						then = int (time.strftime ("%s", time.localtime ())) + 10
						continue
					elif state == 16:
						quit = True
					else:
						continue
				continue
			
			elif state == 32:
				print ("  \"" + instance.tags [0]["Value"] + "\" instance is shutting down.")
				
				then = int (time.strftime ("%s", time.localtime ())) + 10
				quit = False
				while quit == False:
					timer = int (time.strftime ("%s", time.localtime ()))
					
					instance.reload ()
					state = instance.state ["Code"]
					if timer == then:
						print ("  \"" + instance.tags [0]["Value"] + "\" instance is still shutting down.")
						then = int (time.strftime ("%s", time.localtime ())) + 10
						continue
					elif state == 48:
						quit = True
					else:
						continue
				continue
				
			else:
				continue
	time.sleep (1)

# goodbye message to display at the end of the program
def goodbyes ():
	formatting ()
	time.sleep (1)
	print ("EC2 INSTANCE HAS BEEN CREATED.\nBe sure to give your new SSH key the required permissions to login to your new instance.\n\nThank you for using this script to build an ec2 instance.")
	time.sleep (1)

# function to get the hour of day to display a small goodbye to the user on exiting the program
def check_time ():
	time_of_day = int (time.strftime ("%H", time.localtime()))
	bye = "  Have a great"
	if time_of_day in range (5, 12):
		print (bye, "morning!")
	elif time_of_day in range (12, 17):
		print (bye, "afternoon!")
	elif time_of_day in range (17, 21):
		print (bye, "evening!")
	elif time_of_day in range (21, 24) or time_of_day in range (0, 5):
		print (bye, "night!")
	else:
		print ("\nDEV ERROR MESSAGE: Check the check_time () function for errors.\n")

# quit function to check for "q" on any input section of the program to quit then and there
def quit (input):
	try:
		input = str (input)
		
	except:
		return input
	
	if len (input) > 1:
		return input
	
	input = input.lower ()
	
	if input == "q":
		checking ()
		print (action_approved () + "  The program will now exit.")
		print ("\n  --- EXITING PROGRAM")
		time.sleep (1)
		check_time ()
		formatting ()
		raise os._exit (0)
		
	else:
		return input

# function to lower case the input from users in the settings section because that is what is required on input for AWS
def lower_case (settings_list):
	return_list = []
	return_str = ""
	
	if isinstance (settings_list, list) == True:
		for setting in settings_list:
			setting = setting.lower ()
			return_list.append (setting)
		return return_list
		
	elif isinstance (settings_list, str) == True and len (settings_list) == 1:
		return_str = settings_list.lower ()
		return return_str
		
	elif isinstance (settings_list, str) == True and len (settings_list) > 1:
		return settings_list
		
	else:
		print ("\nDEV ERROR MESSAGE: Check the lower_case () function for errors.\n")

# small action approved message for easier formatting and editing
def action_approved ():
	return "  ACTION: APPROVED\n  MESSAGE:"

# small action denied message for easier formatting and editing
def action_denied ():
	return "  ACTION: DENIED\n  MESSAGE: Wrong selection"

# small solution message for easier formatting and editing
def solution ():
	return "  SOLUTION: Please choose a valid"

# small checking message for easier formatting and editing
def checking ():
	print ("\n  --- CHECKING INPUT")
	time.sleep (1)

# small function for seperating main sections of the program
def formatting ():
	print ("-" * 100)

###### MAIN ##############
if __name__ == "__main__":
	# Try and except statement to catch the "Ctrl + c" quit method
	try:
		# Greeting message and program description along with some rules for the user to interact with the script
		greetings ()
		
		# will either have True or False
		main_login_choice = login_choice ()
		
		# will either have session or True
		main_login = login (main_login_choice)
		
		# will store the ec2 session
		main_declare_instance = declare_instance (main_login)
		
		# stores the name of the ec2 instance that the user will give
		main_name_instance = name_instance (main_declare_instance)
		
		# stores the settings that will be used for the instance
		main_create_settings = create_settings (main_name_instance, main_declare_instance)
		
		# now to create the instance with user settings
		create_instance (main_name_instance, main_create_settings, main_declare_instance)
		
		# Goodbye message and start of end of program
		goodbyes ()
		
		# Program is over exiting program
		formatting ()
		time.sleep (1)
		print ("END OF PROGRAM")
		print ("The program will now end.")
		print ("\n  --- EXITING PROGRAM")
		time.sleep (1)
		check_time ()
		formatting ()
		raise os._exit (0)
	
	# if keyboard interrupt exception thrown quit the program
	except KeyboardInterrupt:
		print ()
		quit ("q")
