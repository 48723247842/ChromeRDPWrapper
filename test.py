import time
from chrome_rdp_wrapper import ChromeRDPWrapper

if __name__ == "__main__":
	chrome = ChromeRDPWrapper()
	tab = chrome.open_solo_url( "https://www.disneyplus.com/video/8b998fae-f7a6-434a-a8c2-79d853247782" )
	chrome.enable_runtime_on_tab( tab )
	chrome.attach_xdo_tool( "Disney+ | Video Player" )
	time.sleep( 10 )
	chrome.xdotool.press_keyboard_key( "F11" )
	# chrome.xdotool.move_mouse( chrome.geometry["center"]["x"] , chrome.geometry["center"]["y"] )
	# chrome.xdotool.left_click()
	# time.sleep( 1 )
	# chrome.xdotool.press_keyboard_key( "f" )
	#time.sleep( 200 )
	#chrome.close_tab_id( tab["id"] )