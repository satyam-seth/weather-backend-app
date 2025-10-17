import unittest
from unittest.mock import MagicMock, Mock, patch

import requests

from climate.parsers import (
    MONTH_FIELDS,
    SEASON_FIELDS,
    ClimateDataFetcher,
    ClimateDataHandler,
    ClimateDataParser,
    ClimateDataProcessor,
)


class TestClimateDataFetcher(unittest.TestCase):
    """Tests for ClimateDataFetcher"""

    @patch("requests.get")
    def test_fetch_data_success(self, mock_get: Mock) -> None:
        """Test successful data fetch"""

        # Prepare the mock response
        mock_response = Mock()
        mock_response.text = "sample data"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Call the method
        url = "http://example.com/climate_data"
        result = ClimateDataFetcher.fetch_data(url)

        # Assertions
        mock_get.assert_called_once_with(url, timeout=10)
        self.assertEqual(result, "sample data")

    @patch("requests.get")
    def test_fetch_data_request_exception(self, mock_get: Mock) -> None:
        """Test data fetch with request exception"""

        # Prepare the mock to raise an exception
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Call the method and assert exception is raised
        url = "http://example.com/climate_data"
        with self.assertRaises(requests.exceptions.RequestException):
            ClimateDataFetcher.fetch_data(url)

        # Ensure that the mock was called
        mock_get.assert_called_once_with(url, timeout=10)


