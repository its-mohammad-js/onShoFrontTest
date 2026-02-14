#!/bin/bash

# Script to fix common subdomain issues

echo "=========================================="
echo "  Fixing Subdomain Issues"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Fix Firewall
echo "1. Opening port 443 in UFW..."
if sudo ufw allow 443/tcp; then
    echo -e "${GREEN}✓${NC} Port 443 opened in UFW"
else
    echo -e "${RED}✗${NC} Failed to open port 443"
fi
echo ""

# 2. Reload Nginx
echo "2. Reloading Nginx..."
if sudo systemctl reload nginx; then
    echo -e "${GREEN}✓${NC} Nginx reloaded"
else
    echo -e "${RED}✗${NC} Failed to reload Nginx"
fi
echo ""

# 3. Test with Host header (proper way to test from server)
echo "3. Testing subdomain with Host header..."
SUBDOMAIN="kaafel.onsho24.ir"
HTTP_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" --max-time 10 \
    -H "Host: $SUBDOMAIN" \
    https://127.0.0.1 2>/dev/null)

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
    echo -e "${GREEN}✓${NC} Subdomain responds correctly (HTTP $HTTP_CODE)"
    echo "   This means Nginx is configured correctly!"
else
    echo -e "${YELLOW}⚠${NC} Subdomain returned HTTP $HTTP_CODE"
    echo "   Testing with verbose output..."
    curl -k -v -H "Host: $SUBDOMAIN" https://127.0.0.1 2>&1 | head -30
fi
echo ""

# 4. Check UFW status
echo "4. Current UFW Status..."
sudo ufw status | head -20
echo ""

# 5. Check if port 443 is listening
echo "5. Checking if port 443 is listening..."
if sudo netstat -tlnp | grep -q ":443" || sudo ss -tlnp | grep -q ":443"; then
    echo -e "${GREEN}✓${NC} Port 443 is listening"
    sudo netstat -tlnp | grep ":443" || sudo ss -tlnp | grep ":443"
else
    echo -e "${RED}✗${NC} Port 443 is NOT listening"
    echo "   ${YELLOW}This is a problem! Nginx should be listening on 443${NC}"
fi
echo ""

# 6. Check DNS (from external perspective)
echo "6. Checking DNS Resolution (external)..."
echo "   Note: This requires external DNS to be configured"
echo "   Run this from your local machine or use online DNS checker:"
echo "   ${YELLOW}nslookup kaafel.onsho24.ir${NC}"
echo "   ${YELLOW}dig kaafel.onsho24.ir${NC}"
echo ""

# 7. Show Nginx access logs for subdomain
echo "7. Recent Nginx Access Logs (last 5 lines)..."
if [ -f /var/log/nginx/access.log ]; then
    sudo tail -n 5 /var/log/nginx/access.log | grep -i "kaafel\|subdomain" || echo "   No subdomain requests in recent logs"
else
    echo "   Access log not found"
fi
echo ""

echo "=========================================="
echo "  Fix Complete"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Test from external browser: https://kaafel.onsho24.ir"
echo "2. Check DNS is pointing to this server:"
echo "   - kaafel.onsho24.ir should resolve to your server IP"
echo "   - Use: nslookup kaafel.onsho24.ir (from your local machine)"
echo "3. If DNS is correct but still not working, check:"
echo "   sudo tail -f /var/log/nginx/error.log"
echo ""


