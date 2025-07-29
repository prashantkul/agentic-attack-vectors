#!/usr/bin/env python3
"""
Memory Security Test Runner
Orchestrates all memory poisoning tests and provides comprehensive reporting.
"""

import asyncio
import argparse
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class MemorySecurityTestRunner:
    """Orchestrates all memory security tests."""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "basic_tests": {},
            "advanced_tests": {},
            "sophisticated_tests": {},
            "summary": {}
        }
        
    async def run_basic_tests(self):
        """Run basic memory poisoning tests."""
        print("🔬 Running Basic Memory Poisoning Tests")
        print("=" * 45)
        
        try:
            # Import and run basic tests
            sys.path.insert(0, str(Path(__file__).parent / "basic"))
            from memory_poisoning_tests import MemoryPoisoningTester
            
            tester = MemoryPoisoningTester()
            await tester.run_all_tests()
            
            # Extract results
            basic_results = {
                "total_tests": len(tester.test_results),
                "vulnerable": sum(1 for r in tester.test_results if r["attack_successful"]),
                "protected": sum(1 for r in tester.test_results if not r["attack_successful"]),
                "details": tester.test_results
            }
            
            self.results["basic_tests"] = basic_results
            return basic_results
            
        except Exception as e:
            print(f"❌ Basic tests failed: {e}")
            self.results["basic_tests"] = {"error": str(e)}
            return None
    
    async def run_advanced_tests(self):
        """Run advanced memory poisoning tests."""
        print("\n🔬 Running Advanced Memory Poisoning Tests")
        print("=" * 47)
        
        try:
            # Import and run quick advanced tests
            sys.path.insert(0, str(Path(__file__).parent / "advanced"))
            from quick_advanced_tests import QuickAdvancedTester
            
            tester = QuickAdvancedTester()
            await tester.run_quick_tests()
            
            # Extract results
            advanced_results = {
                "total_tests": len(tester.test_results),
                "vulnerable": sum(1 for r in tester.test_results if r["vulnerable"]),
                "protected": sum(1 for r in tester.test_results if not r["vulnerable"]),
                "details": tester.test_results
            }
            
            self.results["advanced_tests"] = advanced_results
            return advanced_results
            
        except Exception as e:
            print(f"❌ Advanced tests failed: {e}")
            self.results["advanced_tests"] = {"error": str(e)}
            return None
    
    async def run_sophisticated_tests(self):
        """Run sophisticated memory poisoning tests."""
        print("\n🔬 Running Sophisticated Memory Poisoning Tests")
        print("=" * 52)
        
        try:
            # Import and run sophisticated tests
            sys.path.insert(0, str(Path(__file__).parent / "sophisticated"))
            from sophisticated_attacks import SophisticatedAttackTester
            
            tester = SophisticatedAttackTester()
            await tester.run_sophisticated_tests()
            
            # Extract results
            sophisticated_results = {
                "total_tests": len(tester.results),
                "vulnerable": sum(1 for r in tester.results if r["vulnerable"]),
                "protected": sum(1 for r in tester.results if not r["vulnerable"]),
                "details": tester.results
            }
            
            self.results["sophisticated_tests"] = sophisticated_results
            return sophisticated_results
            
        except Exception as e:
            print(f"❌ Sophisticated tests failed: {e}")
            self.results["sophisticated_tests"] = {"error": str(e)}
            return None
    
    def calculate_overall_summary(self):
        """Calculate overall security assessment."""
        total_tests = 0
        total_vulnerable = 0
        total_protected = 0
        
        for test_category in ["basic_tests", "advanced_tests", "sophisticated_tests"]:
            category_results = self.results.get(test_category, {})
            if "error" not in category_results:
                total_tests += category_results.get("total_tests", 0)
                total_vulnerable += category_results.get("vulnerable", 0)
                total_protected += category_results.get("protected", 0)
        
        # Calculate risk level
        if total_vulnerable == 0:
            risk_level = "LOW"
        elif total_vulnerable <= 2:
            risk_level = "MEDIUM"
        elif total_vulnerable <= 5:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        vulnerability_rate = (total_vulnerable / total_tests * 100) if total_tests > 0 else 0
        
        summary = {
            "total_tests": total_tests,
            "vulnerable": total_vulnerable,
            "protected": total_protected,
            "vulnerability_rate": round(vulnerability_rate, 1),
            "risk_level": risk_level
        }
        
        self.results["summary"] = summary
        return summary
    
    def print_comprehensive_report(self):
        """Print comprehensive security assessment report."""
        print("\n" + "="*60)
        print("📊 COMPREHENSIVE MEMORY SECURITY ASSESSMENT")
        print("="*60)
        
        summary = self.results["summary"]
        
        print(f"🔍 OVERALL RESULTS:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   🔴 Vulnerable: {summary['vulnerable']}")
        print(f"   🟢 Protected: {summary['protected']}")
        print(f"   📈 Vulnerability Rate: {summary['vulnerability_rate']}%")
        print(f"   ⚠️  Risk Level: {summary['risk_level']}")
        
        # Category breakdown
        print(f"\n📋 CATEGORY BREAKDOWN:")
        
        categories = [
            ("Basic Tests", "basic_tests", "Fundamental attack vectors"),
            ("Advanced Tests", "advanced_tests", "Sophisticated techniques"),
            ("Sophisticated Tests", "sophisticated_tests", "State-of-the-art attacks")
        ]
        
        for name, key, description in categories:
            results = self.results.get(key, {})
            if "error" in results:
                print(f"   ❌ {name}: Failed to execute")
            else:
                vuln = results.get("vulnerable", 0)
                total = results.get("total_tests", 0)
                print(f"   {'🔴' if vuln > 0 else '🟢'} {name}: {vuln}/{total} vulnerable - {description}")
        
        # Risk assessment and recommendations
        print(f"\n🛡️  SECURITY RECOMMENDATIONS:")
        
        if summary["risk_level"] == "LOW":
            print("   ✅ Excellent security posture!")
            print("   - Continue regular security testing")
            print("   - Monitor for new attack vectors")
            
        elif summary["risk_level"] == "MEDIUM":
            print("   ⚠️  Some vulnerabilities detected")
            print("   - Implement input validation")
            print("   - Add memory content filtering")
            print("   - Consider Model Armor integration")
            
        elif summary["risk_level"] == "HIGH":
            print("   🚨 Multiple vulnerabilities found")
            print("   - Urgent security hardening required")
            print("   - Implement comprehensive input validation")
            print("   - Add Model Armor protection")
            print("   - Implement memory audit mechanisms")
            
        else:  # CRITICAL
            print("   🆘 CRITICAL security issues detected")
            print("   - Immediate security review required")
            print("   - Consider disabling memory features until hardened")
            print("   - Implement all available security measures")
            print("   - Regular security monitoring essential")
        
        print(f"\n📅 Test completed: {self.results['timestamp']}")
        print("="*60)
    
    def save_results(self, output_file: str):
        """Save test results to JSON file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"📄 Results saved to: {output_file}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
    
    async def run_all(self, basic_only=False, advanced_only=False, sophisticated_only=False, output_file=None):
        """Run selected test suites."""
        
        # Check prerequisites
        if not os.getenv("AGENT_ENGINE_ID"):
            print("❌ AGENT_ENGINE_ID environment variable not set")
            print("Set it with: export AGENT_ENGINE_ID=your-agent-engine-id")
            return
        
        print("🚀 MEMORY SECURITY TEST SUITE")
        print("=" * 50)
        print(f"Agent Engine ID: {os.getenv('AGENT_ENGINE_ID')}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()
        
        # Run selected tests
        if not advanced_only and not sophisticated_only:
            await self.run_basic_tests()
            
        if not basic_only and not sophisticated_only:
            await self.run_advanced_tests()
            
        if not basic_only and not advanced_only:
            await self.run_sophisticated_tests()
        
        # Generate summary
        self.calculate_overall_summary()
        self.print_comprehensive_report()
        
        # Save results if requested
        if output_file:
            self.save_results(output_file)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Memory Security Test Runner")
    parser.add_argument("--basic-only", action="store_true", help="Run only basic tests")
    parser.add_argument("--advanced-only", action="store_true", help="Run only advanced tests")
    parser.add_argument("--sophisticated-only", action="store_true", help="Run only sophisticated tests")
    parser.add_argument("--output", "-o", help="Save results to JSON file")
    
    args = parser.parse_args()
    
    runner = MemorySecurityTestRunner()
    
    try:
        asyncio.run(runner.run_all(
            basic_only=args.basic_only,
            advanced_only=args.advanced_only,
            sophisticated_only=args.sophisticated_only,
            output_file=args.output
        ))
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test runner failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()