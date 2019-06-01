#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.90.1),
    on April 23, 2019, at 11:05
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle 
import os
import sys
import math
import copy
from random import shuffle
from psychopy.tools.monitorunittools import posToPix
from iViewXAPI import  *
from psychopy import visual, core

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'Experiment_Error_Detection'
expInfo = {u'session': u'001', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# current experiment dir
dir_experiment = _thisDir + os.sep

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# ---------------------------------------------
# Connect to iViewX
# ---------------------------------------------

res = iViewXAPI.iV_SetLogger(c_int(1), c_char_p("logs/logs.txt"))
res = iViewXAPI.iV_Connect(c_char_p('141.54.159.23'), c_int(4444), c_char_p('141.54.159.21'), c_int(5555))

res = iViewXAPI.iV_GetSystemInfo(byref(systemData))
print "iV_GetSystemInfo: " + str(res)
print "Samplerate: " + str(systemData.samplerate)
print "iViewX Version: " + str(systemData.iV_MajorVersion) + "." + str(systemData.iV_MinorVersion) + "." + str(systemData.iV_Buildnumber)
print "iViewX API Version: " + str(systemData.API_MajorVersion) + "." + str(systemData.API_MinorVersion) + "." + str(systemData.API_Buildnumber)

# ---------------------------------------------
# Calibrate iViewX
# ---------------------------------------------

calibrate = 0

if calibrate:
    calibrationData = CCalibration(9, 1, 1, 0, 0, 250, 180, 2, 10, b"")

    res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))
    print "iV_SetupCalibration " + str(res)
    res = iViewXAPI.iV_Calibrate()
    print "iV_Calibrate " + str(res)
    res = iViewXAPI.iV_Validate()
    print "iV_Validate " + str(res)
    print "iV_GetAccuracy " + str(res)
    print "deviationXLeft " + str(accuracyData.deviationLX) + " deviationYLeft " + str(accuracyData.deviationLY)
    print "deviationXRight " + str(accuracyData.deviationRX) + " deviationYRight " + str(accuracyData.deviationRY)

# ---------------------------------------------
# Setup the main window
# ---------------------------------------------

win = visual.Window(
    size=[1680, 1050], fullscr=True, screen=1,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix'
)
    
# Setup the frame rate
expInfo['frameRate'] = win.getActualFrameRate()

if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# ---------------------------------------------
# Routine setups
# ---------------------------------------------

