import rest_framework.test    as rf_test
import rest_framework.status  as status
import rest_framework.reverse as reverse


class SchemaTest(rf_test.APITestCase):
    def test_schema_exists(self):
        """
        Ensure that we can access the API schema. The schema call should return HTTP_200_OK.
        """
        url = reverse.reverse('schema')
        data = {}
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

