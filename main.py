from src.mbulak_tools.events import exit_signal
from src.mybootstrap_core_itskovichanton.di import injector

from src.unikron.app import UnikronApp


def main() -> None:
    # alert_service = injector.inject(AlertService)
    # alert_service.get_interceptors().append(lambda e: None if isinstance(e,
    #                                                                      CoreException) and e.reason == ERR_REASON_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND else e)
    app = injector().inject(UnikronApp)
    app.run()


def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    exit_signal.set()


if __name__ == '__main__':
    import signal

    for sig in ('TERM', 'HUP', 'INT'):
        sig_name = 'SIG' + sig
        if hasattr(signal, sig_name):
            sig = getattr(signal, sig_name)
            if sig:
                signal.signal(sig, quit)
    main()
