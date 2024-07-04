import adafruit_requests as requests

BASE_URL = "http://10.0.0.50:3000"
API_URL = BASE_URL + "/api"

last_update_checksum = ""

def fetchCheck():
    global last_update_checksum

    try:
        response = requests.get(API_URL + "/check")
        check = response.json()
        response.close()
    except Exception as e:
        print("Couldn't fetch check! -", e)
        return
    
    checksum = check["checksum"]
    if checksum != last_update_checksum:
        print ("Update available! (" + checksum + ")")
        last_update_checksum = checksum
        return True
    
    return False


def fetchUpdate():

    print ("Fetching update...")
    try:
        response = requests.get(API_URL + "/update")
        update = response.json()
        response.close()
    except Exception as e:
        print("Couldn't fetch update! -", e)

    print ("[DEBUG] Update ID:", update["checksum"])
    print ("[DEBUG] Anim:", update["anim"])

    return update
    


def fetchAnimations(files):

    # Check for new Animations
    print ("Fetching new animations...")

    # --- Animation Downloading ---
    for animation in files:

        filepath = '/data/' + animation[0]
        file_exists = False
        try:
            with open(filepath, 'r') as f:
                file_exists = True
                print ("Animation '" + animation[0] + "' already exists!")
        except Exception as e:
            pass

        if not file_exists:
            print ("Downloading new animation '" + animation[0] + "'...")
            try:
                with open('/data/' + animation[0], 'wb') as f:
                    response = requests.get(BASE_URL + "/files/" + animation[0])
                    for chunk in response.iter_content(1024):  # Stream 1024 bytes at a time
                        f.write(chunk)
                    f.close()
                print ("Saved new animation '" + animation[0] + "'!")
            except Exception as e:
                print("Couldn't download new animation! -", e)