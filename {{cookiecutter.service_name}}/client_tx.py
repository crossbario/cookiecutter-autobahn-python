import os
import sys
import argparse
import six
import txaio
import uuid
import socket
import platform

from pprint import pformat

from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.wamp.types import RegisterOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError


class ClientSession(ApplicationSession):
    """
    Our WAMP session class .. place your app code here!
    """

    def onConnect(self):
        self.log.info("Client connected: {klass}, {extra}", klass=ApplicationSession, extra=self.config.extra)
        self.join(self.config.realm, ['anonymous'])

    def onChallenge(self, challenge):
        self.log.info("Challenge for method {authmethod} received", authmethod=challenge.method)
        raise Exception("We haven't asked for authentication!")

    @inlineCallbacks
    def onJoin(self, details):

        self.log.info("Connected: {details}", details=details)

        self._ident = details.authid
        self._type = 'Python'

        self.log.info("Component ID is  {ident}", ident=self._ident)
        self.log.info("Component type is  {type}", type=self._type)

        # REGISTER
        def add2(a, b):
            print('----------------------------')
            print("add2 called on {}".format(self._ident))
            return [ a + b, self._ident, self._type]

        yield self.register(add2, 'com.example.add2', options=RegisterOptions(invoke='roundrobin'))
        print('----------------------------')
        print('procedure registered: com.myexample.add2')

        # SUBSCRIBE
        def oncounter(counter, id, type):
            print('----------------------------')
            self.log.info("'oncounter' event, counter value: {counter}", counter=counter)
            self.log.info("from component {id} ({type})", id=id, type=type)

        yield self.subscribe(oncounter, 'com.example.oncounter')
        print('----------------------------')
        self.log.info("subscribed to topic 'oncounter'")

        x = 0
        counter = 0
        while True:

            # CALL
            try:
                res = yield self.call('com.example.add2', x, 3)
                print('----------------------------')
                self.log.info("add2 result: {result}",
                result=res[0])
                self.log.info("from component {id} ({type})", id=res[1], type=res[2])
                x += 1
            except ApplicationError as e:
                ## ignore errors due to the frontend not yet having
                ## registered the procedure we would like to call
                if e.error != 'wamp.error.no_such_procedure':
                    raise e

            # PUBLISH
            yield self.publish('com.example.oncounter', counter, self._ident, self._type)
            print('----------------------------')
            self.log.info("published to 'oncounter' with counter {counter}",
                          counter=counter)
            counter += 1

            yield sleep(2)


    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Router connection closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    # parse command line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Enable debug output.')

    parser.add_argument('--url',
                        dest='url',
                        type=str,
                        default="ws://localhost:8080/ws",
                        help='The router URL (default: "ws://localhost:8080/ws").')

    parser.add_argument('--realm',
                        dest='realm',
                        type=str,
                        default='realm1',
                        help='The realm to join (default: "realm1").')

    parser.add_argument('--service_name',
                        dest='service_name',
                        type=str,
                        default=socket.gethostname(),
                        help='Optional service name.')

    parser.add_argument('--service_uuid',
                        dest='service_uuid',
                        type=str,
                        default=str(uuid.uuid4()),
                        help='Optional service UUID.')

    args = parser.parse_args()

    # start logging
    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    # any extra info we want to forward to our ClientSession (in self.config.extra)
    extra = {
        'service_name': args.service_name,
        'service_uuid': args.service_uuid,
        'service_host': {
            'executable': os.path.realpath(sys.executable),
            'platform': platform.platform(),
            'machine': platform.machine(),
            'python_version': platform.python_version(),
            'python_implementation': platform.python_implementation(),
        }
    }

    # now actually run a WAMP client using our session class ClientSession
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(ClientSession, auto_reconnect=True)
