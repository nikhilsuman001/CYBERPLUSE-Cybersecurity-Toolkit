"""
API Tester Module
Enables sending HTTP GET and POST requests, inspecting headers, measuring response latency,
and displaying formatted JSON responses.
"""

import time
import json
import requests


# Parent Base Class
class BaseTool:
    def __init__(self, name="API Tester"):
        self.name = name
        self._status = "Ready"

    def get_status(self):
        return self._status


# Child Class (Inheritance & Encapsulation)
class APITester(BaseTool):
    def __init__(self):
        super().__init__("REST API Tester")

    def send_request(self, url, method="GET", headers=None, body=None, timeout=10):
        """
        Send an HTTP request and parse response details.
        Returns a dictionary with status, latency, headers, and parsed data.
        """
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        method = method.upper().strip()
        req_headers = {"User-Agent": "CyberPulse-APITester/1.0"}
        if headers:
            if isinstance(headers, dict):
                req_headers.update(headers)
            elif isinstance(headers, str):
                try:
                    parsed_h = json.loads(headers)
                    if isinstance(parsed_h, dict):
                        req_headers.update(parsed_h)
                except Exception:
                    pass

        start_time = time.time()
        try:
            if method == "POST":
                # Handle JSON or string body
                json_payload = None
                data_payload = None
                if body:
                    if isinstance(body, dict):
                        json_payload = body
                    elif isinstance(body, str):
                        try:
                            json_payload = json.loads(body)
                        except Exception:
                            data_payload = body

                resp = requests.post(
                    url,
                    json=json_payload,
                    data=data_payload,
                    headers=req_headers,
                    timeout=timeout
                )
            else:
                resp = requests.get(url, headers=req_headers, timeout=timeout)

            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            self._status = f"Completed ({resp.status_code})"

            # Try to decode JSON
            is_json = False
            json_data = None
            try:
                json_data = resp.json()
                is_json = True
            except Exception:
                json_data = None

            return {
                "success": True,
                "url": url,
                "method": method,
                "status_code": resp.status_code,
                "status_reason": resp.reason,
                "elapsed_ms": elapsed_ms,
                "headers": dict(resp.headers),
                "is_json": is_json,
                "json_data": json_data,
                "text": resp.text[:10000] if not is_json else json.dumps(json_data, indent=2),
                "error": None
            }

        except requests.exceptions.Timeout:
            self._status = "Request Timed Out"
            return {
                "success": False,
                "url": url,
                "method": method,
                "status_code": None,
                "error": f"Request to {url} timed out after {timeout} seconds."
            }
        except Exception as e:
            self._status = f"Error: {e}"
            return {
                "success": False,
                "url": url,
                "method": method,
                "status_code": None,
                "error": str(e)
            }


def main():
    print("=" * 50)
    print("🌐 REST API TESTER")
    print("=" * 50)
    tester = APITester()

    url = input("Enter API URL (e.g., https://jsonplaceholder.typicode.com/posts/1): ").strip()
    if not url:
        url = "https://jsonplaceholder.typicode.com/posts/1"

    method = input("Method (GET/POST) [Default: GET]: ").strip().upper() or "GET"
    body = None
    if method == "POST":
        body = input("Enter JSON payload (optional): ").strip()

    print(f"\nSending {method} request to {url}...")
    res = tester.send_request(url, method=method, body=body)

    if res.get("success"):
        print(f"Status: {res['status_code']} {res['status_reason']}")
        print(f"Latency: {res['elapsed_ms']} ms")
        print("\nResponse Body:")
        print(res["text"])
    else:
        print(f"Failed: {res.get('error')}")


if __name__ == "__main__":
    main()
