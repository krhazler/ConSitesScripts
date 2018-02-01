# ----------------------------------------------------------------------------------------
# ConSite-Tools.pyt
# Version:  ArcGIS 10.3.1 / Python 2.7.8
# Creation Date: 2017-08-11
# Last Edit: 2018-02-01
# Creator:  Kirsten R. Hazler

# Summary:
# A toolbox for automatic delineation of Natural Heritage Conservation Sites

# TO DO:
#
# ----------------------------------------------------------------------------------------

import libConSiteFx
from libConSiteFx import *
from CreateSBBs import *
from CreateConSites import *

# First define some handy functions
def defineParam(p_name, p_displayName, p_datatype, p_parameterType, p_direction, defaultVal = None):
   '''Simplifies parameter creation. Thanks to http://joelmccune.com/lessons-learned-and-ideas-for-python-toolbox-coding/'''
   param = arcpy.Parameter(
      name = p_name,
      displayName = p_displayName,
      datatype = p_datatype,
      parameterType = p_parameterType,
      direction = p_direction)
   param.value = defaultVal 
   return param

def declareParams(params):
   '''Sets up parameter dictionary, then uses it to declare parameter values'''
   d = {}
   for p in params:
      name = str(p.name)
      value = str(p.valueAsText)
      d[name] = value
      
   for p in d:
      globals()[p] = d[p]
   return 

# Define the toolbox
class Toolbox(object):
   def __init__(self):
      """Define the toolbox (the name of the toolbox is the name of the
      .pyt file)."""
      self.label = "ConSite Toolbox"
      self.alias = "ConSite-Toolbox"

      # List of tool classes associated with this toolbox
      self.tools = [coalesce, shrinkwrap, create_sbb, expand_sbb, create_consite]

# Define the tools
class coalesce(object):
   def __init__(self):
      """Define the tool (tool name is the name of the class)."""
      self.label = "Coalesce"
      self.description = ""
      self.canRunInBackground = True

   def getParameterInfo(self):
      """Define parameters"""
      parm0 = defineParam("in_Feats", "Input features", "GPFeatureLayer", "Required", "Input")
      parm1 = defineParam("dil_Dist", "Dilation distance", "GPLinearUnit", "Required", "Input")
      parm2 = defineParam("out_Feats", "Output features", "DEFeatureClass", "Required", "Output")
      parm3 = defineParam("scratch_GDB", "Scratch geodatabase", "DEWorkspace", "Optional", "Input")
      
      parm3.filter.list = ["Local Database"]
      parms = [parm0, parm1, parm2, parm3]
      return parms

   def isLicensed(self):
      """Set whether tool is licensed to execute."""
      return True

   def updateParameters(self, parameters):
      """Modify the values and properties of parameters before internal
      validation is performed.  This method is called whenever a parameter
      has been changed."""
      return

   def updateMessages(self, parameters):
      """Modify the messages created by internal validation for each tool
      parameter.  This method is called after internal validation."""
      return

   def execute(self, parameters, messages):
      """The source code of the tool."""
      # Set up parameter names and values
      declareParams(parameters)

      if scratch_GDB != 'None':
         scratchParm = scratch_GDB 
      else:
         scratchParm = "in_memory" 
      
      Coalesce(in_Feats, dil_Dist, out_Feats, scratchParm)

      return out_Feats

class shrinkwrap(object):
   def __init__(self):
      """Define the tool (tool name is the name of the class)."""
      self.label = "Shrinkwrap"
      self.description = ""
      self.canRunInBackground = True

   def getParameterInfo(self):
      """Define parameters"""
      parm0 = defineParam("in_Feats", "Input features", "GPFeatureLayer", "Required", "Input")
      parm1 = defineParam("dil_Dist", "Dilation distance", "GPLinearUnit", "Required", "Input")
      parm2 = defineParam("out_Feats", "Output features", "DEFeatureClass", "Required", "Output")
      parm3 = defineParam("smthMulti", "Smoothing multiplier", "GPDouble", "Optional", "Input", 8)
      parm4 = defineParam("scratch_GDB", "Scratch geodatabase", "DEWorkspace", "Optional", "Input")
      
      parm4.filter.list = ["Local Database"]
      parms = [parm0, parm1, parm2, parm3, parm4]
      return parms

   def isLicensed(self):
      """Set whether tool is licensed to execute."""
      return True

   def updateParameters(self, parameters):
      """Modify the values and properties of parameters before internal
      validation is performed.  This method is called whenever a parameter
      has been changed."""
      return

   def updateMessages(self, parameters):
      """Modify the messages created by internal validation for each tool
      parameter.  This method is called after internal validation."""
      return

   def execute(self, parameters, messages):
      """The source code of the tool."""
      # Set up parameter names and values
      declareParams(parameters)

      if scratch_GDB != 'None':
         scratchParm = scratch_GDB 
      else:
         scratchParm = "in_memory" 
         
      if smthMulti != 'None':
         multiParm = smthMulti
      else:
         multiParm = 8
      
      ShrinkWrap(in_Feats, dil_Dist, out_Feats, multiParm, scratchParm)

      return out_Feats

