"""Tests for analyze_project module.

Comprehensive test coverage for Phase 2.1 implementation following Testing Concurrente principle.
Validates all heuristics, edge cases, and AnalysisResult schema compliance.
"""

import pytest
from tools.architect.analyze_project import (
    analyze_project,
    extract_keywords,
    detect_patterns,
    calculate_complexity,
    classify_domain,
    suggest_technology_stack,
    extract_implicit_requirements,
    DOMAIN_KEYWORDS,
    PROJECT_PATTERNS
)
from schemas.architect_payloads import AnalysisResult


class TestExtractKeywords:
    """Test keyword extraction functionality."""
    
    def test_extract_web_keywords(self):
        """Test extraction of web-related keywords."""
        description = "Create a web application with React frontend and Django backend"
        keywords = extract_keywords(description)
        
        assert "web" in keywords
        assert "react" in keywords
        assert "django" in keywords
        assert "frontend" in keywords
        assert "backend" in keywords
    
    def test_extract_mobile_keywords(self):
        """Test extraction of mobile-related keywords."""
        description = "Build a mobile app for iOS and Android using React Native"
        keywords = extract_keywords(description)
        
        assert "mobile" in keywords
        assert "app" in keywords
        assert "ios" in keywords
        assert "android" in keywords
        assert "react-native" in keywords
    
    def test_extract_data_keywords(self):
        """Test extraction of data-related keywords."""
        description = "Data analytics pipeline with PostgreSQL database and ETL processes"
        keywords = extract_keywords(description)
        
        assert "data" in keywords
        assert "analytics" in keywords
        assert "pipeline" in keywords
        assert "postgresql" in keywords
        assert "etl" in keywords
    
    def test_case_insensitive_extraction(self):
        """Test case-insensitive keyword extraction."""
        description = "API development with REST endpoints and GraphQL integration"
        keywords = extract_keywords(description)
        
        assert "api" in keywords
        assert "rest" in keywords
        assert "graphql" in keywords
    
    def test_no_duplicate_keywords(self):
        """Test that duplicate keywords are removed."""
        description = "web web application web development"
        keywords = extract_keywords(description)
        
        assert keywords.count("web") == 1
    
    def test_empty_description(self):
        """Test extraction from empty description."""
        keywords = extract_keywords("")
        assert keywords == []
    
    def test_no_matching_keywords(self):
        """Test description with no matching keywords."""
        description = "some random text with no technical terms"
        keywords = extract_keywords(description)
        assert keywords == []


class TestDetectPatterns:
    """Test pattern detection functionality."""
    
    def test_detect_crud_pattern(self):
        """Test CRUD operations pattern detection."""
        description = "System to create, read, update and delete user records"
        patterns = detect_patterns(description)
        
        assert "crud_operations" in patterns
    
    def test_detect_user_management_pattern(self):
        """Test user management pattern detection."""
        description = "User registration and login system with profile management"
        patterns = detect_patterns(description)
        
        assert "user_management" in patterns
    
    def test_detect_real_time_pattern(self):
        """Test real-time pattern detection."""
        description = "Real-time chat application with live notifications"
        patterns = detect_patterns(description)
        
        assert "real_time" in patterns
    
    def test_detect_payment_pattern(self):
        """Test payment pattern detection."""
        description = "E-commerce checkout with Stripe payment integration"
        patterns = detect_patterns(description)
        
        assert "payment" in patterns
    
    def test_detect_multiple_patterns(self):
        """Test detection of multiple patterns."""
        description = "Dashboard with user authentication, file upload, and real-time analytics"
        patterns = detect_patterns(description)
        
        assert "dashboard" in patterns
        assert "user_management" in patterns
        assert "file_handling" in patterns
        assert "real_time" in patterns
    
    def test_case_insensitive_pattern_detection(self):
        """Test case-insensitive pattern detection."""
        description = "REAL-TIME WebSocket integration"
        patterns = detect_patterns(description)
        
        assert "real_time" in patterns
    
    def test_no_patterns_detected(self):
        """Test description with no detectable patterns."""
        description = "simple text processing"
        patterns = detect_patterns(description)
        assert patterns == []


