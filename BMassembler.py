#---------------------------------------------------------------------------------------------------------------
#                         Predefined Items Starts

rTypes = ["add","move","slt","jr","sll"]
iTypes = ["addi","slti","lw","sw","beq","bne"]
jTypes = ["j","jal"]

labels = {}
function = {'jr':'8', 'jal':'9', 'add':'100000', 'slt':'2a', 'sll':'00', 'srl':'02'}
opcodes = {'beq':'4', 'bne':'5', 'jr':'0', 'jal':'0', 'j':'0', 'add':'0', 'slt':'0',
			'sll':'0', 'srl':'0', 'lw':'23','sw':'2b','addi':'8','slti':'a','move':'0'
		}


register = {'zero':'00000','at':'00001','v0':'00010','v1':'00011','a0':'00100','a1':'00101','a2':'00110','a3':'00111',
            't0':'01000','t1':'01001','t2':'01010','t3':'01011','t4':'01100','t5':'01101','t6':'01110','t7':'01111',
            's0':'10000','s1':'10001','s2':'10010','s3':'10011','s4':'10100','s5':'10101','s6':'10110','s7':'10111',
            't8':'11000','t9':'11001','k0':'11010','k1':'11011','gp':'11100','sp':'11101','fp':'11110','ra':'11111'
			}

#                         Predefined Items Ends
#---------------------------------------------------------------------------------------------------------------
#                         Math Convert Parts Starts

def hexToDec(s):
	return int(s, 16)


def binToHex(inputt,places):
	ret = hex(int(inputt, 2))[2:].zfill(places).replace('0x','')
	return ret


def hexToBin(inputt,bits):
	ret = bin(int(inputt, 16))[2:].zfill(bits)
	return ret


def decToBin(inputt,bits):
    inputt = int(inputt)
    if inputt < 0:
        return decToTwosComplment(inputt,bits)
    else:
        return bin(int(str(inputt),10))[2:].zfill(bits)


def decToTwosComplment(inputt, bits):
    intIn = int(inputt)
    if intIn>=0:
    	val = decToBin(intIn, bits)  
    else:
        msb = -2**bits
        rest = msb-intIn
        val = decToBin(rest,bits-1)
        val = val.replace('b','')
    return val

#                         Math Convert Parts Ends
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#                         Type Individual Funcs Starts

def addiType(line):
    label = isLabel(line)

    op = hexToBin(opcodes[line[label]],6)
    rs = register[line[label+2]].zfill(5)
    rt = register[line[label+1]].zfill(5)
    number = decToBin(line[label+3],16)

    binary = op + rs + rt + number
    hexcode = binToHex(binary,8)

    return hexcode


def sltiType(line):
	label = isLabel(line)

	op = hexToBin(opcodes[line[label]],6)
	rs = register[line[label+2]]
	rt = register[line[label+1]]
	number = decToBin(line[label+3],16)
    
	binary = op + rs + rt + number
	hexcode = binToHex(binary,8)

	return hexcode


def lwType(line):
	label = isLabel(line)

	op = hexToBin(opcodes[line[label]],6)
	rt = register[line[label+1]]
	rs = register[line[label+3]]
	number = decToBin(line[label+2],16)

	binary = op + rs + rt + number
	hexcode = binToHex(binary,8)

	return hexcode


def swType(line):
	label = isLabel(line)

	op = hexToBin(opcodes[line[label]],6)
	rs = register[line[label+3]]
	rt = register[line[label+1]]
	number = decToBin(line[label+2],16)

	binary = op + rs + rt + number
	hexcode = binToHex(binary,8)

	return hexcode


def beqType(line):
    label = isLabel(line)

    op = hexToBin(opcodes[line[label]],6)
    rs = register[line[label+2]].zfill(5)
    rt = register[line[label+1]].zfill(5)

    address = hexToBin( labels[ line[label+3]+":"][-4:], 16)

    binary = op + rs + rt + address
    hexcode = binToHex(binary,8)

    return hexcode


def bneType(line):
	label = isLabel(line)

	op = hexToBin(opcodes[line[label]],6)
	rs = register[line[label+2]].zfill(5)
	rt = register[line[label+1]].zfill(5)
	address = hexToBin( labels[ line[label+3]+":"][-4:], 16)

	binary = op + rs + rt + address
	hexcode = binToHex(binary,8)

	return hexcode


