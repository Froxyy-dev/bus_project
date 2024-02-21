import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from bus_project.data_collecting import helper_functions, collect_data, url_builders
from bus_project.config.config import get_time_to_wait

TIME_TO_WAIT = get_time_to_wait()


class TestDataCollecting(unittest.TestCase):

    @patch('bus_project.data_collecting.helper_functions.requests.get')
    def test_get_response(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': [{'data': 'example'}]}
        mock_requests_get.return_value = mock_response

        response = helper_functions.get_response('http://example.com')

        self.assertEqual(response, {'result': [{'data': 'example'}]})

    @patch('bus_project.data_collecting.helper_functions.save_json_to_file')
    @patch('bus_project.data_collecting.helper_functions.get_response')
    def test_get_and_save_response(self, mock_get_response, mock_save_json_to_file):
        mock_response = {'result': [{'data': 'example'}]}
        mock_get_response.return_value = mock_response

        result = helper_functions.get_and_save_response(['arg1', 'arg2'], 'bus_stop_lines_link', 'file/path.json')

        self.assertEqual(result, [{'data': 'example'}])

        mock_save_json_to_file.assert_called_once_with(mock_response, 'file/path.json')

    @patch('bus_project.data_collecting.helper_functions.time')
    def test_wait_if_necessary(self, mock_time):
        mock_time.time.side_effect = [0, 2]

        helper_functions.wait_if_necessary(0)
        mock_time.sleep.assert_called_once_with(TIME_TO_WAIT)

        helper_functions.wait_if_necessary(0)

        mock_time.sleep.assert_called_with(TIME_TO_WAIT - 2)

    def test_create_directory(self):
        bus_stop_id = 'stop_id'
        bus_stop_nr = '123'

        filepath = helper_functions.create_directory(bus_stop_id, bus_stop_nr)

        expected_filepath = f"{str(helper_functions.BUS_STOP_INFO_PATH)}{bus_stop_id}_{bus_stop_nr}_lines"
        self.assertEqual(filepath, expected_filepath)

        self.test_data_path = Path(helper_functions.DATA_PATH / filepath)

        self.assertTrue(Path(helper_functions.DATA_PATH / filepath).exists())
        self.test_data_path.rmdir()

    @patch('bus_project.data_collecting.collect_data.gather_bus_stop_data')
    @patch('bus_project.data_collecting.collect_data.gather_bus_positions_data')
    def test_collect_data(self, mock_gather_bus_positions_data, mock_gather_bus_stop_data):
        mock_gather_bus_stop_data.return_value = None
        mock_gather_bus_positions_data.return_value = None

        with patch('builtins.print') as mock_print:
            collect_data.collect_data(2, True)

            mock_print.assert_any_call("Collecting static data...")
            mock_print.assert_any_call("Finished collecting static data!")
            mock_print.assert_any_call("Collecting bus position data...")
            mock_print.assert_any_call("Finished collecting bus position data!")

            self.assertEqual(mock_print.call_count, 4)

            mock_print.reset_mock()
            collect_data.collect_data(0, False)

            mock_print.assert_not_called()

    @patch('bus_project.data_collecting.url_builders.API_KEY', 'test_api_key')
    @patch('bus_project.data_collecting.url_builders.URLS', {
        'test_link': ['http://example.com/', '&arg1=', '&arg2=']
    })
    def test_build_url(self):
        url = url_builders.build_url(['value1', 'value2'], 'test_link')

        expected_url = 'http://example.com/value1&arg1=value2&arg2=test_api_key'
        self.assertEqual(url, expected_url)


if __name__ == '__main__':
    unittest.main()