# --- Routine: balanceStrategy
stim_writing_output = visual.TextStim(win=win, name='stim_writing_output',
    text='',
    font='Arial',
    units='pix', pos=[0, 50], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
    
stim_writing_input = visual.TextStim(win=win, name='stim_writing_input',
    text='',
    font='Arial',
    units='pix', pos=[0, -400], height=30, wrapWidth=None, ori=0, 
    color='#cccccc', colorSpace='rgb', opacity=1,
    depth=-1.0);

# --- Routine: balanceStrategy
stim_balanceStrategy = visual.TextStim(win=win, name='stim_balanceStrategy',
    text='Einstellung durch den Versuchsleiter\n\n1: 1,2,3\n2: 1,3,2\n3: 2,1,3\n4: 2,3,1\n5: 3,2,1\n6: 3,1,2',
    font='Arial',
    units='pix', pos=[0, 0], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

# --- Routine: balance
balanceText = visual.TextStim(win=win, name='balanceText',
    text='Einstellung durch den Versuchsleiter\n\n1: 3,9,3,9,3,9\n2: 3,9,3,9,9,3\n3: 3,9,9,3,3,9\n4: 3,9,9,3,9,3\n5: 9,3,3,9,3,9\n6: 9,3,3,9,9,3\n7: 9,3,9,3,3,9\n8: 9,3,9,3,9,3',
    font='Arial',
    units='pix', pos=[0, 0], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

# --- Routine: baselineInstruction
stim_baseline_instruction = visual.TextStim(win=win, name='stim_baseline_instruction',
    text='Press space to record the baseline',
    font='Arial',
    units='pix', pos=[0, 0], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

# --- Routine: baseline
text_8 = visual.TextStim(win=win, name='text_8',
    text=None,
    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
    
# --- Routine: trial
text_2 = visual.TextStim(win=win, name='text_2',
    text=None,
    font='Arial',
    pos=[0, 0], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

# --- Routine: pause
stim_pause_text = visual.TextStim(win=win, name='stim_pause_text',
    text='press space to continue',
    font='Arial',
    units='pix', pos=[0, 0], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0);

# Create some handy timers
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ---------------------------------------------
# global variables
# ---------------------------------------------
endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Size of outer feedback in px
pupil_circle_goal_size = 50

# Time until an object is selected (in fps)
gaze_required_time = 25 # 1/nth second

cursorTimer = 0

# the interval after performing a writing operation, during which an undo operation can be performed
undo_interval = 60

# the pupil value required above the baseline sd to perform an undo operation
required_pupil_std_diff = 1

#Factor of scaling object size
scaling = 20
gazePosX = 0
gazePosY = 0
posPix = 0

formList = []

radius = 300
keyColor = '#a6a6a6'
 
colorHover = '#81dbcf'
colorSelect = '#80DBA1'

dwellTimeColor='#808080'
dwellTimeBackgroundColor='#dadada'

letterColor = '#333333'

buttonLineColor = '#707070'
buttonHoverLineColor= '#000000'
buttonLineWidth = 1

# required for the baseline algorithm
psizeliste = [0]*900 # ca. 900 bei 30Hz | ca. 1900 bei 60Hz
psize = 0



#################################################
# Start Routine: baselineInstruction
#################################################

key_resp_3 = event.BuilderKeyResponse()

# keep track of which components have finished
baselineInstructionComponents = [stim_baseline_instruction, key_resp_3]

for thisComponent in baselineInstructionComponents:
    if hasattr(thisComponent, 'status'): thisComponent.status = NOT_STARTED

t = 0
baselineInstructionClock = core.Clock()
baselineInstructionClock.reset()
frameN = -1
continueRoutine = True
while continueRoutine:
    # Current time and frame
    t = baselineInstructionClock.getTime()
    frameN = frameN + 1
    
    # *stim_baseline_instruction* updates
    if t >= 0.0 and stim_baseline_instruction.status == NOT_STARTED:
        # keep track of start time/frame for later
        stim_baseline_instruction.tStart = t
        stim_baseline_instruction.frameNStart = frameN  # exact frame index
        stim_baseline_instruction.setAutoDraw(True)
    
    # *key_resp_3* updates
    if t >= 0.0 and key_resp_3.status == NOT_STARTED:
        key_resp_3.tStart = t
        key_resp_3.frameNStart = frameN
        key_resp_3.status = STARTED
        
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
        
    if key_resp_3.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine: break
        
    continueRoutine = False
    
    for thisComponent in baselineInstructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]): core.quit()
    
    # refresh the screen
    if continueRoutine: win.flip()
# --end while

# -------Ending Routine "baselineInstruction"-------
for thisComponent in baselineInstructionComponents:
    if hasattr(thisComponent, "setAutoDraw"): thisComponent.setAutoDraw(False)
routineTimer.reset()

#################################################
# Start Routine: baseline
#################################################
routineTimer.add(5.000000)

# algorithm code (just use as is)

bsize_liste = [0]*900 # ca. 900 bei 30Hz | ca. 1900 bei 60Hz
bsize = 0

# starting values
state_no = 0
lmarker = -1
delay_size = 2

# filter preferences
step_limit = 0.19    # 30Hz: 0.19 | 60Hz: 0.09
lower_th = 2

# cross
baseline_cross_1 = visual.Line(win, start=(0, -20), end=(0, 20), lineColor=(-1, -1, -1))
baseline_cross_2 = visual.Line(win, start=(-20, 0), end=(20, 0), lineColor=(-1, -1, -1))

#######
iViewXAPI.iV_StartRecording()

# keep track of which components have finished
baselineComponents = [text_8]
for thisComponent in baselineComponents:
    if hasattr(thisComponent, 'status'): thisComponent.status = NOT_STARTED

t = 0
baselineClock = core.Clock()
baselineClock.reset()
frameN = -1
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # Current time and frame
    t = baselineClock.getTime()
    frameN = frameN + 1
    
    # API Call
    # Collect pupil eye diameter
    res = iViewXAPI.iV_GetSample(byref(sampleData))
    bsize = (sampleData.leftEye.diam) # /32 fur highspeed eyetracker, ohne /32 fur RED
    
    # The following if statements remove blinks, etc. Use as is
    
    #--------------------
    # state 0: starting
    #--------------------
    if state_no == 0:
        if lmarker < 1:
            lmarker = lmarker + 1
            bsize_liste[lmarker] = bsize
            state_next = 0
     
        else:
            if bsize > lower_th and bsize_liste[lmarker] > lower_th and bsize_liste[lmarker-1] > lower_th and (abs(bsize-bsize_liste[lmarker]) <= step_limit) and (abs(bsize_liste[lmarker]-bsize_liste[lmarker-1]) <= step_limit):
                lmarker = lmarker + 1
                bsize_liste[lmarker] = bsize
                state_next = 1
            else:
                bsize_liste[lmarker-1] = bsize_liste[lmarker]
                bsize_liste[lmarker] = bsize

                state_next = 0

    #----------------------
    # state 1: observation
    #----------------------
    if state_no == 1:

        # Filter Activation
        #- - - - - - - - - - -
        if bsize <= lower_th:
            on = 1
            jump_marker = lmarker + 1 # marks values to be replaced 
      
            # Identification of last valid_value before the blink
            #- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            while on == 1:
                if bsize_liste[lmarker] >= lower_th and bsize_liste[lmarker-1] >= lower_th and bsize_liste[lmarker-2] >= lower_th and abs(bsize_liste[lmarker]-bsize_liste[lmarker-1]) <= step_limit and abs(bsize_liste[lmarker-1]-bsize_liste[lmarker-2]) <= step_limit:
                    valid_value = bsize_liste[lmarker]
                    lmarker = lmarker + 1
                    for i in range(lmarker, jump_marker, 1):
                        bsize_liste[i] = valid_value

                    bsize_liste[jump_marker] = valid_value

                    lmarker = jump_marker
                    puffer_size = jump_marker + delay_size

                    on = 0
                    state_next = 2

                else:
                    lmarker = lmarker-1

        else:
            lmarker = lmarker + 1
            bsize_liste[lmarker] = bsize

            state_next = 1
    
    #-------------------------------------------------------------
    # state 2: identification of next valid_value after the blink
    #-------------------------------------------------------------
    
    if state_no == 2:
        # collecting values following the blink
        #- - - - - - - - - - - - - - - - - - - - - -
        if lmarker < puffer_size:
            lmarker = lmarker + 1
            bsize_liste[lmarker] = bsize

            state_next = 2
    
        else:
            # identification of next valid_value after the blink
            #- - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            if bsize > lower_th and abs(bsize-bsize_liste[lmarker]) <= step_limit and abs(bsize_liste[lmarker]-bsize_liste[lmarker-1]) <= step_limit:               
                lmarker = lmarker + 1
                bsize_liste[lmarker] = bsize

                state_next = 1
        
            else:
                lmarker = lmarker + 1
                bsize_liste[lmarker] = bsize
                bsize_liste[lmarker-2] = valid_value

                state_next = 2
    
    state_no = state_next
    
    # Draw the crosses
    baseline_cross_1.draw()
    baseline_cross_2.draw()
    
    # *text_8* updates
    if t >= 0.0 and text_8.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_8.tStart = t
        text_8.frameNStart = frameN  # exact frame index
        text_8.setAutoDraw(True)
        
    frameRemains = 0.0 + 10 - win.monitorFramePeriod * 0.75  # most of one frame period left
    
    if text_8.status == STARTED and t >= frameRemains:
        text_8.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine: break
    
    continueRoutine = False
    for thisComponent in baselineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]): core.quit()
    
    # refresh the screen
    if continueRoutine: win.flip()
# end while

# -------Ending Routine "baseline"-------
for thisComponent in baselineComponents:
    if hasattr(thisComponent, "setAutoDraw"): thisComponent.setAutoDraw(False)
routineTimer.reset()

iViewXAPI.iV_StopRecording()
iViewXAPI.iV_SaveData(str(dir_experiment + expName +expInfo['participant'] + '_baseline'), str(), str(),1)

### Eye pupil diameter

# Baseline mean
bsize_liste = filter(None, bsize_liste)
baseline_mean = round((sum(bsize_liste)/(len(bsize_liste))),2)

# Baseline sd
baseline_sd = abs(round(np.std(bsize_liste),8))

# prevent very low baseline values from affecting our study later
if baseline_sd < 0.5:
    baseline_sd = 0.5

# Percent-change: sd / mean
# prozent_change1 = round((baseline_sd/baseline_mean),2)
    
# Save data
thisExp.addData('Baseline_Liste', bsize_liste)
thisExp.addData('Baseline_Mittelwert', baseline_mean)
thisExp.addData('Baseline_Standardabweichung', baseline_sd)


#################################################
# Start Routine: Live writing
#################################################

# update component parameters for each repeat
# trialCounter += 1
# shapeStyle = 0
# feedbackCounter = 0

current_pupil_change_size = 0
b = 0
m = 0

beginGazeTimer = False
gazeTimer = [0] * 27
next_writing_frame = [0] * 27
undo_success = [False] * 27

# quitTimer = 0

#Size of selectable area around Object 3* = original
objArea = 2.5 * scaling

# pupilSizeList=[]
# pupilSizeRound=0

#Bool if Gaze Pos is inside Object
beInsideRight=False
beInsideRight2=False
beInsideWrong=False

# checkmarkStatus = 0

# percent = [0, 1/stimuli, 1/stimuli*2, 1/stimuli*3, 1/stimuli*4, 1/stimuli*5, 1/stimuli*6, 1/stimuli*7, 1/stimuli*8]

# rest2 = percent[:stimuli]
# shuffle(rest2)
# percent = rest2 + percent[stimuli:]

# Create the object
vert1 = ((-2*scaling, -2*scaling),  (-2*scaling, 2*scaling), (2*scaling, 2*scaling), (2*scaling, -2*scaling))
vertSpace = ((-2*scaling, -2*scaling),  (-2*scaling, 2*scaling), (4*scaling, 2*scaling), (4*scaling, -2*scaling))

# Define keys
Y1 = -100
formQ = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-450, Y1), name='Q')
formW = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-350, Y1), name='W')
formE = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-250, Y1), name='E')
formR = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-150, Y1), name='R')
formT = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-50, Y1), name='T')
formY = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(50, Y1), name='Y')
formU = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(150, Y1), name='U')
formI = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(250, Y1), name='I')
formO = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(350, Y1), name='O')
formP = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(450, Y1), name='P')
Y2 = -200
formA = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-400, Y2), name='A')
formS = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-300, Y2), name='S')
formD = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-200, Y2), name='D')
formF = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-100, Y2), name='F')
formG = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-0, Y2), name='G')
formH = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(100, Y2), name='H')
formJ = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(200, Y2), name='J')
formK = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(300, Y2), name='K')
formL = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(400,Y2), name='L')
Y3 = -300
formZ = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-350, Y3), name='Z')
formX = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-250, Y3), name='X')
formC = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-150, Y3), name='C')
formV = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(-50, Y3), name='V')
formB = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(50, Y3), name='B')
formN = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(150, Y3), name='N')
formM = visual.ShapeStim(win, fillColor=keyColor, vertices=vert1, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(250, Y3), name='M')

