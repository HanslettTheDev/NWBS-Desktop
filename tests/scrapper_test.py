from nwbs.scheduler.scrapper import JWIZARD
import asyncio
import config as config


weeklist=[x for x in range(10, 18)]
weeklist.pop(4)
basepath=config.NEW_LINK
jwizard = JWIZARD(basepath=basepath,weeklist=weeklist, pname="march-april")
asyncio.run(jwizard.main())
