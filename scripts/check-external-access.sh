#!/bin/bash

# Script to check external access issues

echo "=========================================="
echo "  Checking External Access Issues"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Get Server IP
echo "1. Server IP Addresses..."
echo "   Public IP (if available):"
curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || echo "   Could not determine public IP"
echo ""
echo "   All IP addresses:"
ip addr show | grep "inet " | awk '{print "   " $2}'
echo ""

# 2. Check iptables (if UFW is inactive, might be using iptables)
echo "2. Checking iptables rules..."
if command -v iptables &> /dev/null; then
    echo "   Current iptables rules for port 443:"
    sudo iptables -L -n | grep -E "443|ACCEPT|REJECT|DROP" | head -10 || echo "   No specific rules found"
    echo ""
    echo "   INPUT chain:"
    sudo iptables -L INPUT -n -v | head -10
else
    echo "   iptables not found"
fi
echo ""

# 3. Check if port 443 is accessible from outside
echo "3. Testing port 443 accessibility..."
echo "   ${YELLOW}Note: This requires external access${NC}"
echo "   You can test from your local machine with:"
echo "   ${YELLOW}telnet YOUR_SERVER_IP 443${NC}"
echo "   or"
echo "   ${YELLOW}nc -zv YOUR_SERVER_IP 443${NC}"
echo ""

# 4. Check cloud firewall (if applicable)
echo "4. Cloud Firewall Check..."
echo "   ${YELLOW}If you're using a cloud provider (AWS, DigitalOcean, etc.),${NC}"
echo "   ${YELLOW}check their firewall/security group settings:${NC}"
echo "   - AWS: Security Groups"
echo "   - DigitalOcean: Cloud Firewalls"
echo "   - Google Cloud: Firewall Rules"
echo "   - Azure: Network Security Groups"
echo "   Make sure port 443 (HTTPS) is open for inbound traffic"
echo ""

# 5. Check DNS from server's perspective
echo "5. Checking DNS from server..."
SUBDOMAIN="kaafel.onsho24.ir"
echo "   Testing DNS resolution for $SUBDOMAIN:"
if command -v nslookup &> /dev/null; then
    nslookup $SUBDOMAIN 2>/dev/null | head -10 || echo "   DNS resolution failed"
elif command -v dig &> /dev/null; then
    dig $SUBDOMAIN +short 2>/dev/null || echo "   DNS resolution failed"
else
    echo "   nslookup/dig not available"
fi
echo ""

# 6. Check Nginx server blocks
echo "6. Checking Nginx server blocks for subdomain..."
if [ -f /etc/nginx/sites-available/onsho24 ]; then
    echo "   Server blocks matching '*.onsho24.ir':"
    grep -A 5 "server_name.*onsho24.ir" /etc/nginx/sites-available/onsho24 | head -20
else
    echo "   Nginx config file not found at /etc/nginx/sites-available/onsho24"
    echo "   Checking other locations..."
    sudo find /etc/nginx -name "*.conf" -exec grep -l "onsho24.ir" {} \; 2>/dev/null | head -5
fi
echo ""

# 7. Test SSL certificate for subdomain
echo "7. Testing SSL certificate for subdomain..."
echo "   Testing with openssl:"
echo | openssl s_client -connect 127.0.0.1:443 -servername kaafel.onsho24.ir 2>/dev/null | \
    grep -E "subject=|issuer=|Verify return code" | head -3 || \
    echo "   Could not test SSL (openssl might not be available)"
echo ""

# 8. Check if server is behind NAT/proxy
echo "8. Network Configuration..."
echo "   Checking if server is behind NAT or proxy..."
if [ -f /etc/cloud/cloud.cfg ]; then
    echo "   ${YELLOW}Cloud-init detected - might be cloud instance${NC}"
fi

# Check for proxy settings
if [ -n "$HTTP_PROXY" ] || [ -n "$HTTPS_PROXY" ]; then
    echo "   ${YELLOW}Proxy environment variables detected${NC}"
    [ -n "$HTTP_PROXY" ] && echo "   HTTP_PROXY: $HTTP_PROXY"
    [ -n "$HTTPS_PROXY" ] && echo "   HTTPS_PROXY: $HTTPS_PROXY"
else
    echo "   No proxy detected"
fi
echo ""

# 9. Show recent connection attempts
echo "9. Recent Connection Attempts..."
if [ -f /var/log/nginx/access.log ]; then
    echo "   Last 10 access log entries:"
    sudo tail -n 10 /var/log/nginx/access.log | awk '{print "   " $0}'
else
    echo "   Access log not found"
fi
echo ""

echo "=========================================="
echo "  Diagnostic Complete"
echo "=========================================="
echo ""
echo "Most Likely Issues:"
echo "1. ${YELLOW}DNS not configured${NC} - kaafel.onsho24.ir doesn't resolve to your server IP"
echo "2. ${YELLOW}Cloud firewall blocking${NC} - Check your cloud provider's firewall rules"
echo "3. ${YELLOW}iptables blocking${NC} - Even though UFW is inactive, iptables might have rules"
echo ""
echo "Next Steps:"
echo "1. From your local machine, check DNS:"
echo "   ${YELLOW}nslookup kaafel.onsho24.ir${NC}"
echo "   It should return your server's IP address"
echo ""
echo "2. Check your cloud provider's firewall/security groups"
echo ""
echo "3. Test port 443 from external:"
echo "   ${YELLOW}telnet YOUR_SERVER_IP 443${NC}"
echo ""


