import json
from logging import raiseExceptions
from kktfunc.initkkt import initkkt
from libfptr10 import IFptr

def returnDict(success: bool, errorDesc: str):
    return {'succes':success, 'descr':errorDesc}

#Проверка кода маркировки
def checkdm(fptr):
    fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_TYPE, IFptr.LIBFPTR_MCT12_AUTO)
    fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE, '014494550435306821QXYXSALGLMYQQ\u001D91EE06\u001D92YWCXbmK6SN8vvwoxZFk7WAY8WoJNMGGr6Cgtiuja04c=')
    fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_STATUS, 2)
    fptr.setParam(IFptr.LIBFPTR_PARAM_QUANTITY, 1.000)
    fptr.setParam(IFptr.LIBFPTR_PARAM_MEASUREMENT_UNIT, IFptr.LIBFPTR_IU_PIECE)
    fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_PROCESSING_MODE, 0)
    fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_FRACTIONAL_QUANTITY, '1/2')
    fptr.beginMarkingCodeValidation()
    while True:
        fptr.getMarkingCodeValidationStatus()
        if fptr.getParamBool(IFptr.LIBFPTR_PARAM_MARKING_CODE_VALIDATION_READY):
            break
    validationResult = fptr.getParamInt(IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_RESULT)

#Инициализация ККТ 
def initKKT(settings: dict[str, any]):
    fptr = IFptr("")
    if not settings:
    # TODO Тут если не получили настройки, тогда надо бы взять их из DB#
        settings = {
            IFptr.LIBFPTR_SETTING_MODEL: IFptr.LIBFPTR_MODEL_ATOL_11F,
            IFptr.LIBFPTR_SETTING_PORT: IFptr.LIBFPTR_PORT_COM,
            IFptr.LIBFPTR_SETTING_COM_FILE: "COM5",
            IFptr.LIBFPTR_SETTING_BAUDRATE: IFptr.LIBFPTR_PORT_BR_115200
    }
    fptr.setSettings(settings)
    fptr.open()
    if fptr.isOpened():
        return returnDict(True,'')
    else:
        return returnDict(False, fptr.errorDescription())

# Установка кассира
def setcashier(cashier: json, fptr: IFptr):
    fptr.setParam(1021, "Кассир Иванов И.")
    fptr.setParam(1203, "123456789047")
    fptr.operatorLogin()
    if fptr.errorCode() == 0:
        return returnDict(True, '')
    else:    
        return returnDict(False, fptr.errorDescription())

#Открытие смены
def openShift(cashier: json):
    if cashier:
        pass
    else: #TODO кассир не пришел, надо взять из БД
        pass
    fptr = initKKT(None)
    if fptr.isinstance(IFptr):
        fptr.openShift()
        if fptr.isOpened():
            return returnDict(True, '')
        else:
            return returnDict(False, fptr.errorDescription())
    else:
        return fptr.errorDescription()

#Закрытие смены
def closeShift(cashier: json):
    if cashier:
        pass
    else:
        pass
    fptr = initKKT(None)
    
    