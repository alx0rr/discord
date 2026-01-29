from setuptools import setup, find_packages

with open("README.md", "r") as file:
	long_description = file.read()

link = 'https://github.com/alx0rr/discord/archive/refs/heads/main.zip'
ver = '1.3.8'

setup(
	name = "udiscord",
	version = ver,
	url = "https://github.com/alx0rr/discord",
	download_url = link,
	license = "MIT",
	author = "alx0rr",
	author_email = "anon.mail.al@proton.me",
	description = "Library for creating discord bots and scripts.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	keywords = [
		"discord.py",
		"discord",
		"discord-py",
		"discord-bot",
		"api",
		"python",
		"python3",
		"python3.x",
		"alx0rr",
		"official",
		"sync",
		"async",
		"udiscord",
		"discord-self-bot"
	],
	install_requires = [
		"requests",
		"ujson",
		"logging",
		"websocket-client",
		"colorama",
		"aiohttp"
	],
	packages = find_packages()
)