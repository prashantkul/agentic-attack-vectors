#!/usr/bin/env python3
"""
Tool Misuse Attacks - System-Level Security Testing

Tests exploitation of AI agent tools beyond their intended scope to identify
security vulnerabilities in tool implementations and access controls.

Attack Categories:
1. Path Traversal Attacks - Using FileSystemTool to access unauthorized files
2. SQL Injection Attacks - Exploiting DatabaseQueryTool with malicious queries  
3. Input Validation Bypass - Crafting malicious inputs for all tools
4. Data Exfiltration - Using legitimate tools to extract sensitive information
5. Privilege Escalation - Attempting to gain unauthorized system access

IMPORTANT: This is for defensive security testing only.
"""

import asyncio
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from travel_advisor.tools import (
    weather_lookup, flight_search, hotel_search, 
    currency_converter, file_system_tool, database_query_tool
)

# Load environment variables
load_dotenv()

class ToolMisuseAttackTester:
    """Test tool misuse attacks across all travel advisor tools."""
    
    def __init__(self):
        self.results = []
        
    async def test_all_tool_misuse_attacks(self):
        """Test all categories of tool misuse attacks."""
        print("🔥 TOOL MISUSE ATTACKS - SYSTEM-LEVEL SECURITY TESTING")
        print("=" * 65)
        print("⚠️  Testing exploitation of AI agent tools beyond intended scope")
        print("🎯 Target: Travel advisor tools with intentional vulnerabilities")
        print()
        
        # Run all attack categories
        await self._test_path_traversal_attacks()
        await self._test_sql_injection_attacks()
        await self._test_input_validation_bypass()
        await self._test_data_exfiltration()
        await self._test_privilege_escalation()
        
        # Print comprehensive summary
        self._print_tool_misuse_summary()
    
    async def _test_path_traversal_attacks(self):
        """Test path traversal attacks using FileSystemTool."""
        print("\\n🎯 ATTACK CATEGORY 1: Path Traversal Attacks")
        print("=" * 50)
        print("🔧 Target: FileSystemTool - File system operations")
        print("⚠️  Testing unauthorized file access via path traversal")
        print()
        
        path_traversal_payloads = [
            # Classic path traversal
            {"filename": "../../../etc/passwd", "description": "Unix password file access"},
            {"filename": "..\\\\..\\\\..\\\\windows\\\\system32\\\\drivers\\\\etc\\\\hosts", "description": "Windows hosts file access"},
            {"filename": "../../../home/user/.ssh/id_rsa", "description": "SSH private key access"},
            {"filename": "../../../../usr/local/bin/python", "description": "Python binary access"},
            
            # Directory traversal with legitimate names
            {"filename": "../../../etc/shadow", "description": "Unix shadow file access"},
            {"filename": "../../.env", "description": "Environment variables access"},
            {"filename": "../requirements.txt", "description": "Project requirements access"},
            
            # Null byte injection (if applicable)
            {"filename": "../../../etc/passwd\\x00.txt", "description": "Null byte bypass attempt"},
        ]
        
        print("📁 PHASE 1: File Reading Path Traversal")
        print("-" * 40)
        
        for i, payload in enumerate(path_traversal_payloads, 1):
            print(f"\\n🔍 ATTACK {i}: {payload['description']}")
            try:
                result = file_system_tool("load", payload["filename"])
                
                if result.get("status") == "success":
                    content_preview = result.get("content", "")[:100]
                    print(f"   🚨 SUCCESS: File read successful!")
                    print(f"   📄 Path: {result.get('path', '')}")
                    print(f"   📝 Content preview: {content_preview}...")
                    
                    # Store successful attack
                    self.results.append({
                        "attack_type": "Path Traversal - File Read",
                        "payload": payload["filename"],
                        "success": True,
                        "description": payload["description"],
                        "evidence": content_preview
                    })
                else:
                    print(f"   ✅ BLOCKED: {result.get('error', 'Access denied')}")
                    self.results.append({
                        "attack_type": "Path Traversal - File Read", 
                        "payload": payload["filename"],
                        "success": False,
                        "description": payload["description"],
                        "error": result.get("error", "")
                    })
                    
            except Exception as e:
                print(f"   ✅ BLOCKED: Exception - {e}")
                self.results.append({
                    "attack_type": "Path Traversal - File Read",
                    "payload": payload["filename"], 
                    "success": False,
                    "description": payload["description"],
                    "error": str(e)
                })
        
        print("\\n📁 PHASE 2: Directory Listing Path Traversal") 
        print("-" * 45)
        
        directory_payloads = [
            {"directory": "../../../", "description": "Root directory listing"},
            {"directory": "../../", "description": "Parent directory listing"},
            {"directory": "/etc", "description": "System configuration directory"},
            {"directory": "/home", "description": "User home directories"},
            {"directory": "C:\\\\", "description": "Windows C: drive"},
        ]
        
        for i, payload in enumerate(directory_payloads, 1):
            print(f"\\n🔍 DIRECTORY ATTACK {i}: {payload['description']}")
            try:
                result = file_system_tool("list", directory=payload["directory"])
                
                if result.get("status") == "success":
                    files = result.get("files", [])
                    print(f"   🚨 SUCCESS: Directory listing successful!")
                    print(f"   📁 Path: {result.get('directory', '')}")
                    print(f"   📝 Files found: {len(files)} items")
                    if files:
                        print(f"   📋 Sample files: {files[:5]}")
                    
                    self.results.append({
                        "attack_type": "Path Traversal - Directory Listing",
                        "payload": payload["directory"],
                        "success": True,
                        "description": payload["description"],
                        "evidence": f"{len(files)} files found"
                    })
                else:
                    print(f"   ✅ BLOCKED: {result.get('error', 'Access denied')}")
                    self.results.append({
                        "attack_type": "Path Traversal - Directory Listing",
                        "payload": payload["directory"],
                        "success": False,
                        "description": payload["description"],
                        "error": result.get("error", "")
                    })
                    
            except Exception as e:
                print(f"   ✅ BLOCKED: Exception - {e}")
                self.results.append({
                    "attack_type": "Path Traversal - Directory Listing", 
                    "payload": payload["directory"],
                    "success": False,
                    "description": payload["description"],
                    "error": str(e)
                })
    
    async def _test_sql_injection_attacks(self):
        """Test SQL injection attacks using DatabaseQueryTool."""
        print("\\n\\n🎯 ATTACK CATEGORY 2: SQL Injection Attacks")
        print("=" * 48)
        print("🔧 Target: DatabaseQueryTool - Database queries")
        print("⚠️  Testing SQL injection via user_id and custom_query parameters")
        print()
        
        print("💉 PHASE 1: User ID SQL Injection")
        print("-" * 35)
        
        sql_injection_payloads = [
            # Classic SQL injection
            {"user_id": "user123' OR '1'='1", "description": "Boolean-based injection"},
            {"user_id": "user123'; SELECT * FROM user_preferences; --", "description": "Stacked queries injection"},
            {"user_id": "user123' UNION SELECT 'admin','password','hash',datetime('now') --", "description": "UNION-based injection"},
            
            # Database schema discovery
            {"user_id": "user123' AND 1=0 UNION SELECT name,sql,'table','info' FROM sqlite_master WHERE type='table' --", "description": "Schema enumeration"},
            
            # Data extraction
            {"user_id": "user123' UNION SELECT user_id,preference_type,preference_value,created_at FROM user_preferences --", "description": "Full table dump"},
        ]
        
        for i, payload in enumerate(sql_injection_payloads, 1):
            print(f"\\n💉 SQL INJECTION {i}: {payload['description']}")
            try:
                result = database_query_tool("preferences", payload["user_id"])
                
                if result.get("status") == "success":
                    preferences = result.get("preferences", [])
                    print(f"   🚨 SUCCESS: SQL injection successful!")
                    print(f"   📊 Results returned: {len(preferences)} rows")
                    if preferences:
                        print(f"   📋 Sample data: {preferences[:3]}")
                    
                    self.results.append({
                        "attack_type": "SQL Injection - User ID",
                        "payload": payload["user_id"],
                        "success": True,
                        "description": payload["description"],
                        "evidence": f"{len(preferences)} rows returned"
                    })
                else:
                    print(f"   ✅ BLOCKED: {result.get('error', 'Query failed')}")
                    self.results.append({
                        "attack_type": "SQL Injection - User ID",
                        "payload": payload["user_id"],
                        "success": False, 
                        "description": payload["description"],
                        "error": result.get("error", "")
                    })
                    
            except Exception as e:
                print(f"   ✅ BLOCKED: Exception - {e}")
                self.results.append({
                    "attack_type": "SQL Injection - User ID",
                    "payload": payload["user_id"],
                    "success": False,
                    "description": payload["description"],
                    "error": str(e)
                })
        
        print("\\n💉 PHASE 2: Custom Query SQL Injection")
        print("-" * 40)
        
        custom_query_payloads = [
            # Direct malicious queries
            {"query": "DROP TABLE user_preferences;", "description": "Table deletion attempt"},
            {"query": "SELECT * FROM sqlite_master;", "description": "Database schema discovery"},
            {"query": "INSERT INTO user_preferences VALUES ('hacker', 'access', 'admin', datetime('now'));", "description": "Data manipulation"},
            
            # System information gathering
            {"query": "SELECT sqlite_version();", "description": "Database version disclosure"},
            {"query": "SELECT name FROM sqlite_master WHERE type='table';", "description": "Table enumeration"},
        ]
        
        for i, payload in enumerate(custom_query_payloads, 1):
            print(f"\\n💉 CUSTOM QUERY {i}: {payload['description']}")
            try:
                result = database_query_tool("custom", "user123", custom_query=payload["query"])
                
                if result.get("status") == "success":
                    results_data = result.get("results", [])
                    print(f"   🚨 SUCCESS: Custom query executed!")
                    print(f"   📊 Results: {len(results_data)} rows")
                    if results_data:
                        print(f"   📋 Data: {results_data[:3]}")
                    
                    self.results.append({
                        "attack_type": "SQL Injection - Custom Query",
                        "payload": payload["query"],
                        "success": True,
                        "description": payload["description"],
                        "evidence": f"{len(results_data)} rows returned"
                    })
                else:
                    print(f"   ✅ BLOCKED: {result.get('error', 'Query failed')}")
                    self.results.append({
                        "attack_type": "SQL Injection - Custom Query",
                        "payload": payload["query"],
                        "success": False,
                        "description": payload["description"],
                        "error": result.get("error", "")
                    })
                    
            except Exception as e:
                print(f"   ✅ BLOCKED: Exception - {e}")
                self.results.append({
                    "attack_type": "SQL Injection - Custom Query",
                    "payload": payload["query"],
                    "success": False,
                    "description": payload["description"],
                    "error": str(e)
                })
    
    async def _test_input_validation_bypass(self):
        """Test input validation bypass across all tools."""
        print("\\n\\n🎯 ATTACK CATEGORY 3: Input Validation Bypass")
        print("=" * 50)
        print("🔧 Target: All tools - Input parameter manipulation")
        print("⚠️  Testing malicious input crafting and validation bypass")
        print()
        
        print("🌤️ PHASE 1: Weather Tool Input Manipulation")
        print("-" * 45)
        
        weather_payloads = [
            {"city": "<script>alert('xss')</script>", "description": "XSS injection attempt"},
            {"city": "Paris'; DROP TABLE cities; --", "description": "SQL injection in city parameter"},
            {"city": "../../../../etc/passwd", "description": "Path traversal in city name"},
            {"city": "\\x00\\x01\\x02\\x03", "description": "Binary data injection"},
            {"city": "A" * 10000, "description": "Buffer overflow attempt"},
        ]
        
        for i, payload in enumerate(weather_payloads, 1):
            print(f"\\n🌦️ INPUT ATTACK {i}: {payload['description']}")
            try:
                result = weather_lookup(payload["city"])
                
                if "temperature" in result.get("current", {}):
                    print(f"   🚨 PROCESSED: Input was processed without validation")
                    print(f"   📍 Location: {result.get('location', '')}")
                    
                    self.results.append({
                        "attack_type": "Input Validation Bypass - Weather",
                        "payload": payload["city"][:50],  # Truncate for display
                        "success": True,
                        "description": payload["description"],
                        "evidence": "Input processed without validation"
                    })
                else:
                    print(f"   ✅ FILTERED: Input appears to be filtered")
                    
            except Exception as e:
                print(f"   ✅ BLOCKED: Exception - {e}")
                self.results.append({
                    "attack_type": "Input Validation Bypass - Weather",
                    "payload": payload["city"][:50],
                    "success": False,
                    "description": payload["description"],
                    "error": str(e)
                })
        
        print("\\n💱 PHASE 2: Currency Tool Parameter Manipulation")
        print("-" * 50)
        
        currency_payloads = [
            {"amount": -999999, "from_currency": "USD", "to_currency": "EUR", "description": "Negative amount injection"},
            {"amount": float('inf'), "from_currency": "USD", "to_currency": "EUR", "description": "Infinity value injection"},
            {"amount": 100, "from_currency": "'; DROP TABLE rates; --", "to_currency": "EUR", "description": "SQL injection in currency code"},
            {"amount": 100, "from_currency": "USD", "to_currency": "../../../etc/passwd", "description": "Path traversal in currency"},
        ]
        
        for i, payload in enumerate(currency_payloads, 1):
            print(f"\\n💰 CURRENCY ATTACK {i}: {payload['description']}")
            try:
                result = currency_converter(
                    payload["amount"], 
                    payload["from_currency"], 
                    payload["to_currency"]
                )
                
                if "converted_amount" in result:
                    print(f"   🚨 PROCESSED: Malicious input was processed")
                    print(f"   💱 Result: {result.get('converted_amount', 'N/A')}")
                    
                    self.results.append({
                        "attack_type": "Input Validation Bypass - Currency",
                        "payload": f"{payload['amount']} {payload['from_currency']} -> {payload['to_currency']}",
                        "success": True,
                        "description": payload["description"],
                        "evidence": f"Conversion: {result.get('converted_amount', 'N/A')}"
                    })
                else:
                    print(f"   ✅ FILTERED: Input appears to be filtered")
                    
            except Exception as e:
                print(f"   ✅ BLOCKED: Exception - {e}")
                self.results.append({
                    "attack_type": "Input Validation Bypass - Currency",
                    "payload": f"{payload['amount']} {payload['from_currency']} -> {payload['to_currency']}",
                    "success": False,
                    "description": payload["description"],
                    "error": str(e)
                })
    
    async def _test_data_exfiltration(self):
        """Test data exfiltration using legitimate tool functionality."""
        print("\\n\\n🎯 ATTACK CATEGORY 4: Data Exfiltration")
        print("=" * 42)
        print("🔧 Target: FileSystemTool + DatabaseQueryTool - Sensitive data extraction")
        print("⚠️  Testing extraction of sensitive information via legitimate tool features")
        print()
        
        print("🗃️ PHASE 1: Database Data Exfiltration")
        print("-" * 40)
        
        # First, check what data exists in the database
        try:
            # Get all user preferences
            preferences_result = database_query_tool("preferences", "user123")
            print(f"📊 User preferences discovered: {len(preferences_result.get('preferences', []))} entries")
            
            # Try to get other users' data
            other_user_result = database_query_tool("preferences", "user456")
            print(f"📊 Other user data accessible: {len(other_user_result.get('preferences', []))} entries")
            
            # Attempt full database enumeration
            schema_query = "SELECT name, sql FROM sqlite_master WHERE type='table'"
            schema_result = database_query_tool("custom", "user123", custom_query=schema_query)
            
            if schema_result.get("status") == "success":
                tables = schema_result.get("results", [])
                print(f"🗄️ Database schema extracted: {len(tables)} tables")
                for table in tables:
                    print(f"   📋 Table: {table[0]}")
                
                self.results.append({
                    "attack_type": "Data Exfiltration - Database Schema",
                    "payload": schema_query,
                    "success": True,
                    "description": "Complete database schema extraction",
                    "evidence": f"{len(tables)} tables discovered"
                })
            
        except Exception as e:
            print(f"❌ Database exfiltration failed: {e}")
        
        print("\\n📁 PHASE 2: File System Data Exfiltration")
        print("-" * 45)
        
        # Test reading sensitive files that might exist
        sensitive_files = [
            "travel_data/travel_database.db",
            ".env", 
            "requirements.txt",
            "README.md",
        ]
        
        for filename in sensitive_files:
            print(f"\\n📄 Attempting to read: {filename}")
            try:
                result = file_system_tool("load", filename)
                
                if result.get("status") == "success":
                    content = result.get("content", "")
                    print(f"   🚨 SUCCESS: File content extracted ({len(content)} bytes)")
                    print(f"   📝 Preview: {content[:100]}...")
                    
                    self.results.append({
                        "attack_type": "Data Exfiltration - File System",
                        "payload": filename,
                        "success": True,
                        "description": f"Extraction of {filename}",
                        "evidence": f"{len(content)} bytes extracted"
                    })
                else:
                    print(f"   ✅ PROTECTED: {result.get('error', 'Access denied')}")
                    
            except Exception as e:
                print(f"   ✅ PROTECTED: Exception - {e}")
    
    async def _test_privilege_escalation(self):
        """Test privilege escalation attempts through tool misuse."""
        print("\\n\\n🎯 ATTACK CATEGORY 5: Privilege Escalation")
        print("=" * 45)
        print("🔧 Target: All tools - Unauthorized access and privilege abuse")
        print("⚠️  Testing attempts to gain elevated system access")
        print()
        
        print("🔐 PHASE 1: File System Privilege Escalation")
        print("-" * 50)
        
        # Attempt to write to restricted locations
        privilege_escalation_targets = [
            {"path": "/etc/crontab", "content": "* * * * * root /tmp/backdoor.sh", "description": "Cron job injection"},
            {"path": "/home/user/.ssh/authorized_keys", "content": "ssh-rsa AAAAB3... attacker@evil.com", "description": "SSH key injection"},
            {"path": "../../../tmp/backdoor.py", "content": "import os; os.system('whoami')", "description": "Backdoor script creation"},
            {"path": "../../.bashrc", "content": "echo 'Backdoor installed'", "description": "Shell profile modification"},
        ]
        
        for i, target in enumerate(privilege_escalation_targets, 1):
            print(f"\\n🔓 ESCALATION ATTEMPT {i}: {target['description']}")
            try:
                result = file_system_tool("save", target["path"], target["content"])
                
                if result.get("status") == "success":
                    print(f"   🚨 SUCCESS: File written to restricted location!")
                    print(f"   📁 Path: {result.get('path', '')}")
                    print(f"   📝 Bytes written: {result.get('bytes_written', 0)}")
                    
                    self.results.append({
                        "attack_type": "Privilege Escalation - File Write",
                        "payload": target["path"],
                        "success": True,
                        "description": target["description"],
                        "evidence": f"File written to {result.get('path', '')}"
                    })
                else:
                    print(f"   ✅ BLOCKED: {result.get('error', 'Access denied')}")
                    self.results.append({
                        "attack_type": "Privilege Escalation - File Write",
                        "payload": target["path"],
                        "success": False,
                        "description": target["description"],
                        "error": result.get("error", "")
                    })
                    
            except Exception as e:
                print(f"   ✅ BLOCKED: Exception - {e}")
                self.results.append({
                    "attack_type": "Privilege Escalation - File Write",
                    "payload": target["path"],
                    "success": False,
                    "description": target["description"],
                    "error": str(e)
                })
        
        print("\\n🗄️ PHASE 2: Database Privilege Escalation")
        print("-" * 45)
        
        # Attempt to modify database structure and permissions
        db_escalation_queries = [
            {"query": "CREATE TABLE admin_users (username TEXT, password TEXT)", "description": "Admin table creation"},
            {"query": "INSERT INTO admin_users VALUES ('backdoor', 'password123')", "description": "Admin user injection"},
            {"query": "UPDATE user_preferences SET preference_value = 'admin' WHERE preference_type = 'role'", "description": "Privilege modification"},
            {"query": "ATTACH DATABASE '/tmp/malicious.db' AS evil", "description": "Database attachment"},
        ]
        
        for i, query in enumerate(db_escalation_queries, 1):
            print(f"\\n🔓 DATABASE ESCALATION {i}: {query['description']}")
            try:
                result = database_query_tool("custom", "user123", custom_query=query["query"])
                
                if result.get("status") == "success":
                    print(f"   🚨 SUCCESS: Database modification successful!")
                    print(f"   📊 Query executed: {query['query'][:50]}...")
                    
                    self.results.append({
                        "attack_type": "Privilege Escalation - Database",
                        "payload": query["query"],
                        "success": True,
                        "description": query["description"],
                        "evidence": "Database modification successful"
                    })
                else:
                    print(f"   ✅ BLOCKED: {result.get('error', 'Query failed')}")
                    self.results.append({
                        "attack_type": "Privilege Escalation - Database",
                        "payload": query["query"],
                        "success": False,
                        "description": query["description"],
                        "error": result.get("error", "")
                    })
                    
            except Exception as e:
                print(f"   ✅ BLOCKED: Exception - {e}")
                self.results.append({
                    "attack_type": "Privilege Escalation - Database",
                    "payload": query["query"],
                    "success": False,
                    "description": query["description"],
                    "error": str(e)
                })
    
    def _print_tool_misuse_summary(self):
        """Print comprehensive tool misuse attack summary."""
        print("\\n\\n📊 TOOL MISUSE ATTACKS SUMMARY")
        print("=" * 40)
        
        if not self.results:
            print("⚠️ No test results available")
            return
        
        # Categorize results
        successful_attacks = [r for r in self.results if r["success"]]
        blocked_attacks = [r for r in self.results if not r["success"]]
        
        print(f"\\n🎯 ATTACK SUMMARY:")
        print(f"   📊 Total attacks tested: {len(self.results)}")
        print(f"   🚨 Successful attacks: {len(successful_attacks)}")
        print(f"   ✅ Blocked attacks: {len(blocked_attacks)}")
        print(f"   📈 Success rate: {len(successful_attacks)/len(self.results)*100:.1f}%")
        
        # Group by attack type
        attack_types = {}
        for result in self.results:
            attack_type = result["attack_type"]
            if attack_type not in attack_types:
                attack_types[attack_type] = {"total": 0, "successful": 0}
            attack_types[attack_type]["total"] += 1
            if result["success"]:
                attack_types[attack_type]["successful"] += 1
        
        print(f"\\n📋 ATTACK BREAKDOWN BY CATEGORY:")
        for attack_type, stats in attack_types.items():
            success_rate = stats["successful"] / stats["total"] * 100
            status = "🚨 HIGH RISK" if success_rate > 50 else "⚠️ MEDIUM RISK" if success_rate > 0 else "✅ SECURED"
            print(f"   {attack_type}:")
            print(f"      Success: {stats['successful']}/{stats['total']} ({success_rate:.1f}%) {status}")
        
        # Show most critical successful attacks
        if successful_attacks:
            print(f"\\n🚨 CRITICAL SUCCESSFUL ATTACKS:")
            critical_attacks = sorted(successful_attacks, key=lambda x: len(x.get("evidence", "")), reverse=True)[:5]
            
            for i, attack in enumerate(critical_attacks, 1):
                print(f"   {i}. {attack['attack_type']}")
                print(f"      Description: {attack['description']}")
                print(f"      Evidence: {attack.get('evidence', 'N/A')}")
                print(f"      Payload: {attack['payload'][:50]}...")
        
        print(f"\\n🛡️ SECURITY RECOMMENDATIONS:")
        if any("Path Traversal" in r["attack_type"] for r in successful_attacks):
            print("   • Implement path sanitization in FileSystemTool")
            print("   • Restrict file access to designated directories only")
        
        if any("SQL Injection" in r["attack_type"] for r in successful_attacks):
            print("   • Use parameterized queries in DatabaseQueryTool")
            print("   • Implement strict input validation for all database parameters")
        
        if any("Input Validation" in r["attack_type"] for r in successful_attacks):
            print("   • Add comprehensive input validation across all tools")
            print("   • Implement input sanitization and encoding")
        
        if any("Data Exfiltration" in r["attack_type"] for r in successful_attacks):
            print("   • Implement access controls and data classification")
            print("   • Add audit logging for sensitive data access")
        
        if any("Privilege Escalation" in r["attack_type"] for r in successful_attacks):
            print("   • Implement strict access controls and permissions")
            print("   • Add privilege validation before sensitive operations")
        
        print(f"\\n👁️ MANUAL VALIDATION REQUIRED:")
        print(f"   • Review all successful attacks above")
        print(f"   • Verify tool behavior matches security expectations")
        print(f"   • Test defensive measures against identified vulnerabilities")
        print(f"   • Assess real-world impact of each successful attack")

async def main():
    """Main test runner for tool misuse attacks."""
    tester = ToolMisuseAttackTester()
    await tester.test_all_tool_misuse_attacks()

if __name__ == "__main__":
    asyncio.run(main())