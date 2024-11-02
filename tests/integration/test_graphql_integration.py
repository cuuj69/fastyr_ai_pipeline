import pytest
from fastapi.testclient import TestClient
from fastyr.api.main import app

@pytest.mark.integration
class TestGraphQLIntegration:
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient):
        self.client = client
        
    async def test_query_get_process(self):
        # Arrange
        query = """
        query GetProcess($id: Int!) {
            getProcess(id: $id) {
                id
                status
                audioUrl
                createdAt
            }
        }
        """
        variables = {"id": 1}
        
        # Act
        response = self.client.post(
            "/graphql",
            json={"query": query, "variables": variables},
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "getProcess" in data["data"]
        
    async def test_mutation_process_audio(self):
        # Arrange
        mutation = """
        mutation ProcessAudio($file: Upload!) {
            processAudio(file: $file) {
                id
                status
                audioUrl
            }
        }
        """
        # Act & Assert implementation 