formSpace = visual.ShapeStim(win, fillColor=keyColor, vertices=vertSpace, closeShape=True, lineWidth=buttonLineWidth, lineColor=buttonLineColor, pos=(350, Y3), name=' ')

formList = [formQ, formW, formE, formR, formT, formY, formU, formI, formO, formP, formA, formS, formD, formF, formG, formH, formJ, formK, formL, formZ, formX, formC, formV, formB, formN, formM, formSpace]

keyCounter = 0
for key in formList:
    gazeTimer[keyCounter] = 0
    next_writing_frame[keyCounter] = 0
    keyCounter += 1

letterQ = visual.TextStim(win, text = 'Q',  pos=(posToPix(formQ)), color=letterColor)
letterW = visual.TextStim(win, text = 'W',  pos=(posToPix(formW)), color=letterColor)
letterE = visual.TextStim(win, text = 'E',  pos=(posToPix(formE)), color=letterColor)
letterR = visual.TextStim(win, text = 'R',  pos=(posToPix(formR)), color=letterColor)
letterT = visual.TextStim(win, text = 'T',  pos=(posToPix(formT)), color=letterColor)
letterY = visual.TextStim(win, text = 'Y',  pos=(posToPix(formY)), color=letterColor)
letterU = visual.TextStim(win, text = 'U',  pos=(posToPix(formU)), color=letterColor)
letterI = visual.TextStim(win, text = 'I',  pos=(posToPix(formI)), color=letterColor)
letterO = visual.TextStim(win, text = 'O',  pos=(posToPix(formO)), color=letterColor)
letterP = visual.TextStim(win, text = 'P',  pos=(posToPix(formP)), color=letterColor)

