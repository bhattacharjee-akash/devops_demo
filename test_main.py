from fastapi.testclient import TestClient
from main import app, get_agent

# 🎭 Fake agent — mimics ChatGroq's .invoke().content
class FakeResult:
    content = "42"

class FakeAgent:
    def invoke(self, question):
        return FakeResult()

# 🔁 Swap the real Groq agent for the fake one
app.dependency_overrides[get_agent] = lambda: FakeAgent()

client = TestClient(app)

# ✅ Happy path: valid request returns a typed answer
def test_ask_returns_answer():
    resp = client.post("/ask", json={"question": "meaning of life?"})
    assert resp.status_code == 200
    assert resp.json() == {"answer": "42"}

# 🚫 Validation: missing field → 422 Unprocessable Entity
def test_ask_requires_question():
    resp = client.post("/ask", json={})
    assert resp.status_code == 422

# 📐 Schema: response always matches AskResponse
def test_response_shape():
    resp = client.post("/ask", json={"question": "hi"})
    assert list(resp.json().keys()) == ["answer"]
