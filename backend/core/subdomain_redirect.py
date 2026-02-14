from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

try:
    from companies.models import Company
    COMPANY_MODEL_AVAILABLE = True
except ImportError:
    COMPANY_MODEL_AVAILABLE = False
    Company = None

class SubdomainRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not COMPANY_MODEL_AVAILABLE:
            return None
            
        subdomain = request.headers.get("X-Subdomain")

        if not subdomain:
            return None

        # ignore www / api / admin etc
        if subdomain in ["www", "api", "admin"]:
            return None

        try:
            company = Company.objects.get(subdomain=subdomain)
        except Company.DoesNotExist:
            return None

        return redirect(
            f"https://onsho24.ir/company/{company.slug}",
            permanent=True
        )

