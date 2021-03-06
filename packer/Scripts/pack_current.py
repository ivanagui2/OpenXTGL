# Copyright (c) 2001, Stanford University
# All rights reserved.
#
# See the file LICENSE.txt for information on redistributing this software.

# This script generates the pack_current.c file.

import sys
sys.path.append(sys.argv[1])
import apiutil

from pack_currenttypes import *

apiutil.CopyrightC()

print ( """
/* DO NOT EDIT - THIS FILE GENERATED BY THE pack_current.py SCRIPT */

#include <memory.h>
#include "packer.h"
#include "state/cr_currentpointers.h"

#include <stdio.h>

void crPackOffsetCurrentPointers( int offset )
{
	CR_GET_PACKER_CONTEXT(pc);
	GLnormal_p		*normal		= &(pc->current.c.normal);
	GLcolor_p		*color		= &(pc->current.c.color);
	GLsecondarycolor_p	*secondaryColor	= &(pc->current.c.secondaryColor);
	GLtexcoord_p	*texCoord	= &(pc->current.c.texCoord);
	GLindex_p		*index		= &(pc->current.c.index);
	GLedgeflag_p	*edgeFlag	= &(pc->current.c.edgeFlag);
	GLvertexattrib_p *vertexAttrib = &(pc->current.c.vertexAttrib);
	GLfogcoord_p    *fogCoord   = &(pc->current.c.fogCoord);
	int i;
""" )

for k in current_fns.keys():
	name = '%s%s' % (k[:1].lower(),k[1:])
	if 'array' in current_fns[k]:
			print ( '\tfor (i = 0 ; i < %s ; i++)' % current_fns[k]['array'] )
			print ( '\t{' )
	for type in current_fns[k]['types']:
		for size in current_fns[k]['sizes']:
			indent = ""
			ptr = "%s->%s%d" % (name, type, size )
			if 'array' in current_fns[k]:
				ptr += "[i]"
				indent = "\t"
			print ( "%s\tif ( %s )" % (indent, ptr) )
			print ( "%s\t{" % indent )
			print ( "%s\t\t%s += offset;" % (indent, ptr ) )
			print ( "%s\t}" % indent )
	if 'array' in current_fns[k]:
		print ( '\t}' )
print ( """
}

void crPackNullCurrentPointers( void )
{
	CR_GET_PACKER_CONTEXT(pc);
	CRCurrentStateAttr	*c		= &(pc->current.c);
""")
print ( '\tmemset ( c, 0, sizeof (CRCurrentStateAttr));' )
print ( "}" )