class create_sbb(object):
   def __init__(self):
      """Define the tool (tool name is the name of the class)."""
      self.label = "Create Site Building Blocks"
      self.description = ""
      self.canRunInBackground = True

   def getParameterInfo(self):
      """Define parameter definitions"""
      parm0 = defineParam('in_PF', "Input Procedural Features", "GPFeatureLayer", "Required", "Input")
      parm1 = defineParam('fld_SFID', "Source Feature ID field", "String", "Required", "Input", 'SFID')
      parm2 = defineParam('fld_Rule', "SBB Rule field", "String", "Required", "Input", 'RULE')
      parm3 = defineParam('fld_Buff', "SBB Buffer field", "String", "Required", "Input", 'BUFFER')
      parm4 = defineParam('in_nwi5', "Input Rule 5 NWI Features", "GPFeatureLayer", "Required", "Input", "VA_Wetlands_Rule5")
      parm5 = defineParam('in_nwi67', "Input Rule 67 NWI Features", "GPFeatureLayer", "Required", "Input", "VA_Wetlands_Rule67")
      parm6 = defineParam('in_nwi9', "Input Rule 9 NWI Features", "GPFeatureLayer", "Required", "Input", "VA_Wetlands_Rule9")
      parm7 = defineParam('out_SBB', "Output Site Building Blocks", "DEFeatureClass", "Required", "Output")
      parm8 = defineParam('scratch_GDB', "Scratch Geodatabase", "DEWorkspace", "Optional", "Output")

      parms = [parm0, parm1, parm2, parm3, parm4, parm5, parm6, parm7, parm8]
      return parms

   def isLicensed(self):
      """Set whether tool is licensed to execute."""
      return True

   def updateParameters(self, parameters):
      """Modify the values and properties of parameters before internal
      validation is performed.  This method is called whenever a parameter
      has been changed."""
      if parameters[0].altered:
         fc = parameters[0].valueAsText
         field_names = [f.name for f in arcpy.ListFields(fc)]
         for i in [1,2,3]:
            parameters[i].filter.list = field_names
      return

   def updateMessages(self, parameters):
      """Modify the messages created by internal validation for each tool
      parameter.  This method is called after internal validation."""
      return

   def execute(self, parameters, messages):
      """The source code of the tool."""
      # Set up parameter names and values
      declareParams(parameters)

      if scratch_GDB != 'None':
         scratchParm = scratch_GDB 
      else:
         scratchParm = "in_memory" 

      CreateSBBs(in_PF, fld_SFID, fld_Rule, fld_Buff, in_nwi5, in_nwi67, in_nwi9, out_SBB, scratchParm)
      arcpy.MakeFeatureLayer_management (out_SBB, "SBB_lyr")

      return out_SBB
      
