import requests
from bs4 import BeautifulSoup

class WebScrapingPlugin:
    def __init__(self):
        pass

    def get_spec(self):
        return [
            {
                "name": "fetch_webpage_content",
                "description": "Fetch the textual content of a webpage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL of the webpage to fetch content from"
                        }
                    },
                    "required": ["url"]
                }
            }
        ]

    def fetch_webpage_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        else:
            raise Exception(f"Failed to fetch the webpage: {response.status_code}")

    async def execute(self, function_name, helper, **kwargs):
        if function_name == "fetch_webpage_content":
            url = kwargs.get("url")
            content = self.fetch_webpage_content(url)
            return {"content": content.strip()}

        else:
            return {"error": f"Function {function_name} not found"}

    def get_source_name(self):
        return "WebScrapingPlugin"
