from websocket import create_connection
import json
import requests
import time
from pprint import pprint
from XDoToolWrapper import XDoToolWrapper

class ChromeRDPWrapper:

	def __init__( self , options={} ):
		self.options = options

	def websocket_send_message( self , address , message ):
		try:
			ws = create_connection( address )
			ws.send( json.dumps( message ) )
			data = None
			while True:
				data = ws.recv()
				try:
					data = json.loads( data )
					break
				except Exception as e:
					print( e )
					ws.close()
			ws.close()
			return data
		except Exception as e:
			print( "Couldn't Send Websocket Message" )
			print( e )
			return False

	def get_tabs( self ):
		try:
			tabs = requests.get( "http://127.0.0.1:9222/json" )
			tabs.raise_for_status()
			tabs = tabs.json()
			return tabs
		except Exception as e:
			print( "Couldn't Get Tabs" )
			print( e )
			return False

	def open_url( self , url ):
		try:
			result = requests.get( f"http://127.0.0.1:9222/json/new?{url}" )
			result.raise_for_status()
			result = result.json()
			return result
		except Exception as e:
			print( "Couldn't Open URL" )
			print( e )
			return False

	def close_tab_id( self , tab_id ):
		try:
			result = requests.get( f"http://localhost:9222/json/close/{tab_id}" )
			result.raise_for_status()
			result = result.json()
			return result
		except Exception as e:
			#print( "Couldn't Close Tab ID" )
			#print( e )
			return False

	def enable_runtime_on_tab( self , tab ):
		try:
			result = self.websocket_send_message( tab["webSocketDebuggerUrl"] , {"id":1 ,"method": "Runtime.enable"} )
			return result
		except Exception as e:
			print( "Couldn't Load Runtime" )
			print( e )
			return False

	def open_solo_url( self , url ):
		try:

			# 1.) Open URL
			new_url_result = self.open_url( url )
			#pprint( new_url_result )

			# 2.) Get List of Tabs
			chrome_tabs = self.get_tabs()
			pages = [ x for x in chrome_tabs if x["type"] == "page" ]
			other_pages = [ x for x in pages if x["id"] != new_url_result["id"] ]
			#pprint( other_pages )

			# 3.) Close All Pages Except the Tab We Just Opened
			for index , page in enumerate( other_pages ):
				pprint( self.close_tab_id( page["id"] ) )

			return new_url_result

		except Exception as e:
			print( "Couldn't Open Solo URL" )
			print( e )
			return False

	def attach_xdo_tool( self , window_name="Chrome" ):
		try:
			self.xdotool = None
			self.xdotool = XDoToolWrapper()
			self.xdotool.get_monitors()
			self.xdotool.attach_via_name( window_name )
			self.geometry = self.xdotool.get_window_geometry()
			print( self.geometry )
		except Exception as e:
			print( "Couldn't Attach XDOTool" )
			print( e )
			return False

if __name__ == "__main__":

	chrome = ChromeRDPWrapper()
	tab = chrome.open_solo_url( "https://www.disneyplus.com/video/8b998fae-f7a6-434a-a8c2-79d853247782" )
	chrome.enable_runtime_on_tab( tab )
	chrome.attach_xdo_tool( "Disney+ | Video Player" )
	#chrome.xdotool.press_keyboard_key( "Ctrl+r" )
	chrome.xdotool.move_mouse( chrome.geometry["center"]["x"] , chrome.geometry["center"]["y"] )
	time.sleep( 20 )
	chrome.close_tab_id( tab["id"] )