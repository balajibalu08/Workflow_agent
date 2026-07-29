from agent_framework import (
    AgentExecutorResponse,
    Executor,
    WorkflowContext,
    handler,
)
import httpx
import aiofiles
import uuid
import os

from websockets import route
from src.utils.logs import logger

# 4. Small helper isolated outside the class for clean logic
def is_pdf(content: bytes) -> bool:
    return content.startswith(b'%PDF')

class PDFDownloadExecutor(Executor):
    def __init__(self):
        super().__init__(id="pdf_downloader")
        self.download_dir = os.path.join(".", "downloads")
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Define strict bounds for file processing
        self.min_size_bytes = 100                 # 5. Reject empty or tiny error files
        self.max_size_bytes = 50 * 1024 * 1024    # 6. Reject anything over 50MB

    @handler
    # 3. Type annotations added for better developer experience
    async def download_pdf(self, response: AgentExecutorResponse, context: WorkflowContext[str]):
        route = response.output   # or the correct property if your framework differs
        url = route.source_value

        # 7. URL Validation: First line of defense
        if not url.startswith(("http://", "https://")):
            logger.error(f"Invalid URL scheme provided: {url}")
            raise ValueError(f"URL must start with http:// or https://. Received: {url}")

        filename = f"resume_{uuid.uuid4().hex}.pdf"
        output_path = os.path.join(self.download_dir, filename)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                
                # OPTIONAL: Check headers first to prevent downloading a massive 20GB file
                head_response = await client.head(url)
                content_length = head_response.headers.get("Content-Length")
                if content_length and int(content_length) > self.max_size_bytes:
                    raise ValueError(f"Reported file size ({content_length} bytes) exceeds {self.max_size_bytes} byte limit.")

                # Proceed with actual download
                response = await client.get(url,follow_redirects=True)
                response.raise_for_status() 
                
            # Content-Type header check
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/pdf" not in content_type:
                logger.warning(f"Unexpected Content-Type header: '{content_type}' for URL: {url}")

            # 5 & 6. Size validations on the actual downloaded payload
            payload_size = len(response.content)
            if payload_size < self.min_size_bytes:
                raise ValueError(f"File too small ({payload_size} bytes). Likely a disguised error page.")
            if payload_size > self.max_size_bytes:
                raise ValueError(f"Downloaded file ({payload_size} bytes) exceeds {self.max_size_bytes} byte limit.")

            # 4. Binary signature validation using our helper
            if not is_pdf(response.content):
                raise ValueError("Validation failed: Downloaded binary stream does not start with %PDF signature.")

            # Save the file asynchronously
            async with aiofiles.open(output_path, 'wb') as file:
                await file.write(response.content)
            
            logger.info(f"PDF verified and downloaded successfully to: {output_path}")
            
            # Send ONLY the path to the downstream executor
            await context.send_message(output_path)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error {e.response.status_code} while downloading from {url}")
            # 1 & 2. Fail naturally and preserve the traceback
            raise
            
        except httpx.RequestError as e:
            logger.error(f"Network transfer or connectivity failure: {str(e)}")
            raise
            
        except Exception as e:
            logger.error(f"Unexpected failure in PDFDownloadExecutor: {str(e)}")
            raise