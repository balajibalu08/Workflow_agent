import httpx
from a2a.client import A2ACardResolver, ClientConfig, create_client
import asyncio
from a2a.types import Role, SendMessageRequest
from a2a.helpers import new_text_message
from src.models.route_decision_models import RouteDecision
async def get_card():
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url="http://127.0.0.1:9999",
        )
        public_agent_card = await resolver.get_agent_card()
        return public_agent_card


async def main():
    # Run the async main and obtain the result
    card = await get_card()
    # optionally print or use the card
    print(card)
    config = ClientConfig(streaming=False)
    client = await create_client(
        agent=card, client_config=config
    )
    query = input("Enter Your Query: ").strip()
    message = new_text_message(text=query, role= Role.ROLE_USER)
    request = SendMessageRequest(message=message)
    async for response in client.send_message(request=request):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
