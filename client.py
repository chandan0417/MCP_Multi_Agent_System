from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio
import os

# Load environment variables
load_dotenv()

# Initialize MCP Client with multiple servers
client = MultiServerMCPClient(
    {
        "web_search": {
            "command": "python",
            "args": ["websearch_server.py"],
            "transport": "stdio"
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http"
        },
        "papers": {
            "command": "python",
            "args": ["papers_server.py"],
            "transport": "stdio"
        }
    }
)

async def main():
    # Get tools from MCP servers
    tools = await client.get_tools()
    
    # Initialize the language model
    model = ChatGroq(
        model="qwen-qwq-32b",
        temperature=0.7
    )
    
    # Create the agent
    agent = create_react_agent(model, tools)
    
    print("Welcome to the MCP Agent")
    print("Available tools: Web Search, Weather, Research Papers")
    print("Type 'exit' to quit.")
    
    while True:
        try:
            user_input = input("\nWhat would you like to know? ")
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            print("\nProcessing your request...")
            
            # Process the input with the agent
            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]}
            )
            
            print("\n" + "="*80)
            
            # Extract messages from response
            if isinstance(response, dict) and 'messages' in response:
                messages = response['messages']
                
                # Find the final AI response (last message in the list)
                final_response = next((msg for msg in reversed(messages) if msg.type == 'ai'), None)
                
                # Find tool calls and their results
                tool_calls = []
                tool_results = []
                
                for msg in messages:
                    if hasattr(msg, 'additional_kwargs') and 'tool_calls' in msg.additional_kwargs:
                        for tool_call in msg.additional_kwargs['tool_calls']:
                            tool_name = tool_call['function']['name']
                            tool_args = tool_call['function']['arguments']
                            tool_calls.append(f"{tool_name}({tool_args})")
                    
                    if msg.type == 'tool':
                        tool_results.append({
                            'tool': msg.name,
                            'content': msg.content[:500] + '...' if len(msg.content) > 500 else msg.content
                        })
                
                # Print tool calls if any
                if tool_calls:
                    print("\n Tools called:")
                    for i, call in enumerate(tool_calls, 1):
                        print(f"  {i}. {call}")
                
                # Print tool results if any
                if tool_results:
                    print("\n =>Tool results:")
                    for i, result in enumerate(tool_results, 1):
                        print(f"\n  Tool {i}: {result['tool']}")
                        print("  " + "-" * 40)
                        print(f"  {result['content']}")
                
                # Print final response
                if final_response and final_response.content:
                    print("\n =>Response:")
                    print(final_response.content)
                
                # Print token usage if available
                if hasattr(final_response, 'response_metadata') and 'token_usage' in final_response.response_metadata:
                    usage = final_response.response_metadata['token_usage']
                    print(f"\n =>Tokens used: {usage.get('total_tokens', 'N/A')} (Input: {usage.get('prompt_tokens', 'N/A')}, Output: {usage.get('completion_tokens', 'N/A')})")
            else:
                print("Unexpected response format. Raw response:")
                print(response)
            
            print("="*80)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again or type 'exit' to quit.")

asyncio.run(main())
