clean-logs:
	del /S/Q .\bin\logs\*

build-exe:
	pyinstaller --noconfirm --clean "NWBS Client.spec" 

test-scrapper:
	python nwbs\scheduler\scrapper.py
