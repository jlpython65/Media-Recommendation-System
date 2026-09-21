from playwright.sync_api import sync_playwright
import json
import time
#The profile dorectory is where your persistent login details are stored
#Relative to the pwd of course
#Data like your cookiesfor login information 
USER_DATA_DIR = "./youtube/youtube_profile"

def extract_recommendations():

    #Start a context (browser with its own data like cookies and cache )
    #with keyword means that the context is saved in p AND is killed after use
    with sync_playwright() as p:

        #Persistent context means that context data is stored in 
        # disk, data like my Youtube Login informationnterface stays hid 
        #Headless means chrome runs in the background with no UI
        browser = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        #Goes onto Youtube
        page = browser.new_page()

        # time.sleep(60*5)
        print("Opening YouTube...")

        #Wait until network activity is idle (implies the brwosner has loaded )
        page.goto("https://www.youtube.com", wait_until="networkidle",timeout=600000)

        # Give YouTube a few seconds to finish rendering
        page.wait_for_timeout(5)
        time.sleep(20*60)
        print("Extracting ytInitialData...")

        # The evaluate command executes a Javascript script into the 
        # browser context. All of the varaibles the browser possess 
        # can be accessed and returned
        yt_data = page.evaluate("""
        () => {
            return window.ytInitialData;
        }
        """)

        if yt_data is None:
            print("ytInitialData was not found.")
        else:
            with open("outputs/ytInitialData.json", "w", encoding="utf-8") as f:
                json.dump(yt_data, f, indent=2)

            print("Saved ytInitialData.json")

        browser.close()


if __name__ == "__main__":
    extract_recommendations()