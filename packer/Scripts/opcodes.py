# Copyright (c) 2001, Stanford University
# All rights reserved.
#
# See the file LICENSE.txt for information on redistributing this software.

# This script generates include/cr_opcodes.h from the gl_header.parsed file.
 
import sys;
import pickle;
import string;
import re;

sys.path.append(sys.argv[1])
import apiutil

apiutil.CopyrightC()

print ( "" )
print ( "/* DO NOT EDIT - THIS FILE GENERATED BY THE opcodes.py SCRIPT */" )
print ( "" )
print ( "#ifndef CR_OPCODES_H" )
print ( "#define CR_OPCODES_H" )
print ( "" )

keys = apiutil.GetDispatchedFunctions(sys.argv[1]+"/APIspec.txt")
assert len(keys) > 0

print ( "/* Functions with no return value and input-only parameters */" )
print ( "typedef enum {" )

enum_index = 0
for func in keys:
	if "pack" in apiutil.ChromiumProps(func):
		print ( "\t%s = %d," % ( apiutil.OpcodeName(func), enum_index ) )
		enum_index = enum_index + 1

print ( "\tCR_EXTEND_OPCODE=%d," % enum_index )
enum_index = enum_index + 1
print ( "\tCR_CMDBLOCKBEGIN_OPCODE=%d," % enum_index )
enum_index = enum_index + 1
print ( "\tCR_CMDBLOCKEND_OPCODE=%d," % enum_index )
enum_index = enum_index + 1
print ( "\tCR_CMDBLOCKFLUSH_OPCODE=%d," % enum_index )
print ( "\tCR_NOP_OPCODE=255" )
if enum_index > 254:
	# This would have saved Mike some grief if it had been here earlier.
	print ( "You have more than 255 opcodes!  You've been adding functions to", file=sys.stderr )
	print ( "glapi_parser/APIspec!  Each new function you add", file=sys.stderr )
	print ( "gets an opcode assigned to it.  Fortunately for you, we have", file=sys.stderr )
	print ( "an ``extend'' opcode.  Please mark the function as", file=sys.stderr )
	print ( "'extpack' in APIspec so as to keep the main opcode pool" , file=sys.stderr)
	print ( "less than 255!  THIS IS A CATASTROPHIC FAILURE, and I WILL NOT CONTINUE!", file=sys.stderr )
	print ( "I'm putting an error in the generated header file so you won't miss", file=sys.stderr )
	print (  "this even if you're doing a 'make -k.'", file=sys.stderr )
	print ( "#error -- more than 255 opcodes!" )
	sys.exit(-1)
print ( "} CROpcode;\n" )

# count up number of extended opcode commands
num_extends = 0
num_auto_codes = 0
for func in keys:
	if "extpack" in apiutil.ChromiumProps(func):
		num_extends += 1
		if apiutil.ChromiumRelOpCode(func) < 0:
			num_auto_codes += 1

# sanity check for compatibility breakage
# we currently have 304
if num_auto_codes != 304:
	print ( "number of auto-generated op-codes should be 304, but is " + str(num_auto_codes), file=sys.stderr )
	print ( "which breaks backwards compatibility", file=sys.stderr )
	print ( "if this is really what you want to do, please adjust this script", file=sys.stderr )
	print (  "to handle a new auto-generated opcodes count", file=sys.stderr )
	print ( "#error -- num_auto_codes should be 304, but is " + str(num_auto_codes) )
	sys.exit(-1)

print ( "/* Functions with a return value or output parameters */" )
print ( "typedef enum {" )

opcode_index = 0
enum_index = 0
chrelopcodes = {}
for func in keys:
	if "extpack" in apiutil.ChromiumProps(func):
		opcodeName = apiutil.ExtendedOpcodeName(func)
		chrelopcode = apiutil.ChromiumRelOpCode(func)
		opcode = -1
		if chrelopcode >= 0:
			if not chrelopcode in chrelopcodes.keys():
				chrelopcodes[chrelopcode] = chrelopcode
			else:
				print (  "non-unique chrelopcode: " + str(chrelopcode), file=sys.stderr )
				print ( "#error -- non-unique chrelopcode:  " + str(num_auto_codes) )
				sys.exit(-1)
			opcode = num_auto_codes + chrelopcode
		else:
			opcode = opcode_index
			opcode_index = opcode_index + 1

		if enum_index != num_extends-1:
			print ( "\t%s = %d," % (opcodeName, opcode ) )
		else:
			print ( "\t%s = %d" % (opcodeName, opcode ) )
		enum_index = enum_index + 1
print ( "} CRExtendOpcode;\n" )
print ( "#endif /* CR_OPCODES_H */" )
