import asyncio
import aiohttp
import time

# Function to read tokens from a file
def read_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

# Function to create headers with the given token
def create_headers(token):
    return {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Content-Type": "application/json",
        "Origin": "https://telegram.blum.codes",
        "X-Requested-With": "org.telegram.messenger",
        "Authorization": f"Bearer {token}",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://telegram.blum.codes/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-US;q=0.9",
    }

# Function to make the POST request
async def make_post_request(session, token):
    url = 'https://game-domain.blum.codes/api/v1/daily-reward?offset=-420'
    headers = create_headers(token)
    
    async with session.post(url, headers=headers) as response:
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            return await response.json()
        else:
            text = await response.text()
            return {'error': 'Unexpected content type', 'content': text}

# Main function to run multiple requests concurrently
async def main(tokens):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for token in tokens:
            # Create 200 tasks for each token
            for _ in range(500):
                tasks.append(make_post_request(session, token))  
        responses = await asyncio.gather(*tasks)  # Run all tasks concurrently
        for response in responses:
            print(response)  # Print each response

if __name__ == "__main__":
    start_time = time.time()
    tokens = read_tokens('token.txt')  # Read tokens from the file
    asyncio.run(main(tokens))
    elapsed_time = time.time() - start_time
    print(f"Completed requests in {elapsed_time:.2f} seconds.")