letterA = visual.TextStim(win, text = 'A',  pos=(posToPix(formA)), color=letterColor)
letterS = visual.TextStim(win, text = 'S',  pos=(posToPix(formS)), color=letterColor)
letterD = visual.TextStim(win, text = 'D',  pos=(posToPix(formD)), color=letterColor)
letterF = visual.TextStim(win, text = 'F',  pos=(posToPix(formF)), color=letterColor)
letterG = visual.TextStim(win, text = 'G',  pos=(posToPix(formG)), color=letterColor)
letterH = visual.TextStim(win, text = 'H',  pos=(posToPix(formH)), color=letterColor)
letterJ = visual.TextStim(win, text = 'J',  pos=(posToPix(formJ)), color=letterColor)
letterK = visual.TextStim(win, text = 'K',  pos=(posToPix(formK)), color=letterColor)
letterL = visual.TextStim(win, text = 'L',  pos=(posToPix(formL)), color=letterColor)

letterZ = visual.TextStim(win, text = 'Z',  pos=(posToPix(formZ)), color=letterColor)
letterX = visual.TextStim(win, text = 'X',  pos=(posToPix(formX)), color=letterColor)
letterC = visual.TextStim(win, text = 'C',  pos=(posToPix(formC)), color=letterColor)
letterV = visual.TextStim(win, text = 'V',  pos=(posToPix(formV)), color=letterColor)
letterB = visual.TextStim(win, text = 'B',  pos=(posToPix(formB)), color=letterColor)
letterN = visual.TextStim(win, text = 'N',  pos=(posToPix(formN)), color=letterColor)
letterM = visual.TextStim(win, text = 'M',  pos=(posToPix(formM)), color=letterColor)