class TestCalculateComplexity:
    """Test complexity calculation functionality."""
    
    def test_low_complexity_short_description(self):
        """Test low complexity for short descriptions."""
        description = "Simple web page"
        keywords = ["web", "html"]
        complexity = calculate_complexity(description, keywords)
        
        assert complexity == "Baja"
    
    def test_medium_complexity_moderate_description(self):
        """Test medium complexity for moderate descriptions."""
        description = "Web application with user authentication and basic CRUD operations for managing tasks"
        keywords = ["web", "authentication", "crud", "database"]
        complexity = calculate_complexity(description, keywords)
        
        assert complexity in ["Baja", "Media"]  # Depends on exact length and keyword count
    
    def test_high_complexity_long_description_many_keywords(self):
        """Test high complexity for long descriptions with many keywords."""
        description = """Complete e-commerce platform with user management, product catalog, 
        shopping cart, payment processing, order tracking, inventory management, analytics dashboard, 
        real-time notifications, mobile app, API integration, and third-party services"""
        keywords = [
            "web", "ecommerce", "user", "authentication", "database", "payment", "api",
            "mobile", "real-time", "analytics", "dashboard", "integration", "microservice",
            "notification", "inventory", "cart", "checkout"
        ]
        complexity = calculate_complexity(description, keywords)
        
        assert complexity == "Alta"
    
    def test_edge_case_empty_keywords(self):
        """Test complexity calculation with empty keywords."""
        description = "A moderately complex project description with sufficient length"
        keywords = []
        complexity = calculate_complexity(description, keywords)
        
        assert complexity in ["Baja", "Media"]


class TestClassifyDomain:
    """Test domain classification functionality."""
    
    def test_classify_web_domain(self):
        """Test classification of web domain."""
        keywords = ["web", "frontend", "backend", "javascript", "react", "html"]
        domain = classify_domain(keywords)
        
        assert domain == "web"
    
    def test_classify_mobile_domain(self):
        """Test classification of mobile domain."""
        keywords = ["mobile", "app", "ios", "android", "react-native"]
        domain = classify_domain(keywords)
        
        assert domain == "mobile"
    
    def test_classify_data_domain(self):
        """Test classification of data domain."""
        keywords = ["data", "analytics", "database", "pipeline", "etl", "postgresql"]
        domain = classify_domain(keywords)
        
        assert domain == "data"
    
    def test_classify_api_domain(self):
        """Test classification of API domain."""
        keywords = ["api", "rest", "graphql", "microservice", "endpoint"]
        domain = classify_domain(keywords)
        
        assert domain == "api"
    
    def test_mixed_domain_highest_score(self):
        """Test that highest scoring domain is selected."""
        keywords = ["web", "api", "rest", "frontend", "backend", "javascript"]
        domain = classify_domain(keywords)
        
        # Should be 'web' as it has more matching keywords
        assert domain == "web"
    
    def test_no_domain_classification(self):
        """Test no domain classification for non-matching keywords."""
        keywords = []
        domain = classify_domain(keywords)
        
        assert domain is None
    
    def test_unknown_keywords_no_domain(self):
        """Test unknown keywords result in no domain."""
        keywords = ["unknown", "random", "terms"]
        domain = classify_domain(keywords)
        
        assert domain is None


class TestSuggestTechnologyStack:
    """Test technology stack suggestion functionality."""
    
    def test_direct_technology_match(self):
        """Test direct technology matching from keywords."""
        keywords = ["python", "django", "react", "postgresql"]
        domain = "web"
        tech_stack = suggest_technology_stack(keywords, domain)
        
        assert "python" in tech_stack
        assert "javascript" in tech_stack
    
    def test_domain_based_suggestion(self):
        """Test domain-based technology suggestions."""
        keywords = ["web", "frontend", "backend"]
        domain = "web"
        tech_stack = suggest_technology_stack(keywords, domain)
        
        assert len(tech_stack) > 0
        assert any(tech in ["javascript", "python"] for tech in tech_stack)
    
    def test_mobile_domain_suggestions(self):
        """Test mobile domain technology suggestions."""
        keywords = ["mobile", "app"]
        domain = "mobile"
        tech_stack = suggest_technology_stack(keywords, domain)
        
        assert "javascript" in tech_stack or "java" in tech_stack
    
    def test_ai_domain_python_suggestion(self):
        """Test AI domain suggests Python."""
        keywords = ["ai", "machine learning"]
        domain = "ai"
        tech_stack = suggest_technology_stack(keywords, domain)
        
        assert "python" in tech_stack
    
    def test_no_suggestions_unknown_domain(self):
        """Test no suggestions for unknown domain and keywords."""
        keywords = ["unknown"]
        domain = None
        tech_stack = suggest_technology_stack(keywords, domain)
        
        assert tech_stack == []


