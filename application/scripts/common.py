import datetime


def getTime(days = 1,DateSplit=None):
    if not DateSplit:
        Datetype = "%Y%m%d"
    else:
        Datetype = "%Y"+DateSplit+"%m"+DateSplit+"%d"
    aimDate = (datetime.datetime.now() - datetime.timedelta(days = days)).strftime(Datetype)
    return aimDate

def handlestr(str):
	return str.replace("'","''")