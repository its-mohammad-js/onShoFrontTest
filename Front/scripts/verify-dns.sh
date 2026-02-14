#!/bin/bash

# Script to verify DNS configuration for subdomain

echo "=========================================="
echo "  DNS Verification Script"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SUBDOMAIN="kaafel.onsho24.ir"
EXPECTED_IP="62.60.198.169"

echo "Checking DNS for: $SUBDOMAIN"
echo "Expected IP: $EXPECTED_IP"
echo ""

# 1. Check from server
echo "1. DNS Resolution from Server..."
if command -v nslookup &> /dev/null; then
    RESULT=$(nslookup $SUBDOMAIN 2>&1)
    if echo "$RESULT" | grep -q "$EXPECTED_IP"; then
        echo -e "${GREEN}✓${NC} DNS resolves correctly to $EXPECTED_IP"
    elif echo "$RESULT" | grep -q "NXDOMAIN\|Non-existent domain"; then
        echo -e "${RED}✗${NC} DNS record does NOT exist"
        echo "   ${YELLOW}Action: Add A record for $SUBDOMAIN → $EXPECTED_IP${NC}"
    else
        RESOLVED_IP=$(echo "$RESULT" | grep -A 2 "Name:" | grep "Address:" | awk '{print $2}' | head -1)
        if [ -n "$RESOLVED_IP" ]; then
            echo -e "${YELLOW}⚠${NC} DNS resolves to: $RESOLVED_IP (expected: $EXPECTED_IP)"
        else
            echo -e "${RED}✗${NC} Could not resolve DNS"
        fi
    fi
elif command -v dig &> /dev/null; then
    RESOLVED_IP=$(dig +short $SUBDOMAIN 2>/dev/null | head -1)
    if [ -n "$RESOLVED_IP" ]; then
        if [ "$RESOLVED_IP" = "$EXPECTED_IP" ]; then
            echo -e "${GREEN}✓${NC} DNS resolves correctly to $EXPECTED_IP"
        else
            echo -e "${YELLOW}⚠${NC} DNS resolves to: $RESOLVED_IP (expected: $EXPECTED_IP)"
        fi
    else
        echo -e "${RED}✗${NC} DNS record does NOT exist"
        echo "   ${YELLOW}Action: Add A record for $SUBDOMAIN → $EXPECTED_IP${NC}"
    fi
else
    echo "   ${YELLOW}nslookup/dig not available${NC}"
fi
echo ""

# 2. Check using Google DNS
echo "2. DNS Resolution using Google DNS (8.8.8.8)..."
if command -v nslookup &> /dev/null; then
    RESULT=$(nslookup $SUBDOMAIN 8.8.8.8 2>&1)
    if echo "$RESULT" | grep -q "$EXPECTED_IP"; then
        echo -e "${GREEN}✓${NC} Google DNS resolves correctly to $EXPECTED_IP"
    elif echo "$RESULT" | grep -q "NXDOMAIN\|Non-existent domain"; then
        echo -e "${RED}✗${NC} DNS record does NOT exist (checked via Google DNS)"
    else
        RESOLVED_IP=$(echo "$RESULT" | grep -A 2 "Name:" | grep "Address:" | awk '{print $2}' | head -1)
        if [ -n "$RESOLVED_IP" ]; then
            echo -e "${YELLOW}⚠${NC} Google DNS resolves to: $RESOLVED_IP (expected: $EXPECTED_IP)"
        fi
    fi
elif command -v dig &> /dev/null; then
    RESOLVED_IP=$(dig @8.8.8.8 +short $SUBDOMAIN 2>/dev/null | head -1)
    if [ -n "$RESOLVED_IP" ]; then
        if [ "$RESOLVED_IP" = "$EXPECTED_IP" ]; then
            echo -e "${GREEN}✓${NC} Google DNS resolves correctly to $EXPECTED_IP"
        else
            echo -e "${YELLOW}⚠${NC} Google DNS resolves to: $RESOLVED_IP (expected: $EXPECTED_IP)"
        fi
    else
        echo -e "${RED}✗${NC} DNS record does NOT exist (checked via Google DNS)"
    fi
fi
echo ""

# 3. Check wildcard DNS
echo "3. Checking Wildcard DNS (*.onsho24.ir)..."
WILDCARD_TEST="test-$(date +%s).onsho24.ir"
if command -v dig &> /dev/null; then
    WILDCARD_IP=$(dig +short $WILDCARD_TEST 2>/dev/null | head -1)
    if [ -n "$WILDCARD_IP" ]; then
        if [ "$WILDCARD_IP" = "$EXPECTED_IP" ]; then
            echo -e "${GREEN}✓${NC} Wildcard DNS is configured correctly"
        else
            echo -e "${YELLOW}⚠${NC} Wildcard DNS resolves to: $WILDCARD_IP (expected: $EXPECTED_IP)"
        fi
    else
        echo -e "${YELLOW}⚠${NC} Wildcard DNS might not be configured"
        echo "   ${YELLOW}Note: This is OK if you're using specific subdomain records${NC}"
    fi
else
    echo "   ${YELLOW}dig not available for wildcard test${NC}"
fi
echo ""

# 4. Instructions
echo "=========================================="
echo "  DNS Setup Instructions"
echo "=========================================="
echo ""
echo "To fix DNS, add an A record in your DNS provider:"
echo ""
echo "  Type: A"
echo "  Name: kaafel (or * for wildcard)"
echo "  Value: $EXPECTED_IP"
echo "  TTL: 3600 (or default)"
echo ""
echo "After adding the record:"
echo "  1. Wait 5-30 minutes for DNS propagation"
echo "  2. Test from your local machine:"
echo "     ${YELLOW}nslookup kaafel.onsho24.ir${NC}"
echo "  3. It should return: $EXPECTED_IP"
echo "  4. Then test in browser: https://kaafel.onsho24.ir"
echo ""
echo "See docs/DNS_SETUP_GUIDE.md for detailed instructions"
echo ""