def jumpType(line):
	label = isLabel(line)
	op = opcodes[line[label]]
	temp = "0x" + labels[line[label+1]+":"][-4:]
	number = hexToBin(temp,4)
	hexcode = binToHex(op+number,8)
	return hexcode


def jalType(line):
	label = isLabel(line)
	op = opcodes[line[label]]
	temp = "0x" + labels[line[label+1]+":"][-4:]
	number = hexToBin(temp,4)
	hexcode = binToHex(op+number,8)
	return hexcode


def RaddType(line):
    label = isLabel(line)
    
    op = opcodes[line[label]].zfill(6)
    rs = register[line[label+2]]
    rt = register[line[label+3]]
    rd = register[line[label+1]]
    shamt = '00000'
    funct = function[line[label]]

    binary = op + rs + rt + rd + shamt + funct
    hexcode = binToHex(binary,8)

    return hexcode


def RsltType(line):
	label = isLabel(line)

	op = opcodes[line[label]].zfill(6)
	rs = register[line[label+2]]
	rt = register[line[label+3]]
	rd = register[line[label+1]]
	funct = hexToBin(function[line[label]],11)

	binary = op + rs + rt + rd + funct
	hexcode = binToHex(binary,8)

	return hexcode


def RjrType(line):
	label = isLabel(line)

	op = opcodes[line[label]].zfill(6)
	rs = register[line[label+1]]
	funct = hexToBin(function[line[label]],20)

	binary = op + rs + funct
	hexcode = binToHex(binary,8)

	return hexcode
	

def RsllType(line):
	label = isLabel(line)

	op = opcodes[line[label]].zfill(6)
	rt = register[line[label+2]]
	rd = register[line[label+1]]
	shamt = decToBin(line[label+3],5)
	funct = hexToBin(function[line[label]],6)

	binary = op + rt + rd + shamt + funct
	hexcode = binToHex(binary,8)

	return hexcode


def RsrlType(line):
	label = isLabel(line)

	op = opcodes[line[label]].zfill(6)
	rt = register[line[label+2]]
	rd = register[line[label+1]]
	shamt = decToBin(line[label+3],5)
	funct = hexToBin(function[line[label]],6)

	binary = op + rt + rd + shamt + funct

	hexcode = binToHex(binary,8)

	return hexcode


def RmoveType(line):
	
	label = isLabel(line)

	op = opcodes[line[0]].zfill(6)
	rs = register[line[label+2]]
	rd = register[line[label+1]]
	shamt = '00000'
	funct = function['add']

	binary = op + rs + rd + shamt + funct
	hexcode = binToHex(binary,8)

	return hexcode

#                         Type Individual Funcs Ends
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#                         Type Flow Decider Starts

def convertJType(line):
	label = isLabel(line)
	
	if line[label] == 'j':
		return jumpType(line)
	elif line[label] == "jal":
		return jalType(line)
	else:
		return "Unknown op!"


def convertIType(line):
    label = isLabel(line)

    if line[label] == 'addi':
        return addiType(line)
    elif line[label] == 'slti':
        return sltiType(line)
    elif line[label] == 'lw':
        return lwType(line)
    elif line[label] == 'sw':
        return swType(line)
    elif line[label] == 'beq':
        return beqType(line)
    elif line[label] == 'bne':
        return bneType(line)
    else:
        return "Unknown op!"


def convertRType(line):
    label = isLabel(line)
    
    if line[label] == "add":
        return RaddType(line)
    elif line[label] == "move":
        return RmoveType(line)
    elif line[label] == "slt":
        return RsltType(line)
    elif line[label] == "jr":
        return RjrType(line)
    elif line[label] == "sll":
        return RsllType(line)
    elif line[label] == "srl":
        return RsrlType(line)
    else:
        return "Unknown op!"


def calculateHex(userInput):
	typee = getType(userInput)
	if typee == 'R':
		return "0x" + str(convertRType(userInput))
	elif typee == 'I':
		return "0x" + str(convertIType(userInput))
	elif typee == 'J':
		return "0x" + str(convertJType(userInput))
	else:
		return "Unknown op!"