class expand_sbb(object):
   def __init__(self):
      """Define the tool (tool name is the name of the class)."""
      self.label = "Expand Site Building Blocks with Core Area"
      self.description = "Expands SBBs by adding core area."
      self.canRunInBackground = True

   def getParameterInfo(self):
      """Define parameter definitions"""
      parm0 = defineParam('in_Cores', "Input Cores", "GPFeatureLayer", "Required", "Input")
      parm1 = defineParam('in_SBB', "Input Site Building Blocks", "GPFeatureLayer", "Required", "Input")
      parm2 = defineParam('in_PF', "Input Procedural Features", "GPFeatureLayer", "Required", "Input")
      parm3 = defineParam('joinFld', "Source Feature ID field", "String", "Required", "Input", 'SFID')
      parm4 = defineParam('out_SBB', "Output Expanded Site Building Blocks", "DEFeatureClass", "Required", "Output")
      parm5 = defineParam('scratch_GDB', "Scratch Geodatabase", "DEWorkspace", "Optional", "Output")

      parms = [parm0, parm1, parm2, parm3, parm4, parm5]
      return parms

   def isLicensed(self):
      """Set whether tool is licensed to execute."""
      return True

   def updateParameters(self, parameters):
      """Modify the values and properties of parameters before internal
      validation is performed.  This method is called whenever a parameter
      has been changed."""
      if parameters[1].altered:
         fc = parameters[1].valueAsText
         field_names = [f.name for f in arcpy.ListFields(fc)]
         parameters[3].filter.list = field_names
      return

   def updateMessages(self, parameters):
      """Modify the messages created by internal validation for each tool
      parameter.  This method is called after internal validation."""
      return

   def execute(self, parameters, messages):
      """The source code of the tool."""
      # Set up parameter names and values
      declareParams(parameters)

      if scratch_GDB != 'None':
         scratchParm = scratch_GDB 
      else:
         scratchParm = "in_memory" 

      ExpandSBBs(in_Cores, in_SBB, in_PF, joinFld, out_SBB, scratchParm)
      arcpy.MakeFeatureLayer_management (out_SBB, "SBB_lyr")
      
      return out_SBB
      
class create_consite(object):
   def __init__(self):
      """Define the tool (tool name is the name of the class)."""
      self.label = "Create Conservation Sites"
      self.description = ""
      self.canRunInBackground = True

   def getParameterInfo(self):
      """Define parameter definitions"""
      parm00 = defineParam("in_SBB", "Input Site Building Blocks", "GPFeatureLayer", "Required", "Input")
      parm01 = defineParam("ysn_Expand", "Expand SBB Selection?", "GPBoolean", "Required", "Input", "false")
      parm02 = defineParam("in_PF", "Input Procedural Features", "GPFeatureLayer", "Required", "Input")
      parm03 = defineParam("joinFld", "Source Feature ID field", "String", "Required", "Input", "SFID")
      parm04 = defineParam("in_TranSurf", "Input Transportation Surfaces", "GPFeatureLayer", "Required", "Input")
      parm04.multiValue = True
      parm05 = defineParam("in_Hydro", "Input Hydro Features", "GPFeatureLayer", "Required", "Input")
      parm06 = defineParam("in_Exclude", "Input Exclusion Features", "GPFeatureLayer", "Required", "Input")
      parm07 = defineParam("in_ConSites", "Input Current Conservation Sites", "GPFeatureLayer", "Required", "Input")
      parm08 = defineParam("out_ConSites", "Output Updated Conservation Sites", "DEFeatureClass", "Required", "Output")
      parm09 = defineParam("scratch_GDB", "Scratch Geodatabase", "DEWorkspace", "Optional", "Input")

      parms = [parm00, parm01, parm02, parm03, parm04, parm05, parm06, parm07, parm08, parm09]
      return parms

   def isLicensed(self):
      """Set whether tool is licensed to execute."""
      return True

   def updateParameters(self, parameters):
      """Modify the values and properties of parameters before internal
      validation is performed.  This method is called whenever a parameter
      has been changed."""
      if parameters[0].altered:
         fc = parameters[0].valueAsText
         field_names = [f.name for f in arcpy.ListFields(fc)]
         parameters[3].filter.list = field_names
      return

   def updateMessages(self, parameters):
      """Modify the messages created by internal validation for each tool
      parameter.  This method is called after internal validation."""
      return

   def execute(self, parameters, messages):
      """The source code of the tool."""
      # Set up parameter names and values
      declareParams(parameters)

      if scratch_GDB != 'None':
         scratchParm = scratch_GDB 
      else:
         scratchParm = "in_memory" 

      CreateConSites(in_SBB, ysn_Expand, in_PF, joinFld, in_TranSurf, in_Hydro, in_Exclude, in_ConSites, out_ConSites, scratchParm)

      return out_ConSites