class TestExtractImplicitRequirements:
    """Test implicit requirements extraction functionality."""
    
    def test_crud_pattern_requirements(self):
        """Test requirements for CRUD patterns."""
        description = "User management with create, read, update, delete operations"
        patterns = ["crud_operations", "user_management"]
        domain = "web"
        requirements = extract_implicit_requirements(description, patterns, domain)
        
        assert "Database design and ORM integration" in requirements
        assert "Authentication and authorization system" in requirements
    
    def test_real_time_pattern_requirements(self):
        """Test requirements for real-time patterns."""
        description = "Real-time chat application"
        patterns = ["real_time"]
        domain = "web"
        requirements = extract_implicit_requirements(description, patterns, domain)
        
        assert "WebSocket or Server-Sent Events implementation" in requirements
    
    def test_payment_pattern_requirements(self):
        """Test requirements for payment patterns."""
        description = "E-commerce with payment processing"
        patterns = ["payment"]
        domain = "ecommerce"
        requirements = extract_implicit_requirements(description, patterns, domain)
        
        assert "Payment gateway integration and security compliance" in requirements
    
    def test_domain_based_requirements(self):
        """Test domain-based requirement extraction."""
        description = "Mobile application development"
        patterns = []
        domain = "mobile"
        requirements = extract_implicit_requirements(description, patterns, domain)
        
        assert "Platform-specific optimization and app store compliance" in requirements
    
    def test_complex_project_requirements(self):
        """Test additional requirements for complex projects."""
        long_description = "A" * 150  # Long description
        patterns = ["crud_operations"]
        domain = "web"
        requirements = extract_implicit_requirements(long_description, patterns, domain)
        
        assert "Comprehensive testing strategy" in requirements
        assert "Documentation and API specifications" in requirements
        assert "Error handling and logging system" in requirements
    
    def test_no_duplicate_requirements(self):
        """Test that duplicate requirements are removed."""
        description = "Simple project"
        patterns = []
        domain = None
        requirements = extract_implicit_requirements(description, patterns, domain)
        
        # Should not have duplicates
        assert len(requirements) == len(set(requirements))


class TestAnalyzeProject:
    """Test main analyze_project function."""
    
    def test_complete_web_project_analysis(self):
        """Test complete analysis of a web project."""
        description = """Create a web application for task management with user authentication, 
        CRUD operations for tasks, real-time notifications, and REST API endpoints"""
        
        result = analyze_project(description)
        
        # Validate return type
        assert isinstance(result, AnalysisResult)
        
        # Validate required fields are present
        assert result.keywords is not None
        assert result.patterns is not None
        assert result.complexity is not None
        assert result.requirements_implicit is not None
        
        # Validate content makes sense
        assert "web" in result.keywords
        assert "api" in result.keywords
        assert "authentication" in result.keywords
        
        assert "crud_operations" in result.patterns
        assert "user_management" in result.patterns
        assert "real_time" in result.patterns
        
        assert result.complexity in ["Baja", "Media", "Alta"]
        assert result.domain in ["web", "api"]  # Can be either depending on keyword density
        assert result.technology_stack is not None
    
    def test_mobile_project_analysis(self):
        """Test analysis of a mobile project."""
        description = "Build a mobile app for iOS and Android with user profiles and offline sync"
        
        result = analyze_project(description)
        
        assert isinstance(result, AnalysisResult)
        assert "mobile" in result.keywords
        assert "app" in result.keywords
        assert "ios" in result.keywords
        assert "android" in result.keywords
        
        assert result.domain == "mobile"
        assert "user_management" in result.patterns
    
    def test_data_project_analysis(self):
        """Test analysis of a data project."""
        description = "Data analytics pipeline with ETL processes, PostgreSQL database, and reporting dashboard"
        
        result = analyze_project(description)
        
        assert isinstance(result, AnalysisResult)
        assert "data" in result.keywords
        assert "analytics" in result.keywords
        assert "pipeline" in result.keywords
        assert "etl" in result.keywords
        
        assert result.domain == "data"
        assert "dashboard" in result.patterns
    
    def test_ai_project_analysis(self):
        """Test analysis of an AI project."""
        description = "Machine learning model for prediction with Python and TensorFlow"
        
        result = analyze_project(description)
        
        assert isinstance(result, AnalysisResult)
        assert "machine learning" in result.keywords or "ml" in result.keywords
        assert "model" in result.keywords
        assert "prediction" in result.keywords
        
        assert result.domain == "ai"
        assert "python" in result.technology_stack
    
    def test_minimal_project_analysis(self):
        """Test analysis of a minimal project description."""
        description = "Simple website"
        
        result = analyze_project(description)
        
        assert isinstance(result, AnalysisResult)
        assert result.complexity == "Baja"
        assert len(result.keywords) > 0  # Should find 'website'
    
    def test_complex_ecommerce_analysis(self):
        """Test analysis of a complex e-commerce project."""
        description = """Full-featured e-commerce platform with user registration, product catalog, 
        shopping cart, payment processing with Stripe, order tracking, inventory management, 
        admin dashboard with analytics, real-time notifications, mobile app, REST API, 
        and third-party integrations"""
        
        result = analyze_project(description)
        
        assert isinstance(result, AnalysisResult)
        assert result.complexity == "Alta"
        assert len(result.keywords) > 10
        assert len(result.patterns) >= 5
        assert any("ecommerce" in kw or "cart" in kw or "payment" in kw for kw in result.keywords)
        assert "payment" in result.patterns
        assert "dashboard" in result.patterns
        assert "real_time" in result.patterns
        
        # Should have comprehensive implicit requirements
        assert len(result.requirements_implicit) > 5
    
    def test_empty_description_error(self):
        """Test that empty description raises ValueError."""
        with pytest.raises(ValueError, match="task_description cannot be empty"):
            analyze_project("")
    
    def test_whitespace_only_description_error(self):
        """Test that whitespace-only description raises ValueError."""
        with pytest.raises(ValueError, match="task_description cannot be empty"):
            analyze_project("   \n\t  ")
    
    def test_pydantic_validation(self):
        """Test that result passes Pydantic validation."""
        description = "Web application with user authentication"
        result = analyze_project(description)
        
        # This should not raise validation errors
        validated_result = AnalysisResult.model_validate(result.model_dump())
        assert validated_result == result
    
    def test_all_required_fields_present(self):
        """Test that all required AnalysisResult fields are present."""
        description = "API development project"
        result = analyze_project(description)
        
        # Required fields according to AnalysisResult schema
        assert hasattr(result, 'keywords')
        assert hasattr(result, 'patterns')
        assert hasattr(result, 'complexity')
        assert hasattr(result, 'requirements_implicit')
        
        # Optional fields should also be handled
        assert hasattr(result, 'domain')
        assert hasattr(result, 'technology_stack')
    
    def test_consistent_results(self):
        """Test that same input produces consistent results."""
        description = "Web application with React and Node.js"
        
        result1 = analyze_project(description)
        result2 = analyze_project(description)
        
        assert result1.keywords == result2.keywords
        assert result1.patterns == result2.patterns
        assert result1.complexity == result2.complexity
        assert result1.domain == result2.domain