class TestClimateDataParser(unittest.TestCase):
    """Tests for ClimateDataParser"""

    def test_filter_data_lines_valid(self) -> None:
        """Test filtering valid data lines"""

        # Sample raw data with mixed valid and invalid lines
        raw_data = """
        2020 1.0 2.0 3.0 4.0
        abc 1.0 2.0 3.0 4.0
        2021 1.1 2.1 3.1 4.1
        2019 0.9 1.9 2.9 3.9
        xyz 1.0 2.0 3.0 4.0
        """

        # Expected filtered result
        expected_result = [
            "2020 1.0 2.0 3.0 4.0",
            "2021 1.1 2.1 3.1 4.1",
            "2019 0.9 1.9 2.9 3.9",
        ]

        # Call the method
        filtered_data = ClimateDataParser.filter_data_lines(raw_data)

        # Assertions
        self.assertEqual(filtered_data, expected_result)

    def test_filter_data_lines_all_invalid(self) -> None:
        """Test filtering all invalid data lines"""

        # Raw data with all invalid lines
        raw_data = """
        abc 1.0 2.0 3.0 4.0
        xyz 1.0 2.0 3.0 4.0
        """

        # Call the method and expect an empty list
        filtered_data = ClimateDataParser.filter_data_lines(raw_data)

        # Assertions
        self.assertEqual(filtered_data, [])

    def test_filter_data_lines_all_valid(self) -> None:
        """Test filtering all valid data lines"""

        # Raw data with all valid lines
        raw_data = """
        2022 1.0 2.0 3.0 4.0
        2023 5.0 6.0 7.0 8.0
        """

        # Expected result should be exactly the same as raw data
        expected_result = ["2022 1.0 2.0 3.0 4.0", "2023 5.0 6.0 7.0 8.0"]

        # Call the method
        filtered_data = ClimateDataParser.filter_data_lines(raw_data)

        # Assertions
        self.assertEqual(filtered_data, expected_result)

    def test_filter_data_lines_empty_input(self):
        """Test filtering with empty input"""

        # Test with empty input
        raw_data = ""

        # Expect an empty list
        filtered_data = ClimateDataParser.filter_data_lines(raw_data)

        # Assertions
        self.assertEqual(filtered_data, [])

    def test_filter_data_lines_no_valid_lines(self):
        """Test filtering with no valid lines"""

        raw_data = """
        abc 1.0 2.0 3.0 4.0
        xyz 5.0 6.0 7.0 8.0
        """

        # Expect an empty list since all lines are invalid
        filtered_data = ClimateDataParser.filter_data_lines(raw_data)

        # Assertions
        self.assertEqual(filtered_data, [])

    def test_extract_year_valid(self):
        """Test extracting a valid year"""

        parts = ["2021", "1.0", "2.0", "3.0", "4.0", "5.0"]
        year = ClimateDataParser.extract_year(parts)
        self.assertEqual(year, 2021)

    def test_extract_year_invalid(self):
        """Test extracting an invalid year"""

        parts = ["abc", "1.0", "2.0", "3.0", "4.0", "5.0"]
        year = ClimateDataParser.extract_year(parts)
        self.assertIsNone(year)

    def test_extract_values(self):
        """Test extracting values with missing data"""

        parts = ["2021", "1.0", "2.0", "---", "4.0"]
        values = ClimateDataParser.extract_values(parts)
        self.assertEqual(values, [1.0, 2.0, None, 4.0])

    def test_process_months(self):
        """Test processing month values"""

        values = [
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
        ]
        month_values = ClimateDataParser.process_months(values)
        self.assertEqual(
            month_values,
            dict(
                zip(
                    MONTH_FIELDS,
                    [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
                )
            ),
        )

    def test_process_seasons(self):
        """Test processing season values"""

        values = [
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
        ]
        season_values = ClimateDataParser.process_seasons(values)
        self.assertEqual(
            season_values,
            dict(
                zip(
                    SEASON_FIELDS,
                    [
                        13.0,
                        14.0,
                        15.0,
                        16.0,
                        17.0,
                    ],
                )
            ),
        )

    @patch("climate.parsers.ClimateDataParser.filter_data_lines")
    @patch("climate.parsers.ClimateDataParser.process_line")
    def test_parse_data_valid(
        self,
        mock_process_line: Mock,
        mock_filter_data_lines: Mock,
    ) -> None:
        """Test parsing valid data"""

        # Sample raw data
        raw_data = """
        2020 1.0 2.0 3.0 4.0
        2021 1.1 2.1 3.1 4.1
        """

        # Mock filter_data_lines to return the raw lines as is
        mock_filter_data_lines.return_value = [
            "2020 1.0 2.0 3.0 4.0",
            "2021 1.1 2.1 3.1 4.1",
        ]

        # Mock process_line to return parsed results for each line
        mock_process_line.side_effect = [
            (2020, {"jan": 1.0, "feb": 2.0}, {"win": 3.0}),
            (2021, {"jan": 1.1, "feb": 2.1}, {"win": 3.1}),
        ]

        # Expected parsed data
        expected_result = [
            (2020, {"jan": 1.0, "feb": 2.0}, {"win": 3.0}),
            (2021, {"jan": 1.1, "feb": 2.1}, {"win": 3.1}),
        ]

        # Call the method
        parsed_data = ClimateDataParser.parse_data(raw_data)

        # Assertions
        self.assertEqual(parsed_data, expected_result)

    @patch("climate.parsers.ClimateDataParser.filter_data_lines")
    @patch("climate.parsers.ClimateDataParser.process_line")
    def test_parse_data_invalid_line(
        self,
        mock_process_line: Mock,
        mock_filter_data_lines: Mock,
    ) -> None:
        """Test parsing data with an invalid line"""

        # Sample raw data with one invalid line
        raw_data = """
        2020 1.0 2.0 3.0 4.0
        invalid data
        2021 1.1 2.1 3.1 4.1
        """

        # Mock filter_data_lines to return the raw lines as is
        mock_filter_data_lines.return_value = [
            "2020 1.0 2.0 3.0 4.0",
            "invalid data",
            "2021 1.1 2.1 3.1 4.1",
        ]

        # Mock process_line to return parsed results for valid lines and None for invalid
        mock_process_line.side_effect = [
            (2020, {"jan": 1.0, "feb": 2.0}, {"win": 3.0}),
            None,  # This will skip the invalid line
            (2021, {"jan": 1.1, "feb": 2.1}, {"win": 3.1}),
        ]

        # Expected parsed data, ignoring the invalid line
        expected_result = [
            (2020, {"jan": 1.0, "feb": 2.0}, {"win": 3.0}),
            (2021, {"jan": 1.1, "feb": 2.1}, {"win": 3.1}),
        ]

        # Call the method
        parsed_data = ClimateDataParser.parse_data(raw_data)

        # Assertions
        self.assertEqual(parsed_data, expected_result)

    @patch("climate.parsers.ClimateDataParser.filter_data_lines")
    def test_parse_data_empty_input(self, mock_filter_data_lines: Mock) -> None:
        """Test parsing with empty input"""

        # Test with empty input
        raw_data = ""

        # Mock filter_data_lines to return an empty list
        mock_filter_data_lines.return_value = []

        # Call the method
        parsed_data = ClimateDataParser.parse_data(raw_data)

        # Assertions
        self.assertEqual(parsed_data, [])

    @patch("climate.parsers.ClimateDataParser.filter_data_lines")
    @patch("climate.parsers.ClimateDataParser.process_line")
    def test_parse_data_single_line(
        self,
        mock_process_line: Mock,
        mock_filter_data_lines: Mock,
    ) -> None:
        """Test parsing with a single valid line"""

        # Test with a single valid line
        raw_data = "2020 1.0 2.0 3.0 4.0"

        # Mock filter_data_lines to return the single line
        mock_filter_data_lines.return_value = ["2020 1.0 2.0 3.0 4.0"]

        # Mock process_line to return parsed results for the single line
        mock_process_line.side_effect = [(2020, {"jan": 1.0, "feb": 2.0}, {"win": 3.0})]

        # Expected parsed data
        expected_result = [(2020, {"jan": 1.0, "feb": 2.0}, {"win": 3.0})]

        # Call the method
        parsed_data = ClimateDataParser.parse_data(raw_data)

        # Assertions
        self.assertEqual(parsed_data, expected_result)

    @patch("climate.parsers.ClimateDataParser.extract_year")
    @patch("climate.parsers.ClimateDataParser.extract_values")
    @patch("climate.parsers.ClimateDataParser.process_months")
    @patch("climate.parsers.ClimateDataParser.process_seasons")
    def test_process_line_valid(
        self,
        mock_process_seasons: Mock,
        mock_process_months: Mock,
        mock_extract_values: Mock,
        mock_extract_year: Mock,
    ) -> None:
        """Test processing a valid line"""

        # Test valid line
        line = "2020 1.0 2.0 3.0 4.0"

        # Mocking the helper methods
        mock_extract_year.return_value = 2020
        mock_extract_values.return_value = [1.0, 2.0, 3.0, 4.0]
        mock_process_months.return_value = {"jan": 1.0, "feb": 2.0}
        mock_process_seasons.return_value = {"win": 3.0}

        # Expected result (a tuple of year, month values, and season values)
        expected_result = (2020, {"jan": 1.0, "feb": 2.0}, {"win": 3.0})

        # Call the method
        result = ClimateDataParser.process_line(line)

        # Assertions
        self.assertEqual(result, expected_result)
        mock_extract_year.assert_called_once_with(["2020", "1.0", "2.0", "3.0", "4.0"])
        mock_extract_values.assert_called_once_with(
            ["2020", "1.0", "2.0", "3.0", "4.0"]
        )
        mock_process_months.assert_called_once_with([1.0, 2.0, 3.0, 4.0])
        mock_process_seasons.assert_called_once_with([1.0, 2.0, 3.0, 4.0])

    @patch("climate.parsers.ClimateDataParser.extract_year")
    @patch("climate.parsers.ClimateDataParser.extract_values")
    @patch("climate.parsers.ClimateDataParser.process_months")
    @patch("climate.parsers.ClimateDataParser.process_seasons")
    def test_process_line_invalid(
        self,
        mock_process_seasons: Mock,
        mock_process_months: Mock,
        mock_extract_values: Mock,
        mock_extract_year: Mock,
    ) -> None:
        """Test processing an invalid line"""

        # Test invalid line (missing data, invalid format)
        line = "invalid data"

        # Mocking the helper methods to raise an exception or return unexpected values
        mock_extract_year.side_effect = Exception("Invalid year format")
        mock_extract_values.return_value = []

        # Call the method
        result = ClimateDataParser.process_line(line)

        # Assertions
        self.assertIsNone(result)  # Return None on error
        mock_extract_year.assert_called_once_with(["invalid", "data"])
        mock_process_months.assert_not_called()
        mock_process_seasons.assert_not_called()

    @patch("climate.parsers.ClimateDataParser.extract_year")
    @patch("climate.parsers.ClimateDataParser.extract_values")
    @patch("climate.parsers.ClimateDataParser.process_months")
    @patch("climate.parsers.ClimateDataParser.process_seasons")
    def test_process_line_partial_data(
        self,
        mock_process_seasons: Mock,
        mock_process_months: Mock,
        mock_extract_values: Mock,
        mock_extract_year: Mock,
    ):
        """Test processing a line with partial data"""

        # Test partial data in line (e.g., missing some values)
        line = "2020 1.0 2.0"

        # Mocking the helper methods
        mock_extract_year.return_value = 2020
        mock_extract_values.return_value = [1.0, 2.0]
        mock_process_months.return_value = {"jan": 1.0}
        mock_process_seasons.return_value = {}

        # Expected result
        expected_result = (2020, {"jan": 1.0}, {})

        # Call the method
        result = ClimateDataParser.process_line(line)

        # Assertions
        self.assertEqual(result, expected_result)
        mock_extract_year.assert_called_once_with(["2020", "1.0", "2.0"])
        mock_extract_values.assert_called_once_with(["2020", "1.0", "2.0"])
        mock_process_months.assert_called_once_with([1.0, 2.0])
        mock_process_seasons.assert_called_once_with([1.0, 2.0])


class TestClimateDataProcessor(unittest.TestCase):
    """Tests for ClimateDataProcessor"""

    def setUp(self):
        self.region = "UK"
        self.dataset = "Rainfall"
        self.processor = ClimateDataProcessor(region=self.region, dataset=self.dataset)

    @patch("climate.models.ClimateRegion.objects.get_or_create")
    @patch("climate.models.ClimateParameter.objects.get_or_create")
    def test_ensure_region_and_parameter_exist(
        self,
        mock_get_param: MagicMock,
        mock_get_region: MagicMock,
    ) -> None:
        """Test ensuring region and parameter exist"""
        mock_region = MagicMock()
        mock_param = MagicMock()

        mock_get_region.return_value = (mock_region, True)
        mock_get_param.return_value = (mock_param, True)

        self.processor.ensure_region_and_parameter_exist()

        self.assertEqual(self.processor.region_obj, mock_region)
        self.assertEqual(self.processor.parameter_obj, mock_param)
        mock_get_region.assert_called_once_with(region=self.region)
        mock_get_param.assert_called_once_with(parameter=self.dataset)

    @patch("climate.models.ClimateRecord.objects.get_or_create")
    def test_fetch_or_create_record(self, mock_get_record: MagicMock) -> None:
        """Test fetching or creating a ClimateRecord"""

        mock_record = MagicMock()
        self.processor.region_obj = MagicMock()
        self.processor.parameter_obj = MagicMock()

        mock_get_record.return_value = (mock_record, True)

        result = self.processor.fetch_or_create_record(2020)
        self.assertEqual(result, mock_record)
        mock_get_record.assert_called_once_with(
            region=self.processor.region_obj,
            parameter=self.processor.parameter_obj,
            year=2020,
        )

    @patch("climate.models.ClimateMonthly.objects.update_or_create")
    def test_upsert_monthly_data(self, mock_update: MagicMock) -> None:
        """Test upserting monthly data"""

        mock_record = MagicMock()
        month_values = {"jan": 1.1, "feb": 2.2}

        self.processor.upsert_monthly_data(mock_record, month_values)

        self.assertEqual(mock_update.call_count, 2)

    @patch("climate.models.ClimateSeasonal.objects.update_or_create")
    def test_upsert_seasonal_data(self, mock_update: MagicMock) -> None:
        """Test upserting seasonal data"""

        mock_record = MagicMock()
        season_values = {"win": 3.3, "spr": 4.4}

        self.processor.upsert_seasonal_data(mock_record, season_values)

        self.assertEqual(mock_update.call_count, 2)

    @patch("climate.parsers.scripts.transaction.atomic")
    @patch.object(ClimateDataProcessor, "upsert_seasonal_data")
    @patch.object(ClimateDataProcessor, "upsert_monthly_data")
    @patch.object(ClimateDataProcessor, "fetch_or_create_record")
    def test_update_database(
        self,
        mock_fetch: MagicMock,
        mock_upsert_month: MagicMock,
        mock_upsert_season: MagicMock,
        mock_atomic: MagicMock,
    ) -> None:
        """Test updating the database"""

        mock_record = MagicMock()
        mock_fetch.return_value = mock_record

        self.processor.update_database(2020, {"jan": 1.0}, {"win": 3.0})

        mock_fetch.assert_called_once_with(2020)
        mock_upsert_month.assert_called_once()
        mock_upsert_season.assert_called_once()
        mock_atomic.assert_called_once()

    @patch.object(ClimateDataProcessor, "update_database")
    @patch.object(ClimateDataProcessor, "ensure_region_and_parameter_exist")
    def test_process(self, mock_ensure, mock_update: MagicMock) -> None:
        """Test processing parsed data"""

        parsed_data = [
            (2020, {"jan": 1.0}, {"win": 3.0}),
            (2021, {"jan": 2.0}, {"win": 4.0}),
        ]

        self.processor.process(parsed_data)

        mock_ensure.assert_called_once()
        self.assertEqual(mock_update.call_count, 2)


class TestClimateDataHandler(unittest.TestCase):
    """Tests for ClimateDataHandler"""

    def setUp(self) -> None:
        self.url = "http://fake-url"
        self.region = "UK"
        self.dataset = "Rainfall"
        self.handler = ClimateDataHandler(self.url, self.region, self.dataset)

    def test_init(self) -> None:
        """Test initialization of ClimateDataHandler"""

        self.assertEqual(self.handler.url, self.url)
        self.assertEqual(self.handler.region, self.region)
        self.assertEqual(self.handler.dataset, self.dataset)

    @patch("climate.parsers.ClimateDataFetcher.fetch_data")
    def test_fetch_calls_fetcher(self, mock_fetch_data: Mock) -> None:
        """Test fetch calls ClimateDataFetcher"""

        mock_fetch_data.return_value = "raw data"
        result = self.handler.fetch()
        mock_fetch_data.assert_called_once_with(self.url)
        self.assertEqual(result, "raw data")

    @patch("climate.parsers.ClimateDataParser.parse_data")
    def test_parse_calls_parser(self, mock_parse_data: Mock) -> None:
        """Test parse calls ClimateDataParser"""

        mock_parse_data.return_value = [(2020, {"jan": 1.0}, {"win": 2.0})]
        result = self.handler.parse("raw data")
        mock_parse_data.assert_called_once_with("raw data")
        self.assertEqual(result, [(2020, {"jan": 1.0}, {"win": 2.0})])

    @patch("climate.parsers.scripts.ClimateDataProcessor")
    def test_process_calls_processor_correctly(self, mock_processor_cls: MagicMock) -> None:
        """Test process calls ClimateDataProcessor correctly"""

        mock_processor = MagicMock()
        mock_processor_cls.return_value = mock_processor

        parsed_data = [
            (2020, {"jan": 1.0, "feb": 2.0}, {"win": 3.0}),
            (2021, {"jan": 1.5, "feb": 2.5}, {"win": 3.5}),
        ]

        self.handler.process(parsed_data)

        mock_processor.ensure_region_and_parameter_exist.assert_called_once()
        self.assertEqual(mock_processor.update_database.call_count, 2)
        mock_processor.update_database.assert_any_call(
            2020, {"jan": 1.0, "feb": 2.0}, {"win": 3.0}
        )
        mock_processor.update_database.assert_any_call(
            2021, {"jan": 1.5, "feb": 2.5}, {"win": 3.5}
        )

    @patch.object(ClimateDataHandler, "fetch")
    @patch.object(ClimateDataHandler, "parse")
    @patch.object(ClimateDataHandler, "process")
    def test_fetch_parse_process_success(self, mock_process: Mock, mock_parse: Mock, mock_fetch: Mock) -> None:
        """Test fetch_parse_process success scenario"""

        mock_fetch.return_value = "raw data"
        mock_parse.return_value = [(2020, {"jan": 1.0}, {"win": 2.0})]

        self.handler.fetch_parse_process()

        mock_fetch.assert_called_once()
        mock_parse.assert_called_once_with("raw data")
        mock_process.assert_called_once_with([(2020, {"jan": 1.0}, {"win": 2.0})])

    @patch.object(ClimateDataHandler, "fetch", side_effect=Exception("Fetch failed"))
    @patch("climate.parsers.scripts.logger")
    def test_fetch_parse_process_handles_exception(self, mock_logger: Mock, mock_fetch: Mock) -> None:
        """Test fetch_parse_process handles exceptions"""

        self.handler.fetch_parse_process()
        mock_logger.error.assert_called_once()
        self.assertIn(
            "Error during data fetching, parsing, or processing",
            mock_logger.error.call_args[0][0],
        )
