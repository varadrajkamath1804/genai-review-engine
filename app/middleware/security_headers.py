from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response


#     Header	Purpose
# X-Content-Type-Options		Tells the browser not to try to "guess" a different content type than what's declared in Content-Type. Prevents MIME-sniffing attacks (e.g., a browser deciding to execute a file as JS/HTML when it's actually meant to be plain text).
# X-Frame-Options		Prevents your site from being loaded inside an <iframe> on any site (including your own). Protects against clickjacking, where an attacker overlays your page in a hidden iframe to trick users into clicking something.
# Referrer-Policy		Controls how much of the URL is sent in the Referer header when a user navigates away from your site. This setting sends the full URL for same-origin requests, but only the origin (no path/query) for cross-origin requests — avoiding leaking sensitive URL data to third parties.
# X-XSS-Protection 	Legacy header that told older browsers (old Chrome/IE) to block a page if it detected a reflected XSS attack.
