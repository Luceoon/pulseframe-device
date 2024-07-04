import api
import os
import time
import anim

UPDATE_INTERVAL = 10

state = None
last_update = 0

def init():
    global state, last_update

    checkForUpdate()
    last_update = time.monotonic()


def tick():
    global last_update

    if time.monotonic() - last_update > UPDATE_INTERVAL:
        checkForUpdate()
        last_update = time.monotonic()

def checkForUpdate():
    global state

    print ("Checking for updates...")
    if api.fetchCheck():

        state = api.fetchUpdate()
        
        animation_list = getAnimations()
        print("Animations: ", animation_list)
        removeUnusedAnimations()
        api.fetchAnimations(animation_list)

def getAnimations():
    result = []

    for anim in state["anim"]:
        entry = []
        entry.append(anim["filename"])
        entry.append(anim["duration"])
        result.append(entry)

    return result

def removeUnusedAnimations():
    usedAnimations = getAnimations()

    for anim in os.listdir("/data"):
        if anim == "pulseframe_loading.gif":
            continue
        for entry in usedAnimations:
            if anim == entry[0]:
                continue

        try:
            print ("Removing unused animation '" + anim + "'...")
            os.remove("/data/" + anim)
        except Exception as e:
            print ("Couldn't remove unused animation! -", e)