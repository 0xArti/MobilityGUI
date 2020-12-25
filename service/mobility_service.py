import win32serviceutil
import servicemanager
import win32event
import win32service


class MobilityService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MobilityService'
    _svc_display_name_ = 'Mobility Service'
    _svc_description_ = 'Display GUI popup based on interval to remind you that you need to move. \
        and provide an exercise designed for you'

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        pass

    def stop(self):
        pass

    def main(self):
        pass
