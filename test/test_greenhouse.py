from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock

from mock import GPIO
from mock.seesaw import Seesaw
from src.greenhouse import Greenhouse, GreenhouseError


class TestGreenhouse(TestCase):

    @patch.object(Seesaw, attribute='moisture_read')
    def test_soil_measure_moisture_valid_range(self, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 300
        system = Greenhouse()
        moisture = system.measure_soil_moisture()
        self.assertEqual(300, moisture)

    @patch.object(Seesaw, attribute='moisture_read')
    def test_measure_soil_moisture_below_range(self, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 299
        system = Greenhouse()
        self.assertRaises(GreenhouseError, system.measure_soil_moisture)

    @patch.object(Seesaw, attribute="moisture_read")
    def test_measure_soil_moisture_above_range(self, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 501
        system = Greenhouse()
        self.assertRaises(GreenhouseError, system.measure_soil_moisture)

    @patch.object(GPIO, attribute="output")
    def test_turn_on_sprikler(self, mock_sprinkler: Mock):
        system = Greenhouse()
        system.turn_on_sprinkler()
        mock_sprinkler.assert_called_with(system.SPRINKLER_PIN, True)
        self.assertTrue(system.is_sprinkler_on())

    @patch.object(GPIO, attribute="output")
    def test_turn_on_sprikler(self, mock_sprinkler: Mock):
        system = Greenhouse()
        system.turn_off_sprinkler()
        mock_sprinkler.assert_called_with(system.SPRINKLER_PIN, False)
        self.assertFalse(system.is_sprinkler_on())

    @patch.object(Seesaw, attribute="moisture_read")
    @patch.object(GPIO, attribute="output")
    def test_manage_sprinkler_should_be_turned_on_when_below_375(self,mock_sprinkler: Mock, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 374
        system = Greenhouse()
        system.manage_sprinkler()
        mock_sprinkler.assert_called_with(system.SPRINKLER_PIN, True)
        self.assertTrue(system.is_sprinkler_on())

    @patch.object(Seesaw, attribute="moisture_read")
    @patch.object(GPIO, attribute="output")
    def test_manage_sprinkler_should_be_turned_on_when_above_425(self, mock_sprinkler: Mock, mock_moisture_sensor: Mock):
        mock_moisture_sensor.return_value = 426
        system = Greenhouse()
        system.sprinkler_on = True
        system.manage_sprinkler()
        mock_sprinkler.assert_called_with(system.SPRINKLER_PIN, False)
        self.assertFalse(system.is_sprinkler_on())

    @patch.object(GPIO, attribute="input")
    def test_check_too_much_light(self, mock_photoresistor: Mock):
        system = Greenhouse()
        mock_photoresistor.return_value = True
        self.assertTrue(system.check_too_much_light())

    @patch.object(GPIO, attribute="output")
    @patch.object(GPIO, attribute="input")
    def test_turn_on_lightbulb_should_be_turned_on(self, mock_photoresistor: Mock, mock_red_light: Mock):
        mock_photoresistor.return_value = True
        system = Greenhouse()
        system.manage_lightbulb()
        mock_red_light.assert_called_with(system.LED_PIN, True)
        self.assertTrue(system.red_light_on)

    @patch.object(GPIO, attribute="output")
    @patch.object(GPIO, attribute="input")
    def test_turn_off_lightbulb_should_be_turned_off(self, mock_photoresistor: Mock, mock_red_light: Mock):
        mock_photoresistor.return_value = False
        system = Greenhouse()
        system.manage_lightbulb()
        mock_red_light.assert_called_with(system.LED_PIN, False)
        self.assertFalse(system.red_light_on)








