from mcp.server.fastmcp import FastMCP
from langchain_community.vectorstores import FAISS
import os
from openai import AzureOpenAI
from langchain_core.embeddings import Embeddings
from dotenv import load_dotenv
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

# Initialize FastMCP server
mcp = FastMCP("rag")
load_dotenv()
# 嵌入模型配置
endpoint = "https://20242-m9bfmsab-eastus2.cognitiveservices.azure.com/"
model_name = "text-embedding-3-small"
deployment = "text-embedding-3-small"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=os.getenv("API_KEY"),
)


# 自定义嵌入类
class CustomAzureOpenAIEmbeddings(Embeddings):
    def __init__(self, client, deployment):
        self.client = client
        self.deployment = deployment

    def embed_documents(self, texts):
        response = self.client.embeddings.create(
            input=texts,
            model=self.deployment
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text):
        return self.embed_documents([text])[0]


# 初始化嵌入模型
embedding_model = CustomAzureOpenAIEmbeddings(client, deployment)

@mcp.tool()
async def retrieve(query: str) -> str:
    """Use this tool when the user asks about python.
    Retrieve the most relevant documents from the python learning textbook.

    Args:
        query: The user's input query
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    faiss_path = os.path.join(base_dir, "text_index")
    vectorstore = FAISS.load_local(faiss_path, embedding_model, allow_dangerous_deserialization=True)
    docs = vectorstore.similarity_search(query, k=3)
    text = "\n\n".join([doc.page_content if doc.page_content is not None else "" for doc in docs])
    context = []
    context.append(text)
    return "\n---\n".join(context)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')