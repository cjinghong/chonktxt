import anthropic

class ChonktxtClient:
    def __init__(self, anthropic_api_key: str):
        self.anthropic_client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=anthropic_api_key,
        )


    # def get(self, endpoint):
    #     url = f"{self.base_url}/{endpoint}"
    #     headers = {"Authorization": f"Bearer {self.api_key}"}
    #     response = requests.get(url, headers=headers)
    #     return response.json()

    # def post(self, endpoint, data):
    #     url = f"{self.base_url}/{endpoint}"
    #     headers = {"Authorization": f"Bearer {self.api_key}"}
    #     response = requests.post(url, json=data, headers=headers)
    #     return response.json()