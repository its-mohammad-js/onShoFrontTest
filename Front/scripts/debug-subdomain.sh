#!/bin/bash

# Script برای عیب‌یابی مشکل Subdomain Connection Closed

echo "=========================================="
echo "  Subdomain Debugging Script"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

# 1. Check Nuxt App
echo "1. Checking Nuxt App Status..."
if netstat -tlnp 2>/dev/null | grep -q ":3000" || ss -tlnp 2>/dev/null | grep -q ":3000"; then
    print_status 0 "Nuxt is running on port 3000"
    PROCESS=$(netstat -tlnp 2>/dev/null | grep ":3000" | awk '{print $7}' | cut -d'/' -f2 | head -1)
    echo "   Process: $PROCESS"
else
    print_status 1 "Nuxt is NOT running on port 3000"
    echo "   ${YELLOW}Action: Start Nuxt app${NC}"
fi
echo ""

# 2. Check Nginx
echo "2. Checking Nginx Status..."
if systemctl is-active --quiet nginx 2>/dev/null; then
    print_status 0 "Nginx is running"
else
    print_status 1 "Nginx is NOT running"
    echo "   ${YELLOW}Action: sudo systemctl start nginx${NC}"
fi
echo ""

# 3. Test Nginx Configuration
echo "3. Testing Nginx Configuration..."
if sudo nginx -t 2>&1 | grep -q "syntax is ok"; then
    print_status 0 "Nginx configuration is valid"
else
    print_status 1 "Nginx configuration has errors"
    echo "   ${YELLOW}Errors:${NC}"
    sudo nginx -t 2>&1 | grep -i error
fi
echo ""

# 4. Check SSL Certificate
echo "4. Checking SSL Certificate..."
if sudo certbot certificates 2>/dev/null | grep -q "onsho24.ir"; then
    print_status 0 "SSL certificate found"
    CERT_INFO=$(sudo certbot certificates 2>/dev/null | grep -A 3 "onsho24.ir" | head -4)
    echo "$CERT_INFO" | while IFS= read -r line; do
        echo "   $line"
    done
else
    print_status 1 "SSL certificate not found or expired"
    echo "   ${YELLOW}Action: sudo certbot renew${NC}"
fi
echo ""

# 5. Test Local Connection to Nuxt
echo "5. Testing Local Connection to Nuxt..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1:3000 2>/dev/null)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
    print_status 0 "Nuxt responds on localhost (HTTP $HTTP_CODE)"
else
    print_status 1 "Nuxt does NOT respond on localhost (HTTP $HTTP_CODE)"
fi
echo ""

# 6. Check Firewall
echo "6. Checking Firewall..."
if command -v ufw &> /dev/null; then
    if sudo ufw status | grep -q "443/tcp.*ALLOW"; then
        print_status 0 "Port 443 is open in UFW"
    else
        print_status 1 "Port 443 might be closed in UFW"
        echo "   ${YELLOW}Action: sudo ufw allow 443/tcp${NC}"
    fi
elif command -v firewall-cmd &> /dev/null; then
    if sudo firewall-cmd --list-ports 2>/dev/null | grep -q "443"; then
        print_status 0 "Port 443 is open in firewalld"
    else
        print_status 1 "Port 443 might be closed in firewalld"
        echo "   ${YELLOW}Action: sudo firewall-cmd --add-port=443/tcp --permanent${NC}"
    fi
else
    echo "   ${YELLOW}Firewall tool not found, please check manually${NC}"
fi
echo ""

# 7. Check Recent Nginx Errors
echo "7. Recent Nginx Errors (last 10 lines)..."
if [ -f /var/log/nginx/error.log ]; then
    RECENT_ERRORS=$(sudo tail -n 10 /var/log/nginx/error.log 2>/dev/null)
    if [ -z "$RECENT_ERRORS" ]; then
        echo "   No recent errors"
    else
        echo "$RECENT_ERRORS" | while IFS= read -r line; do
            echo "   $line"
        done
    fi
else
    echo "   ${YELLOW}Error log file not found${NC}"
fi
echo ""

# 8. Check PM2 (if installed)
echo "8. Checking PM2..."
if command -v pm2 &> /dev/null; then
    if pm2 list | grep -q "nuxt"; then
        print_status 0 "PM2 is managing Nuxt process"
        echo "   PM2 Status:"
        pm2 list | grep nuxt
    else
        echo "   ${YELLOW}PM2 is installed but not managing Nuxt${NC}"
    fi
else
    echo "   PM2 not installed (optional)"
fi
echo ""

# 9. Test Subdomain from Server
echo "9. Testing Subdomain from Server..."
SUBDOMAIN="kaafel.onsho24.ir"
HTTP_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" --max-time 10 "https://$SUBDOMAIN" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
    print_status 0 "Subdomain responds from server (HTTP $HTTP_CODE)"
else
    print_status 1 "Subdomain does NOT respond from server (HTTP $HTTP_CODE)"
    echo "   ${YELLOW}Trying with verbose output...${NC}"
    curl -k -v "https://$SUBDOMAIN" 2>&1 | head -20
fi
echo ""

# 10. Check Disk Space
echo "10. Checking Disk Space..."
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 90 ]; then
    print_status 0 "Disk space is OK (${DISK_USAGE}% used)"
else
    print_status 1 "Disk space is low (${DISK_USAGE}% used)"
    echo "   ${YELLOW}Action: Free up disk space${NC}"
fi
echo ""

# 11. Check Memory
echo "11. Checking Memory..."
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -lt 90 ]; then
    print_status 0 "Memory usage is OK (${MEM_USAGE}% used)"
else
    print_status 1 "Memory usage is high (${MEM_USAGE}% used)"
    echo "   ${YELLOW}Action: Check for memory leaks${NC}"
fi
echo ""

echo "=========================================="
echo "  Debugging Complete"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. If Nuxt is not running, start it:"
echo "   cd /path/to/front-end && npm run start"
echo ""
echo "2. Check Nginx logs in real-time:"
echo "   sudo tail -f /var/log/nginx/error.log"
echo ""
echo "3. Test subdomain:"
echo "   curl -k -I https://kaafel.onsho24.ir"
echo ""


