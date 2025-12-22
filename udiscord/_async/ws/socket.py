from ujson import dumps, loads

from ...utils.requester import Requester
from ... import log
from .socket_handler import Handler
from traceback import format_exc


from aiohttp import ClientSession, WSMsgType, ClientWebSocketResponse, ClientConnectionError, WSServerHandshakeError, ClientTimeout
from asyncio import create_task, CancelledError
from asyncio import sleep
from json import loads, dumps
import asyncio





class AsyncSocket(Handler):
	heartbeat_started: bool = False
	req: Requester
	heartbeat_interval: int = None

	def __init__(self, os: str, browser: str, device: str, detailed_error: bool = False):
		self.socket_url = "wss://gateway.discord.gg"
		self.detailed_error = detailed_error
		self.os, self.browser, self.device = os, browser, device


		self.connection: ClientWebSocketResponse = None
		self.task_receiver = None
		self.task_pinger = None
		self.ws_client_session = None


		Handler.__init__(self)


	async def connect(self):
		try:
			if self.connection: return
			log.debug(f"[socket][start] Starting Socket")


			if self.ws_client_session:
				try:
					log.debug("[socket][start] Closing old session...")
					await asyncio.wait_for(self.ws_client_session.close(), timeout=5)
				except:
					pass
				self.ws_client_session = None

			self.ws_client_session = ClientSession(
				base_url=self.socket_url,
				headers=self.req.headers(),
				timeout=ClientTimeout(total=20, connect=15, sock_connect=10, sock_read=15)
			)

			self.connection = await asyncio.wait_for(
				self.ws_client_session.ws_connect(
					f"/?encoding=json&v=9",
					heartbeat=10,
					autoclose=True
				),
				timeout=30
			)

			if not self.task_receiver:
				self.task_receiver = create_task(self.resolve())
			if not self.task_pinger:
				self.task_pinger = create_task(self.start_heartbeat())
			
			log.debug(f"[socket][start] Socket Started")
		except Exception as e:
			log.error(f"[socket][start] Error while starting Socket : {e}{'' if not self.detailed_error else f'\n{format_exc()}'}")


	async def disconnect(self):
		log.debug(f"[socket][close] Closing Socket")
		try:

			if self.task_pinger:
				log.debug(f"[socket][pinger] Closing...")
				self.task_pinger.cancel()
				self.task_pinger = None

			if self.connection:
				log.debug("[socket][stop] Closing connection...")
				try:
					await asyncio.wait_for(self.connection.close(), timeout=3.0)
				except Exception as e:
					log.debug(f"[socket][stop] Error closing connection: {e}")
				self.connection = None

			if self.ws_client_session:
				log.debug("[socket][stop] Closing session...")
				try:
					await asyncio.wait_for(self.ws_client_session.close(), timeout=3.0)
				except Exception as e:
					log.debug(f"[socket][stop] Error closing session: {e}")
				self.ws_client_session = None


			log.debug(f"[socket][close] Socket closed")
		except Exception as e:
			log.error(f"[socket][close] Error while closing Socket : {e}{'' if not self.detailed_error else f'\n{format_exc()}'}")




	async def resolve(self):
		retry_count = 0
		max_retries = 5
		
		while True:
			try:
				if self.connection is None:
					await sleep(1)
					continue
				
				retry_count = 0 
					
				try:
					msg = await asyncio.wait_for(
						self.connection.receive(), 
						timeout=60
					)
				except asyncio.TimeoutError:
					log.debug("[socket][receive] Timeout, attempting reconnect...")
					await self.reconnect()
					continue
				except CancelledError:
					log.debug("[socket][receive] Task cancelled")
					return
					
				if msg.type != WSMsgType.TEXT:
					continue
					
				try:
					data = loads(msg.data)
				except Exception as e:
					log.debug(f"[socket][receive] Failed to parse message: {e}")
					continue

				log.debug(f"[socket][receive]: {data}")
				if data.get("op") == 10:
					self.heartbeat_interval = data['d']['heartbeat_interval'] / 1000
					continue
				await self.handle_data(data)
				
			except (WSServerHandshakeError, ClientConnectionError) as e:
				log.debug(f"[socket][receive] Connection error: {e}")
				retry_count += 1
				if retry_count > max_retries:
					log.error("[socket][receive] Max retries exceeded")
					return
				await self.reconnect()
				continue
			except CancelledError:
				log.debug("[socket][receive] Task cancelled")
				return
			except Exception as e:
				log.error(f"[socket][receive] Unexpected error: {e}")
				retry_count += 1
				if retry_count > max_retries:
					log.error("[socket][receive] Max retries exceeded")
					return
				await self.reconnect()
				continue



	async def reconnect(self):
		log.debug("[socket][reconnect] Socket reconnecting...")
		await self.disconnect()
		await sleep(2)
		try:
			await asyncio.wait_for(self.connect(), timeout=25)
		except asyncio.TimeoutError:
			log.error("[socket][reconnect] Reconnection timeout")
		except Exception as e:
			log.error(f"[socket][reconnect] Reconnection failed: {e}")



	async def start_heartbeat(self):
		await sleep(0.5)
		identify_payload = {
			"op": 2,
			"d": {
				"token": self.req.token,
				"properties": {
					"os": self.os,
					"browser": self.browser,
					"device": self.device
				}
			}
		}
		for i in range(5):
			try:
				await self.send(identify_payload)
				break
			except Exception as e:
				log.error("[socket][start] Failed connect to discord socket. reconnecting...")
				sleep(1.5)
		else:
			log.critical("[socket][start] Failed connect to discord socket.")

		while self.connection:
			if not self.heartbeat_interval: continue
			await sleep(self.heartbeat_interval)
			if self.connection:
				await self.send({"op": 1, "d": None})

	async def send(self, data: str | dict):
		if self.connection is None:
			log.debug(f"[socket][send][error]: socket is disabled or not running.")
			return
		log.debug(f"[socket][send]: {data}")
		await self.connection.send_str(
			data if isinstance(data, str) else dumps(data)
		)



	async def socket_wait(self):
		"""
		Starts a loop that continuously listens for new messages from the WebSocket connection.
		
		This method is used to keep the program running and process incoming messages in real-time. 
		It ensures that the WebSocket connection remains open, and the program doesn't exit unexpectedly while 
		awaiting messages. 

		The loop will run as long as `self.socket_enable` is True. The method sleeps for 3 seconds between 
		iterations to prevent unnecessary CPU usage while waiting for new data.

		Example:
			await client.socket_wait()
		"""
		try:
			while True:
				await sleep(3)
		except (CancelledError, KeyboardInterrupt):
			log.debug("[socket][socket_wait] Socket wait cancelled")
			await self.disconnect()