letterSpace = visual.TextStim(win, text = '  SPACE',  pos=(posToPix(formSpace)), color=letterColor)

letterList=[letterQ, letterW, letterE, letterR, letterT, letterY, letterU, letterI, letterO, letterP, letterA, letterS, letterD, letterF, letterG, letterH, letterJ, letterK, letterL, letterZ, letterX, letterC, letterV, letterB, letterN, letterM, letterSpace]
################################

psizeliste = [0]*36000 # ca. 900 bei 30Hz | ca. 1900 bei 60Hz
psize = 0
current_pupil_mean = 0

psizeliste_len = len(psizeliste)

#---------------------
# starting values
state_no = 0
lmarker = -1 
delay_size = 2

#---------------------
# filter preferences
step_limit = 0.19    # 30Hz: 0.19 | 60Hz: 0.09
lower_th = 1 # was 2

#---------------------
# plot settings
plot_marker = 0
mean_length = 3
plot_buffer = 5

write_same_letter_interval = 60

###################
iViewXAPI.iV_StartRecording()
iViewXAPI.iV_SendImageMessage(c_char_p('trialStart'))
###################

# keep track of which components have finished
trialComponents = [text_2, stim_writing_output]
for thisComponent in trialComponents:
    if hasattr(thisComponent, 'status'): thisComponent.status = NOT_STARTED