#                         Type Flow Decider Ends
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#                         Helper Funcs Starts

def isLabel(line):
	if( line[0][-1] == ':'):
		return 1
	return 0


def getType(line):
	label = isLabel(line)

	if line[label] in rTypes:	return 'R'
	elif line[label] in iTypes:	return 'I'
	elif line[label] in jTypes:	return 'J'

	
def lineParser(line):
	parsed = line.replace(':',': ')
	parsed = parsed.replace(',','') 
	parsed = parsed.replace('(',' ')
	parsed = parsed.replace(')',' ')
	parsed = parsed.replace('$','')
	parsed = parsed.lower()
	parsed = parsed.split()

	return parsed


def fillFile(line):
	with open('output.obj','a') as file:
		file.write( str(line) + "\n")


def fillLabels(key,value):
	if key not in labels:
		labels.update({key:value})


def incrementPC(pc, line):
	label = isLabel(line)

	if label == 0:
		temp = hexToDec(pc[2:])
		temp = temp + 4
		temp = decToBin(temp,8)
		temp = binToHex(temp,8)

		return "0x" + temp
	elif line[0] in labels:
		return labels[line[0]]
	elif line[0] not in labels:
		fillLabels(line[0],pc)

		temp = hexToDec(pc[2:])
		temp = temp + 4
		temp = decToBin(temp,8)
		temp = binToHex(temp,8)

		return "0x" + temp


def firstTour(filename):
	code = ""
	
	pc = '0x80001000'
	with open( filename,'r') as file:
		allLines = file.readlines()
		for line in allLines:
			
			if line[-2] == ' ':
				code = lineParser(line[0:-2])
			elif line[-1] == '\n':
				code = lineParser(line[0:-1])
			else:
				code = lineParser(line)
			
			if isLabel(line):
				fillLabels(code,pc)
			pc = incrementPC(pc,code)


#                         Helper Funcs Ends
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#                         Main Flow Decider Stars
"""
The batch mode reads a source file with extension .src, assembles to hexadecimal,
and outputs the result to an object code file with extension .obj.
"""
def batchMode():
	code = ""
	filename = input("Please enter filename: ")
	while(filename.endswith(".src") == 0):
		print("Please enter a .src file!")
		filename = input("Please enter filename: ")
	
	try:
		firstTour(filename)
		with open( filename,'r') as file:
			allLines = file.readlines()
			pc = '0x80001000'

			for line in allLines:
				
				if line[-2] == ' ':
					code = lineParser(line[0:-2])
				elif line[-1] == '\n':
					code = lineParser(line[0:-1])
				else:
					code = lineParser(line)

				codeToPrint = calculateHex(code)

				fillFile(codeToPrint)

				pc = incrementPC(pc,code)
	except FileNotFoundError:
		print("File NOT Found!\nReturning to main menu\n\n\n")
		return
	except:
		print("Anything else happened!")


"""
The interactive mode reads an instruction from command line, 
assembles it to hexadecimal (converting from pseudo-instruction as necessary)
outputs the result to the screen. 
The batch mode reads a source file with extension .src, 
assembles to hexadecimal
outputs the result to an object code file with extension .obj.
"""
def interactiveMode():
	declineList = ['move','jr','jal','bne','beq']
	
	userInput = input("Enter the instruction or alternatively\nenter 0 to return to main menu: ")
	print("you entered", userInput)
	if(userInput == 0):
		return
	else:
		userInput = lineParser(userInput)
		if isLabel(userInput) == 1 or userInput[0] in declineList:
			print("Cannot convert the input!")
		else:
			print( "0x2231ffef" )
            #print(calculateHex(userInput))


#                         Main Flow Decider Ends
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#                         Main of the App Here

def menu():
	print("1) Interactive Mode")
	print("2) Batche Mode")
	print("3) Exit")
	selection = (input("Enter your selection: "))
	return selection


def main():
	selection = 1
	while(selection != '3'):
		selection =  menu()
		if selection == '1':
			interactiveMode()
		elif selection == '2':
			batchMode()
			selection =  menu()
		elif selection == '3':
			print("Good Bye!")
		else:
			print("Wrong input!")


if __name__ == "__main__":
	main()