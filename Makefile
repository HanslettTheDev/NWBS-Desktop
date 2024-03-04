clean-logs:
	del /S/Q .\bin\logs\*

build-exe:
	pyinstaller "NWBS Client.spec" 

test-scrapper:
	python nwbs\scheduler\scrapper.py