class TestIntegration:
    """Integration tests for the complete analyze_project workflow."""
    
    def test_domain_keywords_coverage(self):
        """Test that DOMAIN_KEYWORDS covers major technology areas."""
        required_domains = ['web', 'api', 'data', 'mobile', 'ai']
        
        for domain in required_domains:
            assert domain in DOMAIN_KEYWORDS
            assert len(DOMAIN_KEYWORDS[domain]) > 3  # Each domain should have multiple keywords
    
    def test_pattern_regex_validity(self):
        """Test that all pattern regexes are valid and functional."""
        test_text = "user authentication with real-time notifications and file upload"
        
        for pattern_name, pattern_regex in PROJECT_PATTERNS.items():
            # Should not raise regex errors
            import re
            compiled_pattern = re.compile(pattern_regex, re.IGNORECASE)
            matches = compiled_pattern.search(test_text)
            # Just ensure no exceptions are raised
            assert compiled_pattern is not None
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow with realistic input."""
        description = """Develop a social media platform with user registration and profiles, 
        real-time chat functionality, file upload for images and videos, REST API for mobile app, 
        admin dashboard with analytics, payment system for premium features, and third-party 
        OAuth integration with Google and Facebook"""
        
        result = analyze_project(description)
        
        # Validate comprehensive analysis
        assert len(result.keywords) >= 8
        assert len(result.patterns) >= 5
        assert result.complexity in ["Media", "Alta"]
        assert result.domain in ["web", "social", "api"]
        assert len(result.technology_stack) >= 2
        assert len(result.requirements_implicit) >= 6
        
        # Validate specific expectations
        assert any("social" in kw or "user" in kw for kw in result.keywords)
        assert "real_time" in result.patterns
        assert "payment" in result.patterns
        assert "file_handling" in result.patterns
        assert "user_management" in result.patterns
        
        # Validate requirements include security and scalability concerns
        requirements_text = " ".join(result.requirements_implicit)
        assert any("authentication" in req.lower() or "security" in req.lower() 
                  for req in result.requirements_implicit)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])