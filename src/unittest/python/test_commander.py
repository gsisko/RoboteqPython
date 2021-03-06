#system imports to provide proper test execution
import sys, os
from io import StringIO
#for pre build tests
#sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir) + "\\commanders"))

#testing module imports
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

#import Commander for testing
from RoboteqCommand import RoboteqCommand, RoboteqCommandLibrary, RoboteqCommander, RuntimeCommand, RuntimeQuery, ConfigSetting



class RoboteqCommanderFixture(unittest.TestCase):


    #Function to emulate controller response to given command strings
    def EvaluateControllerResponse(self, _CommandString):
            return 'Place Holder Controller Response'

    TestStreamBuffer = StringIO()

    #Mock readline so that controller alwasy returns an incorrect response
    TestStreamBuffer.readline = MagicMock(return_value = 'Place Holder Controller Response')

    def setUp(self):
        self.gocommand = RuntimeCommand('G', 0)
        self.ampsquery = RuntimeQuery('A', 0)
        self.operatingconfig = ConfigSetting('MMOD', 0)
        self.commander = RoboteqCommander(RoboteqCommandLibrary({'_G': self.gocommand , '_A': self.ampsquery, '_MMOD': self.operatingconfig}), self.TestStreamBuffer)


class TestRoboteqCommanderMethods(RoboteqCommanderFixture):

    def test_SubmitCommand(self):

        #test Cases for command cosntruction
        self.assertEqual(self.commander._ConstructOutput('!','_G', 1, 300), ('!', 'G', 1, 300))
        #test sending a normal motor CommandDictionary
        self.assertEqual(self.commander._FormatOutput(("!",'G', 1, 300)), '!G 1 300')
        #test multiple arguments case
        self.assertEqual(self.commander._FormatOutput(("!",'G', 1, 300, 300)), '!G 1 300 300')


    #test output of Getcommand
    #TODO: Implement context manager to clear TestStreamBuffer between tests


    def test_getValue(self):
        self.assertEqual(self.commander.getValue('_A', 1), self.EvaluateControllerResponse('?A 1'))
        self.assertEqual(self.TestStreamBuffer.getvalue().splitlines().pop(), '?A 1')


    def test_setCommand(self):
        self.assertEqual(self.commander.setCommand('_G', 1, 300), self.EvaluateControllerResponse('!G 1 300'))
        self.assertEqual(self.TestStreamBuffer.getvalue().splitlines().pop(),'!G 1 300')


    def test_setConfig(self):
        self.assertEqual(self.commander.setConfig('_MMOD', 1), self.EvaluateControllerResponse('^MMOD 1'))
        self.assertEqual(self.TestStreamBuffer.getvalue().splitlines().pop(), '^MMOD 1')

    def test_getConfig(self):
        self.assertEqual(self.commander.getConfig('_MMOD'), self.EvaluateControllerResponse('~MMOD'))
        self.assertEqual(self.TestStreamBuffer.getvalue().splitlines().pop(), '~MMOD')

#TODO add sections for each type of serial commander

if __name__ == '__main__':
        unittest.main()