t = 0
trialClock = core.Clock()
trialClock.reset()
frameN = -1
continueRoutine = True
while continueRoutine:
    # Current time and frame
    t = trialClock.getTime()
    frameN = frameN + 1
    
    # Eye pupil
    res = iViewXAPI.iV_GetSample(byref(sampleData))
    psize = (sampleData.leftEye.diam) # /32 fur highspeed eyetracker, ohne /32 fur RED
    
    # Gaze
    gazeRx = (sampleData.rightEye.gazeX)-840
    gazeRy = ((sampleData.rightEye.gazeY)-525)*-1
    
    if lmarker == len(psizeliste) - 1:
        lmarker = -1
    
    #--------------------
    # state 0: starting
    #--------------------
    if state_no == 0:
        if lmarker < 1:
            lmarker = lmarker + 1
            psizeliste[lmarker] = psize
            state_next = 0
         
        else:
            if psize > lower_th and psizeliste[lmarker] > lower_th and psizeliste[lmarker-1] > lower_th and (abs(psize-psizeliste[lmarker]) <= step_limit) and (abs(psizeliste[lmarker]-psizeliste[lmarker-1]) <= step_limit):
                lmarker = lmarker + 1
                psizeliste[lmarker] = psize
                state_next = 1
            else:
                psizeliste[lmarker-1] = psizeliste[lmarker]
                psizeliste[lmarker] = psize
                
                state_next = 0

    #----------------------
    # state 1: observation
    #----------------------            
    if state_no == 1:
        plot_marker = 1 
         
        # Filter Activation
        #- - - - - - - - - - -
        
        if psize <= lower_th:
            on = 1
            jump_marker = lmarker + 1 # marks values to be replaced 
            
            # Identification of last valid_value before the blink
            #- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            while on == 1:
                if psizeliste[lmarker] >= lower_th and psizeliste[lmarker-1] >= lower_th and psizeliste[lmarker-2] >= lower_th and abs(psizeliste[lmarker]-psizeliste[lmarker-1]) <= step_limit and abs(psizeliste[lmarker-1]-psizeliste[lmarker-2]) <= step_limit:
                    valid_value = psizeliste[lmarker]
                    
                    lmarker = lmarker + 1
                    
                    # replacing values
                    for i in range(lmarker, jump_marker, 1):
                        psizeliste[i] = valid_value
                        
                    psizeliste[jump_marker] = valid_value
                        
                    lmarker = jump_marker
                    puffer_size = jump_marker + delay_size

                    on = 0
                    state_next = 2
                else:
                    lmarker = lmarker-1

        else:
            if lmarker+1 >= 0 and lmarker+1 < len(psizeliste):
                lmarker = lmarker + 1
                psizeliste[lmarker] = psize
            state_next = 1
    
    #-------------------------------------------------------------
    # state 2: identification of next valid_value after the blink
    #-------------------------------------------------------------
    if state_no == 2:
        plot_marker = 1
        # collecting values following the blink
        #- - - - - - - - - - - - - - - - - - - - - -
        
        if lmarker < puffer_size:
            lmarker = lmarker + 1
            psizeliste[lmarker] = psize
            state_next = 2
    
        else:
            # identification of next valid_value after the blink
            #- - - - - - - - - - - - - - - - - - - - - - - - - - - - 
            if psize > lower_th and abs(psize-psizeliste[lmarker]) <= step_limit and abs(psizeliste[lmarker]-psizeliste[lmarker-1]) <= step_limit:               
                lmarker = lmarker + 1
                psizeliste[lmarker] = psize
                state_next = 1
            else:
                lmarker = lmarker + 1
                psizeliste[lmarker] = psize
                psizeliste[lmarker-2] = valid_value
            
                state_next = 2
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - -
    # smooth & plot data:
    #- - - - - - - - - - - - - - - - - - - - - - - - - - -
    if state_no == 0 or state_no == 1 or state_no == 2:
        if plot_marker == 1:
            # BASELINE RINGE (schwarz): MW +/-SD
            #- - - - - - - - - - - - - - - - - - - -
            #- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # FEEDBACK RINGE (rot | grau): Pupillengröße u. Extrema
            #- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            if lmarker >= mean_length + plot_buffer:
                current_pupil_mean = 0
                for p in range(1, mean_length+1, 1):
                    current_pupil_mean = psizeliste[lmarker-p-plot_buffer] + current_pupil_mean
            
                # current_pupil_mean = (current_pupil_mean/mean_length)*35
                current_pupil_mean = current_pupil_mean/mean_length

    state_no = state_next
    
    #############################################
    
    ### Draw the keys and letters on them
    for key in formList:
        key.draw()
    
    for letter in letterList:
        letter.draw()

	### Draw text to input
    stim_writing_input.text  = "HELLO WORLD"
    stim_writing_input.draw()

    ### Do magic here
	# Make cursor blink	
    cursorTimer += 1
    
    if cursorTimer >= 60:
        stim_writing_output.text = stim_writing_output.text.replace('_', '')
        cursorTimer = 0
    elif cursorTimer == 30:
        stim_writing_output.text = stim_writing_output.text + '_'
    
    keyCounter = 0
    for key in formList:
        posPix = posToPix(key)
        # Check which of the objects is being viewed
        
		# Make space have a bigger area
        if key.name == ' ':
            objBoundary_X_1 = posPix[0] - objArea
            objBoundary_X_2 = posPix[0] + (objArea*2)
        
            objBoundary_Y_1 = posPix[1] - objArea
            objBoundary_Y_2 = posPix[1] + objArea
        else:
            objBoundary_X_1 = posPix[0] - objArea
            objBoundary_X_2 = posPix[0] + objArea
        
            objBoundary_Y_1 = posPix[1] - objArea
            objBoundary_Y_2 = posPix[1] + objArea

        # Are we gazing at the object?
        if gazeRx > objBoundary_X_1 and gazeRx < objBoundary_X_2 and gazeRy > objBoundary_Y_1 and gazeRy < objBoundary_Y_2:
            
            # Increment gaze timer
            gazeTimer[keyCounter] += 1
            
            # Set the current gaze coordinates to the object's coordinates
            gazePosX = posPix[0]
            gazePosY = posPix[1]
            
            # Update object color > Hover
            key.fillColor = colorHover
            
            ##################
            # Select object
            if gazeTimer[keyCounter] >= gaze_required_time:
             
                # record the frame that we first wrote on
                # frameNDeep = copy.deepcopy(frameN)
                
                # Update object color > Select
                key.fillColor = colorSelect
                
                iViewXAPI.iV_SendImageMessage(c_char_p('checkStart'))
                    
                # Write a letter when the object is gazed
                # Also keep writing the same letter specified according to a time interval
                if next_writing_frame[keyCounter] == 0 or frameN == next_writing_frame[keyCounter]:
                    # print("no undo")
                    # update the interval to the next frame to write on
                    
                    if next_writing_frame[keyCounter] == 0:
                        # update the interval to the next frame to write on
                        # *2: because there is an undo interval between every two write inter
                        next_writing_frame[keyCounter] = frameN + (write_same_letter_interval + undo_interval)
                    else:
                        next_writing_frame[keyCounter] += write_same_letter_interval + undo_interval
                    
                    # Write
                    stim_writing_output.text = stim_writing_output.text.replace('_', '')
                    stim_writing_output.text = stim_writing_output.text + key.name
					cursorTimer = 0
                    
                    # allow undo
                    undo_success[keyCounter] = False
                
                # do undo
                if frameN < next_writing_frame[keyCounter]:
                    # print("--can undo" + str(frameN) + "-" + str(next_writing_frame))
                    
                    ############
                    # UNDO
                    ############
                    # Check eye pupil
                    
                    # check how many sd the current pupil value is
                    pupil_std_diff = (current_pupil_mean - baseline_mean) / baseline_sd
                    print(str(current_pupil_mean) + " - " + str(baseline_mean) + " - " + str(baseline_sd) + " - " + str(pupil_std_diff))
                    
                    # Undo if pupil_std_diff > required number above std
                    current_pupil_change_size = (pupil_std_diff * pupil_circle_goal_size) / required_pupil_std_diff
                    if current_pupil_change_size < 0.2 * pupil_circle_goal_size: current_pupil_change_size = 0.2*pupil_circle_goal_size # minimum feedback size
                    if current_pupil_change_size > pupil_circle_goal_size: current_pupil_change_size = pupil_circle_goal_size #maximum feedback size
                    
                    # Draw eye pupil
                    
                    # The pupil eye circle
                    circle1 = visual.RadialStim(win, tex='none', mask='none', pos=(gazePosX, gazePosY), size=(current_pupil_change_size, current_pupil_change_size), color=dwellTimeColor, colorSpace='hex', depth=1, interpolate=True)
                    
                    # The outer circle
                    circle2 = visual.RadialStim(win, tex='none', mask='none', pos=(gazePosX, gazePosY), size=(pupil_circle_goal_size, pupil_circle_goal_size), color=dwellTimeBackgroundColor, colorSpace='hex', depth=1, interpolate=True)
                    
                    # draw both circles
                    circle2.draw()
                    circle1.draw()
                    
                    # Actually do the undo
                    if pupil_std_diff >= required_pupil_std_diff and undo_success[keyCounter] == False:
                        # disallow undo
                        undo_success[keyCounter] = True
                        
                        current_text = stim_writing_output.text
                        stim_writing_output.text = current_text[:-1]
                    #############
        
        # not gazing any anything
        # Reset gaze checker and other variables
        else:
            # gaze checker reset
            # beginGazeTimer = False
            gazeTimer[keyCounter] = 0
            
            # Unselect all objects
            key.fillColor = keyColor
            
            # reset everything else
            next_writing_frame[keyCounter] = 0
            
            undo_success[keyCounter] = False
        
        keyCounter += 1
        
        #########################################################
        
        # *text_2* updates
    if t >= 0.0 and text_2.status == NOT_STARTED:
        text_2.tStart = t
        text_2.frameNStart = frameN
        text_2.setAutoDraw(True)
        
    # *stim_writing_output* updates
    if t >= 0.0 and stim_writing_output.status == NOT_STARTED:
        stim_writing_output.tStart = t
        stim_writing_output.frameNStart = frameN
        stim_writing_output.setAutoDraw(True)
        
    # frameRemains = 0.0 + 30- win.monitorFramePeriod * 0.75
    
    # if text_2.status == STARTED: text_2.setAutoDraw(False)
    # if stim_writing_output.status == STARTED: stim_writing_output.setAutoDraw(False)
    
    continueRoutine = True
    
    # check if all components have finished
    # if not continueRoutine:  break
        
    # continueRoutine = False
    # for thisComponent in trialComponents:
        # if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            # continueRoutine = True
            # break
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]): core.quit()
    
    # refresh the screen
    if continueRoutine: win.flip()
# - end while

# -------Ending Routine "trial"-------
for thisComponent in trialComponents:
    if hasattr(thisComponent, "setAutoDraw"): thisComponent.setAutoDraw(False)

####################
iViewXAPI.iV_StopRecording()
iViewXAPI.iV_SaveData(str(dir_experiment + expName + expInfo['participant'] + '_trial'), str(), str(),1)

psizeliste = filter(None, psizeliste)
psizemean = round((sum(psizeliste)/(len(psizeliste))),2)

# Save data
thisExp.addData('Pupil_Liste', psizeliste)
thisExp.addData('Pupil_Mean', psizemean)

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()

# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()